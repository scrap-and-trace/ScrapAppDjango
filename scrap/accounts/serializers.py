from rest_framework import serializers
from .models import CustomUser, TextElement, ImageElement, Scrapbook, Page, Comment, Follow
from django.contrib.auth import authenticate
from django.http import JsonResponse, response


class ScrapbookSerializer(serializers.ModelSerializer):
    pages = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Scrapbook
        fields = ['id', 'title', 'author', 'username', 'pages',
                  'date_created', 'friends_only', ]

    def get_username(self, obj):
        return obj.author.username

    def get_pages(self, scrapbook):
        pages = Page.objects.filter(scrapbook=scrapbook)
        page_data = []
        for page in pages:
            page_data.append({
                'id': page.id,
                'title': page.title
            })
        return page_data


# class TextElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TextElement
#         fields = '__all__'


# class ImageElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageElement
#         fields = '__all__'


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'scrapbook', ]


class FollowSerializer(serializers.ModelSerializer):
    # follower = UserSerializer(read_only=True)
    scrapbook = ScrapbookSerializer(read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'user_details', 'scrapbook', ]

    def get_user_details(self, follow):
        user = CustomUser.objects.filter(id=follow.follower.id).first()
        user_data = []
        user_data.append({
            'follower': user.id,
            'follower_username': user.username,
        })
        return user_data


# User Serializer


class UserSerializer(serializers.ModelSerializer):
    follower = FollowSerializer(many=True, read_only=True)
    scrapbooks = ScrapbookSerializer(many=True, read_only=True)
    # following = serializers.SerializerMethodField()
    # scrapbooks = serializers.SerializerMethodField()
    # scrapbooks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'dob', 'phone', 'follower', 'scrapbooks', ]

    # def get_following(self, obj):
    #     follows = Follow.objects.filter(follower=obj)
    #     serializer = FollowSerializer(follows, many=True)
    #     return serializer.data

    # def get_scrapbooks(self, obj):
    #     books = Scrapbook.objects.filter(author=obj)
    #     serializer = ScrapbookSerializer(books, many=True)
    #     return serializer.data


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


class CommentSerializer(serializers.ModelSerializer):
    author_data = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'page', 'author_data', 'body', ]

    def get_author_data(self, comment):
        author = CustomUser.objects.get(comment_author=comment)
        author_data = []
        author_data.append({'id': author.id,
                            'author_id': author.id,
                            'author_username': author.username,
                            })
        return author_data


class PageSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'body',
                  'date_created', 'scrapbook', 'comments', 'longitude', 'latitude', ]

    def get_comments(self, page):
        comments = Comment.objects.filter(page=page)
        comment_data = []
        for comment in comments:
            comment_data.append({
                'id': comment.id,
                'author_id': comment.authorid.id,
                'author_username': comment.authorid.username,
                'body': comment.body
            })
        return comment_data
