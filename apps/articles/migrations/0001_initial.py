import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ArticleCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Category Name")),
                ("slug", models.SlugField(max_length=120, unique=True, verbose_name="URL Slug")),
                ("description", models.TextField(blank=True, default="", verbose_name="Category Description")),
            ],
            options={
                "verbose_name": "Article Category",
                "verbose_name_plural": "Article Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=240, verbose_name="Article Title")),
                ("slug", models.SlugField(max_length=255, unique=True, verbose_name="URL Slug")),
                ("author_name", models.CharField(default="Arvind Betkar", max_length=120, verbose_name="Author Name")),
                ("tags", models.CharField(blank=True, default="Buddha Dhamma, Equality, Compassion, Meditation", help_text="Comma-separated topics, e.g.: Buddha Dhamma, Meditation, Panchsheel, Rational Inquiry", max_length=250, verbose_name="Tags (Comma-separated)")),
                ("summary", models.TextField(help_text="Brief summary shown on article cards and search results.", max_length=500, verbose_name="Article Summary / Excerpt")),
                ("content", models.TextField(help_text="Write plain text paragraphs separated by blank lines. Rendered safely using Django's auto-escaping and linebreaks filter (no unsafe raw HTML execution).", verbose_name="Full Article Content")),
                ("cover_image_url", models.URLField(blank=True, default="", max_length=500, verbose_name="Cover Image Secure URL")),
                ("cover_public_id", models.CharField(blank=True, default="", max_length=255, verbose_name="Cloudinary Cover Public ID")),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("PUBLISHED", "Published")], db_index=True, default="DRAFT", max_length=15, verbose_name="Publication Status")),
                ("published_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name="Publication Date")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="articles", to="articles.articlecategory", verbose_name="Category")),
            ],
            options={
                "verbose_name": "Educational Article",
                "verbose_name_plural": "Educational Articles",
                "ordering": ["-published_at", "-created_at"],
                "indexes": [models.Index(fields=["status", "-published_at"], name="articles_ar_status_35f520_idx")],
            },
        ),
    ]
