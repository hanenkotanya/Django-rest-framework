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
        cls.login_url = reverse("login")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class LoginTestCase(Settings):
    def test_login_authenticated(self):
        data = {"email": "test@mail.ru", "password": "test123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginTestCaseNegativ(Settings):
    def test_login_not_authenticated(self):
        data = {"email": "wrong@mail.ru", "password": "test123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)