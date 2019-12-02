from builtins import int, ValueError, len
from django.contrib.gis.geoip2 import GeoIP2
from datetime import date, datetime

from django.shortcuts import render, render_to_response
from django.template import Context
from requests import HTTPError

from Blendr.firebase_config import db, auth, pyrebase, storage
from main.forms import UploadFileForm
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

        # photo = request.POST.get('pic')
        # print(photo)
        # storage.child("Pics").put(photo)
        #
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     UserCard.picture = UploadFileForm.cleaned_data['picture']
        #     UserCard.save()
        #     print(UserCard.picture)
        # else:
        #     form= UploadFileForm()

        biography = request.POST.get('biography')
        sexuality = request.POST.get('sexuality')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        age = calculate_age(birthday)
        ip_address = get_client_ip_address(request)
        friends_list = [False]
        if age >= 21:
            # upload user to database
            new_user = {'email': email, 'username': username, 'biography': biography,
                        'sexuality': sexuality, 'gender': gender, 'birthday': birthday,
                        'age': age, 'friends': friends_list, 'ip_address': ip_address, }
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
    context_dict = retrieve_database_users()
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


def user_info(user_token):
    account_info = auth.get_account_info(user_token)
    key = clean_email(account_info['users'][0]['email'])
    card_info = db.child("users").get()
    username = card_info.val()[key]['username']
    age = card_info.val()[key]['age']
    biography = card_info.val()[key]['biography']
    sexuality = card_info.val()[key]['sexuality']
    gender = card_info.val()[key]['gender']
    birthday = card_info.val()[key]['birthday']
    email = card_info.val()[key]['email']
    ip_address = card_info.val()[key]['ip_address']
    friends = card_info.val()[key]['friends']
    info_dict = {'username': username, "age": age, "biography": biography, "sexuality": sexuality,
                 "gender": gender, "birthday": birthday, "email": email, "ip_address": ip_address, "friends": friends,}
    return info_dict


def verify_login_credentials(request):
    print("Verify Login Credentials")
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        # try:
        # sign_in_with_email_and_password returns user data with an "idToken"
        user = auth.sign_in_with_email_and_password(email, password)
        response = goto_homepage(request)
        response.set_cookie('user_id_token', user['idToken'], max_age=None)
        user_info(user['idToken'])
        # except HTTPError:
            # print("WRONG!")
        return response


def goto_friends_page(request):
    current_user = user_info(request.COOKIES.get('user_id_token'))
    current_user_friends = current_user['friends']
    print(current_user_friends)
    context_dict = retrieve_database_users_friends_only(current_user_friends)
    return render(request, 'main/friends.html', context=context_dict)


def get_client_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    if ip_address == '127.0.0.1':
        # assuming it is one of us, manually setting ip address to the school's external IP address
        ip_address = '141.219.226.150'
    return ip_address


def get_city_from_ip_address(ip_address):
    g = GeoIP2()
    city = g.city(ip_address).get('city')
    return city


def get_distance_between_ip_addresses(ip1, ip2):
    g = GeoIP2()
    coordinates1 = g.lat_lon(ip1)
    coordinates2 = g.lon_lat(ip2)
    print(coordinates1 + ', ' + coordinates2)
    # TODO implement distance calculation


def goto_edit_profile(request):
    return render(request, 'main/ViewProfile.html', context=user_info(request.COOKIES.get('user_id_token')))


def retrieve_database_users():
    user_card_list = []
    results = db.child("users").get()
    for key in results.val():
        username = results.val()[key]["username"]
        bio = results.val()[key]["biography"]
        birthday = results.val()[key]["birthday"]
        gender = results.val()[key]["gender"]
        sexuality = results.val()[key]["sexuality"]
        email = results.val()[key]["email"]
        age = results.val()[key]["age"]
        city = get_city_from_ip_address(results.val()[key]["ip_address"])
        new_user_card = UserCard(username=username, biography=bio, birthday=birthday, gender=gender, iso=sexuality,
                                 email=email, age=age, city=city)
        user_card_list.append(new_user_card)
    context_dict = {"Users": user_card_list}
    return context_dict


def retrieve_database_users_friends_only(current_user_friends):
    user_card_list = []
    results = db.child("users").get()
    for key in results.val():
        email = results.val()[key]["email"]
        if clean_email(email) in current_user_friends:
            username = results.val()[key]["username"]
            bio = results.val()[key]["biography"]
            birthday = results.val()[key]["birthday"]
            gender = results.val()[key]["gender"]
            sexuality = results.val()[key]["sexuality"]
            age = results.val()[key]["age"]
            city = get_city_from_ip_address(results.val()[key]["ip_address"])
            new_user_card = UserCard(username=username, biography=bio, birthday=birthday, gender=gender, iso=sexuality,
                                     email=email, age=age, city=city)
            user_card_list.append(new_user_card)
    context_dict = {"Users": user_card_list}
    return context_dict


def update_friends(request):
    cleaned_friends_email = clean_email(request.POST.get('like_button'))
    current_user = user_info(request.COOKIES.get('user_id_token'))
    for friend in current_user["friends"]:
            if friend == cleaned_friends_email:
                return goto_homepage(request)
    current_user["friends"].append(cleaned_friends_email)
    current_user_cleaned_email = clean_email(current_user['email'])
    db.child("users").child(current_user_cleaned_email).set(current_user)
    return goto_homepage(request)

def remove_friend(request):
    cleaned_friends_email = clean_email(request.POST.get('like_button'))
    current_user = user_info(request.COOKIES.get('user_id_token'))
    for friend in current_user["friends"]:
        if friend == cleaned_friends_email:
            current_user["friends"].remove(friend)
            current_user_cleaned_email = clean_email(current_user['email'])
            db.child("users").child(current_user_cleaned_email).set(current_user)
    return goto_friends_page(request)