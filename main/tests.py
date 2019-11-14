from builtins import range, classmethod

import random
from django.test import TestCase
import string

from Blendr.firebase_config import auth
from .views import clean_email, user_info
from selenium import webdriver
import unittest


# Create your tests here.
class TestCases(unittest.TestCase):
    def test_user_info(self):
        user = auth.sign_in_with_email_and_password('lgrimaso@mtu.edu', 123123)
        correct_dict = {"username": "Logan", "age": 22, "biography": "Just want the physical affection and personal connection with another human being.",
                        "sexuality": "female", "gender": "male", "birthday": "1997-05-18", "email": "lgrimaso@mtu.edu"}
        self.assertEqual(correct_dict, user_info(user['idToken']))


    def test_email_cleaning(self):
        email = "lgrimaso@mtu.edu"
        self.assertEqual(clean_email(email), "lgrimasomtuedu")


    @classmethod
    def test_createUser(cls):

        def random_string(string_length=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(string_length))
        username = random_string(10)

        cls.browser = webdriver.Chrome('C:\Selenium Drivers\chromedriver')
        cls.browser.maximize_window()
        cls.browser.get('http://127.0.0.1:8000/')
        cls.browser.find_element_by_name('Username').send_keys(username)
        cls.browser.find_element_by_name('Email').send_keys(username + "@gmail.com")
        cls.browser.find_element_by_name('Password').send_keys('qwertyu')
        cls.browser.find_element_by_name('confirmPassword').send_keys('qwertyu')
        cls.browser.find_element_by_name('signUP').click()

