from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def manage_invitations(request, event_id):
    # Static data for now
    event = {
        "id": event_id,
        "title": "Sample Event",
    }
    invitations = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "status": "Accepted",
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "status": "Pending",
        },
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "status": "Declined",
        },
    ]
    return render(
        request,
        "invitations/manage_invitations.html",
        {"event": event, "invitations": invitations},
    )
