from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.shortcuts import render
from page.views import index
from page.models import User

# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page(self):
        response = self.client.get('https://dataprivacy.herokuapp.com/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>page</title>', html)
        self.assertIn(
            '<div id="myModal" class="modal fade" role="dialog">', html)
        self.assertTrue(html.endswith('</html>'))


class LoginTest(TestCase):
    def test_check_login(self):
        request = HttpRequest()
        response = render(request, 'login.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Login</title>', html)

class DBTest(TestCase):
    def setUp(self):
        User.objects.create(session_id="1", user_name="Bob", user_token="123")
        User.objects.create(session_id="2", user_name="Jane", user_token="456")

    def test_properly_added(self):
        bob = User.objects.get(user_name="Bob")
        jane = User.objects.get(user_name="Jane")
        self.assertTrue(bob)
