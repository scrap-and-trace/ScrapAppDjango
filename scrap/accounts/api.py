from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
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
