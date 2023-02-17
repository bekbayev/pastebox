from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    def test_get_absolute_url(self):
        user = User.objects.create(username="fizzbuzz")
        expected_url = reverse("profile", kwargs={"username": user.username})
        self.assertEquals(user.get_absolute_url(), expected_url)
