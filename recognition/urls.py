from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings

app_name='recognition'

urlpatterns = [
 	path('', views.Home.as_view(), name='home'),
 	path('settings/', views.Home.as_view(), name='settings'),

 	path('login/', views.UserLoginView.as_view(), name='login'),
 	path('logout/', views.LogoutView.as_view(), name='logout'),
 	path('register/', views.UserRegistrationView.as_view(), name='register'),
 	path('settings/profile/', views.ProfileSettingsView.as_view(), name='edit-profile'),
 	path('settings/reg-face/', views.UserFaceRegView.as_view(), name='reg-face'),
 	path('apis/auth/', views.UserFaceLogInView.as_view(), name='api-auth')
]

