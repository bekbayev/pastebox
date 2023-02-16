from django.contrib.auth import get_user_model
from django.test import TestCase

from snippets.models import Snippet

User = get_user_model()


class ProfileDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")

    def test_uses_template(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_display_user_snippets(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertNotContains(response, "fizzbuzz")

        Snippet.objects.create(author=self.user, title="fizzbuzz", body="1")
        response = self.client.get(self.user.get_absolute_url())
        self.assertContains(response, "fizzbuzz")
