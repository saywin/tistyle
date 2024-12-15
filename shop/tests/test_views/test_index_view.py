from datetime import datetime, timedelta

import pytest
from django.urls import reverse

from shop.models import CategoryDB
from shop.tests.fixtures import product_1, product_2, user


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
def response(client):
    return client.get(reverse("shop:index"))


@pytest.mark.django_db
def test_index_extra_content(response):
    assert response.context["title"] == "Головна сторінка"


@pytest.mark.django_db
def test_get_queryset(
    client,
    response,
):
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
