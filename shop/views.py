from django.shortcuts import render
from django.views import generic

from shop import models


class Index(generic.ListView):
    model = models.ProductDB
    context_object_name = "categories"
    template_name = "shop/index.html"
    extra_context = {"title": "Головна сторінка"}

    def get_queryset(self):
        """Вивід батьківських категорій"""
        categories = models.CategoryDB.objects.filter(parent=None)[:12]
        return categories


class SubCategories(generic.ListView):
    """Вивід підкатегорій на окремій сторінці"""

    model = models.ProductDB
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        """Отримання всіх товарів категорії та її підкатегорій"""
        parent_category = models.CategoryDB.objects.get(slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()
        products = models.ProductDB.objects.filter(category__in=subcategories).order_by(
            "?"
        )
        return products
