from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from events.models import Event
from .models import Invitation
from django.contrib import messages


@login_required
def manage_invitations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    invitations = Invitation.objects.filter(event=event)

    return render(
        request,
        "invitations/manage_invitations.html",
        {"event": event, "invitations": invitations},
    )


@login_required
def create_invitation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    users = User.objects.all()  # Include all users, including the current user
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        if Invitation.objects.filter(event=event, user=user).exists():
            messages.error(request, "Invitation already exists for this user.")
            return redirect("create_invitation", event_id=event_id)
        Invitation.objects.create(event=event, user=user, status="Pending")
        messages.success(request, "Invitation sent successfully.")
        return redirect("manage_invitations", event_id=event_id)
    return render(
        request,
        "invitations/create_invitation.html",
        {"event": event, "users": users},
    )
