from django.contrib import admin
from apps.events.forms import EventAdminForm, EventImageInlineForm
from apps.events.models import Event, EventImage


class EventImageInline(admin.TabularInline):
    model = EventImage
    form = EventImageInlineForm
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ("title", "start_date", "venue", "status", "updated_at")
    list_filter = ("status", "start_date")
    search_fields = ("title", "venue", "description", "registration_info")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventImageInline]
    actions = ["make_published", "make_draft"]

    @admin.action(description="Publish selected events")
    def make_published(self, request, queryset):
        queryset.update(status=Event.Status.PUBLISHED)

    @admin.action(description="Unpublish (mark as Draft) selected events")
    def make_draft(self, request, queryset):
        queryset.update(status=Event.Status.DRAFT)
