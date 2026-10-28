"""
Forms for single and multi-image gallery uploads and replacements with Cloudinary validation.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.validators import validate_image_file
from apps.gallery.models import GalleryAlbum, GalleryImage
from apps.gallery.services import upload_image_to_cloudinary


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp", "multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)] if data else []
        for f in result:
            validate_image_file(f)
        return result


class BulkGalleryUploadForm(forms.Form):
    """Allows authorized staff/admins to upload multiple photographs into an album in one workflow."""
    album = forms.ModelChoiceField(
        queryset=GalleryAlbum.objects.all(),
        label=_("Select Destination Album"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    default_caption_prefix = forms.CharField(
        max_length=160,
        required=False,
        label=_("Default Title / Caption Prefix (Optional)"),
        help_text=_("If left blank, each image's filename is cleaned and used as its default title and alt text."),
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Dhamma Study Workshop"}),
    )
    images = MultipleImageField(
        label=_("Select Photographs (JPG, PNG, WEBP — up to 5 MB each)"),
        required=True,
    )


class GalleryImageAdminForm(forms.ModelForm):
    """Admin form supporting direct file upload/replacement to Cloudinary OR pasting an existing HTTPS URL."""
    upload_file = forms.ImageField(
        label=_("Upload / Replace Image via Cloudinary"),
        required=False,
        validators=[validate_image_file],
        help_text=_("Select a JPG, PNG, or WEBP image (max 5 MB) to upload directly to Cloudinary."),
    )

    class Meta:
        model = GalleryImage
        fields = [
            "album",
            "title",
            "alt_text",
            "caption",
            "upload_file",
            "image_url",
            "cloudinary_public_id",
            "display_order",
            "is_published",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_url"].required = False

    def clean(self):
        cleaned_data = super().clean()
        upload_file = cleaned_data.get("upload_file")
        image_url = cleaned_data.get("image_url")

        if upload_file:
            existing_pid = self.instance.cloudinary_public_id if self.instance.pk else ""
            result = upload_image_to_cloudinary(
                upload_file,
                subfolder="gallery",
                existing_public_id=existing_pid,
            )
            if not result.success:
                raise ValidationError({"upload_file": result.error_message})
            cleaned_data["image_url"] = result.secure_url
            cleaned_data["cloudinary_public_id"] = result.public_id
            self.instance.width = result.width
            self.instance.height = result.height
        elif not image_url:
            raise ValidationError(
                _("Please either select an image file to upload to Cloudinary or provide a valid HTTPS image URL.")
            )
        return cleaned_data


class GalleryAlbumAdminForm(forms.ModelForm):
    upload_cover = forms.ImageField(
        label=_("Upload / Replace Cover Image via Cloudinary"),
        required=False,
        validators=[validate_image_file],
    )

    class Meta:
        model = GalleryAlbum
        fields = [
            "title",
            "slug",
            "category",
            "description",
            "upload_cover",
            "cover_image_url",
            "cover_public_id",
            "display_order",
            "is_published",
        ]

    def clean(self):
        cleaned_data = super().clean()
        upload_cover = cleaned_data.get("upload_cover")
        if upload_cover:
            existing_pid = self.instance.cover_public_id if self.instance.pk else ""
            result = upload_image_to_cloudinary(
                upload_cover,
                subfolder="gallery/covers",
                existing_public_id=existing_pid,
            )
            if not result.success:
                raise ValidationError({"upload_cover": result.error_message})
            cleaned_data["cover_image_url"] = result.secure_url
            cleaned_data["cover_public_id"] = result.public_id
        return cleaned_data
