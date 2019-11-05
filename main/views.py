from datetime import date, datetime

from django.shortcuts import render, render_to_response
from django.template import Context
from Blendr.firebase_config import db, auth
from main.models import UserCard


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

        if not username:
            raise ValueError('Empty username')

        if not email:
            raise ValueError('Empty email')

        if password != conf_password:
            raise ValueError('Passwords do not match')

        if len(password) < 6:
            raise ValueError('Passwords must be at least 6 characters long')

        response = render(request, 'main/profileCreation.html')
        response.set_cookie('registration_value_email', email, max_age=None)
        response.set_cookie('registration_value_username', username, max_age=None)
        response.set_cookie('registration_value_password', password, max_age=None)
        return response


def goto_complete_registration(request):
    if request.method == 'POST':
        # after finishing registration
        username = request.COOKIES.get('registration_value_username')
        email = request.COOKIES.get('registration_value_email')
        password = request.COOKIES.get('registration_value_password')

        biography = request.POST.get('biography')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        age = calculate_age(birthday)

        if age >= 21:
            # upload user to database
            new_user = {'email': email, 'username': username, 'biography': biography,
                        'sexuality': sexuality, 'gender': gender, 'birthday': birthday,
                        'age': age, }
            db.child("users").child(clean_email(email)).set(new_user)

            # authentication process
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            return render(request, 'main/emailVerification.html')
        else:
            print('under aged')
            raise ValueError('You have to be 21 to be on Blendr')


def calculate_age(birth_date_string):
    days_in_year = 365.2425
    birth_date = datetime.strptime(birth_date_string, '%Y-%m-%d').date()
    age = int((date.today() - birth_date).days / days_in_year)
    return age


def goto_homepage(request):
    # create users based on the database
    user_card_list = []
    results = db.child("users").get()
    for key in results.val():
        username = results.val()[key]["username"]
        bio = results.val()[key]["biography"]
        birthday = results.val()[key]["birthday"]
        gender = results.val()[key]["gender"]
        sexuality = results.val()[key]["sexuality"]
        email = results.val()[key]["email"]
        new_user_card = UserCard(username=username, biography=bio, birthday=birthday, gender=gender, iso=sexuality, email=email)
        user_card_list.append(new_user_card)
    context_dict = {"Users" : user_card_list}
    return render(request, "main/homepage.html", context=context_dict)


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        auth.send_password_reset_email(email)
    return render(request, 'main/login.html')


def clean_email(email):
    cleaned_email = ""
    for i in email:
        if i != '@' and i != '.':
            cleaned_email += i
    return cleaned_email


def verify_login_credentials(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        user = auth.sign_in_with_email_and_password(email, password)

        return goto_homepage(request)




