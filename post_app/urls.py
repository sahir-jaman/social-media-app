from django.contrib import admin
from django.urls import path, include
from post_app import views

urlpatterns = [

    path('/user/posts', views.CreatePost.as_view()),
    path('/user/posts/<str:uid>',views.PostDetail.as_view()),
    path('/posts', views.PrivateAllFriendsPosts.as_view()),
    path('/posts', views.SerachPost.as_view()),


    path('/posts/<str:uid>/likes', views.LikePost.as_view()),

    path('/posts/<str:uid>/comments', views.CommentPost.as_view()),
]