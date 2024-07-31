from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "", include("accounts.urls")
    ),  # Ensure this comes before allauth.urls
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("invitations/", include("invitations.urls")),
    path("notifications/", include("notifications.urls")),
    path("accounts/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
