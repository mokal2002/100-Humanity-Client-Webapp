"""Global template context processor providing SiteSettings and environment flags."""
from django.conf import settings
from apps.core.models import SiteSettings


def site_settings(request):
    return {
        "site_settings": SiteSettings.get_solo(),
        "cloudinary_configured": getattr(settings, "CLOUDINARY_CONFIGURED", False),
    }
