from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from invitations.models import Invitation


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
