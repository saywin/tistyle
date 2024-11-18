from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "category/<slug:slug>/",
        views.SubCategories.as_view(),
        name="category_detail",
    ),
    path("product/<slug:slug>", views.ProductPage.as_view(), name="product_page"),
]
