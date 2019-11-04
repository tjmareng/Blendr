from django.test import TestCase
from .views import clean_email
from selenium import webdriver
import unittest
import string
import random


# Create your tests here.
class TestCases(unittest.TestCase):
    #def test_email_cleaning(self):
       # email = "lgrimaso@mtu.edu"
        # self.assertEqual(clean_email(email), "lgrimasomtuedu")

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

