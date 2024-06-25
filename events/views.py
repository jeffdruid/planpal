from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def add_event(request):
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

    return render(request, "events/edit_event.html", {"event": event})
