from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
