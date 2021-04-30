from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from django.http import HttpResponseRedirect, HttpRequest
from django.test.client import Client, RequestFactory
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.helpers import complete_social_login
from django.test.utils import override_settings
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length
from django.contrib import auth
from django.contrib.sites.models import Site
from accounts.views import index
from json2html import *

class TestLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.username = "test@test.com"
        self.password = "password"
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_login_page(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse(
            'account_login'), {"login": self.username, "password": self.password}
        )
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)

class TestUnauthenticatedUser(TestCase):
    def test_view_exists_at_desired_location_and_redirects(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name_and_redirects(self):
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code, 302)

class TestJson(TestCase):
    def test_empty_json(self):
            self.assertEqual(json2html.convert(json = ""),"")
            self.assertEqual(json2html.convert(json = []), "")
            self.assertEqual(json2html.convert(json = {}), "")
    def test_json(self):
        test = {
                  "name": "John",
                  "age": 30,
                  "city": "New York"
                }
        expected = '<table border="1"><tr><th>name</th><td>John</td></tr><tr><th>age</th><td>30</td></tr><tr><th>city</th><td>New York</td></tr></table>'
        self.assertEqual(json2html.convert(json = test), expected)