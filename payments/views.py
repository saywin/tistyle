import stripe
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.contrib import messages

from conf import settings
from cart.utils import CartForAuthenticatedUser
from order.forms import ShippingForm
from users.forms import CustomerForm
from users.models import CustomerDB


def create_checkout_session(request: HttpRequest):
    """Платіж на stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        customer = CustomerDB.objects.get(user=request.user)
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer.first_name = customer_form.cleaned_data["first_name"]
            customer.last_name = customer_form.cleaned_data["last_name"]
            customer.email = customer_form.cleaned_data["email"]
            customer.phone = customer_form.cleaned_data["phone"]
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = customer
            address.cart = cart_info["cart"]
            address.save()

        total_price = cart_info["cart_total_price"]

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "uah",
                        "product_data": {"name": "Товари з TiStore"},
                        "unit_amount": int(total_price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("payments:success")),
            cancel_url=request.build_absolute_uri(reverse("payments:success")),
        )
        return redirect(session.url, 303)


def success_payment(request: HttpRequest) -> HttpResponse:
    """Оплата виконана успішно"""
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear_cart()
    messages.success(request, "Оплата пройшла успішно")
    return render(request, "shop/success.html")
