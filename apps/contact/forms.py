"""
Contact form with strict validation and basic spam prevention (hidden honeypot field + length checks).
"""
import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.contact.models import ContactSubmission


class ContactForm(forms.ModelForm):
    # Honeypot field: hidden from human users via CSS & aria-hidden, bots fill it in
    website_url_honeypot = forms.CharField(
        required=False,
        label=_("Leave this field empty"),
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "class": "honeypot-field",
                "aria-hidden": "true",
            }
        ),
    )

    class Meta:
        model = ContactSubmission
        fields = ["full_name", "email", "phone", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter your full name"),
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("your.email@example.com"),
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Optional 10-digit mobile number"),
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Optional subject (e.g., Dhamma Study Circle, Event Inquiry)"),
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": _("Write your message or question here..."),
                    "required": True,
                }
            ),
        }

    def clean_website_url_honeypot(self):
        value = self.cleaned_data.get("website_url_honeypot", "")
        if value:
            raise ValidationError(_("Spam submission detected."))
        return value

    def clean_full_name(self):
        name = (self.cleaned_data.get("full_name") or "").strip()
        if len(name) < 2:
            raise ValidationError(_("Please enter your full name (at least 2 characters)."))
        return name

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if phone:
            digits = re.sub(r"[^0-9+]", "", phone)
            if len(digits) < 7 or len(digits) > 16:
                raise ValidationError(_("Please enter a valid phone number."))
        return phone

    def clean_message(self):
        msg = (self.cleaned_data.get("message") or "").strip()
        if len(msg) < 10:
            raise ValidationError(_("Please write a message of at least 10 characters."))
        if len(msg) > 5000:
            raise ValidationError(_("Message cannot exceed 5,000 characters."))
        return msg
