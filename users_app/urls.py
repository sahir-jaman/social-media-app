from django.contrib import admin
from django.urls import path, include
from authentication import views
from users_app import views

urlpatterns = [
    path("/profile", views.PrivateUserProfileViewDetail.as_view(), name="user_profile"),
    # path("/profile/search", views.SearchUser.as_view(), name="search user"),
    path("/follows/<str:uid>", views.UserConnectionView.as_view(), name="follow a person"),
    path("/follows", views.UserConnectionView.as_view(), name="followers list"),
]
