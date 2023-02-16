from crispy_forms.layout import Submit

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import DeletionMixin

from .forms import SnippetForm
from .mixins import AuthorSnippetRequiredMixin
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


class SnippetUpdateView(AuthorSnippetRequiredMixin, UpdateView):
    form_class = SnippetForm
    template_name = "snippets/snippet_edit.html"

    def get_form(self, form_class=None) -> SnippetForm:
        form = super().get_form(form_class)
        form.helper.form_action = reverse(
            "snippets:snippet_edit", kwargs={"url": self.object.url}
        )
        # change submit button
        form.helper.layout[1][2] = Submit("edit", "Edit", css_class="btn btn-warning")
        return form


class SnippetDeleteView(AuthorSnippetRequiredMixin, DeletionMixin, View):
    def get_success_url(self):
        return self.request.user.get_absolute_url()
