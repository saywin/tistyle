from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cart.utils import CartForAuthenticatedUser
from order.forms import ShippingForm
from users.forms import CustomerForm


def checkout(request: HttpRequest) -> HttpResponse:
    """Сторінка оформлення замовлення"""
    cart_info = CartForAuthenticatedUser(request).get_cart_info()
    context = {
        "title": "Оформлення замовлення",
        "cart": cart_info["cart"],
        "products_to_cart": cart_info["products_to_cart"],
        "cart_total_price": cart_info["cart_total_price"],
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "customer_form": CustomerForm(),
        "shipping_form": ShippingForm(),
    }
    return render(request, "shop/checkout.html", context)
