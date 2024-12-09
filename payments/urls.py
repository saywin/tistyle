from django.urls import path
from payments.views import create_checkout_session, success_payment

app_name = "payments"

urlpatterns = [
    path("", create_checkout_session, name="payment"),
    path("payment_success/", success_payment, name="success"),
]
