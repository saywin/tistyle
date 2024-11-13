from django.contrib import admin
from .models import CategoryDB, ProductDB, SizeDB, GalleryDB, ProductVariantDB


class GalleryAdminInline(admin.TabularInline):
    extra = 3
    model = GalleryDB


class ProductVariantAdmin(admin.TabularInline):
    extra = 1
    model = ProductVariantDB


@admin.register(CategoryDB)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "parent", "slug"]
    list_display_links = ["id", "title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ProductDB)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "article",
        "price",
        "color",
        "description",
        "info",
        "slug",
        "category",
        "material",
    ]
    list_display = [
        "id",
        "title",
        "article",
        "price",
        "color",
        "get_products_count",
        "category",
        "slug",
        "created_at",
    ]
    inlines = (GalleryAdminInline, ProductVariantAdmin)
    list_display_links = ["id", "title"]
    search_fields = ["id", "title", "article", "category"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_editable = ["price", "color", "article"]

    def save_model(self, request, obj, form, change):
        print(request.user)
        if not obj.user:
            obj.user = request.user
        obj.save()

    def get_products_count(self, obj):
        count = 0
        if obj.variants:
            for variant in obj.variants.all():
                count += variant.stock_quantity
        return count

    get_products_count.short_description = "Кількість"


@admin.register(GalleryDB)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]


@admin.register(SizeDB)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
