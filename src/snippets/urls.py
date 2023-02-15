from django.urls import path

from .views import SnippetCreateView

app_name = "snippets"
urlpatterns = [
    path("", SnippetCreateView.as_view(), name="index"),
]
