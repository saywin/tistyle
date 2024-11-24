from django.contrib import admin

from cart.models import CartDB, CartItemDB


@admin.register(CartDB)
class CartDBAdmin(admin.ModelAdmin):
    """Кошик"""

    list_display = (
        "id",
        "customer",
        "created_at",
        "is_completed",
        "shipping",
        "get_price_total_cart",
        "get_cart_total_quantity",
    )
    readonly_fields = ("customer", "is_completed", "shipping")
    list_filter = ("customer", "created_at", "is_completed")


@admin.register(CartItemDB)
class CartItemDBAdmin(admin.ModelAdmin):
    """Товари в кошику"""

    list_display = ("id", "product", "quantity", "added_at", "get_total_price")
    readonly_fields = ("product", "quantity", "added_at", "get_total_price")
    list_filter = ("product",)
