from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from apps.events.models import Event


def event_list_view(request):
    """
    Displays published events with search, upcoming/past filtering, and pagination.
    """
    today = timezone.localdate()
    search_query = request.GET.get("q", "").strip()
    period_filter = request.GET.get("period", "all").strip().lower()

    base_qs = Event.objects.filter(status=Event.Status.PUBLISHED)
    if search_query:
        base_qs = base_qs.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(venue__icontains=search_query)
        )

    upcoming_qs = base_qs.filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True, start_date__gte=today)
    ).order_by("start_date", "start_time")

    past_qs = base_qs.filter(
        Q(end_date__lt=today) | Q(end_date__isnull=True, start_date__lt=today)
    ).order_by("-start_date", "-start_time")

    if period_filter == "upcoming":
        active_qs = upcoming_qs
    elif period_filter == "past":
        active_qs = past_qs
    else:
        active_qs = base_qs.order_by("-start_date", "start_time")

    paginator = Paginator(active_qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "events/event_list.html",
        {
            "upcoming_events": upcoming_qs[:6],
            "past_events": past_qs[:6],
            "page_obj": page_obj,
            "search_query": search_query,
            "period_filter": period_filter,
        },
    )


def event_detail_view(request, slug):
    """Displays full event details, venue, schedule, registration info, and additional photos."""
    event = get_object_or_404(
        Event.objects.prefetch_related("additional_images"),
        slug=slug,
        status=Event.Status.PUBLISHED,
    )
    return render(request, "events/event_detail.html", {"event": event})
