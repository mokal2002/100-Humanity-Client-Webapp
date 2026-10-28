"""Shared security and media validators for images and URLs."""
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_file(file_obj):
    """
    Validates uploaded image file extension, size, and integrity using Pillow.
    Prevents malicious script uploads and oversized files that could exhaust free quotas.
    """
    if not file_obj:
        return

    # 1. File size check
    max_bytes = getattr(settings, "MAX_IMAGE_UPLOAD_BYTES", 5 * 1024 * 1024)
    if hasattr(file_obj, "size") and file_obj.size > max_bytes:
        max_mb = max_bytes / (1024 * 1024)
        raise ValidationError(
            _("Image file size cannot exceed %(max_mb).1f MB.") % {"max_mb": max_mb}
        )

    # 2. File extension check
    ext = os.path.splitext(getattr(file_obj, "name", ""))[1].lower()
    allowed_exts = getattr(
        settings, "ALLOWED_IMAGE_EXTENSIONS", {".jpg", ".jpeg", ".png", ".webp"}
    )
    if ext not in allowed_exts:
        raise ValidationError(
            _("Unsupported file extension '%(ext)s'. Allowed formats: JPG, JPEG, PNG, WEBP.")
            % {"ext": ext}
        )

    # 3. Content-Type check if available on uploaded file
    content_type = getattr(file_obj, "content_type", None)
    allowed_mimes = getattr(
        settings, "ALLOWED_IMAGE_MIME_TYPES", {"image/jpeg", "image/png", "image/webp"}
    )
    if content_type and content_type not in allowed_mimes:
        raise ValidationError(
            _("Invalid image MIME type '%(mime)s'. Please upload a valid JPEG, PNG, or WEBP image.")
            % {"mime": content_type}
        )

    # 4. Pillow image header verification
    try:
        from PIL import Image
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        img = Image.open(file_obj)
        img.verify()
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
    except ImportError:
        pass
    except Exception as exc:
        raise ValidationError(
            _("The uploaded file is not a valid or uncorrupted image.")
        ) from exc
