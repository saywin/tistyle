import pytest
from django.contrib.auth import get_user_model

from users.models import CustomerDB


@pytest.fixture
def user():
    user = get_user_model().objects.create_user("test", "test@test.com", "testpassword")
    return user


@pytest.fixture
def customer(user):
    customer = CustomerDB.objects.create(
        user=user,
        first_name="Test name",
        last_name="Test last name",
        phone="0990990999",
    )
    return customer


@pytest.mark.django_db
def test_create_user(user):
    assert get_user_model().objects.count() == 1


@pytest.mark.django_db
def test_customer_create(customer, user):
    assert customer.user == user
    assert customer.first_name == "Test name"
    assert customer.last_name == "Test last name"
    assert customer.phone == "0990990999"

    customer.email = "test@email.com"
    assert customer.email == "test@email.com"


@pytest.mark.django_db
def test_customer_str(customer):
    assert str(customer) == "Test name"
