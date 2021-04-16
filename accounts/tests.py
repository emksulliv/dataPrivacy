from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length


class TestLogin(TestCase):
    def setUp(self):
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


