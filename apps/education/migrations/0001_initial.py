from django.db import migrations, models


def seed_15_principles(apps, schema_editor):
    DhammaPrinciple = apps.get_model("education", "DhammaPrinciple")
    from apps.education.models import DEFAULT_DHAMMA_PRINCIPLES

    for item in DEFAULT_DHAMMA_PRINCIPLES:
        DhammaPrinciple.objects.update_or_create(
            principle_number=item["principle_number"],
            defaults={
                "title": item["title"],
                "slug": item["slug"],
                "summary": item["summary"],
                "detailed_explanation": item["detailed_explanation"],
                "practical_guidance": item["practical_guidance"],
                "learning_resources": item["learning_resources"],
                "display_order": item["principle_number"],
                "is_featured": item["is_featured"],
                "is_published": True,
            },
        )


def unseed_15_principles(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DhammaPrinciple",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("principle_number", models.PositiveSmallIntegerField(help_text="Canonical principle number (1 to 15+).", unique=True, verbose_name="Principle Number")),
                ("title", models.CharField(max_length=220, verbose_name="Principle Title")),
                ("slug", models.SlugField(max_length=240, unique=True, verbose_name="URL Slug")),
                ("summary", models.TextField(help_text="Concise 1-2 sentence overview shown on cards.", verbose_name="Brief Summary")),
                ("detailed_explanation", models.TextField(help_text="Full educational explanation of why this principle matters.", verbose_name="Detailed Explanation")),
                ("practical_guidance", models.TextField(blank=True, default="", help_text="Actionable steps for practicing and applying this principle.", verbose_name="Practical Application for Teachers")),
                ("learning_resources", models.TextField(blank=True, default="", help_text="Optional study topics, books, or workshop references.", verbose_name="Recommended Learning Resources (Optional)")),
                ("display_order", models.PositiveSmallIntegerField(db_index=True, default=1, help_text="Controls ordering on the Dhamma Education page (lowest number first).", verbose_name="Display Order")),
                ("is_featured", models.BooleanField(db_index=True, default=False, verbose_name="Feature on Homepage")),
                ("is_published", models.BooleanField(db_index=True, default=True, verbose_name="Published")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Dhamma Education Principle",
                "verbose_name_plural": "Dhamma Education Principles",
                "ordering": ["display_order", "principle_number"],
                "indexes": [models.Index(fields=["is_published", "display_order"], name="education_d_is_publ_61b184_idx")],
            },
        ),
        migrations.RunPython(seed_15_principles, unseed_15_principles),
    ]
