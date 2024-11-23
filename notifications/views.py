from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

from notifications.models import Subscriber


def save_subscribers(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("email")
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Subscriber.objects.create(email=email, user=user)
        except IntegrityError:
            messages.error(request, "Такий email вже підписан")
    return redirect("shop:index")
