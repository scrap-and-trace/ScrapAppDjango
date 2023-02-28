from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):

    username = models.Charfield()
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    profile_pic = models.ImageField(
        default='default.jpg', upload_to='profile_pics')
    phone = models.PhoneNumberField(blank=True)
    dob = models.DateField()

    def __str__(self):
        return self.email


class Scrapbook(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Scrapbooks')
    name = models.Charfield(maxLength=50)
    date_created = models.DateField(auto_now_add=True)
    private = models.BooleanField()


class Page(models.Model):
    scrapbook = models.ForeignKey(
        Scrapbook, on_delete=models.CASCADE, related_name='pages')
    date_created = models.DateField(auto_now_add)


class TextElement(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='TextElements')
    text = models.Charfield(maxLength=255)
    xCoord = models.IntegerField()
    yCoord = models.IntegerField()


class ImageElement(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='ImageElements')
    # Image uri need or something??
    xCoord = models.IntegerField()
    yCoord = models.IntegerField()


class Comment(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.Charfield(maxLength=255)


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='from_user')
    scrapbook = models.ForeignKey(
        Scrapbook, on_delete=models.CASCADE, related_name='followed_scrapbooks')


# class Friend(models.Model):
#     aFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
#     bFriend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
#     request_status = models.BooleanField()


# class Block(models.Model):
#     blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocks')
#     blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_blocked')

# Look at the premade github in app-dev-resources?
