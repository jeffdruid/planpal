from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        all_notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")
        recent_notifications = all_notifications[:8]
        notification_count = all_notifications.count()
        return {
            "recent_notifications": recent_notifications,
            "notification_count": notification_count,
        }
    return {}
