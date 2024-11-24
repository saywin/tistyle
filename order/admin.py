from django.contrib import admin

from order.models import OrderAddressDB


@admin.register(OrderAddressDB)
class OrderAddressAdmin(admin.ModelAdmin):
    """Адреса доставки"""

    list_display = (
        "id",
        "customer",
        "index",
        "city",
        "state",
        "created_at",
    )
    readonly_fields = ("customer", "cart", "city", "state", "street")
    list_filter = ("customer",)
