from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .forms import SnippetForm
from .models import Snippet


class SnippetCreateView(CreateView):
    model = Snippet
    form_class = SnippetForm
    template_name = "snippets/index.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        return super().form_valid(form)
