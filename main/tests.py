from django.test import TestCase
from .views import clean_email


# Create your tests here.
class BasicTestCase(TestCase):
    def test_email_cleaning(self):
        email = "lgrimaso@mtu.edu"
        self.assertEqual(clean_email(email), "lgrimasomtuedu")
