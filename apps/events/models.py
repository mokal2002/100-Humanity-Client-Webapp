"""
Database models for Events and Event Photographs.
Supports upcoming/past filtering, SEO-friendly slugs, Cloudinary cover & additional images,
and strict validation of start/end dates.
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.gallery.services import delete_image_from_cloudinary


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")

    title = models.CharField(_("Event Title"), max_length=220)
    slug = models.SlugField(_("URL Slug"), max_length=240, unique=True)
    description = models.TextField(_("Event Description & Program Details"))
    start_date = models.DateField(_("Start Date"), db_index=True)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    start_time = models.TimeField(_("Start Time"), blank=True, null=True)
    end_time = models.TimeField(_("End Time"), blank=True, null=True)
    venue = models.CharField(_("Venue / Location"), max_length=255)
    map_link = models.URLField(
        _("Optional Map Link"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Optional Google Maps or OpenStreetMap URL for directions."),
    )
    cover_image_url = models.URLField(
        _("Cover Photograph URL"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Populated automatically via Cloudinary upload or optional HTTPS image URL."),
    )
    cover_public_id = models.CharField(
        _("Cloudinary Cover Public ID"),
        max_length=255,
        blank=True,
        default="",
    )
    registration_info = models.TextField(
        _("Registration or Contact Information"),
        blank=True,
        default="Free and open to all. Contact Arvind Betkar (8983087210 / arvindbet12@gmail.com) for inquiries.",
        help_text=_("No paid ticketing is used. Provide free participation or inquiry details."),
    )
    status = models.CharField(
        _("Publication Status"),
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date", "start_time"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        indexes = [
            models.Index(fields=["status", "start_date"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": _("End date cannot be earlier than the start date.")})
        if (
            self.start_date
            and (not self.end_date or self.end_date == self.start_date)
            and self.start_time
            and self.end_time
            and self.end_time < self.start_time
        ):
            raise ValidationError({"end_time": _("End time cannot be earlier than start time on the same day.")})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:220] or "event"
            slug_candidate = base_slug
            counter = 1
            while Event.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover_public_id:
            delete_image_from_cloudinary(self.cover_public_id)
        for img in self.additional_images.all():
            if img.cloudinary_public_id:
                delete_image_from_cloudinary(img.cloudinary_public_id)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"slug": self.slug})

    @property
    def is_upcoming(self) -> bool:
        comparison_date = self.end_date or self.start_date
        return comparison_date >= timezone.localdate()


class EventImage(models.Model):
    """Additional photographs attached to an Event."""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="additional_images",
        verbose_name=_("Event"),
    )
    caption = models.CharField(_("Caption"), max_length=200, blank=True, default="")
    alt_text = models.CharField(_("Accessible Alt Text"), max_length=220)
    image_url = models.URLField(_("Photograph Secure URL"), max_length=500)
    cloudinary_public_id = models.CharField(_("Cloudinary Public ID"), max_length=255, blank=True, default="")
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "created_at"]
        verbose_name = _("Additional Event Photograph")
        verbose_name_plural = _("Additional Event Photographs")

    def __str__(self):
        return f"{self.event.title} — Photo #{self.display_order}"

    def delete(self, *args, **kwargs):
        if self.cloudinary_public_id:
            delete_image_from_cloudinary(self.cloudinary_public_id)
        super().delete(*args, **kwargs)
