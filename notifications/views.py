from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from notifications.forms import ContactMessageForm
from notifications.models import Subscriber
from notifications.tasks import send_msg_to_email, send_msg_all_emails_browser


def save_subscribers(request: HttpRequest) -> HttpResponse:
    """Зберігаємо email"""
    email = request.POST.get("email")
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Subscriber.objects.create(email=email, user=user)
            send_msg_to_email.delay(email)
        except IntegrityError:
            messages.error(request, "Такий email вже підписан")
    return redirect("shop:index")


def send_email_to_subscribers(request: HttpRequest) -> HttpResponse:
    """Відправка розсилки всім"""
    from django.core.mail import send_mail

    if request.method == "POST":
        title = request.POST.get("title_send_email")
        text = request.POST.get("text_send_email")
        send_msg_all_emails_browser.delay(title=title, text=text)
        print(f"Відправлено все --- {bool(send_mail)}")

    context = {"title": "Спамер"}

    return render(request, "shop/send_email.html", context)


def contact(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Повідомлення відправлено")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error].as_text())
    else:
        form = ContactMessageForm()
    context = {"title": "Контакти", "form": form}
    return render(request, "shop/contact.html", context)
