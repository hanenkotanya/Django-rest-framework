from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from django.contrib.auth import get_user_model


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@gmail.com',
            username = 'Test',
            password = 'password_test'
        ) 
        self.url = reverse('login')
    def test_login_authenticated(self):
        data = {"email": "test@gmail.com", "password": "password_test"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_not_authenticated(self):
        data = {"email": "wrong@mail.ru", "password": "test123"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)