from django import template
from shop.models import CategoryDB

register = template.Library()


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
