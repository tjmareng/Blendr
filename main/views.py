from django.shortcuts import render

from Blendr.firebase_config import db, auth
# from .models import User


def index(request):
    return render(request, 'main/index.html')


def login(request):

    # after finishing registration
    if request.method == 'POST':
        biography = request.POST.get('paragraph_text')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')

    return render(request, 'main/login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        conf_password = request.POST.get('confirmPassword')

        if password == conf_password:
            # user = User(email, name, password)
            # db.child("users").push(user)
            test_data = {"email": email, "name": name}

            db.child("users").push(test_data)
            auth.create_user_with_email_and_password(email, password)

            return render(request, 'main/profileCreation.html')
        # else: handle not matching error
