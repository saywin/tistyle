import pytest
from django.contrib.auth import get_user_model

from shop.models import (
    ProductDB,
    CategoryDB,
    SizeDB,
    ProductVariantDB,
    GalleryDB,
)


@pytest.fixture
def category():
    category = CategoryDB.objects.create(title="Test category")
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
def variants(product_1, product_2):
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
    return variants


@pytest.fixture
def images(product_1):
    image_1 = GalleryDB.objects.create(image="shop/tests/1.jpg", product=product_1)
    image_2 = GalleryDB.objects.create(image="shop/tests/2.jpg", product=product_1)
    return [image_1, image_2]
