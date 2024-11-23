from django.contrib import admin

from notifications.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Поштові підписки"""

    list_display = (
        "pk",
        "email",
        "user",
    )
    readonly_fields = ("email", "user")
