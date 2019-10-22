from django.shortcuts import render

from Blendr.firebase_config import db, auth
# from .models import User
from main.models import User


def goto_index(request):
    return render(request, 'main/index.html')


def goto_login(request):
    # after finishing registration
    if request.method == 'POST':
        biography = request.POST.get('paragraph_text')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')

    return render(request, 'main/login.html')


def goto_profile_creation(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        conf_password = request.POST.get('confirmPassword')

        if password == conf_password:
            auth.create_user_with_email_and_password(email, password)
            new_user = User(email, username)
            db.child("users").child(username).set(user_to_dict(new_user))

            return render(request, 'main/profileCreation.html')
        # else: handle not matching error


# Converts User object to a dictionary to be stored in DB
def user_to_dict(self):
    return {"name": self.name, "email": self.email, }
