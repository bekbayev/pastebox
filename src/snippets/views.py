from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView

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


class SnippetDetailView(DetailView):
    queryset = Snippet.active.all()
    slug_field = "url"
    slug_url_kwarg = "url"
    context_object_name = "snippet"
