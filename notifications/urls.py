from django.urls import path

from notifications.views import save_subscribers, send_email_to_subscribers, contact

urlpatterns = [
    path("save_email", save_subscribers, name="save_subscribers"),
    path("send_email", send_email_to_subscribers, name="send_email"),
    path("contact/", contact, name="contact"),
]

app_name = "notifications"
