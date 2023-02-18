from django.contrib import admin

from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "created_at", "expiration", "syntax")
    list_display_links = ("title",)
