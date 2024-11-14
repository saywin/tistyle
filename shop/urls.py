from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [path("", views.Index.as_view(), name="index")]
