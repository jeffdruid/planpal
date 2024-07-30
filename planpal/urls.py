from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "", include("accounts.urls")
    ),  # Ensure this comes before allauth.urls
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("events/", include("events.urls")),
    path("invitations/", include("invitations.urls")),
    path("notifications/", include("notifications.urls")),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="account_reset_password_from_key_done",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
