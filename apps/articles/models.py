"""
Database models for Educational Articles and Categories.
Uses a ForeignKey relationship (`category`) so `select_related("category")` is valid and fast.
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.gallery.services import delete_image_from_cloudinary


class ArticleCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    slug = models.SlugField(_("URL Slug"), max_length=120, unique=True)
    description = models.TextField(_("Category Description"), blank=True, default="")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")

    title = models.CharField(_("Article Title"), max_length=240)
    slug = models.SlugField(_("URL Slug"), max_length=255, unique=True)
    author_name = models.CharField(
        _("Author Name"),
        max_length=120,
        default="Arvind Betkar",
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("Category"),
    )
    tags = models.CharField(
        _("Tags (Comma-separated)"),
        max_length=250,
        blank=True,
        default="Buddha Dhamma, Equality, Compassion, Meditation",
        help_text=_("Comma-separated topics, e.g.: Buddha Dhamma, Meditation, Panchsheel, Rational Inquiry"),
    )
    summary = models.TextField(
        _("Article Summary / Excerpt"),
        max_length=500,
        help_text=_("Brief summary shown on article cards and search results."),
    )
    content = models.TextField(
        _("Full Article Content"),
        help_text=_(
            "Write plain text paragraphs separated by blank lines. "
            "Rendered safely using Django's auto-escaping and linebreaks filter (no unsafe raw HTML execution)."
        ),
    )
    cover_image_url = models.URLField(
        _("Cover Image Secure URL"),
        max_length=500,
        blank=True,
        default="",
    )
    cover_public_id = models.CharField(
        _("Cloudinary Cover Public ID"),
        max_length=255,
        blank=True,
        default="",
    )
    status = models.CharField(
        _("Publication Status"),
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(_("Publication Date"), default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = _("Educational Article")
        verbose_name_plural = _("Educational Articles")
        indexes = [
            models.Index(fields=["status", "-published_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:235] or "article"
            slug_candidate = base_slug
            counter = 1
            while Article.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover_public_id:
            delete_image_from_cloudinary(self.cover_public_id)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:article_detail", kwargs={"slug": self.slug})

    @property
    def tag_list(self):
        return [t.strip() for t in (self.tags or "").split(",") if t.strip()]
