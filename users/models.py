from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None   # ❌ remove username
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email