from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import Snippet

User = get_user_model()


class SnippetModelTest(TestCase):
    def test_save_and_retrieve(self) -> None:
        """
        The Snippet is saved in the database with the specified values
        and is taken from the database with the same values.
        """
        user = User.objects.create()
        expiration = timezone.now() + timedelta(days=21)
        Snippet.objects.create(
            author=user,
            title="The Python code",
            body="print('Need more tests!')",
            syntax="python",
            expiration=expiration,
            url="4pT5hi6s",
        )
        self.assertEquals(Snippet.objects.count(), 1)
        snippet = Snippet.objects.last()
        self.assertEquals(snippet.author, user)
        self.assertEquals(snippet.title, "The Python code")
        self.assertEquals(snippet.body, "print('Need more tests!')")
        self.assertEquals(snippet.syntax, "python")
        self.assertEquals(snippet.expiration, expiration)
        self.assertEquals(snippet.url, "4pT5hi6s")

    def test_default_title(self) -> None:
        """
        If the Snippet is saved without a title,
        the default title will be used.
        """
        Snippet.objects.create(body="default title")
        snippet = Snippet.objects.last()
        self.assertEquals(snippet.title, "Untitled")
