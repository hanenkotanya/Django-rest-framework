from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User, Profile



class RegisterTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.data = {"email": "test@example.com", "password": "testpassword"}

    def test_login_not_authenticated(self):
        response = self.client.post(self.register_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        profile = Profile.objects.get()
        self.assertEqual(user.email, "test@example.com")
        self.assertIsNotNone(getattr(profile, "invite_hash", None))
        self.assertIsNotNone(getattr(profile, "url", None))



class RegisterTestCaseNegativ(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")

    
    def failure_registration(self, data, counts):
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), counts)


    def test_user_registration_no_email(self):
        data = {
            "email": "",
            "password": "testpassword",
        }

        self.failure_registration(data, 0)


    def test_user_registration_wrong_email(self):
        data = {
            "email": "usermail.ru",
            "password": "testpassword",
        }

        self.failure_registration(data, 0)

    def test_user_registration_user_exists(self):
        User.objects.create_user(email="user@mail.ru", username="Test", password="testpassword")

        data = {
            "email": "user@mail.ru",
            "password": "testpassword",
        }

        self.failure_registration(data, 1)