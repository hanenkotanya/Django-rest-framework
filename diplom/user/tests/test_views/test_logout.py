from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class Settings(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@mail.ru", username = "Test", password="test123"
        )
        cls.data = {
            "email": "test@mail.ru",
            "password": "test123"
        }
        cls.login_url = reverse("login")
        cls.logout_url = reverse("logout")


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class LogoutTestCase(Settings):
    def test_logout_authenticated(self):
        response = self.client.post(self.login_url, self.data, format="json").data
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTestCaseNegativ(Settings):
    def test_login_not_authenticated(self):
        response = self.client.post(self.login_url, self.data, format="json").data
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)