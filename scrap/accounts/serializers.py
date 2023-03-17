from rest_framework import serializers
from .models import CustomUser, TextElement, ImageElement, Scrapbook, Page, Comment, Follow, PageLikes
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
        user = CustomUser.objects.filter(id=follow.follower.id).last()
        user_data = []
        user_data.append({
            'follower_id': user.id,
            'follower_username': user.username,
        })
        return user_data


# User Serializer


class UserSerializer(serializers.ModelSerializer):
    # following = FollowSerializer(many=True, read_only=True)
    following = serializers.SerializerMethodField()
    scrapbooks = ScrapbookSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'dob', 'phone', 'following', 'scrapbooks', ]

    def get_following(self, user):
        following = Follow.objects.filter(follower=user)
        following_data = []
        for follow in following:
            following_data.append({
                'id': follow.id,
                'scrapbook': ScrapbookSerializer(follow.scrapbook).data
            })
        return following_data


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
        author_data = {
            'author_id': author.id,
            'author_username': author.username,
        }
        return author_data


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['authorid', 'page', 'body']


class PageSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'body',
                  'date_created', 'scrapbook', 'comments', 'longitude', 'latitude', 'no_of_likes', ]

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

    def get_no_of_likes(self, page):
        likes = PageLikes.objects.filter(liked_page=page)
        count = 0
        for like in likes:
            count += 1
        return count


class LikeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageLikes
        fields = ['id', 'liker', 'liked_page', ]


class LikeSerializer(serializers.ModelSerializer):
    liker_details = serializers.SerializerMethodField()

    class Meta:
        model = PageLikes
        fields = ['id', 'liker', 'liked_page', 'liker_details', ]

    def get_liker_details(self, like):
        user = CustomUser.objects.get(
            liker=like)
        liker_data = {
            'liker_username': user.username,
        }
        # liker_data.append({
        #     'liker_id': liker.id,
        #     'liker_username': liker.username,
        # })
        return liker_data
