from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
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
    avatar = models.URLField(
        default='https://anxkatxbafgpahipxzsw.supabase.co/storage/v1/object/public/avatar/default.png',   # ảnh mặc định
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
