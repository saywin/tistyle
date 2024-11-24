from django.urls import path

from wishlist.views import save_favorite_product, FavoriteProductView

app_name = "wishlist"

urlpatterns = [
    path(
        "add_favorite/<slug:product_slug>/",
        save_favorite_product,
        name="add_favorite",
    ),
    path("favorites/", FavoriteProductView.as_view(), name="favorites"),
]
