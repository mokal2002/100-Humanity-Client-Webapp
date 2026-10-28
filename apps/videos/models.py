"""
Database models for YouTube Video Categories and Videos.
Uses privacy-enhanced YouTube embeds (`https://www.youtube-nocookie.com/embed/VIDEO_ID`).
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.videos.validators import extract_youtube_video_id


class VideoCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    slug = models.SlugField(_("URL Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True, default="")
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=1)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = _("Video Category")
        verbose_name_plural = _("Video Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(_("Video Title"), max_length=220)
    slug = models.SlugField(_("URL Slug"), max_length=240, unique=True)
    description = models.TextField(_("Video Description & Key Takeaways"), blank=True, default="")
    youtube_url = models.URLField(
        _("YouTube URL"),
        max_length=500,
        help_text=_(
            "Paste a standard watch link (https://www.youtube.com/watch?v=...), "
            "short link (https://youtu.be/...), or Shorts link (https://www.youtube.com/shorts/...)."
        ),
    )
    video_id = models.CharField(
        _("Extracted YouTube Video ID"),
        max_length=20,
        editable=False,
        db_index=True,
    )
    thumbnail_url = models.URLField(
        _("Optional Custom Thumbnail URL"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Leave blank to automatically use the high-resolution YouTube thumbnail."),
    )
    category = models.ForeignKey(
        VideoCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="videos",
        verbose_name=_("Category"),
    )
    is_featured = models.BooleanField(_("Featured on Homepage"), default=False, db_index=True)
    is_published = models.BooleanField(_("Published"), default=True, db_index=True)
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=1, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = _("YouTube Video")
        verbose_name_plural = _("YouTube Videos")
        indexes = [
            models.Index(fields=["is_published", "display_order"]),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.youtube_url:
            self.video_id = extract_youtube_video_id(self.youtube_url)

    def save(self, *args, **kwargs):
        if self.youtube_url:
            self.video_id = extract_youtube_video_id(self.youtube_url)
        if not self.slug:
            base_slug = slugify(self.title)[:220] or f"video-{self.video_id}"
            slug_candidate = base_slug
            counter = 1
            while Video.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("videos:video_detail", kwargs={"slug": self.slug})

    @property
    def embed_url(self) -> str:
        """Returns privacy-enhanced YouTube embed URL."""
        return f"https://www.youtube-nocookie.com/embed/{self.video_id}?rel=0"

    @property
    def effective_thumbnail_url(self) -> str:
        """Returns custom thumbnail if provided, otherwise standard YouTube HQ thumbnail."""
        if self.thumbnail_url:
            return self.thumbnail_url
        return f"https://i.ytimg.com/vi/{self.video_id}/hqdefault.jpg"
