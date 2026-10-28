from django.contrib import admin
from apps.education.models import DhammaPrinciple


@admin.register(DhammaPrinciple)
class DhammaPrincipleAdmin(admin.ModelAdmin):
    list_display = (
        "principle_number",
        "title",
        "display_order",
        "is_featured",
        "is_published",
        "updated_at",
    )
    list_editable = ("display_order", "is_featured", "is_published")
    list_filter = ("is_published", "is_featured")
    search_fields = ("title", "summary", "detailed_explanation", "practical_guidance")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order", "principle_number")
