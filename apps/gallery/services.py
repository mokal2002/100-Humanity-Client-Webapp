"""
Official Cloudinary SDK wrapper for server-side image uploads, replacements, and deletions.
Ensures API secrets never reach the browser, validates files strictly, and handles missing
credentials or quota errors gracefully without crashing the application.
"""
import logging
from dataclasses import dataclass
from typing import Optional
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.core.validators import validate_image_file

logger = logging.getLogger(__name__)


@dataclass
class CloudinaryUploadResult:
    success: bool
    secure_url: str = ""
    public_id: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    format: str = ""
    bytes_size: Optional[int] = None
    error_message: str = ""


def is_cloudinary_ready() -> bool:
    """Returns True if Cloudinary credentials are configured in settings/environment."""
    return bool(
        getattr(settings, "CLOUDINARY_CLOUD_NAME", "")
        and getattr(settings, "CLOUDINARY_API_KEY", "")
        and getattr(settings, "CLOUDINARY_API_SECRET", "")
    )


def upload_image_to_cloudinary(
    file_obj,
    subfolder: str = "gallery",
    existing_public_id: str = "",
) -> CloudinaryUploadResult:
    """
    Validates and uploads an image file to Cloudinary using the official Python SDK.
    If `existing_public_id` is provided, replaces/overwrites or cleans up the previous image.
    """
    try:
        validate_image_file(file_obj)
    except ValidationError as exc:
        msg = "; ".join(exc.messages) if hasattr(exc, "messages") else str(exc)
        return CloudinaryUploadResult(success=False, error_message=msg)

    if not is_cloudinary_ready():
        return CloudinaryUploadResult(
            success=False,
            error_message=(
                "Cloudinary credentials are not configured. Please set CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in your environment (.env), "
                "or paste an external image URL directly."
            ),
        )

    try:
        import cloudinary
        import cloudinary.uploader

        # Ensure SDK config is synced with current Django settings
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

        base_folder = getattr(settings, "CLOUDINARY_FOLDER", "100_humanity").strip("/")
        target_folder = f"{base_folder}/{subfolder.strip('/')}" if subfolder else base_folder

        if hasattr(file_obj, "seek"):
            file_obj.seek(0)

        upload_options = {
            "folder": target_folder,
            "resource_type": "image",
            "overwrite": True,
            "unique_filename": True,
            "AllowedFormats": ["jpg", "jpeg", "png", "webp"],
            "transformation": [
                {"quality": "auto:good", "fetch_format": "auto"}
            ],
        }

        response = cloudinary.uploader.upload(file_obj, **upload_options)
        secure_url = response.get("secure_url", "")
        new_public_id = response.get("public_id", "")

        if not secure_url or not new_public_id:
            return CloudinaryUploadResult(
                success=False,
                error_message="Cloudinary did not return a valid secure URL or public ID.",
            )

        # If replacing an earlier image, delete the old public_id safely
        if existing_public_id and existing_public_id != new_public_id:
            delete_image_from_cloudinary(existing_public_id)

        return CloudinaryUploadResult(
            success=True,
            secure_url=secure_url,
            public_id=new_public_id,
            width=response.get("width"),
            height=response.get("height"),
            format=response.get("format", ""),
            bytes_size=response.get("bytes"),
        )
    except Exception as exc:
        logger.warning("Cloudinary upload failed: %s", exc)
        return CloudinaryUploadResult(
            success=False,
            error_message=(
                f"Cloudinary upload could not be completed ({exc.__class__.__name__}: {exc}). "
                "Please check your network connection, Cloudinary credentials, or free-tier credit quota."
            ),
        )


def delete_image_from_cloudinary(public_id: str) -> bool:
    """
    Safely deletes an image asset from Cloudinary by its public_id.
    Never raises an unhandled exception if credentials are missing or network fails.
    """
    if not public_id or not is_cloudinary_ready():
        return False

    try:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        result = cloudinary.uploader.destroy(public_id, invalidate=True, resource_type="image")
        return result.get("result") in ("ok", "not found")
    except Exception as exc:
        logger.warning("Failed to delete Cloudinary asset %s: %s", public_id, exc)
        return False
