from rest_framework import serializers
from .models import CustomUser, Scrapbook, Page, Comment, Follow, PageLikes
from django.contrib.auth import authenticate
from django.http import JsonResponse, response
from django.contrib.auth.password_validation import validate_password


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


class FollowSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'scrapbook', ]


class FollowSerializer(serializers.ModelSerializer):
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
    following = serializers.SerializerMethodField()
    scrapbooks = ScrapbookSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'image_url', 'delete_url', 'first_name',
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
        validate_password(password)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

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


class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'body', 'image_url',
                  'delete_url', 'scrapbook', 'longitude', 'latitude', ]
        extra_kwargs = {'image_url': {'write_only': True},
                        'delete_url': {'write_only': True}}


class PageSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes_list = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'body',  'image_url', 'delete_url',
                  'date_created', 'scrapbook', 'comments', 'longitude', 'latitude', 'likes_list', ]

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

    def get_likes_list(self, page):
        likes = PageLikes.objects.filter(liked_page=page)
        likes_list = []
        for like in likes:
            likes_list.append(like.liker.id)
        return likes_list


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
        return liker_data
