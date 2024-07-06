from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event
from .forms import EventForm
from invitations.models import Invitation
from notifications.models import Notification


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("dashboard")
    else:
        form = EventForm()
    return render(request, "events/add_event.html", {"form": form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = EventForm(instance=event)
    return render(
        request, "events/edit_event.html", {"form": form, "event_id": event_id}
    )


@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    invitations = Invitation.objects.filter(event=event)

    # Mark the invitations as read if the user opens the event details
    user_invitations = invitations.filter(user=request.user)
    user_invitations.update(read=True)

    # Mark notifications as read when the user views the event
    notifications = Notification.objects.filter(
        user=request.user, event=event, read=False
    )
    notifications.update(read=True)

    if request.method == "POST":
        action = request.POST.get("action")
        if action in ["accept", "deny"]:
            invitation = get_object_or_404(
                Invitation, event=event, user=request.user
            )
            invitation.status = (
                "Accepted" if action == "accept" else "Declined"
            )
            invitation.save()
        elif action == "maybe":
            invitation = get_object_or_404(
                Invitation, event=event, user=request.user
            )
            suggested_date_str = request.POST.get("alternate_date")
            suggested_time_str = request.POST.get("alternate_time")
            if suggested_date_str and suggested_time_str:
                suggested_date = timezone.datetime.strptime(
                    f"{suggested_date_str} {suggested_time_str}",
                    "%Y-%m-%d %H:%M",
                )
                invitation.suggested_date = suggested_date
                invitation.status = "Maybe"
                invitation.save()

    context = {
        "event": event,
        "invitations": invitations,
    }
    return render(request, "events/event_details.html", context)


@login_required
def invite_guests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        # Simulate sending an invitation and add a notification
        notifications = [
            {
                "title": "New Event Invitation",
                "time": "Just now",
                "url": f"/events/{event_id}/invitations/",
            },
            {
                "title": "Event Updated",
                "time": "5 minutes ago",
                "url": f"/events/{event_id}/",
            },
            {
                "title": "Invitation Accepted",
                "time": "10 minutes ago",
                "url": f"/events/{event_id}/invitations/",
            },
        ]
        return render(
            request,
            "events/invite_guests.html",
            {"event": event, "notifications": notifications},
        )

    return render(request, "events/invite_guests.html", {"event": event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        event.delete()
        return redirect("dashboard")
    return render(request, "events/confirm_delete.html", {"event": event})
