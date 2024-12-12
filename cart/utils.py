from django.db.models import Prefetch
from django.http import HttpRequest

from cart.models import CartDB, CartItemDB
from shop.models import ProductDB, ProductVariantDB, SizeDB, GalleryDB
from users.models import CustomerDB


class CartForAuthenticatedUser:
    """Логіка кошика"""

    def __init__(
        self,
        request: HttpRequest,
        size_id: int = None,
        product_id: int = None,
        action: str = None,
    ):
        self.user = request.user
        if product_id and action and size_id:
            self.add_to_delete(product_id, size_id, action)

    def get_cart_info(self):
        """Отримання інфо про кошик (кіл-ть та сума товарів) та замовника"""
        customer, created = CustomerDB.objects.get_or_create(user=self.user)
        cart, created = CartDB.objects.get_or_create(customer=customer)
        products_to_cart = (
            cart.cart_items.all()
            .prefetch_related(
                Prefetch("product__images", GalleryDB.objects.order_by("id"))
            )
            .prefetch_related(Prefetch("product", ProductDB.objects.order_by("id")))
            .select_related("product__category", "size")
        )
        cart_total_price = cart.get_price_total_cart
        cart_total_quantity = cart.get_cart_total_quantity

        context = {
            "cart": cart,
            "products_to_cart": products_to_cart,
            "cart_total_price": cart_total_price,
            "cart_total_quantity": cart_total_quantity,
        }
        return context

    def add_to_delete(self, product_id: int, size_id: int, action: str):
        """Додавання або видалення товару по натисканню < > для окремих розмірів"""
        cart = self.get_cart_info()["cart"]
        product_variant = ProductVariantDB.objects.get(
            product__id=product_id, size_id=size_id
        )

        cart_product, created = CartItemDB.objects.get_or_create(
            cart=cart, product=product_variant.product, size_id=size_id
        )

        if created:
            cart_product.quantity = 0

        if action == "add" and cart_product.quantity < product_variant.stock_quantity:
            cart_product.quantity += 1
            cart_product.save()
        elif action == "delete" and cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        elif action == "delete" and cart_product.quantity == 1:
            cart_product.delete()

        if action == "remove" or cart_product.quantity < 1:
            cart_product.delete()

    def clear_cart(self):
        """Видалення всіх товарів з кошика"""
        cart = self.get_cart_info()["cart"]
        cart_products = cart.cart_items.all()
        for product in cart_products:
            product.delete()
        cart.save()
