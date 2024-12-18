from django.db import models

from shop.models import ProductDB
from users.models import User

CHOICES = (
    (5, "Відмінно"),
    (4, "Добре"),
    (3, "Нормально"),
    (2, "Погано"),
    (1, "Жахливо"),
)


class ReviewDB(models.Model):
    """Модель для відгуків"""

    text = models.TextField(blank=True, verbose_name="Текст")
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    grade = models.IntegerField(
        choices=CHOICES,
        blank=True,
        null=True,
        verbose_name="Оцінка",
    )

    class Meta:
        db_table = "review"
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.author.username
