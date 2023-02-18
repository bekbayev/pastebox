from celery import shared_task

from .models import Snippet


@shared_task
def delete_expired_snippets():
    result = Snippet.inactive.all().delete()
    snippet_deleted_count = result[0]
    return f"Snippets deleted: {snippet_deleted_count}"
