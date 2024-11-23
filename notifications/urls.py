from django.urls import path

from notifications.views import save_subscribers

urlpatterns = [path("save_email", save_subscribers, name="save_subscribers")]

app_name = "notifications"
