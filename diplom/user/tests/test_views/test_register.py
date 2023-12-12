from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.payload = {
            'email' : 'test@gmail.com',
            'username' : 'Test',
            'password' : 'password_test'
        }
        self.url = reverse('register')

    def test_register_authenticated(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

