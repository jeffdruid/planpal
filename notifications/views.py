from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    context = {"notifications": notifications}
    return render(request, "notifications/notifications.html", context)


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()

    if notification.event:
        return redirect(notification.event.get_absolute_url())
    elif notification.type == "friend_request_received":
        return redirect("friends_page")
    else:
        return redirect("notifications")
