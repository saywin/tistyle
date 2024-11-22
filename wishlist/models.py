from django.db import models

from shop.models import ProductDB
from users.models import User


class FavoriteDB(models.Model):
    """Обрані товари"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Користувач",
    )
    product = models.ForeignKey(
        ProductDB,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Товар",
    )

    class Meta:
        db_table = "favorites"
        verbose_name = "Обраний товар"
        verbose_name_plural = "Обрані товари"

    def __str__(self):
        return self.product.title
