from django import forms
from .models import Event


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
