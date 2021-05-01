from allauth.account import app_settings as account_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
from allauth.utils import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
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
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>page</title>', html)
        self.assertIn(
            '<div id="myModal" class="modal fade" role="dialog">', html)
        self.assertTrue(html.endswith('</html>'))

    def test_front_end(self):
        r = requests.get('https://dataprivacy.herokuapp.com/')
        page_src = r.text

        if page_src.find('Helping you become more literate') < 0:
            self.fail("Can't find descriptor text in jumbotron")

        if page_src.find('Twitter') < 0:
            self.fail("Can't find descriptor text in jumbotron")

        if page_src.find('Google') < 0:
            self.fail("Can't find descriptor text in jumbotron")

        if page_src.find('Facebook') < 0:
            self.fail("Can't find descriptor text in jumbotron")

        if page_src.find('Amazon') < 0:
            self.fail("Can't find descriptor text in jumbotron")


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


class SocialAccountTests(TestCase):

    @override_settings(
        SOCIALACCOUNT_AUTO_SIGNUP=True,
        ACCOUNT_SIGNUP_FORM_CLASS=None,
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE  # noqa
    )
    def test_email_address_created(self):
        factory = RequestFactory()
        request = factory.get('/accounts/login/callback/')
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        User = get_user_model()
        user = User()
        setattr(user, account_settings.USER_MODEL_USERNAME_FIELD, 'test')
        setattr(user, account_settings.USER_MODEL_EMAIL_FIELD, 'test@test.com')

        account = SocialAccount(user=user, provider='openid', uid='123')
        sociallogin = SocialLogin(account)
        complete_social_login(request, sociallogin)

        user = User.objects.get(
        **{account_settings.USER_MODEL_USERNAME_FIELD: 'test'}
        )
        self.assertTrue(
            SocialAccount.objects.filter(user=user, uid=account.uid).exists()
        )
        self.assertTrue(
            EmailAddress.objects.filter(user=user,
                                        email=user_email(user)).exists()
        )
