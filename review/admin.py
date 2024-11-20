from django.contrib import admin

from .models import ReviewDB


@admin.register(ReviewDB)
class ReviewAdmin(admin.ModelAdmin):
    """Відображення відгуків в адмін панелі"""

    list_display = ["pk", "author", "product", "created_at"]
    readonly_fields = ["author", "text", "created_at", "product"]
