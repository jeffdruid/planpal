from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event
from .forms import EventForm
from invitations.models import Invitation
from notifications.models import Notification
from .utils import (
    notify_event_created,
    notify_event_updated,
    notify_event_cancelled,
    notify_suggested_alternate_date,
    notify_event_confirmed,
)


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            notify_event_created(event)
            return redirect("manage_invitations", event_id=event.id)
    else:
        form = EventForm()
    return render(request, "events/add_event.html", {"form": form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    previous_status = event.status
    previous_title = event.title
    previous_description = event.description
    previous_proposed_date = event.proposed_date
    previous_location = event.location

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)
            has_changes = (
                updated_event.status != previous_status
                or updated_event.title != previous_title
                or updated_event.description != previous_description
                or updated_event.proposed_date != previous_proposed_date
                or updated_event.location != previous_location
            )
            updated_event.save()
            if has_changes:
                notify_event_updated(event)
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

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            user_invitations.update(status="Accepted")
        elif action == "deny":
            user_invitations.update(status="Declined")
        elif action == "maybe":
            alternate_date = request.POST.get("alternate_date")
            alternate_time = request.POST.get("alternate_time")
            suggested_datetime = f"{alternate_date} {alternate_time}"
            user_invitations.update(
                status="Maybe", suggested_date=suggested_datetime
            )
            notify_suggested_alternate_date(user_invitations.first())

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
        notify_event_cancelled(event)
        event.delete()
        return redirect("dashboard")
    return render(request, "events/confirm_delete.html", {"event": event})
