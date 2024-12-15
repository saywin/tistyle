import pytest
from django.urls import reverse

from shop.models import ProductDB, CategoryDB, SizeDB, ProductVariantDB
from shop.tests.fixtures import user


@pytest.fixture
def category_parent():
    category = CategoryDB.objects.create(
        title="Test parent category",
        slug="test-parent-category",
        parent=None,
        image="shop/tests/1.jpg",
    )
    return category


@pytest.fixture
def category_child(category_parent):
    category = CategoryDB.objects.create(
        title="Test parent category",
        slug="test-child-category",
        parent=category_parent,
        image="shop/tests/1.jpg",
    )
    return category


@pytest.fixture
def product_1(user, category_child):
    product_1 = ProductDB.objects.create(
        title="Test product",
        article="00000",
        description="Test description",
        info="Test info",
        price=1,
        material="skin",
        color="Black",
        category=category_child,
        user=user,
    )
    return product_1


@pytest.fixture
def product_2(user, category_child):
    product_2 = ProductDB.objects.create(
        title="Test product 2",
        article="00001",
        description="Test description",
        info="Test info",
        price=2,
        material="skin",
        color="White",
        category=category_child,
        user=user,
    )
    return product_2


@pytest.fixture
def product_3(user, category_child):
    product_3 = ProductDB.objects.create(
        title="Test product 3",
        article="00002",
        description="Test description",
        info="Test info",
        price=3,
        material="skin",
        color="Green",
        category=category_child,
        user=user,
    )
    return product_3


@pytest.fixture
def url(category_parent):
    return reverse("shop:category_detail", kwargs={"slug": category_parent.slug})


@pytest.mark.django_db
def test_category_show_products(
    client,
    product_1,
    product_2,
    product_3,
    category_parent,
    url,
):
    response = client.get(url)

    assert response.status_code == 200
    for product in [product_1, product_2, product_3]:
        assert product in response.context["products"]


@pytest.mark.django_db
def test_product_filter_by_type(
    client, product_1, product_2, product_3, category_parent, url
):
    product_1.category = category_parent
    product_3.category = category_parent
    product_1.save()
    product_3.save()
    response = client.get(url, {"type": category_parent.slug})

    assert response.status_code == 200

    assert product_1 in response.context["products"]
    assert product_3 in response.context["products"]
    assert product_2 not in response.context["products"]


@pytest.mark.django_db
def test_product_filter_by_sort_by_color(
    product_1,
    product_2,
    product_3,
    client,
    category_child,
    url,
):
    response = client.get(url, {"sort": "color"})
    assert list(response.context["products"]) == [
        product_1,
        product_3,
        product_2,
    ]

    response = client.get(url, {"sort": "-color"})
    assert list(response.context["products"]) == [
        product_2,
        product_3,
        product_1,
    ]


@pytest.mark.django_db
def test_product_filter_by_sort_by_price(
    product_1,
    product_2,
    product_3,
    client,
    category_child,
    url,
):
    response = client.get(url, {"sort": "price"})
    assert list(response.context["products"]) == [
        product_1,
        product_2,
        product_3,
    ]
    response = client.get(url, {"sort": "-price"})
    assert list(response.context["products"]) == [
        product_3,
        product_2,
        product_1,
    ]


@pytest.mark.django_db
def test_product_filter_size(
    product_1, product_2, product_3, url, client, category_child
):
    size_36 = SizeDB.objects.create(name=36)
    size_41 = SizeDB.objects.create(name=41)
    ProductVariantDB.objects.create(product=product_1, size=size_41, stock_quantity=1)
    ProductVariantDB.objects.create(product=product_2, size=size_36, stock_quantity=1)
    ProductVariantDB.objects.create(product=product_3, size=size_36, stock_quantity=1)

    response = client.get(url, {"size": size_36.name})
    assert response.context["products"].count() == 2
    assert product_2 in response.context["products"]
    assert product_3 in response.context["products"]

    response = client.get(url, {"size": size_41.name})
    assert list(response.context["products"]) == [product_1]


@pytest.mark.django_db
def test_subcategory_get_context_data_unauthenticated(
    url,
    client,
    category_parent,
    product_1,
    product_2,
    product_3,
    category_child,
    user,
):
    size_36 = SizeDB.objects.create(name=36)
    size_37 = SizeDB.objects.create(name=37)
    size_41 = SizeDB.objects.create(name=41)
    ProductVariantDB.objects.create(product=product_1, size=size_41, stock_quantity=1)
    ProductVariantDB.objects.create(product=product_2, size=size_36, stock_quantity=1)
    ProductVariantDB.objects.create(product=product_3, size=size_37)
    response = client.get(url)

    assert response.context["category"] == category_parent
    assert response.context["title"] == category_parent.title
    assert list(response.context["sizes"]) == [size_36, size_41]
    assert "fav_products" not in response.context


@pytest.mark.django_db
def test_subcategory_get_context_data_authenticated(
    client,
    url,
    user,
):
    client.force_login(user=user)
    response = client.get(url)

    assert "fav_products" in response.context


@pytest.mark.django_db
def test_subcategory_get_context_data_best_seller(
    product_1, product_2, product_3, client, url
):
    product_2.watched = 6
    product_3.watched = 4
    product_2.save()
    product_3.save()

    response = client.get(url)

    assert list(response.context["best_sellers"]) == [
        product_2,
        product_3,
        product_1,
    ]
