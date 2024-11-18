from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages

from users.forms import LoginForm, RegistrationForm


def login(request: HttpRequest) -> HttpResponse:
    context = {"title": "Увійти в акаунт", "login_form": LoginForm}
    return render(request, "users/login.html", context)


def registration(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Реєстрація акаунта",
        "registration_form": RegistrationForm,
    }
    return render(request, "users/registration.html", context)


def user_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm(data=request.POST)

    if form.is_valid():
        user = form.get_user()
        auth.login(request, user)
        return redirect("shop:index")
    else:
        messages.error(request, "Невірне ім'я користувача або пароль")
        return redirect("users:login")


def user_registration(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm(data=request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Акаунт користувача успішно створено")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())

        # messages.error(request, "Щось пішло не так")
    return redirect("users:registration")


def user_logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect("shop:index")
