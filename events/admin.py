from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_by",
        "proposed_date",
        "finalized_date",
        "status",
    )
    list_filter = ("status", "proposed_date", "finalized_date")
    search_fields = (
        "title",
        "description",
        "location",
        "created_by__username",
    )
