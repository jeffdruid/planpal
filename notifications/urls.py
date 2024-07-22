from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications, name="notifications"),
    path(
        "notifications/mark-read/<int:notification_id>/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "get-notifications/",
        views.get_notifications,
        name="get_notifications",
    ),
]
