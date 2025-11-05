from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "leave_type", "from_date", "to_date", "status", "created_at")
    list_filter = ("status", "leave_type", "created_at")
    search_fields = ("user__username", "user__email", "reason")
    actions = ["mark_approved", "mark_rejected"]

    def mark_approved(self, request, queryset):
        updated = queryset.update(status=LeaveRequest.STATUS_APPROVED)
        self.message_user(request, f"{updated} leave(s) marked as approved.")
    mark_approved.short_description = "Mark selected leaves as Approved"

    def mark_rejected(self, request, queryset):
        updated = queryset.update(status=LeaveRequest.STATUS_REJECTED)
        self.message_user(request, f"{updated} leave(s) marked as rejected.")
    mark_rejected.short_description = "Mark selected leaves as Rejected"
