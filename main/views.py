from django.shortcuts import render

from Blendr.firebase_config import db, auth
from main.models import User


def goto_index(request):
    return render(request, 'main/index.html')


def goto_login(request):
    return render(request, 'main/login.html')


def goto_profile_creation(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        conf_password = request.POST.get('confirmPassword')

        if password == conf_password:
            auth.create_user_with_email_and_password(email, password)

            return render(request, 'main/profileCreation.html')
        # else: handle not matching error


def goto_complete_registration(request):
    if request.method == 'POST':
        # after finishing registration

        username = request.POST.get('Username')
        email = request.POST.get('Email')
        biography = request.POST.get('paragraph_text')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')

        new_user = User(email, username, biography, sexuality, gender)
        db.child("users").child(email).set(user_to_dict(new_user))

    return render(request, '')


def reset_password(request):
    return request(request, '')


# Converts User object to a dictionary to be stored in DB
def user_to_dict(self):
    return {"email": self.email, "name": self.username,
            "biography": self.biography, "sexuality": self.iso,
            "gender": self.gender, }


def clean_email(email):
    cleaned_email = ""
    for i in email:
        if i != '@' and i != '.':
            cleaned_email += i
    return cleaned_email
