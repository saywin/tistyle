from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    """Аутентифікація користувача"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введіть ім'я користувача"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введіть пароль"}
        )
    )


class RegistrationForm(UserCreationForm):
    """Реєстрація користувача"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Придумайте логін"}
        ),
        label="",
        help_text="",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Придумайте Пароль"}
        ),
        label="",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Підтвердження Пароля"}
        ),
        label="",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введіть ваше ім'я",
                }
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введіть ваше прізвище"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введіть електронну пошту",
                }
            ),
        }
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
        }
