from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from django.contrib.auth import get_user_model


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@gmail.com',
            username = 'Test',
            password = 'password_test'
        ) 
        self.url = reverse('logout')

    def test_logout_authenticated(self):
        data = {"email": "test@gmail.com", "password": "password_test"}
        self.client.post(self.url, data, format="json")
        response = self.client.logout()
        self.assertEqual(response, None)

