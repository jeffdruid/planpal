from django.contrib import admin
from .models import UserProfile
from .models import Friendship

admin.site.register(UserProfile)
# admin.site.register(Friendship)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    ordering = ("-created_at",)
