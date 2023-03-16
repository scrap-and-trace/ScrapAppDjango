from rest_framework import generics, permissions
from rest_framework import viewsets, mixins, status

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ScrapbookSerializer, FollowSerializer, CommentSerializer, FollowCreateSerializer, PageSerializer
from .models import CustomUser, Scrapbook, Follow, Comment, Page
from django.shortcuts import get_object_or_404
from django.contrib.auth import login


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        print("User created")

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Call the self's serializer_class to serialize the request's data
        serializer = self.get_serializer(data=request.data)
        # Check the data is in the right formart
        serializer.is_valid(raise_exception=True)
        # Check the data against db
        user = serializer.validated_data
        # logs the user into the django session
        login(request, user)
        # Returns the user's data - password and the token
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ScrapbookAPI(generics.ListCreateAPIView):
    serializer_class = ScrapbookSerializer

    queryset = Scrapbook.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ["exact"],  # note the 'in' field
    }
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]


class ScrapbookDestroyAPI(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Scrapbook.objects.all()
    serializer_class = ScrapbookSerializer

    # def get_queryset(self):
    #     scrapbookid = self.kwargs['pk']
    #     return Scrapbook.objects.filter(id=scrapbookid)

    def delete(self, request, *args, **kwargs):
        scrapbook = self.get_object()
        if scrapbook.author != request.user:
            content = {'Error': 'You cannot delete someone else\'s scrapbook!'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # search_fields = ['first_name', 'last_name']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'id': ["exact"],  # note the 'in' field
    }

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            CustomUser.objects.filter(id=self.kwargs["pk"]))
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class ScrapbookViewSet(viewsets.ModelViewSet):
#     queryset = Scrapbook.objects.all()
#     serializer_class = ScrapbookSerializer

#     def get_followers(self, obj):
#         followers = Follow.objects.filter(follower=self.kwargs["pk"])
#         return list(followers.values_list("follower", flat=True))


class FollowListCreateAPI(generics.ListCreateAPIView):

    queryset = Follow.objects.all()

    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = {
        'id': ["exact"],
    }

    def get_serializer_class(self):
        if (self.request.method == "POST"):
            serializer_class = FollowCreateSerializer
        else:
            serializer_class = FollowSerializer

        return serializer_class

    def get_queryset(self):
        is_following = self.kwargs['pk']
        return Follow.objects.filter(follower=is_following)


class FollowDestroyAPI(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def delete(self, request, *args, **kwargs):
        follow = Follow.objects.get(id=self.kwargs['pk'])
        if follow.follower != request.user:
            content = {'Error': 'You cannot unfollow someone else for them!'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class SearchUsersAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', ]


class PageAPI(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = {
        'id': ["exact"],
    }

    def destroy(self, request, *args, **kwargs):
        page = self.get_object()
        if page.scrapbook.author != request.user:
            content = {'Error': 'This is not your page!'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    # def get_queryset(self):
    #     pageid = self.kwargs['pk']
    #     return Page.objects.get(id=pageid)
