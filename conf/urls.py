"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls", namespace="shop")),
    path("users/", include("users.urls", namespace="users")),
    path("review/", include("review.urls", namespace="review")),
    path("wishlist/", include("wishlist.urls", namespace="wishlist")),
    path(
        "notifications/",
        include("notifications.urls", namespace="notifications"),
    ),
    path("cart/", include("cart.urls", namespace="cart")),
    path("order/", include("order.urls", namespace="order")),
    path("payments/", include("payments.urls", namespace="payments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
