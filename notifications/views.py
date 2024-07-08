from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    all_notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")
    return render(
        request,
        "notifications/notifications.html",
        {"notifications": all_notifications},
    )


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    notification.read = True
    notification.save()
    return redirect(notification.event.get_absolute_url())
