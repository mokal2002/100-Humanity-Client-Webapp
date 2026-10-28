from django.contrib import admin
from apps.contact.models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "subject", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone", "subject", "message", "admin_notes")
    list_editable = ("status",)
    readonly_fields = ("full_name", "email", "phone", "subject", "message", "created_at", "updated_at")
    actions = ["mark_new", "mark_in_progress", "mark_resolved"]

    def has_add_permission(self, request):
        # Submissions come from the public form
        return False

    @admin.action(description="Mark selected submissions as New")
    def mark_new(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.NEW)

    @admin.action(description="Mark selected submissions as In Progress")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.IN_PROGRESS)

    @admin.action(description="Mark selected submissions as Resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(status=ContactSubmission.Status.RESOLVED)
