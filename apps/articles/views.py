from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from apps.articles.models import Article, ArticleCategory


def article_list_view(request):
    """Displays published articles with category filter, tag filter, search, and pagination."""
    category_slug = request.GET.get("category", "").strip()
    tag_query = request.GET.get("tag", "").strip()
    search_query = request.GET.get("q", "").strip()

    articles_qs = (
        Article.objects.filter(status=Article.Status.PUBLISHED)
        .select_related("category")
        .order_by("-published_at", "-created_at")
    )

    if category_slug:
        articles_qs = articles_qs.filter(category__slug=category_slug)
    if tag_query:
        articles_qs = articles_qs.filter(tags__icontains=tag_query)
    if search_query:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_query)
            | Q(summary__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(author_name__icontains=search_query)
            | Q(tags__icontains=search_query)
        )

    categories = ArticleCategory.objects.all()
    paginator = Paginator(articles_qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "articles/article_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "selected_category": category_slug,
            "selected_tag": tag_query,
            "search_query": search_query,
        },
    )


def article_detail_view(request, slug):
    """Displays a full published article with safe HTML escaping and related articles."""
    article = get_object_or_404(
        Article.objects.select_related("category"),
        slug=slug,
        status=Article.Status.PUBLISHED,
    )
    related_qs = (
        Article.objects.filter(status=Article.Status.PUBLISHED)
        .exclude(pk=article.pk)
        .select_related("category")
    )
    if article.category_id:
        related_articles = related_qs.filter(category_id=article.category_id)[:3]
        if not related_articles.exists():
            related_articles = related_qs[:3]
    else:
        related_articles = related_qs[:3]

    return render(
        request,
        "articles/article_detail.html",
        {
            "article": article,
            "related_articles": related_articles,
        },
    )
