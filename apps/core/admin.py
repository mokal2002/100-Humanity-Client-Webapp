from django.contrib import admin
from apps.core.models import SiteSettings


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
