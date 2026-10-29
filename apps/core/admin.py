from django.contrib import admin, messages
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from apps.core.models import SiteSettings, EnvironmentSetting, BackgroundMusic


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Website Identity & Contact Information",
            {
                "fields": (
                    "site_name",
                    "tagline",
                    "contact_person",
                    "contact_email",
                    "contact_phone",
                    "contact_address",
                )
            },
        ),
        (
            "Homepage Content",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "dhamma_intro_title",
                    "dhamma_intro_text",
                    "mission_statement",
                    "vision_statement",
                    "community_participation_title",
                    "community_participation_text",
                )
            },
        ),
        (
            "About Us Page Content",
            {
                "fields": (
                    "about_introduction",
                    "about_purpose_of_dhamma",
                    "about_equality_compassion",
                    "about_scientific_thinking",
                    "about_educational_objectives",
                )
            },
        ),
        (
            "YouTube & Social Media Links",
            {
                "fields": (
                    "youtube_channel_name",
                    "youtube_channel_url",
                    "facebook_url",
                    "instagram_url",
                    "telegram_url",
                )
            },
        ),
        (
            "SEO, Analytics & Footer",
            {
                "fields": (
                    "meta_description",
                    "google_analytics_id",
                    "footer_note",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        # Allow adding only if no record exists yet
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class EnvironmentSettingForm(forms.ModelForm):
    class Meta:
        model = EnvironmentSetting
        fields = "__all__"
        widgets = {
            "database_url": forms.TextInput(
                attrs={
                    "class": "vLargeTextField",
                    "placeholder": "postgresql://user:password@ep-example.region.neon.tech/neondb?sslmode=require",
                    "style": "font-family: monospace; width: 100%; max-width: 720px;",
                }
            ),
            "cloudinary_api_secret": forms.PasswordInput(
                render_value=True,
                attrs={
                    "class": "vTextField",
                    "placeholder": "Enter or update Cloudinary API secret",
                    "style": "font-family: monospace;",
                }
            ),
            "secret_key": forms.TextInput(
                attrs={
                    "class": "vLargeTextField",
                    "style": "font-family: monospace; width: 100%; max-width: 720px;",
                }
            ),
            "allowed_hosts": forms.TextInput(
                attrs={
                    "class": "vLargeTextField",
                    "style": "font-family: monospace; width: 100%; max-width: 720px;",
                }
            ),
            "csrf_trusted_origins": forms.TextInput(
                attrs={
                    "class": "vLargeTextField",
                    "style": "font-family: monospace; width: 100%; max-width: 720px;",
                }
            ),
        }


@admin.register(EnvironmentSetting)
class EnvironmentSettingAdmin(admin.ModelAdmin):
    form = EnvironmentSettingForm
    readonly_fields = ("active_database_engine", "cloudinary_status", "updated_at")
    fieldsets = (
        (
            "1. Database Connection (DATABASE_URL)",
            {
                "description": (
                    "Switch or configure your production database (e.g. Neon PostgreSQL, Supabase, Railway). "
                    "Leave blank to use the local SQLite database. Changes are written to the live .env file."
                ),
                "fields": (
                    "active_database_engine",
                    "database_url",
                ),
            },
        ),
        (
            "2. Cloudinary Media & Photos API",
            {
                "description": (
                    "Configure Cloudinary credentials for event photograph and banner uploads. "
                    "Changes apply immediately in-memory and write to .env."
                ),
                "fields": (
                    "cloudinary_status",
                    "cloudinary_cloud_name",
                    "cloudinary_api_key",
                    "cloudinary_api_secret",
                    "cloudinary_folder",
                ),
            },
        ),
        (
            "3. External Integrations (YouTube)",
            {
                "fields": (
                    "youtube_api_key",
                ),
            },
        ),
        (
            "4. Core Django Security & Allowed Domains",
            {
                "classes": ("collapse",),
                "description": "Critical security headers. Only modify if domain names change.",
                "fields": (
                    "secret_key",
                    "allowed_hosts",
                    "csrf_trusted_origins",
                    "updated_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not EnvironmentSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BackgroundMusic)
class BackgroundMusicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "audio_player_preview",
        "is_active_badge",
        "select_active_button",
        "is_enabled",
        "default_volume",
        "loop",
        "updated_at",
    )
    list_filter = ("is_active", "is_enabled")
    search_fields = ("title", "artist_credit")
    actions = ["make_active_action", "enable_tracks", "disable_tracks"]
    readonly_fields = ("audio_player_detail", "created_at", "updated_at")

    fieldsets = (
        (
            "Track Details & Playback Preview",
            {
                "fields": (
                    "audio_player_detail",
                    "title",
                    "artist_credit",
                )
            },
        ),
        (
            "Audio Source (File Upload or Stream URL)",
            {
                "description": "Upload an MP3/WAV/OGG audio file, or provide an external streaming URL.",
                "fields": (
                    "audio_file",
                    "audio_url",
                )
            },
        ),
        (
            "Website Playback & Activation Controls",
            {
                "description": "Control whether this track plays on the live website and adjust default volume.",
                "fields": (
                    "is_active",
                    "is_enabled",
                    "default_volume",
                    "loop",
                    "order",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def audio_player_preview(self, obj):
        url = obj.effective_audio_url
        if url:
            return format_html(
                '<audio controls preload="none" style="height: 32px; width: 220px; vertical-align: middle;">'
                '<source src="{}">Your browser does not support audio element.</audio>',
                url,
            )
        return mark_safe('<span style="color: #999; font-size: 11px;">No audio source</span>')
    audio_player_preview.short_description = "Listen / Preview"

    def is_active_badge(self, obj):
        if obj.is_active and obj.is_enabled:
            return format_html(
                '<span style="background: #1B365D; color: #D49B38; font-weight: bold; '
                'padding: 3px 10px; border-radius: 12px; font-size: 11px; border: 1px solid #D49B38; white-space: nowrap;">'
                '&#9679; ACTIVE ON SITE</span>'
            )
        elif obj.is_active and not obj.is_enabled:
            return mark_safe('<span style="color: #D97706; font-size: 11px; font-weight: bold;">Active (Disabled)</span>')
        return mark_safe('<span style="color: #888; font-size: 11px;">Inactive</span>')
    is_active_badge.short_description = "Live Status"

    def select_active_button(self, obj):
        if obj.is_active:
            return mark_safe('<strong style="color: #059669; font-size: 11px;">&#10004; Currently Playing</strong>')
        return format_html(
            '<a class="button" href="activate/{}/" style="background: #1B365D; color: #FAF7F0; '
            'padding: 3px 8px; border-radius: 6px; font-size: 11px; text-decoration: none; display: inline-block; white-space: nowrap;">'
            '&#9654; Set as Active</a>',
            obj.pk,
        )
    select_active_button.short_description = "Select Active"

    def audio_player_detail(self, obj):
        if not obj or not obj.pk:
            return mark_safe("<em>Save this track to listen to the preview player.</em>")
        url = obj.effective_audio_url
        if url:
            return format_html(
                '<div style="background: #FAF7F0; border: 1px solid #E6DEC8; border-radius: 8px; padding: 14px; max-width: 600px;">'
                '<div style="font-weight: bold; margin-bottom: 8px; color: #1B365D; font-size: 13px;">'
                '&#127925; In-Dashboard Audio Preview Player:'
                '</div>'
                '<audio controls preload="auto" style="width: 100%; max-width: 520px; margin-bottom: 6px;">'
                '<source src="{}">Your browser does not support audio playback.'
                '</audio>'
                '<div style="font-size: 11px; color: #666; line-height: 1.5;">'
                'Source URL: <code>{}</code><br>'
                'Configured Volume: <strong>{}%</strong> | Active On Site: <strong>{}</strong>'
                '</div>'
                '</div>',
                url,
                url,
                obj.default_volume,
                "Yes" if obj.is_active else "No",
            )
        return mark_safe("<em>Provide an audio file upload or streaming URL to enable in-dashboard preview.</em>")
    audio_player_detail.short_description = "Audio Player Preview"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path("activate/<int:track_id>/", self.admin_site.admin_view(self.activate_track_view), name="core_backgroundmusic_activate"),
        ]
        return custom_urls + urls

    def activate_track_view(self, request, track_id):
        track = get_object_or_404(BackgroundMusic, pk=track_id)
        track.is_active = True
        track.is_enabled = True
        track.save()
        self.message_user(
            request,
            f"'{track.title}' is now set as the ACTIVE background music track on the website!",
            level=messages.SUCCESS,
        )
        return HttpResponseRedirect("../../")

    @admin.action(description="Set selected track as active website background music")
    def make_active_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one track to set as active.", level=messages.WARNING)
            return
        track = queryset.first()
        track.is_active = True
        track.is_enabled = True
        track.save()
        self.message_user(request, f"'{track.title}' is now active on the website.", level=messages.SUCCESS)

    @admin.action(description="Enable selected tracks globally")
    def enable_tracks(self, request, queryset):
        count = queryset.update(is_enabled=True)
        self.message_user(request, f"{count} track(s) enabled.", level=messages.SUCCESS)

    @admin.action(description="Disable selected tracks globally")
    def disable_tracks(self, request, queryset):
        count = queryset.update(is_enabled=False)
        self.message_user(request, f"{count} track(s) disabled.", level=messages.SUCCESS)
