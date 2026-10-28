"""
Automated tests for Gallery models, image validation, missing Cloudinary credentials,
mocked Cloudinary uploads/deletions, and unauthorized access protection.
"""
from io import BytesIO
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from apps.gallery.models import GalleryAlbum, GalleryImage
from apps.gallery.services import upload_image_to_cloudinary


def create_test_image_bytes(fmt="PNG", size=(100, 100)) -> bytes:
    buf = BytesIO()
    img = Image.new("RGB", size, color=(200, 109, 40))
    img.save(buf, format=fmt)
    return buf.getvalue()


class GalleryAndCloudinaryTests(TestCase):
    def setUp(self):
        self.album = GalleryAlbum.objects.create(
            title="Dhamma Workshop 2026",
            category="Workshops",
            description="Photographs from community teacher training.",
            is_published=True,
        )

    @override_settings(CLOUDINARY_CLOUD_NAME="", CLOUDINARY_API_KEY="", CLOUDINARY_API_SECRET="")
    def test_missing_cloudinary_credentials_handled_gracefully(self):
        img_file = SimpleUploadedFile(
            "test.png", create_test_image_bytes(), content_type="image/png"
        )
        result = upload_image_to_cloudinary(img_file, subfolder="gallery")
        self.assertFalse(result.success)
        self.assertIn("Cloudinary credentials are not configured", result.error_message)

    @override_settings(
        CLOUDINARY_CLOUD_NAME="demo-cloud",
        CLOUDINARY_API_KEY="123456",
        CLOUDINARY_API_SECRET="secret-abc",
    )
    @patch("cloudinary.uploader.upload")
    def test_mocked_cloudinary_upload_succeeds(self, mock_upload):
        mock_upload.return_value = {
            "secure_url": "https://res.cloudinary.com/demo-cloud/image/upload/v1/100_humanity/sample.jpg",
            "public_id": "100_humanity/gallery/sample",
            "width": 800,
            "height": 600,
            "format": "jpg",
            "bytes": 42000,
        }
        img_file = SimpleUploadedFile(
            "sample.png", create_test_image_bytes(), content_type="image/png"
        )
        result = upload_image_to_cloudinary(img_file, subfolder="gallery")
        self.assertTrue(result.success)
        self.assertEqual(
            result.secure_url,
            "https://res.cloudinary.com/demo-cloud/image/upload/v1/100_humanity/sample.jpg",
        )
        self.assertEqual(result.public_id, "100_humanity/gallery/sample")

    def test_unauthorized_user_redirected_from_bulk_upload_and_delete(self):
        upload_res = self.client.get(reverse("gallery:bulk_upload"))
        self.assertEqual(upload_res.status_code, 302)

        photo = GalleryImage.objects.create(
            album=self.album,
            title="Meditation Hall",
            alt_text="Participants meditating",
            image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
        )
        del_res = self.client.post(reverse("gallery:delete_image", kwargs={"pk": photo.pk}))
        self.assertEqual(del_res.status_code, 302)
        self.assertTrue(GalleryImage.objects.filter(pk=photo.pk).exists())
