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
from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('', views.goto_index, name="index"),
    url('login.html/', views.goto_login, name="login"),
    url('profileCreation.html', views.goto_profile_creation, name="signup"),
    url('homepage.html', views.goto_homepage, name="homepage"),
    url('emailVerification.html', views.goto_complete_registration, name="email_verification"),
    url('login.html', views.reset_password, name="reset_password"),
]