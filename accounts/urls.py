from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="account/logout.html"),
        name="account_logout",
    ),
    path("profile/", views.profile, name="profile"),
    path("login/", views.custom_login, name="account_login"),
]
