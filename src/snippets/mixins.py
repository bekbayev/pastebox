from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Snippet


class AuthorSnippetRequiredMixin(LoginRequiredMixin):
    """Return a snippet if the user is its author."""

    permission_denied_message = "Only the author has access"

    def get_object(self) -> Snippet:
        snippet = get_object_or_404(Snippet.active, url=self.kwargs["url"])
        if snippet.author != self.request.user:
            return self.handle_no_permission()
        return snippet
