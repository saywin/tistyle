from django.db import models
from django.db.models import UniqueConstraint

from shop.models import ProductDB, SizeDB
from users.models import CustomerDB


class CartDB(models.Model):
    """Кошик"""

    customer = models.ForeignKey(
        CustomerDB,
        on_delete=models.SET_NULL,
        null=True,
        related_name="Покупець",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    is_completed = models.BooleanField(default=False, verbose_name="Завершено")
    shipping = models.BooleanField(default=True, verbose_name="Доставка")

    def __str__(self):
        return self.pk

    class Meta:
        db_table = "cart"
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ("-created_at",)

    @property
    def get_price_total_cart(self):
        """Розрахунок вартості всього кошику"""
        price = 0
        for product in self.cart_items.all():
            price += product.get_total_price
        return price

    @property
    def get_cart_total_quantity(self):
        """Розрахунок кількості товарів"""
        count = sum(product.quantity for product in self.cart_items.all())
        return count if count else 0


class CartItemDB(models.Model):
    """Прив'язка товару до кошика, рядки товарів"""

    product = models.ForeignKey(
        ProductDB, on_delete=models.SET_NULL, null=True, verbose_name="Товар"
    )
    cart = models.ForeignKey(
        CartDB, on_delete=models.SET_NULL, null=True, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(
        default=0, null=True, blank=True, verbose_name="Кількість"
    )
    size = models.ForeignKey(
        SizeDB,
        on_delete=models.SET_NULL,
        null=True,
        related_name="cart_items",
        verbose_name="Розмір",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Час додавання")

    def __str__(self):
        return f"{self.product}"

    class Meta:
        db_table = "cart_item"
        verbose_name = "Товар в кошику"
        verbose_name_plural = "Товари в кошику"
        ordering = ["-added_at"]

    @property
    def get_total_price(self):
        """Розрахунок загальної вартості однієї позиції в кошику"""
        return self.product.price * self.quantity
