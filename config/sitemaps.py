"""XML Sitemaps for SEO discoverability of public pages, events, albums, videos, and articles."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.events.models import Event
from apps.articles.models import Article
from apps.gallery.models import GalleryAlbum
from apps.videos.models import Video


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "education:principle_list",
            "events:event_list",
            "gallery:album_list",
            "videos:video_list",
            "articles:article_list",
            "contact:contact",
        ]

    def location(self, item):
        return reverse(item)


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Event.objects.filter(status=Event.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(status=Article.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class GalleryAlbumSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return GalleryAlbum.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class VideoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Video.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    "static": StaticViewSitemap,
    "events": EventSitemap,
    "articles": ArticleSitemap,
    "gallery": GalleryAlbumSitemap,
    "videos": VideoSitemap,
}
