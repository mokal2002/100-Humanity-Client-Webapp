from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from apps.videos.models import Video, VideoCategory


def video_list_view(request):
    """Displays published YouTube videos with category filter, search, and pagination."""
    category_slug = request.GET.get("category", "").strip()
    search_query = request.GET.get("q", "").strip()

    videos_qs = Video.objects.filter(is_published=True).select_related("category")
    if category_slug:
        videos_qs = videos_qs.filter(category__slug=category_slug)
    if search_query:
        videos_qs = videos_qs.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    categories = VideoCategory.objects.all()
    paginator = Paginator(videos_qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "videos/video_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "selected_category": category_slug,
            "search_query": search_query,
        },
    )


def video_detail_view(request, slug):
    """Displays a dedicated video playback page with privacy-enhanced embed and related talks."""
    video = get_object_or_404(
        Video.objects.select_related("category"),
        slug=slug,
        is_published=True,
    )
    related_videos = (
        Video.objects.filter(is_published=True)
        .exclude(pk=video.pk)
        .select_related("category")
        .order_by("-is_featured", "display_order")[:3]
    )
    return render(
        request,
        "videos/video_detail.html",
        {
            "video": video,
            "related_videos": related_videos,
        },
    )
