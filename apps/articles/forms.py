from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.articles.models import Article
from apps.core.validators import validate_image_file
from apps.gallery.services import upload_image_to_cloudinary


class ArticleAdminForm(forms.ModelForm):
    upload_cover = forms.ImageField(
        label=_("Upload / Replace Cover Image via Cloudinary"),
        required=False,
        validators=[validate_image_file],
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "author_name",
            "category",
            "tags",
            "status",
            "published_at",
            "summary",
            "content",
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
                subfolder="articles/covers",
                existing_public_id=existing_pid,
            )
            if not res.success:
                raise ValidationError({"upload_cover": res.error_message})
            cleaned_data["cover_image_url"] = res.secure_url
            cleaned_data["cover_public_id"] = res.public_id
        return cleaned_data
