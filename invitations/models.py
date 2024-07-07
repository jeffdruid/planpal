from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Invitation(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Declined", "Declined"),
    ]

    event = models.ForeignKey(
        Event, related_name="invitations", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )
    suggested_date = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    @property
    def suggested_date_formatted(self):
        return (
            self.suggested_date.strftime("%B %d, %Y, %H:%M")
            if self.suggested_date
            else "-"
        )
