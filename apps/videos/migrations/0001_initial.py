import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VideoCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Category Name")),
                ("slug", models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")),
                ("description", models.TextField(blank=True, default="", verbose_name="Description")),
                ("display_order", models.PositiveSmallIntegerField(default=1, verbose_name="Display Order")),
            ],
            options={
                "verbose_name": "Video Category",
                "verbose_name_plural": "Video Categories",
                "ordering": ["display_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220, verbose_name="Video Title")),
                ("slug", models.SlugField(max_length=240, unique=True, verbose_name="URL Slug")),
                ("description", models.TextField(blank=True, default="", verbose_name="Video Description & Key Takeaways")),
                ("youtube_url", models.URLField(help_text="Paste a standard watch link (https://www.youtube.com/watch?v=...), short link (https://youtu.be/...), or Shorts link (https://www.youtube.com/shorts/...).", max_length=500, verbose_name="YouTube URL")),
                ("video_id", models.CharField(db_index=True, editable=False, max_length=20, verbose_name="Extracted YouTube Video ID")),
                ("thumbnail_url", models.URLField(blank=True, default="", help_text="Leave blank to automatically use the high-resolution YouTube thumbnail.", max_length=500, verbose_name="Optional Custom Thumbnail URL")),
                ("is_featured", models.BooleanField(db_index=True, default=False, verbose_name="Featured on Homepage")),
                ("is_published", models.BooleanField(db_index=True, default=True, verbose_name="Published")),
                ("display_order", models.PositiveSmallIntegerField(db_index=True, default=1, verbose_name="Display Order")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="videos", to="videos.videocategory", verbose_name="Category")),
            ],
            options={
                "verbose_name": "YouTube Video",
                "verbose_name_plural": "YouTube Videos",
                "ordering": ["display_order", "-created_at"],
                "indexes": [models.Index(fields=["is_published", "display_order"], name="videos_vide_is_publ_419a7e_idx")],
            },
        ),
    ]
