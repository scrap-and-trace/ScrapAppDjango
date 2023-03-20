"""scrap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from accounts.api import (RegisterAPI, LoginView, UserAPI, ScrapbookAPI, FollowListCreateAPI,
                          FollowDestroyAPI, SearchUsersAPI, ScrapbookDestroyAPI, PageLikesListAPI,
                          PageLikesDeleteAPI, UserLikesAPI,)
from accounts.api import UserViewSet, PageAPI, CommentViewSet
from knox import views as knox


from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', UserViewSet, 'user')
router.register('page', PageAPI, 'page')
router.register('comment', CommentViewSet, 'comment')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # User APIs
    path('api/auth/register/', RegisterAPI.as_view()),
    path(r'api/auth/', include('knox.urls')),
    # path('api/auth/login/', LoginAPI.as_view()),
    # path('api/auth/logout/', LogoutAPI.as_view()),
    path('api/auth/user/', UserAPI.as_view()),
    path('api/auth/searchUsers/', SearchUsersAPI.as_view()),

    # Scrapbook APIs
    path('api/auth/scrapbooks/', ScrapbookAPI.as_view()),
    path('api/auth/deletescrapbook/<int:pk>/', ScrapbookDestroyAPI.as_view()),

    # Following APIs
    path('api/auth/followlist/<int:pk>/', FollowListCreateAPI.as_view()),
    path('api/auth/deletefollow/<int:pk>/', FollowDestroyAPI.as_view()),

    # Like APIs
    path('api/auth/likes/<int:pk>/', PageLikesListAPI.as_view()),
    # ^ shows all likes from page[PK]
    path('api/auth/deletelike/<int:pk>/', PageLikesDeleteAPI.as_view()),
    # ^ Deletes like[PK]
    path('api/auth/userlikes/<int:pk>/', UserLikesAPI.as_view()),
    # ^ shows all like from user[PK]





]

# urlpatterns = [
#     path('api/auth/', include('knox.urls')),
#     path('api/auth/register', RegisterAPI.as_view()),
#     path('api/auth/login', LoginAPI.as_view()),
#     path('api/auth/user', UserAPI.as_view()),
#     path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
#     path('api/', include(router.urls))
# ]
