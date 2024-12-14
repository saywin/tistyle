import pytest

from notifications.models import Subscriber, ContactMessage
from shop.tests.fixtures import user


@pytest.fixture
def subscriber(user):
    subscriber = Subscriber.objects.create(
        user=user,
        email="test@test.com",
    )
    return subscriber


@pytest.fixture
def contact_message():
    contact_message = ContactMessage.objects.create(
        name="Test name",
        email="test@test.com",
        message="Test message",
    )
    return contact_message


@pytest.mark.django_db
def test_notifications_subscriber_create(subscriber, user):
    assert Subscriber.objects.count() == 1
    assert subscriber.user == user
    assert subscriber.email == "test@test.com"


@pytest.mark.django_db
def test_notifications_subscriber_str(subscriber):
    assert str(subscriber) == "test@test.com"


@pytest.mark.django_db
def test_notifications_contact_message_create(contact_message):
    assert contact_message.name == "Test name"
    assert contact_message.email == "test@test.com"
    assert contact_message.message == "Test message"


@pytest.mark.django_db
def test_notifications_contact_message_create(contact_message):
    assert (
        str(contact_message)
        == f"Повідомлення від {contact_message.name} ({contact_message.email})"
    )
