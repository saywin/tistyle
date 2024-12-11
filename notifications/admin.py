from django.contrib import admin

from notifications.models import Subscriber, ContactMessage


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Поштові підписки"""

    list_display = (
        "pk",
        "email",
        "user",
    )
    readonly_fields = ("email", "user")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("name", "email", "message")
