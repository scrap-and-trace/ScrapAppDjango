from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    phone = PhoneNumberField(blank=True)
    dob = models.DateField(blank=True, null=True)
    image_url = models.CharField(
        max_length=100, blank=True, default='https://i.ibb.co/V9G9x5p/e73a38fc9156.png')
    delete_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email


class Scrapbook(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='scrapbooks')
    title = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    friends_only = models.BooleanField()


class Page(models.Model):
    scrapbook = models.ForeignKey(
        Scrapbook, on_delete=models.CASCADE, related_name='pages')
    date_created = models.DateField(auto_now_add=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    title = models.CharField(max_length=20)
    body = models.CharField(max_length=255)
    image_url = models.CharField(max_length=100, blank=True)
    delete_url = models.CharField(max_length=100, blank=True)


class Comment(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='comments')
    authorid = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comment_author')
    body = models.CharField(max_length=255)


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    scrapbook = models.ForeignKey(
        Scrapbook, on_delete=models.CASCADE, related_name='followed_scrapbook')


class PageLikes(models.Model):
    liker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='liker')
    liked_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='liked_page')


# TODO
# class Friend(models.Model):
#     aFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
#     bFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
#     request_status = models.BooleanField()


# class Block(models.Model):
#     blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocks')
#     blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_blocked')
