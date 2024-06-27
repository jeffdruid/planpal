from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notifications(request):
    # Static data for now
    notifications = [
        {
            "title": "New Event Invitation",
            "time": "Just now",
            "url": "/events/1/",
        },
        {
            "title": "Event Updated",
            "time": "5 minutes ago",
            "url": "/events/1/",
        },
        {
            "title": "Invitation Accepted",
            "time": "10 minutes ago",
            "url": "/events/1/",
        },
    ]
    return render(
        request,
        "notifications/notifications.html",
        {"notifications": notifications},
    )
