"""Blendr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from django.urls import path

urlpatterns = [
    path('', views.goto_index, name="index"),
    path('login.html/', views.goto_login, name="login"),
    path('profileCreation.html/', views.goto_profile_creation, name="signup"),
    path('homepage.html/', views.goto_homepage, name="homepage"),
    path('profileCreation.html/login.html/login.html/', views.goto_login, name="login2"),
    path('login.html/login.html/', views.reset_password, name="reset_password"),


    # THIS IS A TEMPORARY SOLUTION
    path('profileCreation.html/login.html/', views.goto_complete_registration, name="login")
]
