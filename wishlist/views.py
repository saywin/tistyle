from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView

from shop.models import ProductDB, GalleryDB
from wishlist.models import FavoriteDB


def save_favorite_product(request: HttpRequest, product_slug: str) -> HttpResponse:
    """Додавання або видалення товара з обраних"""
    if request.user.is_authenticated:
        user = request.user
        product = ProductDB.objects.get(slug=product_slug)
        favorite_products = FavoriteDB.objects.filter(user=user)
        if product in [i.product for i in favorite_products]:
            fav_product = FavoriteDB.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteDB.objects.create(user=user, product=product)

        next_page = request.META.get("HTTP_REFERER", "category_detail")
        return redirect(next_page)


class FavoriteProductView(LoginRequiredMixin, ListView):
    """Для відображення обраних товарів на сторінці"""

    model = FavoriteDB
    context_object_name = "products"
    template_name = "shop/favorite_products.html"
    login_url = "users:user_login"
    extra_context = {"title": "Обрані товари"}

    def get_queryset(self):
        """Отримуємо товари конкретного користувача"""
        favorites = (
            FavoriteDB.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch("product__images", GalleryDB.objects.order_by("id"))
            )
            .prefetch_related("product__category")
        )
        products = [i.product for i in favorites]
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        best_sellers = ProductDB.objects.order_by("-watched")[:3]
        context["best_sellers"] = best_sellers
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context["count_favorite"] = FavoriteDB.objects.filter(user=self.request.user)
    #     return context
