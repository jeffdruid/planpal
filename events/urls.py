from django.urls import path
from . import views

urlpatterns = [
    path("edit/<int:event_id>/", views.edit_event, name="edit_event"),
    path("<int:event_id>/", views.event_details, name="event_details"),
    path("create/", views.create_event, name="create_event"),
    path("details/<int:event_id>/", views.event_details, name="event_details"),
    path(
        "<int:event_id>/delete/",
        views.delete_event,
        name="delete_event",
    ),
]
