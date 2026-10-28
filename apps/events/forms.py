from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.validators import validate_image_file
from apps.events.models import Event, EventImage
from apps.gallery.services import upload_image_to_cloudinary


class EventAdminForm(forms.ModelForm):
    upload_cover = forms.ImageField(
        label=_("Upload / Replace Cover Photograph via Cloudinary"),
        required=False,
        validators=[validate_image_file],
        help_text=_("Upload a JPG, PNG, or WEBP cover photograph (max 5 MB) to Cloudinary."),
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "slug",
            "status",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "venue",
            "map_link",
            "description",
            "registration_info",
            "upload_cover",
            "cover_image_url",
            "cover_public_id",
        ]

    def clean(self):
        cleaned_data = super().clean()
        upload_cover = cleaned_data.get("upload_cover")
        if upload_cover:
            existing_pid = self.instance.cover_public_id if self.instance.pk else ""
            res = upload_image_to_cloudinary(
                upload_cover,
                subfolder="events/covers",
                existing_public_id=existing_pid,
            )
            if not res.success:
                raise ValidationError({"upload_cover": res.error_message})
            cleaned_data["cover_image_url"] = res.secure_url
            cleaned_data["cover_public_id"] = res.public_id
        return cleaned_data


class EventImageInlineForm(forms.ModelForm):
    upload_photo = forms.ImageField(
        label=_("Upload via Cloudinary"),
        required=False,
        validators=[validate_image_file],
    )

    class Meta:
        model = EventImage
        fields = ["caption", "alt_text", "upload_photo", "image_url", "cloudinary_public_id", "display_order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_url"].required = False

    def clean(self):
        cleaned_data = super().clean()
        upload_photo = cleaned_data.get("upload_photo")
        image_url = cleaned_data.get("image_url")
        if upload_photo:
            existing_pid = self.instance.cloudinary_public_id if self.instance.pk else ""
            res = upload_image_to_cloudinary(
                upload_photo,
                subfolder="events/photos",
                existing_public_id=existing_pid,
            )
            if not res.success:
                raise ValidationError({"upload_photo": res.error_message})
            cleaned_data["image_url"] = res.secure_url
            cleaned_data["cloudinary_public_id"] = res.public_id
        elif not image_url:
            raise ValidationError(_("Provide either an image file upload or an HTTPS image URL."))
        return cleaned_data
