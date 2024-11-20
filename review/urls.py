from django.urls import path

from review.views import save_review

app_name = "review"


urlpatterns = [path("save-review/<int:product_pk>", save_review, name="save_review")]
