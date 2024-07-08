from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        all_unread_notifications = Notification.objects.filter(
            user=request.user, read=False
        ).order_by("-created_at")
        unread_count = all_unread_notifications.count()
        recent_unread_notifications = all_unread_notifications[:8]
        return {
            "recent_unread_notifications": recent_unread_notifications,
            "unread_count": unread_count,
        }
    return {}
