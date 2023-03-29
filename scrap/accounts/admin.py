from django.contrib import admin
from .models import CustomUser, Scrapbook, Page, Comment, Follow, PageLikes
# Register your models here.
# This allows for any models made to be accessed from the admin site

admin.site.register(CustomUser)
admin.site.register(Scrapbook)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(PageLikes)
