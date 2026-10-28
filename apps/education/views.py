from django.shortcuts import render
from apps.education.models import DhammaPrinciple, DEFAULT_DHAMMA_PRINCIPLES


def principle_list_view(request):
    """
    Displays all published Dhamma Education principles in ordered, accessible cards.
    Automatically seeds the 15 canonical principles if the database table is empty.
    """
    if not DhammaPrinciple.objects.exists():
        for item in DEFAULT_DHAMMA_PRINCIPLES:
            DhammaPrinciple.objects.get_or_create(
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

    principles = DhammaPrinciple.objects.filter(is_published=True).order_by(
        "display_order", "principle_number"
    )
    return render(
        request,
        "education/principle_list.html",
        {"principles": principles},
    )
