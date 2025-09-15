from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username
