from django.contrib.auth.models import AbstractUser


# Django highly recommended to set up a custom user model
class User(AbstractUser):
    pass
