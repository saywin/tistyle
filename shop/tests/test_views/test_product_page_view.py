from datetime import timedelta, datetime

import pytest
from django.urls import reverse

from review.forms import ReviewForm
from review.models import ReviewDB
from shop.tests.fixtures import (
    product_1,
    product_2,
    product_3,
    variants,
    category,
    images,
    user,
)


@pytest.fixture
def url(product_1):
    url = reverse("shop:product_page", kwargs={"slug": product_1.slug})
    return url


@pytest.fixture
def reviews(product_1, user):
    reviews = []
    for grade in range(5, 0, -1):
        review = ReviewDB.objects.create(product=product_1, author=user, grade=grade)
        review.created_at = datetime.now() - timedelta(days=grade)
        reviews.append(review)
    return reviews


@pytest.mark.django_db
def test_product_context_size(url, variants, client, category):

    response = client.get(url)

    assert response.status_code == 200
    assert response.context["sizes"].count() == 2
    assert variants[0] in response.context["sizes"]
    assert variants[2] in response.context["sizes"]
    assert variants[1] not in response.context["sizes"]
    assert variants[3] not in response.context["sizes"]


@pytest.mark.django_db
def test_product_context_similar_goods(client, url, product_1, product_2, product_3):
    response = client.get(url)

    assert response.context["similar_goods"].count() == 2
    assert product_1 not in response.context["similar_goods"]
    assert product_2 in response.context["similar_goods"]
    assert product_3 in response.context["similar_goods"]


@pytest.mark.django_db
def test_product_context_images(client, url, product_1, images):

    response = client.get(url)

    assert response.context["images"].count() == 2
    assert list(response.context["images"]) == [images[0], images[1]]


@pytest.mark.django_db
def test_product_context_user_data(url, client, user, product_1):

    response = client.get(url)
    assert response.context["user_data"] is None

    client.force_login(user)
    response = client.get(url)
    assert response.context["user_data"] == user


@pytest.mark.django_db
def test_product_context_review_form(
    url,
    client,
    user,
):
    response = client.get(url)
    assert "review_form" not in response.context

    client.force_login(user)
    response = client.get(url)
    assert "review_form" in response.context
    assert response.context["review_form"] == ReviewForm


@pytest.mark.django_db
def test_product_context_reviews_and_count_reviews(url, client, reviews):
    response = client.get(url)

    assert list(response.context["reviews"]) == reviews[::-1]
    assert response.context["reviews"].count() == 5
    assert response.context["count_reviews"] == 5


@pytest.mark.django_db
def test_product_context_avg_rate(url, client, reviews):
    avg_rate = sum(review.grade for review in reviews) / len(reviews)

    response = client.get(url)
    assert response.context["avg_rate"] == avg_rate


@pytest.mark.django_db
def test_product_context_best_seller(url, client, product_1, product_2, product_3):
    product_3.watched = 5
    product_3.save()

    response = client.get(url)

    assert list(response.context["best_sellers"]) == [
        product_3,
        product_2,
    ]
