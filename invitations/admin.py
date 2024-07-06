# invitations/admin.py
from django.contrib import admin
from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "user",
        "status",
        "suggested_date_formatted",
        "read",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "read", "event__title", "user__username")
    search_fields = ("event__title", "user__username", "status")


admin.site.register(Invitation, InvitationAdmin)
