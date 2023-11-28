from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from personage.models import Personage
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
        
        cls.personage = Personage.objects.create_personage(
            creator = cls.user, 
            name ="Olaf",
            description ="Personage",
        )
        cls.personage_list = reverse("personage_list")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class PersonageListTestCase(Settings):
    def test_personage_list(self):
        personages = Personage.objects.all()
        data = {"personager":personages}
        response = self.client.get(self.personage_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


