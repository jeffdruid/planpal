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
    list_filter = ("status", "read", "created_at", "updated_at")

    def suggested_date_formatted(self, obj):
        return obj.suggested_date_formatted

    suggested_date_formatted.admin_order_field = "suggested_date"
    suggested_date_formatted.short_description = "Suggested Date"


admin.site.register(Invitation, InvitationAdmin)
