from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactSubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120, verbose_name="Your Full Name")),
                ("email", models.EmailField(max_length=254, verbose_name="Email Address")),
                ("phone", models.CharField(blank=True, default="", max_length=30, verbose_name="Phone Number (Optional)")),
                ("subject", models.CharField(blank=True, default="", max_length=200, verbose_name="Subject (Optional)")),
                ("message", models.TextField(verbose_name="Message")),
                ("status", models.CharField(choices=[("NEW", "New"), ("IN_PROGRESS", "In Progress"), ("RESOLVED", "Resolved")], db_index=True, default="NEW", max_length=20, verbose_name="Workflow Status")),
                ("admin_notes", models.TextField(blank=True, default="", help_text="Private notes visible only to authorized administrators.", verbose_name="Internal Admin Notes")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Submitted At")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Contact Submission",
                "verbose_name_plural": "Contact Submissions",
                "ordering": ["-created_at"],
                "indexes": [models.Index(fields=["status", "-created_at"], name="contact_con_status_57795b_idx")],
            },
        ),
    ]
