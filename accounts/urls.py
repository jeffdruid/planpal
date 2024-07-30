from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

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
    path("signup/", views.signup, name="account_signup"),
    path("friends/", views.friends_page, name="friends_page"),
    path(
        "send_friend_request/<int:user_id>/",
        views.send_friend_request,
        name="send_friend_request",
    ),
    path(
        "respond_friend_request/<int:request_id>/<str:response>/",
        views.respond_friend_request,
        name="respond_friend_request",
    ),
    path(
        "delete_friend/<int:user_id>/",
        views.delete_friend,
        name="delete_friend",
    ),
    path(
        "view_profile/<int:user_id>/", views.view_profile, name="view_profile"
    ),
    path(
        "password/reset/", views.custom_password_reset, name="password_reset"
    ),
    path(
        "password_reset/done/",
        views.password_reset_done,
        name="password_reset_done",
    ),
    path("delete_account/", views.delete_account, name="delete_account"),
]
