from django.urls import path

from order.views import checkout

urlpatterns = [path("", checkout, name="checkout")]

app_name = "order"
