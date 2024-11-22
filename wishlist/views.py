from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from shop.models import ProductDB
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
