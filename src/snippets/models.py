from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Snippet(models.Model):
    """
    A model for storing any text or
    source code with syntax highlighting.
    """

    DEFAULT_TITLE = "Untitled"
    BODY_MAX_LENGTH = 65_536  # 256 KiB (utf-8) or less
    URL_LENGTH = 8

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="snippets"
    )
    title = models.CharField(max_length=100, blank=True, default=DEFAULT_TITLE)
    body = models.CharField(max_length=BODY_MAX_LENGTH)
    syntax = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=URL_LENGTH, unique=True, editable=False)

    def __str__(self):
        return self.title
