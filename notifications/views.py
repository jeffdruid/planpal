from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")
    for notification in user_notifications:
        if not notification.read:
            notification.read = True
            notification.save()
    return render(
        request,
        "notifications/notifications.html",
        {"notifications": user_notifications},
    )
