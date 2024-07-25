from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(
        "manage/<int:event_id>/",
        views.manage_invitations,
        name="manage_invitations",
    ),
    path(
        "create/<int:event_id>/",
        views.create_invitation,
        name="create_invitation",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
