"""
Management command to initialize SiteSettings, 15 Dhamma Teacher Principles,
and default demonstration Events, Albums, Videos, and Articles.
Safe and idempotent: runs during deployment or local setup without overwriting user edits.
"""
import os
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import SiteSettings, EnvironmentSetting
from apps.education.models import DhammaPrinciple, DEFAULT_DHAMMA_PRINCIPLES
from apps.events.models import Event
from apps.gallery.models import GalleryAlbum, GalleryImage
from apps.videos.models import Video, VideoCategory
from apps.articles.models import Article, ArticleCategory


class Command(BaseCommand):
    help = "Seeds initial SiteSettings, 15 Dhamma principles, events, albums, videos, and articles."

    def handle(self, *args, **options):
        today = timezone.localdate()

        # 1. SiteSettings & EnvironmentSetting
        site_settings = SiteSettings.get_solo()
        env_settings = EnvironmentSetting.get_solo()
        self.stdout.write(self.style.SUCCESS(f"Verified SiteSettings for '{site_settings.site_name}'."))
        self.stdout.write(self.style.SUCCESS("Verified Environment & API settings."))

        # 2. Dhamma Principles
        created_count = 0
        for item in DEFAULT_DHAMMA_PRINCIPLES:
            _, created = DhammaPrinciple.objects.get_or_create(
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
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Dhamma Principles check complete: {created_count} newly created, "
                f"{DhammaPrinciple.objects.count()} total in database."
            )
        )

        # 3. Events (if none exist)
        if Event.objects.count() == 0:
            Event.objects.create(
                title="Workshop on 15 Principles for Developing Dhamma Teachers",
                description=(
                    "An intensive community seminar led by Arvind Betkar exploring the 15 foundational "
                    "principles for community Dhamma educators, covering the Four Noble Truths, "
                    "scientific inquiry, public speaking, and teaching in local languages."
                ),
                start_date=today + timedelta(days=14),
                venue="Community Study Center, Maharashtra",
                status=Event.Status.PUBLISHED,
                cover_image_url="https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=1200&auto=format&fit=crop",
            )
            Event.objects.create(
                title="Sunday Anapanasati Mindfulness and Metta Meditation Session",
                description=(
                    "Guided breath awareness (Anapanasati) and loving-kindness (Metta) practice "
                    "open to all beginners and families, followed by interactive Q&A on practical "
                    "stress reduction and ethical mindfulness in daily life."
                ),
                start_date=today + timedelta(days=21),
                venue="Peace Pavilion Hall, Maharashtra",
                status=Event.Status.PUBLISHED,
                cover_image_url="https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1200&auto=format&fit=crop",
            )
            Event.objects.create(
                title="Youth Educational Book Share & Equality Awareness Drive",
                description=(
                    "Community book distribution, student notebook support, and open dialogue on "
                    "human dignity, liberty, equality, fraternity, and rational scientific inquiry."
                ),
                start_date=today + timedelta(days=28),
                venue="Ambedkar Nagar Community Courtyard, Maharashtra",
                status=Event.Status.PUBLISHED,
                cover_image_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=1200&auto=format&fit=crop",
            )
            self.stdout.write(self.style.SUCCESS("Seeded 3 sample community events."))

        # 4. Photo Gallery Albums and Images (if none exist)
        if GalleryAlbum.objects.count() == 0:
            alb1 = GalleryAlbum.objects.create(
                title="Community Dhamma Educator Seminar Album",
                category="Education & Workshops",
                description="Photographs from our community study circle, note-taking sessions, and interactive discussions.",
                is_published=True,
                cover_image_url="https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=1200&auto=format&fit=crop",
            )
            GalleryImage.objects.create(
                album=alb1,
                title="Study Circle Participants",
                alt_text="Participants seated studying Dhamma texts together",
                caption="Community study circle taking notes during the 15 Principles seminar.",
                image_url="https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=1200&auto=format&fit=crop",
                is_published=True,
                display_order=1,
            )
            GalleryImage.objects.create(
                album=alb1,
                title="Bodhi Reflection Courtyard",
                alt_text="Morning reflection courtyard prior to session",
                caption="Morning reflection courtyard and pavilion prior to opening session.",
                image_url="https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?q=80&w=1200&auto=format&fit=crop",
                is_published=True,
                display_order=2,
            )

            alb2 = GalleryAlbum.objects.create(
                title="Mindfulness & Youth Book-Sharing Initiative",
                category="Community Service",
                description="Highlights from our weekend meditation preparation and educational book distribution drive.",
                is_published=True,
                cover_image_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=1200&auto=format&fit=crop",
            )
            GalleryImage.objects.create(
                album=alb2,
                title="Educational Book Share Drive",
                alt_text="Students browsing free educational books in community courtyard",
                caption="Students and families browsing free educational books and study notebooks.",
                image_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=1200&auto=format&fit=crop",
                is_published=True,
                display_order=1,
            )
            GalleryImage.objects.create(
                album=alb2,
                title="Meditation Hall Setup",
                alt_text="Meditation hall prepared for Anapanasati mindfulness practice",
                caption="Quiet meditation hall arranged for the weekly Anapanasati practice.",
                image_url="https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1200&auto=format&fit=crop",
                is_published=True,
                display_order=2,
            )
            self.stdout.write(self.style.SUCCESS("Seeded 2 photo albums with 4 sample photographs."))

        # 5. YouTube Videos (if none exist)
        if Video.objects.count() == 0:
            cat_talks, _ = VideoCategory.objects.get_or_create(
                name="Dhamma Talks & Philosophy",
                defaults={"description": "Lectures on Buddha Dhamma, the Noble Eightfold Path, and ethics."}
            )
            cat_med, _ = VideoCategory.objects.get_or_create(
                name="Mindfulness & Meditation",
                defaults={"description": "Practical meditation instruction and mental cultivation."}
            )

            Video.objects.create(
                title="Introduction to the Noble Eightfold Path & Practical Ethics",
                description="An accessible overview of Right View, Right Intention, Right Speech, and Right Action in daily life.",
                youtube_url="https://www.youtube.com/watch?v=M7lc1UVf-VE",
                category=cat_talks,
                is_featured=True,
                is_published=True,
                display_order=1,
            )
            Video.objects.create(
                title="Guided Mindfulness Practice & Scientific Inquiry in Daily Life",
                description="Practical Anapanasati breath awareness and cultivating rational inquiry free from superstition.",
                youtube_url="https://www.youtube.com/watch?v=aqz-KE-bpKQ",
                category=cat_med,
                is_featured=True,
                is_published=True,
                display_order=2,
            )
            self.stdout.write(self.style.SUCCESS("Seeded 2 sample YouTube videos."))

        # 6. Articles & Categories (if none exist)
        if Article.objects.count() == 0:
            cat_edu, _ = ArticleCategory.objects.get_or_create(
                name="Dhamma Education",
                defaults={"description": "Core pedagogical guides and foundational principles."}
            )
            cat_soc, _ = ArticleCategory.objects.get_or_create(
                name="Equality & Social Awareness",
                defaults={"description": "Essays on human dignity, Navayana Buddhism, and Dr. Ambedkar."}
            )

            Article.objects.create(
                title="Understanding Pancasila: How the Five Precepts Foster Social Harmony",
                author_name="Arvind Betkar",
                category=cat_edu,
                tags="Pancasila, Ethics, Non-violence, Daily Life",
                summary="An accessible study guide on how voluntary ethical commitments—non-harming, honesty, respectful relationships, truthful speech, and mental clarity—strengthen families and communities.",
                content=(
                    "In Buddha Dhamma, ethics (Sila) is not a list of arbitrary commandments imposed by fear, but a conscious training undertaken for the welfare and happiness of oneself and society (Bahujana hitaya, bahujana sukhaya).\n\n"
                    "1. Reverence for Life and Non-Violence\n"
                    "Practising abstention from harming living beings cultivates active compassion (Karuna) and peaceful conflict resolution within neighborhoods.\n\n"
                    "2. Honesty, Truthful Speech, and Mental Clarity\n"
                    "When individuals commit to truthful communication and avoid intoxicants that cloud judgment, families experience greater trust, financial stability, and educational progress."
                ),
                cover_image_url="https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=1200&auto=format&fit=crop",
                status=Article.Status.PUBLISHED,
            )
            Article.objects.create(
                title="बुद्ध धम्म आणि वैज्ञानिक दृष्टिकोन: दैनंदिन जीवनातील महत्त्व",
                author_name="Arvind Betkar",
                category=cat_soc,
                tags="मराठी, वैज्ञानिक दृष्टिकोन, समता, प्रज्ञा",
                summary="बुद्ध धम्मातील प्रज्ञा, शील, करुणा आणि चिकित्सक विचारांचे (कालाम सुत्त) आपल्या दैनंदिन कौटुंबिक व सामाजिक जीवनातील व्यावहारिक महत्त्व.",
                content=(
                    "तथागत गौतम बुद्धांनी मानवी जीवनातील दुःखाचे मूळ शोधताना अंधश्रद्धा किंवा दैववाद नाकारून कार्यकारणभावाचा (प्रतीत्यसमुत्पाद) सिद्धांत मांडला.\n\n"
                    "चिकित्सक विचार आणि समता:\n"
                    "कोणतीही गोष्ट केवळ परंपरेने चालत आली आहे म्हणून न स्वीकारता, ती विज्ञानाच्या, तर्कशास्त्राच्या आणि मानवकल्याणाच्या कसोटीवर तपासून पाहण्याची शिकवण बुद्ध धम्म देतो. डॉ. बाबासाहेब आंबेडकरांनी देखील धम्माचा हाच वैज्ञानिक व समतावादी दृष्टिकोन समाजापुढे ठेवला."
                ),
                cover_image_url="https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?q=80&w=1200&auto=format&fit=crop",
                status=Article.Status.PUBLISHED,
            )
            Article.objects.create(
                title="डॉ. बाबासाहेब आंबेडकर और नवयान बौद्ध परंपरा में समता एवं बंधुता",
                author_name="Arvind Betkar",
                category=cat_soc,
                tags="हिन्दी, नवयान, समता, मैत्री",
                summary="स्वतंत्रता, समता, बंधुता (मैत्री) और मानवीय गरिमा के संवर्धन में बुद्ध धम्म और नवयान परंपरा की ऐतिहासिक भूमिका का अध्ययन।",
                content=(
                    "बुद्ध धम्म के केंद्र में मनुष्य का नैतिक उत्थान और समाज में समता की स्थापना है।\n\n"
                    "समता और मैत्री (Fraternity):\n"
                    "जातिगत भेदभाव और अस्पृश्यता का विरोध करते हुए बुद्ध धम्म प्रत्येक व्यक्ति की गरिमा और समानता को स्थापित करता है। शिक्षा, करुणा और वैज्ञानिक चिंतन के माध्यम से एक प्रबुद्ध समाज का निर्माण ही 100% HUMANITY का उद्देश्य है।"
                ),
                cover_image_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=1200&auto=format&fit=crop",
                status=Article.Status.PUBLISHED,
            )
            self.stdout.write(self.style.SUCCESS("Seeded 3 multilingual articles."))

        # 7. Optional Superuser Provisioning from Environment Variables
        admin_user = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        admin_pass = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()
        admin_email = os.environ.get("DJANGO_SUPERUSER_EMAIL", site_settings.contact_email or "admin@100humanity.org").strip()

        if admin_user and admin_pass:
            User = get_user_model()
            if not User.objects.filter(username=admin_user).exists():
                User.objects.create_superuser(
                    username=admin_user,
                    email=admin_email,
                    password=admin_pass,
                )
                self.stdout.write(self.style.SUCCESS(f"Provisioned superuser '{admin_user}'."))
            else:
                self.stdout.write(self.style.NOTICE(f"Superuser '{admin_user}' already exists."))
