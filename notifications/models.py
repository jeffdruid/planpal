from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("event_created", "Event Created"),
        ("event_updated", "Event Updated"),
        ("event_cancelled", "Event Cancelled"),
        ("invitation_response", "Invitation Response"),
        ("suggested_alternate_date", "Suggested Alternate Date"),
        ("event_confirmed", "Event Confirmed"),
        ("friend_request_received", "Friend Request Received"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url = models.URLField(default="/")

    def __str__(self):
        return f"Notification for {self.user.username} - {self.type}"
