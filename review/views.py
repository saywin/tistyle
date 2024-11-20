from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from review.forms import ReviewForm
from shop.models import ProductDB


def save_review(request: HttpRequest, product_pk: int) -> HttpResponse:
    """Збереження відгуку"""
    print(product_pk, "--------------------")
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        product = ProductDB.objects.get(pk=product_pk)
        review = form.save(commit=False)
        review.author = request.user
        review.product = product
        review.save()
        return redirect("shop:product_page", product.slug)
