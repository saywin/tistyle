from django.shortcuts import render
from django.views import generic

from shop import models


class Index(generic.ListView):
    model = models.ProductDB
    template_name = "shop/index.html"
    extra_context = {"title": "Головна сторінка"}
