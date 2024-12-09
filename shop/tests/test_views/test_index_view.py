from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from shop.models import CategoryDB, ProductDB


@pytest.fixture
def category():
    category = CategoryDB.objects.create(
        title="Test parent category",
        slug="test-parent-category",
        parent=None,
        image="shop/tests/1.jpg",
    )
    return category


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        "Test User", "test@test.com", "testpassword"
    )
    return user


@pytest.fixture
def product_1(user, category):
    product_1 = ProductDB.objects.create(
        title="Test product",
        article="00000",
        description="Test description",
        info="Test info",
        price=1,
        material="skin",
        color="Black",
        category=category,
        user=user,
    )
    return product_1


@pytest.fixture
def product_2(user, category):
    product_2 = ProductDB.objects.create(
        title="Test product 2",
        article="00001",
        description="Test description",
        info="Test info",
        price=2,
        material="skin",
        color="White",
        category=category,
        user=user,
    )
    return product_2


@pytest.fixture
def response(client):
    response = client.get(reverse("shop:index"))
    return response


@pytest.mark.django_db
def test_index_extra_content(response):
    assert response.context["title"] == "Головна сторінка"


@pytest.mark.django_db
def test_get_queryset(client):
    parent_category = CategoryDB.objects.create(
        title="Test parent category",
        slug="test-parent-category",
        parent=None,
        image="shop/tests/1.jpg",
    )
    child_category = CategoryDB.objects.create(
        title="Test child category", slug="test-child-category", parent=parent_category
    )

    response = client.get(reverse("shop:index"))
    categories = response.context["categories"]
    assert parent_category in categories
    assert child_category not in categories


@pytest.mark.django_db
def test_product_context_top_product(product_1, product_2, response):
    product_1.watched = 10
    product_2.watched = 20

    assert list(response.context["top_products"]) == [product_2, product_1]


@pytest.mark.django_db
def test_product_context_new_arrival(product_1, product_2, response):
    product_1.created_at = datetime.now() - timedelta(days=2)
    product_2.created_at = datetime.now()

    assert list(response.context["new_arrival"]) == [product_2, product_1]


@pytest.mark.django_db
def test_empty_context(response):

    assert response.status_code == 200
    assert list(response.context["categories"]) == []
    assert list(response.context["top_products"]) == []
    assert list(response.context["new_arrival"]) == []
