from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('/login', views.PrivateUserLoginView_with_otp.as_view(), name='login_using_otp'),
    path('/get-otp', views.PrivateUserLogin_get_otp.as_view(), name='get_otp'),
    path('/register', views.PublicUserRegistrationView.as_view(), name='register'),
]
