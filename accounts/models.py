from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)

    name = models.CharField(max_length=150)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
