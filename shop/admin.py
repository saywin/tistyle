from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CategoryDB, ProductDB, SizeDB, GalleryDB, ProductVariantDB


class GalleryAdminInline(admin.TabularInline):
    extra = 3
    model = GalleryDB


class ProductVariantAdmin(admin.TabularInline):
    extra = 1
    model = ProductVariantDB


@admin.register(CategoryDB)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "get_image",
        "id",
        "title",
        "parent",
        "slug",
        "get_product_count",
    ]
    list_display_links = ["id", "title"]
    prepopulated_fields = {"slug": ("title",)}

    def get_product_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))

    get_product_count.short_description = "Кількість товарів"

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='75'>")
        else:
            return "---"

    get_image.short_description = "Фото"


@admin.register(ProductDB)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "article",
        "price",
        "watched",
        "color",
        "description",
        "info",
        "slug",
        "category",
        "material",
    ]
    list_display = [
        "get_image",
        "id",
        "title",
        "article",
        "price",
        "color",
        "get_quantity",
        "category",
        "slug",
        "created_at",
    ]
    inlines = (GalleryAdminInline, ProductVariantAdmin)
    list_display_links = ["id", "title"]
    readonly_fields = ["watched"]
    search_fields = ["id", "title", "article", "category"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_editable = ["price", "color", "article"]

    def save_model(self, request, obj, form, change):
        print(request.user)
        if not obj.user:
            obj.user = request.user
        obj.save()

    def get_quantity(self, obj):
        count = 0
        if obj.variants:
            for variant in obj.variants.all():
                count += variant.stock_quantity
        return count

    get_quantity.short_description = "Кількість"

    def get_image(self, obj):
        if obj.images.first():
            image_url = obj.images.first().image.url
            return mark_safe(f"<img src='{image_url}' width='75'>")
        else:
            return "---"

    get_image.short_description = "Фото"


@admin.register(GalleryDB)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]


@admin.register(SizeDB)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
