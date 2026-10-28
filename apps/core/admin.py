from django.contrib import admin
from django import forms
from apps.core.models import SiteSettings, EnvironmentSetting


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
            "SEO & Footer",
            {
                "fields": (
                    "meta_description",
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
