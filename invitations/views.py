from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from events.models import Event
from .models import Invitation
from django.contrib import messages
from notifications.models import Notification


@login_required
def manage_invitations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by != request.user:
        return redirect("dashboard")

    invitations = Invitation.objects.filter(event=event).select_related("user")

    return render(
        request,
        "invitations/manage_invitations.html",
        {"event": event, "invitations": invitations},
    )


@login_required
def create_invitation(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the logged-in user is the creator of the event
    if request.user != event.created_by:
        messages.error(
            request,
            "You are not authorized to send invitations for this event.",
        )
        return redirect("event_details", event_id=event_id)

    users = User.objects.all()  # Include all users, including the current user
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        if Invitation.objects.filter(event=event, user=user).exists():
            messages.error(request, "Invitation already exists for this user.")
            return redirect("create_invitation", event_id=event_id)
        Invitation.objects.create(event=event, user=user, status="Pending")

        # Create notification for the invited user
        Notification.objects.create(
            user=user,
            event=event,
            title="New Event Invitation",
            message=f"You have been invited to the event '{event.title}'.",
            url=f"/events/{event.id}/",
        )

        messages.success(request, "Invitation sent successfully.")
        return redirect("manage_invitations", event_id=event_id)
    return render(
        request,
        "invitations/create_invitation.html",
        {"event": event, "users": users},
    )
