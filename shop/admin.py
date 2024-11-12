from django.contrib import admin
from .models import CategoryDB


@admin.register(CategoryDB)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "parent", "slug"]
    list_display_links = ["id", "title"]
    prepopulated_fields = {"slug": ("title",)}
