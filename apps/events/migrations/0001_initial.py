import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220, verbose_name="Event Title")),
                ("slug", models.SlugField(max_length=240, unique=True, verbose_name="URL Slug")),
                ("description", models.TextField(verbose_name="Event Description & Program Details")),
                ("start_date", models.DateField(db_index=True, verbose_name="Start Date")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="End Date")),
                ("start_time", models.TimeField(blank=True, null=True, verbose_name="Start Time")),
                ("end_time", models.TimeField(blank=True, null=True, verbose_name="End Time")),
                ("venue", models.CharField(max_length=255, verbose_name="Venue / Location")),
                ("map_link", models.URLField(blank=True, default="", help_text="Optional Google Maps or OpenStreetMap URL for directions.", max_length=500, verbose_name="Optional Map Link")),
                ("cover_image_url", models.URLField(blank=True, default="", help_text="Populated automatically via Cloudinary upload or optional HTTPS image URL.", max_length=500, verbose_name="Cover Photograph URL")),
                ("cover_public_id", models.CharField(blank=True, default="", max_length=255, verbose_name="Cloudinary Cover Public ID")),
                ("registration_info", models.TextField(blank=True, default="Free and open to all. Contact Arvind Betkar (8983087210 / arvindbet12@gmail.com) for inquiries.", help_text="No paid ticketing is used. Provide free participation or inquiry details.", verbose_name="Registration or Contact Information")),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("PUBLISHED", "Published")], db_index=True, default="DRAFT", max_length=15, verbose_name="Publication Status")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["start_date", "start_time"],
                "indexes": [models.Index(fields=["status", "start_date"], name="events_even_status_dfba18_idx")],
            },
        ),
        migrations.CreateModel(
            name="EventImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("caption", models.CharField(blank=True, default="", max_length=200, verbose_name="Caption")),
                ("alt_text", models.CharField(max_length=220, verbose_name="Accessible Alt Text")),
                ("image_url", models.URLField(max_length=500, verbose_name="Photograph Secure URL")),
                ("cloudinary_public_id", models.CharField(blank=True, default="", max_length=255, verbose_name="Cloudinary Public ID")),
                ("display_order", models.PositiveSmallIntegerField(default=1, verbose_name="Display Order")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="additional_images", to="events.event", verbose_name="Event")),
            ],
            options={
                "verbose_name": "Additional Event Photograph",
                "verbose_name_plural": "Additional Event Photographs",
                "ordering": ["display_order", "created_at"],
            },
        ),
    ]
