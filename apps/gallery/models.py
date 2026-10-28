"""
Database models for Photo Gallery Albums and Gallery Images.
Stores Cloudinary `secure_url` and `public_id` in the database so production images
never rely on an ephemeral serverless/container filesystem.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.gallery.services import delete_image_from_cloudinary


class GalleryAlbum(models.Model):
    """Organizes photographs into thematic albums and categories."""
    title = models.CharField(_("Album Title"), max_length=200)
    slug = models.SlugField(_("URL Slug"), max_length=220, unique=True)
    category = models.CharField(
        _("Category"),
        max_length=100,
        default="Community & Dhamma Events",
        db_index=True,
        help_text=_("E.g., Dhamma Workshops, Meditation Sessions, Community Service, Study Circles."),
    )
    description = models.TextField(_("Album Description"), blank=True, default="")
    cover_image_url = models.URLField(
        _("Cover Image Secure URL"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Populated automatically via Cloudinary upload or optional cover image URL."),
    )
    cover_public_id = models.CharField(
        _("Cloudinary Cover Public ID"),
        max_length=255,
        blank=True,
        default="",
    )
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=1, db_index=True)
    is_published = models.BooleanField(_("Published"), default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = _("Gallery Album")
        verbose_name_plural = _("Gallery Albums")

    def __str__(self):
        return f"{self.title} ({self.category})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "album"
            slug_candidate = base_slug
            counter = 1
            while GalleryAlbum.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery:album_detail", kwargs={"slug": self.slug})

    @property
    def effective_cover_url(self) -> str:
        if self.cover_image_url:
            return self.cover_image_url
        first_img = self.images.filter(is_published=True).first()
        return first_img.image_url if first_img else ""


class GalleryImage(models.Model):
    """Individual photograph belonging to a GalleryAlbum, backed by Cloudinary."""
    album = models.ForeignKey(
        GalleryAlbum,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Album"),
    )
    title = models.CharField(_("Photo Title / Caption"), max_length=200)
    alt_text = models.CharField(
        _("Accessible Alt Text"),
        max_length=220,
        help_text=_("Descriptive text for screen readers and accessibility (required)."),
    )
    caption = models.TextField(_("Detailed Caption (Optional)"), blank=True, default="")
    image_url = models.URLField(
        _("Cloudinary Secure URL"),
        max_length=500,
        help_text=_("HTTPS URL returned by Cloudinary (or verified image URL)."),
    )
    cloudinary_public_id = models.CharField(
        _("Cloudinary Public ID"),
        max_length=255,
        blank=True,
        default="",
        db_index=True,
        help_text=_("Stored automatically when uploaded via Cloudinary so replacements/deletions clean up storage."),
    )
    width = models.PositiveIntegerField(_("Width (px)"), null=True, blank=True)
    height = models.PositiveIntegerField(_("Height (px)"), null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=1, db_index=True)
    is_published = models.BooleanField(_("Published"), default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = _("Gallery Photograph")
        verbose_name_plural = _("Gallery Photographs")
        indexes = [
            models.Index(fields=["is_published", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.album.title}"

    def save(self, *args, **kwargs):
        if not self.alt_text and self.title:
            self.alt_text = self.title
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cloudinary_public_id:
            delete_image_from_cloudinary(self.cloudinary_public_id)
        super().delete(*args, **kwargs)
