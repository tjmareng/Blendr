from builtins import range, classmethod

import random
from django.test import TestCase
import string

from Blendr.firebase_config import auth
from .views import clean_email, user_info, calculate_age, get_city_from_ip_address, get_distance_between_ip_addresses
from selenium import webdriver
import unittest


# Create your tests here.
class TestCases(unittest.TestCase):
    def test_user_info(self):
        user = auth.sign_in_with_email_and_password('lgrimaso@mtu.edu', 123123)
        correct_dict = {"username": "MANBOY II", "age": 25, "biography": "MANBOY RETURNS\r\n                    ",
                        "sexuality": "male", "gender": "female", "birthday": "1994-11-13", "email": "lgrimaso@mtu.edu"
                        , "friends": [False, "acbaurmtuedu", "javenwilliamgmailcom"], "ip_address": "141.219.226.150"}
        self.assertEqual(correct_dict, user_info(user['idToken']))


    def test_email_cleaning(self):
        email = "lgrimaso@mtu.edu"
        self.assertEqual(clean_email(email), "lgrimasomtuedu")


    def test_calculate_age(self):
        birth_date = "1999-05-18"
        self.assertEqual(20, calculate_age(birth_date))


    def test_calculate_age_today(self):
        birth_date = "1999-12-4"
        self.assertEqual(20, calculate_age(birth_date))


    def test_get_city_from_IP_address(self):
        self.assertEqual("Houghton", get_city_from_ip_address('141.219.226.150'))


    def test_get_distance_between_ip_addresses(self):
        print(get_distance_between_ip_addresses("141.219.226.150", "12.2.202.242"))
        self.assertEqual(439.90215249153596, get_distance_between_ip_addresses("141.219.226.150", "12.2.202.242"))

    # @classmethod
    # def test_createUser(cls):
    #
    #     def random_string(string_length=10):
    #         letters = string.ascii_lowercase
    #         return ''.join(random.choice(letters) for i in range(string_length))
    #     username = random_string(10)
    #
    #     cls.browser = webdriver.Chrome('C:\Selenium Drivers\chromedriver')
    #     cls.browser.maximize_window()
    #     cls.browser.get('http://127.0.0.1:8000/')
    #     cls.browser.find_element_by_name('Username').send_keys(username)
    #     cls.browser.find_element_by_name('Email').send_keys(username + "@gmail.com")
    #     cls.browser.find_element_by_name('Password').send_keys('qwertyu')
    #     cls.browser.find_element_by_name('confirmPassword').send_keys('qwertyu')
    #     cls.browser.find_element_by_name('signUP').click()

