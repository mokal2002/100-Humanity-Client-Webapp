"""Global template context processor providing SiteSettings, background music, and environment flags."""
from django.conf import settings
from apps.core.models import SiteSettings, BackgroundMusic


def site_settings(request):
    return {
        "site_settings": SiteSettings.get_solo(),
        "cloudinary_configured": getattr(settings, "CLOUDINARY_CONFIGURED", False),
        "active_music": BackgroundMusic.get_active_track(),
    }
