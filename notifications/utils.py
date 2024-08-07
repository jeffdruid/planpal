from django.utils import timezone
from .models import Notification


def create_notification(user, event, notification_type, message):
    Notification.objects.create(
        user=user,
        event=event,
        type=notification_type,
        message=message,
        created_at=timezone.now(),
    )


def notify_event_created(event):
    message = f"A new event '{event.title}' has been created."
    for invitee in event.invitees.all():
        create_notification(invitee, event, "event_created", message)


def notify_event_updated(event):
    message = f"The event '{event.title}' has been updated."
    for invitee in event.invitees.all():
        create_notification(invitee, event, "event_updated", message)


def notify_event_cancelled(event):
    message = f"The event '{event.title}' has been cancelled."
    for invitee in event.invitees.all():
        create_notification(invitee, event, "event_cancelled", message)


def notify_invitation_response(invitation):
    message = (
        f"{invitation.user.username} has {invitation.status} your invitation "
        f"for the event '{invitation.event.title}'."
    )
    create_notification(
        invitation.event.created_by,
        invitation.event,
        "invitation_response",
        message,
    )


def notify_suggested_alternate_date(invitation):
    message = (
        f"{invitation.user.username} has suggested an alternative date "
        f"for the event '{invitation.event.title}'."
    )
    create_notification(
        invitation.event.created_by,
        invitation.event,
        "suggested_alternate_date",
        message,
    )


def notify_event_confirmed(event):
    message = f"The event '{event.title}' has been confirmed."
    for invitee in event.invitees.all():
        create_notification(invitee, event, "event_confirmed", message)
