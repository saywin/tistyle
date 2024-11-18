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

    # def get_products_category(self, title: str):
    #     men_clothing_category = models.CategoryDB.objects.get(title=title)
    #     all_men_clothing_subclasses = men_clothing_category.subcategories.all()
    #     filter_to_category = models.ProductDB.objects.filter(
    #         category__in=all_men_clothing_subclasses
    #     )
    #     return filter_to_category

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вивід на сторінку допоміжні елементи"""
        context = super().get_context_data()
        context["top_products"] = models.ProductDB.objects.order_by("-watched")[:8]
        context["new_arrival"] = models.ProductDB.objects.order_by("-created_at")[:8]
        return context


class SubCategories(generic.ListView):
    """Вивід підкатегорій на окремій сторінці"""

    model = models.ProductDB
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        """Отримання всіх товарів категорії та її підкатегорій"""
        type_fields = self.request.GET.get("type")
        if type_fields:
            products = models.ProductDB.objects.filter(category__slug=type_fields)
            return products

        parent_category = models.CategoryDB.objects.get(slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()
        products = models.ProductDB.objects.filter(category__in=subcategories).order_by(
            "?"
        )

        sort_fields = self.request.GET.get("sort")
        if sort_fields:
            products = products.order_by(sort_fields)

        size_field = self.request.GET.get("size")
        if size_field:
            products = products.filter(variants__size__name=size_field)

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Додаткові елементи"""
        context = super().get_context_data()
        parent_category = models.CategoryDB.objects.get(slug=self.kwargs["slug"])
        context["category"] = parent_category
        context["title"] = parent_category.title
        print(parent_category)
        sizes = models.SizeDB.objects.filter(
            variants__product__category__in=parent_category.subcategories.all(),
            variants__stock_quantity__gt=0,
        ).distinct()
        context["sizes"] = sizes.order_by("name")
        return context


class ProductPage(generic.DetailView):
    """Вивід товару на окремій сторінці"""

    model = models.ProductDB
    context_object_name = "product"
    template_name = "shop/product_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sizes"] = self.object.variants.filter(stock_quantity__gt=0)
        similar_goods = models.ProductDB.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)
        context["similar_goods"] = similar_goods.order_by("?")[:4]
        context["images"] = models.GalleryDB.objects.filter(product_id=self.object.id)
        return context
