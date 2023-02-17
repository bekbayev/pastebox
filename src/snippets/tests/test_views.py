from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import SnippetForm
from ..models import Snippet

User = get_user_model()


class SnippetCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_page = reverse("snippets:index")
        cls.user = User.objects.create(username="testuser")

    def test_uses_index_template(self):
        response = self.client.get(self.main_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "snippets/index.html")

    def test_uses_form(self):
        response = self.client.get(self.main_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["form"], SnippetForm)

    def test_can_save_post_request(self):
        payload = {"body": "Just a text."}
        response = self.client.post(self.main_page, data=payload)
        self.assertEquals(Snippet.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        snippet = Snippet.objects.first()
        self.assertEquals(snippet.body, "Just a text.")

    def test_snippet_author_is_set_for_authenticated_user(self):
        self.client.force_login(self.user)
        self.client.post(self.main_page, data={"body": "authenticated"})
        snippet = Snippet.objects.first()
        self.assertEquals(snippet.author, self.user)

    def test_snippet_author_is_none_if_user_not_authenticated(self):
        self.client.post(self.main_page, {"body": "not authenticated"})
        snippet = Snippet.objects.first()
        self.assertIsNone(snippet.author)

    def test_redirects_after_save(self):
        response = self.client.post(self.main_page, data={"body": "redirected"})
        snippet = Snippet.objects.first()
        redirect_url = snippet.get_absolute_url()
        self.assertRedirects(response, redirect_url)

    def test_for_invalid_input_doesnt_save(self):
        response = self.client.post(self.main_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Snippet.objects.count(), 0)


class SnippetDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snippet = Snippet.objects.create(body="1")

    def test_uses_template(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")

    def test_snippet_in_context(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertEqual(response.context["snippet"], self.snippet)


class SnippetDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snippet_author = User.objects.create(username="testuser")
        cls.snippet = Snippet.objects.create(
            author=cls.snippet_author, body="Some text."
        )
        cls.snippet_delete_url = reverse(
            "snippets:snippet_delete", kwargs={"url": cls.snippet.url}
        )

    def test_not_authenticated_user_cannot_delete_snippet(self):
        response = self.client.post(self.snippet_delete_url)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertEquals(Snippet.objects.count(), 1)

    def test_author_of_snippet_can_delete_it(self):
        self.client.force_login(self.snippet_author)
        response = self.client.post(self.snippet_delete_url)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertEquals(Snippet.objects.count(), 0)

    def test_only_author_can_delete_his_snippet(self):
        non_author_user = User.objects.create(username="python")
        self.assertNotEquals(self.snippet.author, non_author_user)
        self.client.force_login(non_author_user)

        response = self.client.post(self.snippet_delete_url)
        self.assertEquals(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_redirects_to_profile_after_delete(self):
        self.client.force_login(self.snippet_author)
        response = self.client.post(self.snippet_delete_url)
        self.assertRedirects(response, self.snippet_author.get_absolute_url())
