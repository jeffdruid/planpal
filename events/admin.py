from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "location",
        "created_by",
        "proposed_date",
        "finalized_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_by", "proposed_date", "finalized_date")
    search_fields = ("title", "description", "location")
