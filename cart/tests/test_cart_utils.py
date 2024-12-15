import pytest

from cart.models import CartItemDB
from shop.tests.fixtures import (
    user,
    product_1,
    product_2,
    product_3,
    cart,
    cart_items,
    category,
    customer,
    sizes,
    variants,
    user_request,
    cart_logic,
)


@pytest.mark.django_db
def test_cart_utils_get_cart_info(
    cart_logic, cart, cart_items, customer, product_1, product_2, product_3
):
    info = cart_logic.get_cart_info()
    assert info["cart_total_price"] == 19
    assert info["cart"] == cart
    assert info["products_to_cart"].count() == 4
    assert info["cart_total_quantity"] == 10


@pytest.mark.django_db
def test_cart_utils_add_to_cart(
    cart_logic,
    cart,
    product_1,
    sizes,
    variants,
):
    cart_logic.add_to_delete(product_id=product_1.id, size_id=sizes[0].id, action="add")
    cart_item = CartItemDB.objects.get(
        product_id=product_1.id, cart=cart, size=sizes[0]
    )
    assert cart_item.quantity == 1
    assert cart_item.product == product_1


@pytest.mark.django_db
def test_cart_utils_delete_to_cart(
    cart_logic, cart, product_1, category, sizes, variants, cart_items
):

    cart_logic.add_to_delete(
        product_id=product_1.id, size_id=sizes[0].id, action="delete"
    )

    cart_items[0].refresh_from_db()
    assert cart_items[0].quantity == 1

    cart_logic.add_to_delete(
        product_id=product_1.id, size_id=sizes[0].id, action="delete"
    )

    with pytest.raises(CartItemDB.DoesNotExist):
        CartItemDB.objects.get(product_id=product_1.id, cart=cart, size=sizes[0])


@pytest.mark.django_db
def test_cart_utils_remove_cart(
    cart_logic, product_1, sizes, cart_items, cart, variants
):
    assert cart_items[0].quantity == 2
    cart_logic.add_to_delete(
        product_id=product_1.id, size_id=sizes[0].id, action="remove"
    )

    with pytest.raises(CartItemDB.DoesNotExist):
        CartItemDB.objects.get(product_id=product_1.id, cart=cart, size=sizes[0])


@pytest.mark.django_db
def test_cart_utils_clear_cart(cart_logic, cart_items, cart):
    assert cart.cart_items.count() == 4
    cart_logic.clear_cart()
    assert cart.cart_items.count() == 0
