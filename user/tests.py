from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User
from django.contrib.auth import get_user_model
from rest_framework import status


class TestUserRegistration(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.data = {
            "email": "test@example.com",
            "username": "test_user",
            "password": "password",
        }

    def test_registration(self):

        # Отправить запрос на регистрацию
        response = self.client.post(self.url, self.data)

        # Проверить статус ответа
        self.assertEqual(response.status_code, 201)

        # Получить зарегистрированного пользователя
        user = User.objects.get(username="test_user")

        # Убедиться, что пользователь был успешно зарегистрирован
        self.assertTrue(user.is_active)


class LoginLogoutDeleteTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        # Cоздаем юзера
        self.user = get_user_model().objects.create_user(**self.user_data)

        # Прописываем путь для логинизации
        self.login_url = reverse("login")

        # Прописываем путь для логаута
        self.logout_url = reverse("logout")

        # Данные для логинизации
        self.valid_credentials = {
            "email": "test@example.com",
            "password": "testpassword",
        }

        # Неверные данные для логинизации
        self.invalid_credentials = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }

    # Логинизация с верными данными
    def test_login_with_valid_credentials(self):

        response = self.client.post(
            self.login_url, self.valid_credentials, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "login successful")

    # Логинизация с неверными данными
    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url, self.invalid_credentials, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Invalid email or password")

    # Логaут
    def test_logout(self):
        # Логинизация
        self.client.post(self.login_url, self.valid_credentials, format="json")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertNotIn("_auth_user_id", self.client.session)

    #Удаление юзера
    def test_delete(self):
        # Логинизация
        self.client.post(self.login_url, self.valid_credentials, format="json")
        user = User.objects.get(username="testuser")
        test_id = user.id
        delete_url = reverse("user_delete", args={test_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)