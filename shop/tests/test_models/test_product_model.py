import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse

from shop.models import ProductDB, CategoryDB, GalleryDB, SizeDB, ProductVariantDB


@pytest.fixture
def category():
    return CategoryDB.objects.create(title="Test Category", slug="category")


@pytest.fixture
def subcategory(category):
    return CategoryDB.objects.create(
        title="Subcategory", slug="sub-category", parent=category
    )


@pytest.fixture
def product(category):
    """Фікстура для створення товара"""
    user = get_user_model().objects.create_user(username="test", password="test")
    return ProductDB.objects.create(
        title="Test Product",
        article="00000",
        description="Test Description",
        info="Test Info",
        price=100,
        category=category,
        color="Green",
        user=user,
    )


@pytest.fixture
def size():
    return SizeDB.objects.create(name="Test Size")


@pytest.fixture
def product_variant(size, product):
    return ProductVariantDB.objects.create(size=size, product=product, stock_quantity=2)


@pytest.mark.django_db
def test_product_create(product):
    assert product.title == "Test Product"
    assert product.article == "00000"
    assert product.description == "Test Description"
    assert product.info == "Test Info"
    assert product.price == 100
    assert product.category.title == "Test Category"
    assert product.color == "Green"
    assert product.user.username == "test"
    assert product.watched == 0


@pytest.mark.django_db
def test_product_autosave_slug(product):
    assert product.slug == f"test-product-{product.id}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field_name, field_value",
    [
        ("article", "00000"),
        ("slug", "test-product-1"),
    ],
)
def test_product_field_uniqueness(product, category, field_name, field_value):
    """Перевірка унікальності для полів"""
    with pytest.raises(IntegrityError):
        ProductDB.objects.create(
            title="Duplicate Product",
            article=product.article if field_name == "article" else "unique-article",
            slug=product.slug if field_name == "slug" else "unique-slug",
            description="Another Description",
            info="Another Info",
            price=200,
            category=category,
            color="Blue",
            user=product.user,
        )


@pytest.mark.django_db
def test_product_get_absolute_url(product, category):
    url = reverse("shop:product_page", kwargs={"slug": product.slug})
    assert product.get_absolute_url() == url
    assert category.products.count() == 1


@pytest.mark.django_db
def test_product_first_photo(product):
    assert (
        product.get_first_photo()
        == "https://cdn.pixabay.com/photo/2017/07/28/23/18/coming-soon-2550190_1280.jpg"
    )

    GalleryDB.objects.create(image="categories/1.jpg", product=product)
    assert product.get_first_photo() == "/media/categories/1.jpg"


@pytest.mark.django_db
def test_product_size_and_count(product, size, product_variant):
    assert product.variants.filter(size=size).first().size.name == "Test Size"
    assert product.variants.filter(size=size).first().stock_quantity == 2


@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == "Test Product"


@pytest.mark.django_db
def test_category_creation(category):
    """Перевірка створення категорії"""
    assert category.title == "Test Category"
    assert category.slug == "category"


@pytest.mark.django_db
def test_category_get_absolute_url(category):
    """Перевірка методу get_absolute_url"""
    url = reverse("shop:category_detail", kwargs={"slug": category.slug})
    assert category.get_absolute_url() == url


@pytest.mark.django_db
def test_subcategories(category, subcategory):
    """Перевірка зв'язків parent -> subcategories"""
    assert subcategory.parent == category
    assert category.subcategories.count() == 1
    assert category.subcategories.first().title == "Subcategory"


@pytest.mark.django_db
def test_category_slug_uniqueness(db, category):
    """Перевірка унікальності slug"""
    with pytest.raises(IntegrityError):
        CategoryDB.objects.create(title="Test Category 2", slug="category")


@pytest.mark.django_db
def test_category_str_repr(category):
    assert str(category) == "Test Category"
    assert repr(category) == "title: Test Category, slug: category"


@pytest.mark.django_db
def test_category_cascade_delete(category, subcategory):
    """Перевірка каскадного видалення"""
    category.delete()
    assert CategoryDB.objects.filter(slug="sub-category").count() == 0


@pytest.mark.django_db
def test_size_name_str(size):
    assert size.name == "Test Size"
    assert str(size) == "Test Size"


@pytest.mark.django_db
def test_variants_str(product_variant):
    assert str(product_variant) == "Test Product - Test Size (2 in stock)"
