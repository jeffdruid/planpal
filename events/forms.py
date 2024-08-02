from django import forms
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "location",
            "proposed_date",
            "status",
        ]
        widgets = {
            "proposed_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].initial = "Default Title"
        self.fields["description"].initial = "Default Description"
        self.fields["location"].initial = "The Spire of Dublin"
        self.fields["proposed_date"].initial = (
            timezone.now()
            # add 1 hour (for testing)
            + timezone.timedelta(hours=1)
        )
        self.fields["status"].initial = "Pending"

    def clean_proposed_date(self):
        proposed_date = self.cleaned_data.get("proposed_date")
        # Check if the proposed date is in the past
        if proposed_date < timezone.now():
            raise forms.ValidationError(
                "The proposed date cannot be in the past."
            )
        return proposed_date
