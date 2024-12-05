from django import template
from django.db.models import Avg

from review.models import ReviewDB
from shop.models import CategoryDB

from django.template.defaulttags import register as range_register

from wishlist.models import FavoriteDB

register = template.Library()


@range_register.filter
def get_positive_range(value):
    return range(int(value))


@range_register.filter
def get_negative_range(value):
    return range(5 - int(value))


@register.simple_tag()
def get_subcategories(category):
    return CategoryDB.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            "title": "Ціна",
            "sorters": [
                ("price", "За зростанням"),
                ("-price", "За спаданням"),
            ],
        },
        {
            "title": "Колір",
            "sorters": [
                ("color", "Від А до Я"),
                ("-color", "Від Я до А"),
            ],
        },
    ]
    return sorters


@register.simple_tag()
def get_favorite_products(user):
    """Вивід обраних товарів на сторінку"""
    fav = FavoriteDB.objects.filter(user=user).select_related(
        "product",
    )
    products = [i.product for i in fav]
    return products
