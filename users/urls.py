from django.urls import path

from users.views import registration, login, user_login, user_registration, user_logout

urlpatterns = [
    path("login/", login, name="login"),
    path("registration/", registration, name="registration"),
    path("user-login/", user_login, name="user_login"),
    path("user-registration/", user_registration, name="user_registration"),
    path("user-logout/", user_logout, name="user_logout"),
]

app_name = "users"
