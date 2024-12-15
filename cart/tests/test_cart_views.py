import pytest
from django.urls import reverse

from shop.tests.fixtures import (
    product_1,
    product_2,
    product_3,
    sizes,
    customer,
    cart,
    cart_items,
    user,
    category,
    variants,
)


@pytest.mark.django_db
def test_cart_view(
    client,
    user,
    cart,
    cart_items,
    customer,
    product_1,
    product_2,
    product_3,
):
    url = reverse("cart:user_cart")
    client.force_login(user)
    response = client.get(url)

    assert response.context["title"] == "Кошик"
    assert response.context["cart"] == cart
    assert response.context["products_to_cart"].count() == 4
    assert response.context["cart_total_price"] == 19
    assert response.context["cart_total_quantity"] == 10


@pytest.mark.django_db
def test_cart_add_to_cart(client, product_1, user, sizes, category, variants):
    url = reverse("cart:add_to_cart", args=(product_1.id, sizes[0].id, "add"))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("users:login")

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("cart:user_cart")
