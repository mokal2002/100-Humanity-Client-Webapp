"""Views for Home, About Us, robots.txt, health check, and custom error pages."""
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from apps.education.models import DhammaPrinciple
from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.videos.models import Video
from apps.articles.models import Article


def home_view(request):
    """
    Renders the homepage with dynamic database content and graceful empty states.
    """
    today = timezone.localdate()

    featured_principles = DhammaPrinciple.objects.filter(
        is_published=True, is_featured=True
    ).order_by("display_order", "principle_number")[:6]
    if not featured_principles.exists():
        featured_principles = DhammaPrinciple.objects.filter(
            is_published=True
        ).order_by("display_order", "principle_number")[:6]

    upcoming_events = Event.objects.filter(
        status=Event.Status.PUBLISHED,
    ).filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True, start_date__gte=today)
    ).order_by("start_date", "start_time")[:3]

    recent_photos = (
        GalleryImage.objects.filter(is_published=True, album__is_published=True)
        .select_related("album")
        .order_by("-created_at")[:6]
    )

    featured_videos = (
        Video.objects.filter(is_published=True)
        .select_related("category")
        .order_by("-is_featured", "display_order", "-created_at")[:3]
    )

    latest_articles = (
        Article.objects.filter(status=Article.Status.PUBLISHED)
        .select_related("category")
        .order_by("-published_at", "-created_at")[:3]
    )

    context = {
        "featured_principles": featured_principles,
        "total_principles_count": DhammaPrinciple.objects.filter(is_published=True).count(),
        "upcoming_events": upcoming_events,
        "recent_photos": recent_photos,
        "featured_videos": featured_videos,
        "latest_articles": latest_articles,
    }
    return render(request, "core/home.html", context)


def about_view(request):
    """Renders the About Us page with organization mission, values, and objectives."""
    principles_count = DhammaPrinciple.objects.filter(is_published=True).count()
    return render(
        request,
        "core/about.html",
        {"principles_count": principles_count},
    )


def robots_txt(request):
    """Serves SEO robots.txt pointing crawlers to sitemap.xml and disallowing /admin/."""
    sitemap_url = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def health_check(request):
    """Lightweight health endpoint for Render / uptime monitors."""
    return JsonResponse({"status": "ok", "service": "100% HUMANITY"})


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
