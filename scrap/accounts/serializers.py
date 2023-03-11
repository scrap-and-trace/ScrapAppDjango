from rest_framework import serializers
from .models import CustomUser, TextElement, ImageElement, Scrapbook, Page, Comment
from django.contrib.auth import authenticate
from django.http import JsonResponse, response


class ScrapbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrapbook
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

    def get_comments(self, obj):
        comments = Comment.objects.filter(page=obj)
        return list(comments.values_list("id", flat=True))


class TextElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextElement
        fields = '__all__'


class ImageElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageElement
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'dob', 'phone', ]

    def get_following(self, obj):
        follows = Follow.objects.filter(follower=obj)
        return list(follows.values_list("followed_scrabook", flat=True))

    def get_comments(self, obj):
        commented = Comment.objects.filter(author=obj)
        return list(commented.values_list("text", flat=True))


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'dob', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Turn json data to a dictionary
        data = dict(data)
        # Authenticate the data in the dictionary against db
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
