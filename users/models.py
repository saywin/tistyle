from django.contrib.auth.models import AbstractUser
from django.db import models

from conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class CustomerDB(models.Model):
    """Контактна інформація замовника"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="customers",
        null=True,
        blank=True,
        verbose_name="Користувач",
    )
    first_name = models.CharField(max_length=150, verbose_name="Ім'я")
    last_name = models.CharField(max_length=150, verbose_name="Прізвище")
    email = models.EmailField(blank=True, verbose_name="Електронна пошта")
    phone = models.CharField(max_length=20, verbose_name="Контактний номер")

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "customer"
        verbose_name = "Покупець"
        verbose_name_plural = "Покупці"
