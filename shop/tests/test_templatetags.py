import pytest

from shop.models import CategoryDB
from shop.templatetags import shop_tags
from shop.tests.fixtures import category, product_1, product_2, product_3, user


@pytest.fixture
def child_categories(category):
    child_1 = CategoryDB.objects.create(
        title="Test category child_1", slug="child-category-1", parent=category
    )
    child_2 = CategoryDB.objects.create(
        title="Test category child_2", slug="child-category-2", parent=category
    )
    return [child_1, child_2]


def test_positive_and_negative_range():
    assert shop_tags.get_negative_range(4) == range(1)
    assert shop_tags.get_positive_range(3) == range(3)


@pytest.mark.django_db
def test_get_subcategories(category, child_categories):
    assert list(shop_tags.get_subcategories(category)) == child_categories
