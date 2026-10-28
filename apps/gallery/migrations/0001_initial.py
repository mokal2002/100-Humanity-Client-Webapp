import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GalleryAlbum",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Album Title")),
                ("slug", models.SlugField(max_length=220, unique=True, verbose_name="URL Slug")),
                ("category", models.CharField(db_index=True, default="Community & Dhamma Events", help_text="E.g., Dhamma Workshops, Meditation Sessions, Community Service, Study Circles.", max_length=100, verbose_name="Category")),
                ("description", models.TextField(blank=True, default="", verbose_name="Album Description")),
                ("cover_image_url", models.URLField(blank=True, default="", help_text="Populated automatically via Cloudinary upload or optional cover image URL.", max_length=500, verbose_name="Cover Image Secure URL")),
                ("cover_public_id", models.CharField(blank=True, default="", max_length=255, verbose_name="Cloudinary Cover Public ID")),
                ("display_order", models.PositiveSmallIntegerField(db_index=True, default=1, verbose_name="Display Order")),
                ("is_published", models.BooleanField(db_index=True, default=True, verbose_name="Published")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Gallery Album",
                "verbose_name_plural": "Gallery Albums",
                "ordering": ["display_order", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="GalleryImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Photo Title / Caption")),
                ("alt_text", models.CharField(help_text="Descriptive text for screen readers and accessibility (required).", max_length=220, verbose_name="Accessible Alt Text")),
                ("caption", models.TextField(blank=True, default="", verbose_name="Detailed Caption (Optional)")),
                ("image_url", models.URLField(help_text="HTTPS URL returned by Cloudinary (or verified image URL).", max_length=500, verbose_name="Cloudinary Secure URL")),
                ("cloudinary_public_id", models.CharField(blank=True, db_index=True, default="", help_text="Stored automatically when uploaded via Cloudinary so replacements/deletions clean up storage.", max_length=255, verbose_name="Cloudinary Public ID")),
                ("width", models.PositiveIntegerField(blank=True, null=True, verbose_name="Width (px)")),
                ("height", models.PositiveIntegerField(blank=True, null=True, verbose_name="Height (px)")),
                ("display_order", models.PositiveSmallIntegerField(db_index=True, default=1, verbose_name="Display Order")),
                ("is_published", models.BooleanField(db_index=True, default=True, verbose_name="Published")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("album", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="gallery.galleryalbum", verbose_name="Album")),
            ],
            options={
                "verbose_name": "Gallery Photograph",
                "verbose_name_plural": "Gallery Photographs",
                "ordering": ["display_order", "-created_at"],
                "indexes": [models.Index(fields=["is_published", "-created_at"], name="gallery_gal_is_publ_84a201_idx")],
            },
        ),
    ]
