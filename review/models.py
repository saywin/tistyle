from django.db import models

from shop.models import ProductDB
from users.models import User


class ReviewDB(models.Model):
    """Модель для відгуків"""

    text = models.TextField(verbose_name="Текст")
    product = models.ForeignKey(
        ProductDB,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Товар",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )

    class Meta:
        db_table = "review"
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.author.username
