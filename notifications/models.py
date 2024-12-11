from django.db import models

from conf import settings


class Subscriber(models.Model):
    """Поштова підписка"""

    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subscriber",
        verbose_name="Користувач",
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscriber"
        verbose_name = "Пошта"
        verbose_name_plural = "Пошти"

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Повідомлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Повідомлення від {self.name} ({self.email})"

    class Meta:
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"
        ordering = ["-created_at"]
