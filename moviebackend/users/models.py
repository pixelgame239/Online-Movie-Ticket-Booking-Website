from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Nam'), ('F', 'Nữ')],
        null=True,
        blank=True
    )
    favorite_cinema = models.ForeignKey(
        'movies.Cinema',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_admin or super().has_module_perms(app_label)
