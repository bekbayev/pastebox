from datetime import timedelta

from django.core.exceptions import ValidationError
from freezegun import freeze_time
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Snippet

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

    def test_only_body_field_required_to_save_snippet(self) -> None:
        """
        To save the Snippet you only need to specify the body field.
        """
        empty_snippet = Snippet()
        with self.assertRaises(ValidationError):
            # Note that full_clean() will not be called automatically
            # when you call your model’s save() method. You’ll need to
            # call it manually when you want to run one-step model
            # validation for your own manually created models.
            # https://docs.djangoproject.com/en/3.2/ref/models/instances/#validating-objects
            empty_snippet.full_clean()
            empty_snippet.save()  # won't save if ValidationError raised

        self.assertEquals(Snippet.objects.count(), 0)

        snippet_with_only_body_field = Snippet(body="Only body")
        snippet_with_only_body_field.full_clean()
        snippet_with_only_body_field.save()

        self.assertEquals(Snippet.objects.count(), 1)
        snippet_with_only_body_field.refresh_from_db()
        self.assertEquals(snippet_with_only_body_field.body, "Only body")

    def test_string_representation(self) -> None:
        """
        __str__() method returns the title limited to 50 characters
        and adds an ellipsis at the end if it exceeds 50 characters.
        """
        max_title_length = 50
        short_title = "This title is less than 50 characters long."
        medium_title = "This title has exactly 50 characters, doesn't it?!"
        long_title = "And this title is definitely longer than 50 characters."

        snippet_short_title = Snippet(title=short_title)
        snippet_medium_title = Snippet(title=medium_title)
        snippet_long_title = Snippet(title=long_title)

        self.assertEqual(str(snippet_short_title), short_title)
        self.assertEquals(str(snippet_medium_title), medium_title)

        long_title = long_title[:max_title_length] + "..."
        self.assertEquals(str(snippet_long_title), long_title)

    def test_only_available_languages_that_pygments_supports(self) -> None:
        """
        Snippet.LANGUAGES must contain a short name that pygmetns
        supports: https://pygments.org/languages/
        The short name must be the first element in each tuple.
        Empty short name means no language support.
        """
        for language in Snippet.LANGUAGES:
            short_name, long_name = language
            try:
                get_lexer_by_name(short_name)
            except ClassNotFound:
                if short_name == "":  # no language support
                    continue
                self.fail(
                    f"Pygments does not support the alias`{short_name}` "
                    f"for the `{long_name}` language."
                )

    def test_generate_unique_url_returns_url_that_is_8_chars_long(self) -> None:
        url = Snippet()._generate_unique_url()
        self.assertEquals(len(url), 8, "The url must be exactly 8 characters long")

    def test_save_method_sets_the_url_if_not_given(self) -> None:
        snippet = Snippet()
        self.assertIs(snippet.url, "")
        snippet.save()
        self.assertIsInstance(snippet.url, str)
        self.assertGreater(len(snippet.url), 0)

    def test_generate_unique_url_returns_unique_url(self) -> None:
        """
        _generate_unique_url() always returns
        a new url that is not in the database.
        """
        url = Snippet()._generate_unique_url()
        # save the url to the database
        Snippet.objects.create(body="1", url=url)
        self.assertEquals(Snippet.objects.count(), 1)
        # create a new url that is not in the database
        new_url = Snippet()._generate_unique_url()
        self.assertNotEquals(url, new_url)

    def test_inactive_snippets(self) -> None:
        """InactiveSnippetManager returns only expired snippets."""
        future_time = timezone.now() + timedelta(minutes=10)
        Snippet.objects.create(expiration=future_time)
        Snippet.objects.create()  # no expiration

        self.assertEquals(Snippet.objects.count(), 2)
        self.assertEquals(Snippet.inactive.count(), 0)
        with freeze_time(future_time):  # going to the future
            self.assertEquals(Snippet.inactive.count(), 1)

    def test_active_snippets(self) -> None:
        """ActiveSnippetManager returns only unexpired snippets."""
        past_time = timezone.now() - timedelta(minutes=5)
        Snippet.objects.create(expiration=past_time)
        Snippet.objects.create()  # no expiration

        self.assertEquals(Snippet.objects.count(), 2)
        self.assertEquals(Snippet.active.count(), 1)
        with freeze_time(past_time - timedelta(seconds=1)):  # going back in time
            self.assertEquals(Snippet.active.count(), 2)
