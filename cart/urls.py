from django.urls import path

from cart.views import cart, add_to_cart

app_name = "carts"

urlpatterns = [
    path("", cart, name="user_cart"),
    path(
        "add_to_cart/<int:product_id>/<int:size_id>/<str:action>/",
        add_to_cart,
        name="add_to_cart",
    ),
]
