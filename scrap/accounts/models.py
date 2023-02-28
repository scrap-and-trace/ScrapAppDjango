from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    username = models.Charfield()
    # Is this defined because in the base User class it is not unique?
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


class Page(models.Model):
    scrapbook = models.ForeignKey(
        Scrapbook,  on_delete=models.CASCADE, related_name='pages')


class Post(models.Model):
    page = models.ForeignKey(Page, related_name='posts',
                             on_delete=models.CASCADE)
