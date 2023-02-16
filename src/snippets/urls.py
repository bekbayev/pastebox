from django.urls import path

from .views import (
    SnippetCreateView,
    SnippetDeleteView,
    SnippetDetailView,
    SnippetUpdateView,
)

app_name = "snippets"
urlpatterns = [
    path("", SnippetCreateView.as_view(), name="index"),
    path("<str:url>/", SnippetDetailView.as_view(), name="snippet_detail"),
    path("<str:url>/edit/", SnippetUpdateView.as_view(), name="snippet_edit"),
    path("<str:url>/delete/", SnippetDeleteView.as_view(), name="snippet_delete"),
]
