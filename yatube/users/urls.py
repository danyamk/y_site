from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_reset/',
         PasswordResetView.as_view(), name='password_reset_form'),
]
