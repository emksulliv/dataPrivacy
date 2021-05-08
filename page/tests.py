from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.shortcuts import render
from page.views import index
from page.models import User
import requests

# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page(self):
        response = self.client.get('https://dataprivacy.herokuapp.com/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('<title>page</title>', html)
        self.assertIn(
            '<div id="myModal" class="modal fade" role="dialog">', html)
        self.assertTrue(html.endswith('</html>\r\n') or html.endswith('</html>\r') or html.endswith('</html>\n'))

    def test_front_end(self):
        r = requests.get('https://dataprivacy.herokuapp.com/')
        page_src = r.text

        if page_src.find('Helping you become more literate') < 0:
            self.fail("Can't find descriptor text in jumbotron")

        if page_src.find('>Twitter<') > 0:
            self.fail("Still has old Twitter button instead of logo")

        if page_src.find('>Facebook<') > 0:
            self.fail("Still has old Facebook button instead of logo")

        if page_src.find('>Google<') > 0:
            self.fail("Still has old Google button instead of logo")

        if page_src.find('>Amazon<') > 0:
            self.fail("Still has old Amazon button instead of logo")

class FacebookTest(TestCase):
    def test_information(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertIn('<h4 class="modal-title">Your Facebook information!</h4>', html)

        access_token_test_user = 'EAAEf3EW7k20BAIL1hwmd4V5OqhvQjemXHYHfZATUIlolotIxVeNxqfD5ZCHleZAZBMHbBysRU36VSQhHUWZCHagf2sQfFjNbZCnZCX5KzANQfmc16C663ZC9UxppUFM8XBU0LdSZBZCahiMZAlIcRSH6goMVirtVkZAZC6TjZB9vsBCZBCcHX8iVUgcWTl9IPzFLE5pukwfZCZATudfBnsAZDZD';
        name = 'Tyler Alffecahdfbce Baoberg';
        
        #TODO - Figure out test user integration test

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
