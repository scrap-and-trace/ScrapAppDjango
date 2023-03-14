from .models import CustomUser, Comment, Follow, Scrapbook, Follow
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import UserSerializer, CommentSerializer, ScrapbookSerializer, FollowSerializer


from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# class UpdateUserViewSet (viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     search_fields = ['first_name', 'last_name']

#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = {
#         'id': ["in", "exact"],  # note the 'in' field
#     }

#     def get_queryset(self):
#         return CustomUser.objects.all()

#     def get_object(self):
#         obj = get_object_or_404(
#             CustomUser.objects.filter(id=self.kwargs["pk"]))
#         return obj

#     def update(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             request.user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
