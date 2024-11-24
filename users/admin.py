from django.contrib import admin

from users.models import CustomerDB


@admin.register(CustomerDB)
class CustomerDBAdmin(admin.ModelAdmin):
    """Замовники"""

    list_display = ("id", "user", "first_name", "last_name", "email", "phone")
    readonly_fields = ("user", "first_name", "last_name", "email", "phone")
    list_filter = ("user",)
