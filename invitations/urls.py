from django.urls import path
from . import views

urlpatterns = [
    path(
        "manage/<int:event_id>/",
        views.manage_invitations,
        name="manage_invitations",
    ),
]
