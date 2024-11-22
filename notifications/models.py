from django.db import models

from conf import settings


class Subscriber(models.Model):
    """Поштова розсилка"""

    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subscriber",
        verbose_name="Користувач",
    )

    class Meta:
        db_table = "subscriber"
        verbose_name = "Пошта"
        verbose_name_plural = "Пошти"

    def __str__(self):
        return self.email
