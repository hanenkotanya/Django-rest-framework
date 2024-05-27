from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Post
from django.contrib.auth import get_user_model
from rest_framework import status


class CreatePostTestCase(APITestCase):
    def setUp(self):
        self.user_data1 = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }

        self.user_data2 = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword2",
        }

        self.user_data3 = {
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "testpassword3",
        }
        # Cоздаем юзера
        self.user = get_user_model().objects.create_user(**self.user_data1)

        # Cоздаем юзера2
        self.user2 = get_user_model().objects.create_user(**self.user_data2)

        # Cоздаем юзера3
        self.user = get_user_model().objects.create_user(**self.user_data3)

        # Прописываем путь для логинизации
        self.login_url = reverse("login")

        # Прописываем путь для создания поста
        self.create_post_url = reverse("create_post")

        # Прописываем путь для просмотра активных постов
        self.my_posts_activity_url = reverse("posts_list")

        # Данные для логинизации 1
        self.valid_credentials1 = {
            "email": "test@example.com",
            "password": "testpassword",
        }

        # Данные для логинизации 2
        self.valid_credentials2 = {
            "email": "test2@example.com",
            "password": "testpassword2",
        }

        # Данные для логинизации 3
        self.valid_credentials3 = {
            "email": "test3@example.com",
            "password": "testpassword3",
        }

        self.data_for_post1 = {"name": "Test", "text": "TestText"}

        self.data_for_post2 = {"name": "Test2", "text": "TestText2"}

        self.data_for_post3 = {"name": "Test3", "text": "TestText3"}

        self.data_for_post4 = {"name": "Test4", "text": "TestText4"}

        self.data_for_post5 = {"name": "Test5", "text": "TestText5"}

        self.data_for_post1_update = {"name": "Test_update","text": "Test"}

    # Проверяем функционал постов
    def test_post(self):

        # Логинизация под первым пользователем
        self.client.post(self.login_url, self.valid_credentials1, format="json")

        # Отправить запрос на создание поста1
        response = self.client.post(
            self.create_post_url, self.data_for_post1, format="json"
        )
        posts = Post.objects.all()

        # Проверить статус ответа
        self.assertEqual(response.status_code, 201)

        # Посчитали количество постов
        count_posts = posts.count()
        assert count_posts == 1

        # Создаем от этого пользователя еще 4 поста для тестов
        response = self.client.post(
            self.create_post_url, self.data_for_post2, format="json"
        )

        response = self.client.post(
            self.create_post_url, self.data_for_post3, format="json"
        )
        response = self.client.post(
            self.create_post_url, self.data_for_post4, format="json"
        )

        response = self.client.post(
            self.create_post_url, self.data_for_post5, format="json"
        )
        count_posts = posts.count()
        assert count_posts == 5

        # Проверяем вывод всех активных постов
        response = self.client.get(self.my_posts_activity_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем доступ к одному посту
        post_detail_url = reverse("single_post", args=[1])
        response = self.client.get(post_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем удаление поста пользователем который его создал
        post_delete_url = reverse("delete_post", args=[1])
        response = self.client.delete(post_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count_posts = posts.count()
        assert count_posts == 4

        # Проверяем удаление поста пользователем который его не создал
        self.client.post(self.login_url, self.valid_credentials3, format="json")
        post_delete_url = reverse("delete_post", args=[3])
        response = self.client.delete(post_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        count_posts = posts.count()
        assert count_posts == 4
