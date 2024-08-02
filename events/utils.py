from django.utils import timezone
from notifications.models import Notification
from django.db.models import Q


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
    for invitation in event.invitations.all():
        create_notification(invitation.user, event, "event_created", message)


def notify_event_updated(event):
    for invitee in event.invitations.all():
        message = f"The event '{event.title}' has been updated."

        if event.status == "Cancelled":
            message = f"The event '{event.title}' has been cancelled."
        elif event.status == "Confirmed":
            message = f"The event '{event.title}' has been confirmed."

        Notification.objects.create(
            user=invitee.user,
            event=event,
            type="event_updated",
            message=message,
        )


def notify_event_cancelled(event):
    message = f"The event '{event.title}' has been cancelled."
    for invitation in event.invitations.all():
        create_notification(invitation.user, event, "event_cancelled", message)


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
    for invitation in event.invitations.all():
        create_notification(invitation.user, event, "event_confirmed", message)


def delete_suggested_alternate_date_notification(invitation):
    Notification.objects.filter(
        event=invitation.event,
        user=invitation.event.created_by,
        type="suggested_alternate_date",
        message__icontains=invitation.user.username,
    ).delete()


def delete_related_notifications(user, friend):
    # Delete friend request notifications between user and friend
    Notification.objects.filter(
        Q(
            user=user,
            type="friend_request_received",
            message__icontains=friend.username,
        )
        | Q(
            user=friend,
            type="friend_request_received",
            message__icontains=user.username,
        )
    ).delete()

    # Delete suggested alternate date notifications between user and friend
    Notification.objects.filter(
        Q(
            user=user,
            type="suggested_alternate_date",
            message__icontains=friend.username,
        )
        | Q(
            user=friend,
            type="suggested_alternate_date",
            message__icontains=user.username,
        )
    ).delete()
