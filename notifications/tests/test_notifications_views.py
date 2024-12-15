import pytest
from django.urls import reverse

from notifications.models import Subscriber
from shop.tests.fixtures import user


@pytest.fixture
def url_save_subscribers():
    return reverse("notifications:save_subscribers")


@pytest.fixture
def url_send_email():
    return reverse("notifications:send_email")


@pytest.mark.django_db
def test_notification_save_subscribe_authenticated(
    client, user, mocker, url_save_subscribers
):
    email = "test@email.com"

    client.force_login(user)
    mocked_task = mocker.patch("notifications.tasks.send_msg_to_email.delay")
    response = client.post(url_save_subscribers, {"email": email})

    assert response.status_code == 302
    assert response.url == reverse("shop:index")

    subscriber = Subscriber.objects.get(email=email)
    assert subscriber.user == user

    mocked_task.assert_called_once_with(email)


@pytest.mark.django_db
def test_notification_save_subscribe_unauthenticated(
    client, url_save_subscribers, mocker, user
):
    email = "test@email.com"
    mocked_task = mocker.patch("notifications.tasks.send_msg_to_email.delay")
    response = client.post(url_save_subscribers, {"email": email})

    assert response.status_code == 302
    assert response.url == reverse("shop:index")

    subscriber = Subscriber.objects.get(email=email)
    assert subscriber.user is None

    mocked_task.assert_called_once_with(email)


@pytest.mark.django_db
def test_save_subscribers_duplicate_email(client, user, mocker, url_save_subscribers):
    client.force_login(user)
    email = "duplicate@example.com"
    Subscriber.objects.create(email=email, user=user)
    mocked_task = mocker.patch("notifications.tasks.send_msg_to_email.delay")
    response = client.post(url_save_subscribers, {"email": email})

    assert response.status_code == 302
    assert response.url == reverse("shop:index")

    messages = list(response.wsgi_request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Такий email вже підписан"
    mocked_task.assert_not_called()


@pytest.mark.django_db
def test_notifications_send_email_to_subscribers(client, url_send_email, mocker):
    response = client.get(url_send_email)
    assert response.status_code == 200
    assert response.context["title"] == "Спамер"

    title_message = "Test title"
    text_message = "Test text"

    mocked_send = mocker.patch("notifications.tasks.send_msg_all_emails_browser.delay")
    response = client.post(
        url_send_email,
        {"title_send_email": title_message, "text_send_email": text_message},
    )

    assert response.status_code == 200
    mocked_send.assert_called_once_with(title=title_message, text=text_message)
