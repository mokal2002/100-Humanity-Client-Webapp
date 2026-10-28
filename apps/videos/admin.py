from django.contrib import admin
from django.utils.html import format_html
from apps.videos.models import Video, VideoCategory


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",
        "title",
        "category",
        "video_id",
        "display_order",
        "is_featured",
        "is_published",
        "created_at",
    )
    list_editable = ("display_order", "is_featured", "is_published")
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "description", "video_id", "youtube_url")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("video_id", "created_at", "updated_at")
    list_select_related = ("category",)

    def thumbnail_preview(self, obj):
        if obj.video_id:
            return format_html(
                '<img src="{}" alt="{}" style="height:45px;width:80px;object-fit:cover;border-radius:4px;" />',
                obj.effective_thumbnail_url,
                obj.title,
            )
        return "—"
    thumbnail_preview.short_description = "Thumbnail"
