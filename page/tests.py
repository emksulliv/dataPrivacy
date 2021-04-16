from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from page.views import index

# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page(self):
        response = self.client.get('https://dataprivacy.herokuapp.com/')
        self.assertEqual(response.status_code, 200)
