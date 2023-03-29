"""scrap URL Configuration
"""
from django.contrib import admin

from django.urls import path, include
from accounts.api import (RegisterAPI, LoginAPI, UserAPI, ScrapbookAPI, FollowListCreateAPI,
                          FollowDestroyAPI, SearchUsersAPI, ScrapbookDestroyAPI, PageLikesListAPI,
                          PageLikesDeleteAPI, PageLikedAPI, UserLikesAPI,)
from accounts.api import UserViewSet, PageAPI, CommentViewSet
from knox import views as knox_views


from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', UserViewSet, 'user')
router.register('page', PageAPI, 'page')
router.register('comment', CommentViewSet, 'comment')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(router.urls)),

    # User APIs
    path('api/auth/register/', RegisterAPI.as_view()),
    # path(r'api/auth/', include('knox.urls')),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/logoutall/', knox_views.LogoutAllView.as_view(),
         name='knox_logoutall'),
    path('api/auth/login/', LoginAPI.as_view()),
    # path('api/auth/logout/', LogoutAPI.as_view()),
    path('api/auth/user/', UserAPI.as_view()),
    path('api/auth/searchUsers/', SearchUsersAPI.as_view()),

    # Scrapbook APIs
    path('api/auth/scrapbooks/', ScrapbookAPI.as_view()),
    path('api/auth/deletescrapbook/<int:pk>/', ScrapbookDestroyAPI.as_view()),

    # Following APIs
    path('api/auth/followlist/<int:pk>/', FollowListCreateAPI.as_view()),
    # ^ GET shows the scrapbooks the user follows
    # ^ POST creates new follow from user to the Scrapbook[pk]
    path('api/auth/deletefollow/<int:pk>/', FollowDestroyAPI.as_view()),
    # ^ DELETE deletes the follow from user to Scrapbook[pk]

    # Like APIs
    path('api/auth/likes/<int:pk>/', PageLikesListAPI.as_view()),
    # ^ shows all likes from page[PK]
    path('api/auth/deletelike/<int:pk>/', PageLikesDeleteAPI.as_view()),
    # ^ Deletes like on page[pk] from request's user
    path('api/auth/userlikes/<int:pk>/', UserLikesAPI.as_view()),
    # ^ shows all like from user[PK]
    path(('api/auth/isliked/<int:pk>/'), PageLikedAPI.as_view()),




]

# urlpatterns = [
#     path('api/auth/', include('knox.urls')),
#     path('api/auth/register', RegisterAPI.as_view()),
#     path('api/auth/login', LoginAPI.as_view()),
#     path('api/auth/user', UserAPI.as_view()),
#     path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
#     path('api/', include(router.urls))
# ]
