from datetime import timedelta, datetime

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from review.forms import ReviewForm
from review.models import ReviewDB
from shop.models import SizeDB, CategoryDB, ProductDB, ProductVariantDB, GalleryDB


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
def product_3(user, category):
    product_3 = ProductDB.objects.create(
        title="Test product 3",
        article="00002",
        description="Test description",
        info="Test info",
        price=3,
        material="skin",
        color="Green",
        category=category,
        user=user,
    )
    return product_3


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
def test_product_context_size(url, client, product_1, product_2):
    size = [SizeDB.objects.create(name=size) for size in ["36", "37", "38"]]
    variants = [
        ProductVariantDB.objects.create(
            size=size[0], product=product_1, stock_quantity=2
        ),
        ProductVariantDB.objects.create(
            size=size[1], product=product_1, stock_quantity=0
        ),
        ProductVariantDB.objects.create(
            size=size[2], product=product_1, stock_quantity=4
        ),
        ProductVariantDB.objects.create(
            size=size[2], product=product_2, stock_quantity=1
        ),
    ]

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
def test_product_context_images(client, url, product_1):
    image_1 = GalleryDB.objects.create(image="shop/tests/1.jpg", product=product_1)
    image_2 = GalleryDB.objects.create(image="shop/tests/2.jpg", product=product_1)

    response = client.get(url)

    assert response.context["images"].count() == 2
    assert list(response.context["images"]) == [image_1, image_2]


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
