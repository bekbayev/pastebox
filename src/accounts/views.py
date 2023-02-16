from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

User = get_user_model()


class ProfileDetailView(SingleObjectMixin, ListView):
    slug_field = "username"
    slug_url_kwarg = "username"
    paginate_by = 10
    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object
        return context

    def get_queryset(self):
        return self.object.snippets(manager="active").all()
