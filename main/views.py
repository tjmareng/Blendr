from django.shortcuts import render, render_to_response

from Blendr.firebase_config import db, auth
from main.models import User


def goto_index(request):
    return render(request, 'main/index.html')


def goto_login(request):
    return render(request, 'main/login.html')


def goto_profile_creation(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        conf_password = request.POST.get('confirmPassword')

        if password == conf_password:
            auth.create_user_with_email_and_password(email, password)

            response = render(request, 'main/profileCreation.html')
            response.set_cookie('registration_value_email', email, max_age=None)
            response.set_cookie('registration_value_username', username, max_age=None)

            return response
        # else: handle not matching error


def goto_complete_registration(request):
    if request.method == 'POST':
        # after finishing registration

        username = request.COOKIES.get('registration_value_username')
        email = request.COOKIES.get('registration_value_email')
        biography = request.POST.get('biography')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')

        new_user = {'email': email, 'username': username, 'biography': biography,
                    'sexuality': sexuality, 'gender': gender, }
        db.child("users").child(clean_email(email)).set(new_user)

    return render(request, 'main/login.html')


def reset_password(request):
    return request(request, '')


def clean_email(email):
    cleaned_email = ""
    for i in email:
        if i != '@' and i != '.':
            cleaned_email += i
    return cleaned_email
