from django.db import models

from cart.models import CartDB
from users.models import CustomerDB


class OrderAddressDB(models.Model):
    customer = models.ForeignKey(
        CustomerDB,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Покупець",
    )
    cart = models.ForeignKey(
        CartDB, on_delete=models.SET_NULL, null=True, verbose_name="Кошик"
    )
    index = models.PositiveIntegerField(verbose_name="Індекс")
    city = models.CharField(max_length=255, verbose_name="Місто")
    state = models.CharField(max_length=255, verbose_name="Район/Область")
    street = models.CharField(max_length=255, verbose_name="Вулиця")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")

    def __str__(self):
        return self.street

    class Meta:
        db_table = "order_address"
        verbose_name = "Адреса доставлення"
        verbose_name_plural = "Адреса доставлення"
