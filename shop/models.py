import pathlib
import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from pytils.translit import slugify as translit_slugify

from conf import settings
from users.models import User


class CategoryDB(models.Model):
    title = models.CharField(max_length=150, verbose_name="Назва категорії")
    image = models.ImageField(
        upload_to="categories/",
        null=True,
        blank=True,
        verbose_name="Зображення",
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
        related_name="subcategories",
    )
    slug = models.SlugField(blank=True, unique=True, verbose_name="URL")
    icon = models.ImageField(upload_to="categories/icon/", null=True, blank=True)

    class Meta:
        db_table = "category"
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        """Силка на сторінку категорії"""
        return reverse("shop:category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"title: {self.title}, slug: {self.slug}"


class ProductDB(models.Model):
    title = models.CharField(max_length=255, verbose_name="Товар")
    article = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    description = models.TextField(verbose_name="Опис")
    info = models.TextField(verbose_name="Додаткова інформація")
    price = models.PositiveIntegerField(verbose_name="Ціна")
    watched = models.PositiveIntegerField(default=0, verbose_name="Перегляди")
    category = models.ForeignKey(
        CategoryDB,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )
    slug = models.SlugField(blank=True, unique=True, verbose_name="URL")
    material = models.CharField(max_length=150, verbose_name="Матеріал")
    color = models.CharField(max_length=150, verbose_name="Колір")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="products",
        verbose_name="Користувач",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def save(self, *args, **kwargs):
        super(ProductDB, self).save()
        if not self.slug:
            self.slug = translit_slugify(self.title) + "-" + str(self.id)
            super(ProductDB, self).save()

    def get_first_photo(self):
        """Отримання першого фото"""
        if self.images.first():
            return self.images.first().image.url
        else:
            return "https://cdn.pixabay.com/photo/2017/07/28/23/18/coming-soon-2550190_1280.jpg"

    def get_absolute_url(self):
        return reverse("shop:product_page", kwargs={"slug": self.slug})

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.title


class SizeDB(models.Model):
    name = models.CharField(max_length=50, verbose_name="Розмір")

    class Meta:
        db_table = "size"
        verbose_name = "Розмір"
        verbose_name_plural = "Розміри"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.category.title})"


class ProductVariantDB(models.Model):
    product = models.ForeignKey(
        ProductDB,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Товар",
    )
    size = models.ForeignKey(
        SizeDB,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Розмір",
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")

    class Meta:
        db_table = "product_variants"
        verbose_name = "Розмірна сітка товару"
        verbose_name_plural = "Розмірні сітки товару"

    def __str__(self):
        return (
            f"{self.product.title} - {self.size.name} ({self.stock_quantity} in stock)"
        )


def product_image_path(instance: ProductDB, file_name: str) -> pathlib.Path:
    file_name = (
        f"{slugify(instance.product.title)}-{uuid.uuid4()}"
        + pathlib.Path(file_name).suffix
    )
    return pathlib.Path("product_image/") / pathlib.Path(file_name)


class GalleryDB(models.Model):
    image = models.ImageField(
        upload_to=product_image_path, null=True, blank=True, verbose_name="Зображення"
    )
    product = models.ForeignKey(
        ProductDB,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар",
    )

    class Meta:
        db_table = "gallery"
        verbose_name = "Зображення"
        verbose_name_plural = "Галерея товарів"
