import pytest

from cart.models import CartDB, CartItemDB
from shop.tests.fixtures import (
    customer,
    user,
    product_1,
    product_2,
    product_3,
    sizes,
    category,
)


@pytest.fixture
def cart(customer, user):
    return CartDB.objects.create(customer=customer)


@pytest.fixture
def cart_item(cart, product_1, sizes, category):
    cart_item = CartItemDB.objects.create(
        product=product_1, cart=cart, quantity=2, size=sizes[0]
    )
    return cart_item


@pytest.fixture
def cart_items(cart, sizes, product_1, product_3, product_2):
    cart_item_1 = CartItemDB.objects.create(
        product=product_1, cart=cart, quantity=2, size=sizes[0]
    )
    cart_item_2 = CartItemDB.objects.create(
        product=product_1, cart=cart, quantity=3, size=sizes[1]
    )
    cart_item_3 = CartItemDB.objects.create(
        product=product_3, cart=cart, quantity=4, size=sizes[2]
    )
    cart_item_4 = CartItemDB.objects.create(
        product=product_2, cart=cart, quantity=1, size=sizes[0]
    )
    return [cart_item_1, cart_item_2, cart_item_3, cart_item_4]


@pytest.mark.django_db
def test_cart_create(cart, customer):

    assert cart.customer == customer
    assert cart.is_completed is False
    assert cart.shipping is True


@pytest.mark.django_db
def test_cart_str(cart):
    assert str(cart) == f"{cart.pk}"


@pytest.mark.django_db
def test_cart_get_price_total_cart(cart_items, cart):
    res = 0
    for item in cart_items:
        res += item.product.price * item.quantity
    assert cart.get_price_total_cart == res


@pytest.mark.django_db
def test_cart_get_cart_total_quantity(cart_items, cart):
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
