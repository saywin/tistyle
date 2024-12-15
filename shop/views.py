from django.db.models import Avg, Prefetch, Q, F
from django.views import generic

from review.forms import ReviewForm
from review.models import ReviewDB
from shop import models
from shop.models import ProductDB
from shop.templatetags.shop_tags import get_favorite_products


class Index(generic.ListView):
    """Головна сторінка"""

    model = models.ProductDB
    context_object_name = "categories"
    template_name = "shop/index.html"
    extra_context = {"title": "Головна сторінка"}

    def get_queryset(self):
        """Вивід батьківських категорій"""
        categories = models.CategoryDB.objects.filter(parent=None)[:12]
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вивід на сторінку допоміжні елементи"""
        context = super().get_context_data()
        context["top_products"] = (
            models.ProductDB.objects.order_by("-watched")[:8]
            .select_related("category")
            .prefetch_related(
                Prefetch("images", models.GalleryDB.objects.order_by("id"))
            )
        )
        context["new_arrival"] = (
            models.ProductDB.objects.order_by("-created_at")[:8]
            .select_related("category")
            .prefetch_related(
                Prefetch("images", models.GalleryDB.objects.order_by("id"))
            )
        )
        return context


class SubCategories(generic.ListView):
    """Вивід підкатегорій на окремій сторінці"""

    model = models.ProductDB
    context_object_name = "products"
    template_name = "shop/category_page.html"
    paginate_by = 12

    def get_queryset(self):
        """Отримання всіх товарів категорії та її підкатегорій"""
        type_fields = self.request.GET.get("type")
        if type_fields:
            products = models.ProductDB.objects.filter(category__slug=type_fields)
            return products.prefetch_related(
                Prefetch("images", models.GalleryDB.objects.order_by("id"))
            ).select_related("category")

        parent_category = models.CategoryDB.objects.prefetch_related(
            "subcategories"
        ).get(slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()
        products = (
            models.ProductDB.objects.filter(category__in=subcategories).order_by("?")
        ).prefetch_related(Prefetch("images", models.GalleryDB.objects.order_by("id")))

        sort_fields = self.request.GET.get("sort")
        if sort_fields:
            products = products.order_by(sort_fields)

        size_field = self.request.GET.get("size")
        if size_field:
            products = products.filter(variants__size__name=size_field)

        return products.select_related("category")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Додаткові елементи"""
        context = super().get_context_data()
        parent_category = models.CategoryDB.objects.get(slug=self.kwargs["slug"])
        context["category"] = parent_category
        context["title"] = parent_category.title
        sizes = models.SizeDB.objects.filter(
            variants__product__category__in=parent_category.subcategories.all(),
            variants__stock_quantity__gt=0,
        ).distinct()
        context["sizes"] = sizes.order_by("name")
        if self.request.user.is_authenticated:
            context["fav_products"] = get_favorite_products(self.request.user)
        subcategories = models.CategoryDB.objects.filter(parent=parent_category)
        context["best_sellers"] = ProductDB.objects.filter(
            category__in=subcategories
        ).order_by("-watched")[:3]
        return context


class ProductPage(generic.DetailView):
    """Вивід товару на окремій сторінці"""

    model = models.ProductDB
    context_object_name = "product"
    template_name = "shop/product_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sizes"] = self.object.variants.filter(
            stock_quantity__gt=0
        ).select_related("size")
        similar_goods = (
            models.ProductDB.objects.filter(category=self.object.category)
            .exclude(id=self.object.id)
            .prefetch_related(
                Prefetch("images", models.GalleryDB.objects.order_by("id"))
            )
            .select_related("category")
        )
        context["similar_goods"] = similar_goods.order_by("?")[:4]
        context["images"] = models.GalleryDB.objects.filter(product_id=self.object.id)
        user = self.request.user
        context["user_data"] = user if user.is_authenticated else None
        if context["user_data"]:
            context["review_form"] = ReviewForm

        reviews = (
            ReviewDB.objects.filter(product_id=self.object.id)
            .select_related("author")
            .order_by("-created_at")
        )
        context["reviews"] = reviews
        context["count_reviews"] = reviews.count()
        avg_rate = reviews.aggregate(avg_rating=Avg("grade")).get("avg_rating")
        context["avg_rate"] = round(avg_rate, 1) if avg_rate else avg_rate
        ProductDB.objects.filter(slug=self.kwargs["slug"]).update(
            watched=F("watched") + 1
        )
        context["best_sellers"] = similar_goods.order_by("-watched")[:3]
        return context


class SearchResult(generic.ListView):
    """Пошук слова у заголовку та у змісті статей"""

    template_name = "shop/search_page.html"
    extra_context = {"title": "Пошук"}
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        word = self.request.GET.get("q")
        if word:
            products = ProductDB.objects.filter(
                Q(title__icontains=word)
                | Q(info__icontains=word)
                | Q(description__icontains=word)
            )
            return products
        return ProductDB.objects.none()
