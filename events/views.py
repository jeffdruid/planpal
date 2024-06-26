from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def add_event(request):
    if request.method == "POST":
        # For now, just redirect to the invite guests page for event_id=1
        return redirect("invite_guests", event_id=1)
    return render(request, "events/add_event.html")


@login_required
def edit_event(request, event_id):
    # Static data for now
    event = {
        "title": "Sample Event",
        "date": "2024-06-15",
        "time": "14:00",
        "description": "This is a sample event description.",
        "location": "Sample Location",
        "status": "confirmed",
    }

    if request.method == "POST":
        # Handle form submission and save changes
        # For now, just redirect to the dashboard
        return redirect("dashboard")

    return render(
        request,
        "events/edit_event.html",
        {"event": event, "event_id": event_id},
    )


@login_required
def event_details(request, event_id):
    # Static data for now
    event = {
        "id": event_id,
        "title": "Sample Event",
        "date": "2024-06-15",
        "time": "14:00",
        "description": "This is a sample event description.",
        "location": "Sample Location",
        "status": "confirmed",
    }
    return render(request, "events/event_details.html", {"event": event})


@login_required
def invite_guests(request, event_id):
    # Static data for now
    event = {
        "id": event_id,
        "title": "Sample Event",
    }

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
