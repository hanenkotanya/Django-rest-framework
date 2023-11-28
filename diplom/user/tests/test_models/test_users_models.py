from django.test import TestCase
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from user.models import get_avatar_full_path, Profile, User


class GeneralTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@mail.com", username="Test", password="testpass")

    def test_get_avatar_full_path(self):
        filename = "avatar.png"
        to_test = get_avatar_full_path(self.user, filename)
        self.assertEqual(to_test, "1/image/avatar.png")

    def test_get_avatar_url(self):

        to_test = f"https://protfo.pro/{self.user.id}/image"
        self.assertEqual(to_test, "https://protfo.pro/1/image")

    def test_profile_save(self):

        image = "avatar.png"
        Profile.objects.create(user=self.user, image=image)
        self.assertEqual(self.user.profile.avatar_url, "https://protfo.pro/1/image")