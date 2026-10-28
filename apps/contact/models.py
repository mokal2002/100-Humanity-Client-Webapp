"""
Database model for Contact Us submissions.
Protected from public access; administrators can mark submissions New, In Progress, or Resolved.
Does not require any paid external email service.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactSubmission(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", _("New")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        RESOLVED = "RESOLVED", _("Resolved")

    full_name = models.CharField(_("Your Full Name"), max_length=120)
    email = models.EmailField(_("Email Address"))
    phone = models.CharField(_("Phone Number (Optional)"), max_length=30, blank=True, default="")
    subject = models.CharField(_("Subject (Optional)"), max_length=200, blank=True, default="")
    message = models.TextField(_("Message"))
    status = models.CharField(
        _("Workflow Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    admin_notes = models.TextField(
        _("Internal Admin Notes"),
        blank=True,
        default="",
        help_text=_("Private notes visible only to authorized administrators."),
    )
    created_at = models.DateTimeField(_("Submitted At"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Contact Submission")
        verbose_name_plural = _("Contact Submissions")
        indexes = [
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        subj = self.subject or "General Inquiry"
        return f"{self.full_name} — {subj} ({self.get_status_display()})"
