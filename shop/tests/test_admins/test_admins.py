import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from shop.admin import CategoryAdmin, ProductAdmin
from shop.models import CategoryDB, ProductDB
from shop.tests.fixtures import (
    product_1,
    product_2,
    product_3,
    category,
    variants,
    images,
    user,
)


@pytest.fixture
def admin_user(client):
    user_admin = get_user_model().objects.create_superuser(
        username="Test Admin User",
        password="testpassword",
        email="admin@admin.com",
    )
    client.force_login(user_admin)
    return user_admin


@pytest.fixture
def admin_category(admin_user):
    return CategoryAdmin(CategoryDB, admin_user)


@pytest.fixture
def admin_product(admin_user):
    return ProductAdmin(ProductDB, admin_user)


@pytest.fixture
def url():
    return reverse("admin:shop_categorydb_changelist")


@pytest.mark.django_db
def test_admin_category_count(
    admin_category, category, product_1, product_2, product_3, user
):
    assert admin_category.get_product_count(category) == "3"


@pytest.mark.django_db
def test_admin_category_image(
    admin_category, category, product_1, product_2, product_3, user
):

    assert admin_category.get_image(category) == "---"

    category.image = "shop/tests/1.jpg"
    assert (
        admin_category.get_image(category)
        == "<img src='/media/shop/tests/1.jpg' width='75'>"
    )


@pytest.mark.django_db
def test_admin_product_get_quantity(admin_product, variants, product_1):
    assert admin_product.get_quantity(product_1) == 6


@pytest.mark.django_db
def test_admin_product_get_image(admin_product, product_1, images, product_2, user):
    assert (
        admin_product.get_image(product_1)
        == f"<img src='/media/{images[0].image}' width='75'>"
    )
    assert admin_product.get_image(product_2) == "---"
