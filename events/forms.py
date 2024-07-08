from django import forms
from .models import Event
from datetime import datetime


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
        self.fields["location"].initial = "Default Location"
        self.fields["proposed_date"].initial = datetime.now()
        self.fields["status"].initial = "Pending"
