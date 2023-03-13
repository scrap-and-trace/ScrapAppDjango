from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    # profile_pic = models.ImageField(
    #     default='default.jpg', upload_to='profile_pics')
    phone = PhoneNumberField(blank=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email


class Scrapbook(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Scrapbooks')
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    friends_only = models.BooleanField()


# class Page(models.Model):
#     scrapbook = models.ForeignKey(
#         Scrapbook, on_delete=models.CASCADE, related_name='pages')
#     date_created = models.DateField(auto_now_add=True)
#     longitude = models.DecimalField(
#         max_digits=9, decimal_places=6, blank=True, null=True)
#     latitude = models.DecimalField(
#         max_digits=9, decimal_places=6, blank=True, null=True)

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


class TextElement(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='TextElements')
    text = models.CharField(max_length=255)
    xCoord = models.IntegerField()
    yCoord = models.IntegerField()


class ImageElement(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='ImageElements')
    # Image uri need or something??
    xCoord = models.IntegerField()
    yCoord = models.IntegerField()


# class Comment(models.Model):
#     page = models.ForeignKey(
#         Page, on_delete=models.CASCADE, related_name='page')
#     author = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, related_name='comment_author')
#     text = models.CharField(max_length=255)


class Comment(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='page')
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comment_author')
    body = models.CharField(max_length=255)


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower')
    scrapbook = models.ForeignKey(
        Scrapbook, on_delete=models.CASCADE, related_name='followed_scrapbook')


# class Friend(models.Model):
#     aFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
#     bFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
#     request_status = models.BooleanField()


# class Block(models.Model):
#     blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocks')
#     blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_blocked')

# Look at the premade github in app-dev-resources?
