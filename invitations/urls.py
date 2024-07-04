from django.urls import path
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
]
