from django.contrib import admin
from django.utils.html import format_html
from apps.gallery.forms import GalleryAlbumAdminForm, GalleryImageAdminForm
from apps.gallery.models import GalleryAlbum, GalleryImage
from apps.gallery.services import delete_image_from_cloudinary


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    form = GalleryImageAdminForm
    extra = 1
    fields = ("title", "alt_text", "upload_file", "image_url", "display_order", "is_published")


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    form = GalleryAlbumAdminForm
    list_display = ("title", "category", "image_count", "display_order", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "category", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GalleryImageInline]

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Photos"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = ("thumbnail_preview", "title", "album", "display_order", "is_published", "created_at")
    list_filter = ("is_published", "album__category", "album")
    search_fields = ("title", "alt_text", "caption", "album__title")
    list_select_related = ("album",)
    actions = ["delete_selected_with_cloudinary"]

    def thumbnail_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" alt="{}" style="height:48px;width:64px;object-fit:cover;border-radius:4px;" />',
                obj.image_url,
                obj.alt_text,
            )
        return "—"
    thumbnail_preview.short_description = "Preview"

    @admin.action(description="Delete selected photographs (and remove from Cloudinary)")
    def delete_selected_with_cloudinary(self, request, queryset):
        for img in queryset:
            if img.cloudinary_public_id:
                delete_image_from_cloudinary(img.cloudinary_public_id)
            img.delete()
