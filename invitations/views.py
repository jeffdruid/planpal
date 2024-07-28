from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from events.models import Event
from .models import Invitation
from django.contrib import messages
from notifications.models import Notification
from accounts.models import Friendship
from django.db.models import Q


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

    # Fetch both incoming and outgoing friendships
    friends = Friendship.objects.filter(
        Q(from_user=request.user, status="accepted")
        | Q(to_user=request.user, status="accepted")
    )

    # Extract users who are friends of the current user
    users = []
    for friendship in friends:
        if friendship.from_user == request.user:
            users.append(friendship.to_user)
        else:
            users.append(friendship.from_user)

    user_invitations = set(event.invitations.values_list("user", flat=True))

    if not users:
        messages.info(request, "You have no friends to invite to this event.")
        return redirect("friends_page")

    if request.method == "POST":
        if "send_all" in request.POST:
            for user in users:
                if user.id not in user_invitations:
                    Invitation.objects.create(
                        event=event, user=user, status="Pending"
                    )
                    Notification.objects.create(
                        user=user,
                        event=event,
                        type="event_created",
                        message=f"You have been invited to the event '{event.title}'.",
                    )
            messages.success(request, "All invitations sent successfully.")
            return redirect("create_invitation", event_id=event_id)

        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        # Check if the selected user is a friend
        if user not in users:
            messages.error(
                request, "You can only invite friends to this event."
            )
            return redirect("create_invitation", event_id=event_id)

        if user.id in user_invitations:
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
        return redirect("create_invitation", event_id=event_id)

    return render(
        request,
        "invitations/create_invitation.html",
        {"event": event, "users": users, "user_invitations": user_invitations},
    )
