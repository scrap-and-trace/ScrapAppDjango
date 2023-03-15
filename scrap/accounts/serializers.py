from rest_framework import serializers
from .models import CustomUser, TextElement, ImageElement, Scrapbook, Page, Comment, Follow
from django.contrib.auth import authenticate
from django.http import JsonResponse, response


class ScrapbookSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Scrapbook
        fields = ['id', 'title', 'username', 'pages',
                  'date_created', 'author', 'friends_only']

    def get_username(self, obj):
        return obj.author.username


class PageSerializer(serializers.ModelSerializer):

    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='body'
    )
    # comment_author = serializers.PrimaryKeyRelatedField(
    #     queryset=Page.objects.all())
    # username = CustomUser.objects.get(username=comment_author.username)

    class Meta:
        model = Page
        fields = ['id', 'title', 'body',
                  'date_created', 'scrapbook', 'comments', 'longitude', 'latitude', ]

    # def get_comments(self, obj):
    #     comments = Comment.objects.filter(page=obj)
    #     return list(comments.values_list("id", flat=True))

    # def get_username(self, obj):
    #     return CustomUser.objects.get(username=obj.scrapbook.author.username)


# class TextElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TextElement
#         fields = '__all__'


# class ImageElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageElement
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'page', 'authorid', 'body', ]


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'scrapbook', ]


class FollowSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'book', ]

    def get_book(self, obj):
        book = Scrapbook.objects.get(id=obj.scrapbook.id)
        return ScrapbookSerializer(book).data

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    scrapbooks = serializers.SerializerMethodField()
    # scrapbooks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'dob', 'phone', 'following', 'scrapbooks', ]

    def get_following(self, obj):
        follows = Follow.objects.filter(follower=obj)
        serializer = FollowSerializer(follows, many=True)
        return serializer.data

    def get_scrapbooks(self, obj):
        books = Scrapbook.objects.filter(author=obj)
        serializer = ScrapbookSerializer(books, many=True)
        return serializer.data


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
