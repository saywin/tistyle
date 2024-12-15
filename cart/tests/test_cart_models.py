import pytest

from cart.models import CartItemDB
from shop.tests.fixtures import (
    customer,
    user,
    product_1,
    product_2,
    product_3,
    cart,
    cart_items,
    sizes,
    category,
)


@pytest.fixture
def cart_item(cart, product_1, sizes, category):
    cart_item = CartItemDB.objects.create(
        product=product_1, cart=cart, quantity=2, size=sizes[0]
    )
    return cart_item


@pytest.mark.django_db
def test_cart_create(cart, customer, user):

    assert cart.customer == customer
    assert cart.is_completed is False
    assert cart.shipping is True


@pytest.mark.django_db
def test_cart_str(cart):
    assert str(cart) == f"{cart.pk}"


@pytest.mark.django_db
def test_cart_get_price_total_cart(cart_items, cart, product_1, product_2, product_3):
    res = 0
    for item in cart_items:
        res += item.product.price * item.quantity
    assert cart.get_price_total_cart == res


@pytest.mark.django_db
def test_cart_get_cart_total_quantity(
    cart_items, cart, product_1, product_2, product_3
):
    assert cart.get_cart_total_quantity == 10


@pytest.mark.django_db
def test_cart_items_create(cart_item, product_1, cart, sizes):
    assert cart_item.product == product_1
    assert cart_item.quantity == 2
    assert cart_item.cart == cart
    assert cart_item.size == sizes[0]


@pytest.mark.django_db
def test_cart_items_str(cart_item, product_1):
    assert str(cart_item) == str(product_1)


@pytest.mark.django_db
def test_cart_items_get_total_price(cart_item, product_1):
    assert cart_item.get_total_price == 2
