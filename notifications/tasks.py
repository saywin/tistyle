from conf import settings
from conf.celery import app as background_task

from notifications.service import send, send_all_email, send_email_browser


@background_task.task
def send_msg_to_email(user_email: str):
    send(user_email)


@background_task.task
def send_sale_email():
    send_all_email()


@background_task.task
def send_msg_all_emails_browser(title: str, text: str):
    send_email_browser(title, text)
