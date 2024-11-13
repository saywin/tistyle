from django.contrib import admin
from .models import CategoryDB, ProductDB, SizeDB, GalleryDB, ProductVariantDB


class GalleryAdminInline(admin.TabularInline):
    extra = 3
    model = GalleryDB


class ProductVariantAdmin(admin.TabularInline):
    extra = 1
    model = ProductVariantDB

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Перевіряємо, чи це поле 'size'
        if db_field.name == "size":
            product = request.resolver_match.kwargs.get(
                "object_id"
            )  # Отримуємо ID продукту
            if product:
                # Отримуємо категорію цього продукту
                product_instance = ProductDB.objects.get(id=product)
                # Фільтруємо розміри по категорії продукту
                kwargs["queryset"] = SizeDB.objects.filter(
                    category=product_instance.category
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        "category",
        "slug",
        "created_at",
    ]
    inlines = (GalleryAdminInline, ProductVariantAdmin)
    list_display_links = ["id", "title"]
    search_fields = ["id", "title", "article", "category"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        print(request.user)
        if not obj.user:
            obj.user = request.user
        obj.save()


@admin.register(GalleryDB)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]


@admin.register(SizeDB)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
