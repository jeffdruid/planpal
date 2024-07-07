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
    list_filter = ("event", "status", "read")


admin.site.register(Invitation, InvitationAdmin)
