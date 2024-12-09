from django.core.mail import send_mail

from .models import Subscriber
from conf import settings


def send(user_email: str):
    send_mail(
        subject="tistyle.ua",
        message="Ви підписались на TiStyle.ua, ми будемо відправляти вам кращі пропозиції",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def send_all_email():
    users = Subscriber.objects.all()
    for user in users:
        send_mail(
            subject="tistyle.ua",
            message="Привіт",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


def send_email_browser(title: str, text: str):
    users = Subscriber.objects.all()
    for user in users:
        send_mail(
            subject=title,
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
