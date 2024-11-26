from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from cart.utils import CartForAuthenticatedUser


def cart(request: HttpRequest) -> HttpResponse:
    cart_info = CartForAuthenticatedUser(request).get_cart_info()
    context = {
        "title": "Кошик",
        "cart": cart_info["cart"],
        "products_to_cart": cart_info["products_to_cart"],
        "cart_total_price": cart_info["cart_total_price"],
        "cart_total_quantity": cart_info["cart_total_quantity"],
    }
    return render(request, "shop/cart.html", context)


def add_to_cart(
    request: HttpRequest, product_id: int, size_id: int, action: str
) -> HttpResponse:
    if request.user.is_authenticated:
        CartForAuthenticatedUser(
            request=request,
            size_id=size_id,
            product_id=product_id,
            action=action,
        )
        return redirect("cart:user_cart")
    else:
        messages.error(
            request, "Треба авторизуватись або зареєструватись, щоб завершити покупки"
        )
        return redirect("users:login")
