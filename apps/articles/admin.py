from django.contrib import admin
from apps.articles.forms import ArticleAdminForm
from apps.articles.models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "author_name", "category", "status", "published_at", "updated_at")
    list_filter = ("status", "category", "published_at")
    search_fields = ("title", "author_name", "summary", "content", "tags")
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ("category",)
    actions = ["publish_articles", "draft_articles"]

    @admin.action(description="Publish selected articles")
    def publish_articles(self, request, queryset):
        queryset.update(status=Article.Status.PUBLISHED)

    @admin.action(description="Mark selected articles as Draft")
    def draft_articles(self, request, queryset):
        queryset.update(status=Article.Status.DRAFT)
