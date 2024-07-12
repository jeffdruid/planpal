from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from events.models import Event
from .models import Invitation
from django.contrib import messages
from notifications.models import Notification
from accounts.models import Friendship


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

    # Fetching friends of the current user
    friend_ids = Friendship.objects.filter(
        from_user=request.user, status="accepted"
    ).values_list("to_user_id", flat=True)
    users = User.objects.filter(id__in=friend_ids)

    no_friends = False
    if not users.exists():
        no_friends = True

    # TODO - for testing purposes, we are including all users in the list of potential invitees
    # Uncomment the following line to include the current user in the list of potential invitees
    # users = User.objects.all()

    # TODO - for testing purposes, we are including the current user in the list of potential invitees
    # Exclude the current user from the list of potential invitees
    # users = User.objects.exclude(id=request.user.id)

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
            type="event_created",
            message=f"You have been invited to the event '{event.title}'.",
        )

        messages.success(request, "Invitation sent successfully.")
        return redirect("manage_invitations", event_id=event_id)

    context = {
        "event": event,
        "users": users,
        "no_friends": no_friends,
    }

    return render(
        request,
        "invitations/create_invitation.html",
        context,
    )
