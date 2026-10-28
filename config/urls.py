"""Root URL Configuration for 100% HUMANITY."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from config.sitemaps import SITEMAPS
from apps.core import views as core_views

# Customize Django Admin Branding
admin.site.site_header = "100% HUMANITY — Administration"
admin.site.site_title = "100% HUMANITY Admin"
admin.site.index_title = "Content & Community Management Dashboard"

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("healthz/", core_views.health_check, name="health_check"),
    # Public Application Routes
    path("", include("apps.core.urls", namespace="core")),
    path("dhamma-education/", include("apps.education.urls", namespace="education")),
    path("events/", include("apps.events.urls", namespace="events")),
    path("gallery/", include("apps.gallery.urls", namespace="gallery")),
    path("videos/", include("apps.videos.urls", namespace="videos")),
    path("articles/", include("apps.articles.urls", namespace="articles")),
    path("contact/", include("apps.contact.urls", namespace="contact")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.custom_404"
handler500 = "apps.core.views.custom_500"
