from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Django highly recommended to set up a custom user model
class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})
