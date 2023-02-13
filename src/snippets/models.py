from django.contrib.auth import get_user_model
from django.db import models

from .utils import make_random_string

User = get_user_model()


class Snippet(models.Model):
    """
    A model for storing any text or
    source code with syntax highlighting.
    """

    DEFAULT_TITLE = "Untitled"
    BODY_MAX_LENGTH = 65_536  # limited to 256 KiB (utf-8)
    URL_LENGTH = 8
    LANGUAGES = [
        ("", "None"),
        ("bash", "Bash"),
        ("c", "C"),
        ("cpp", "C++"),
        ("csharp", "C#"),
        ("css", "CSS"),
        ("go", "Go"),
        ("haskell", "Haskell"),
        ("html", "HTML"),
        ("java", "Java"),
        ("js", "JavaScript"),
        ("json", "JSON"),
        ("lua", "Lua"),
        ("md", "Markdown"),
        ("mysql", "MySQL"),
        ("objc", "Objective-C"),
        ("perl", "Perl"),
        ("php", "PHP"),
        ("postgres", "PostgreSQL"),
        ("python", "Python"),
        ("ruby", "Ruby"),
        ("rust", "Rust"),
        ("smalltalk", "Smalltalk"),
        ("sql", "SQL"),
        ("swift", "Swift"),
        ("toml", "TOML"),
        ("ts", "TypeScript"),
        ("yaml", "YAML"),
    ]

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="snippets"
    )
    title = models.CharField(max_length=100, blank=True, default=DEFAULT_TITLE)
    body = models.CharField(max_length=BODY_MAX_LENGTH)
    syntax = models.CharField(max_length=15, blank=True, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=URL_LENGTH, unique=True, editable=False)

    def __str__(self) -> str:
        """Return the snippet title shortened to 30 characters."""
        shorten_to = 30
        title = self.title
        if len(title) > shorten_to:
            title = title[:shorten_to]
            title = f"{title}..."
        return title

    def _generate_unique_url(self) -> str:
        """Return a random URL string, which isn't in the database.

        Called recursively if the URL exists in the database.
        """
        url = make_random_string(self.URL_LENGTH)
        if self.objects.filter(url=url).exists():
            return self._generate_unique_url()
        return url
