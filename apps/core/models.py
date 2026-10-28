"""
Database models for Site Settings, Homepage content, and About Us content.
All content is editable via Django Admin without hardcoding fabricated facts.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """
    Singleton model storing global identity, homepage sections, About Us page text,
    and editable social/contact links for 100% HUMANITY.
    """
    site_name = models.CharField(
        _("Website Name"),
        max_length=120,
        default="100% HUMANITY",
    )
    tagline = models.CharField(
        _("Site Tagline"),
        max_length=255,
        default="Walking the Path of Buddha Dhamma: Equality, Compassion, Scientific Inquiry & Humanity",
    )
    hero_title = models.CharField(
        _("Homepage Hero Title"),
        max_length=200,
        default="Awakening Minds Through Buddha Dhamma, Compassion & Rational Inquiry",
    )
    hero_subtitle = models.TextField(
        _("Homepage Hero Subtitle"),
        default=(
            "100% HUMANITY is an educational initiative dedicated to sharing Gautama Buddha's "
            "teachings of pragmatic wisdom, universal equality, ethical conduct, mindfulness "
            "meditation, scientific temperament, and social awareness."
        ),
    )
    dhamma_intro_title = models.CharField(
        _("Buddha Dhamma Introduction Heading"),
        max_length=200,
        default="Understanding Buddha Dhamma as a Living Educational Path",
    )
    dhamma_intro_text = models.TextField(
        _("Buddha Dhamma Introduction Content"),
        default=(
            "Buddha Dhamma is grounded in direct observation, ethical responsibility (Sila), "
            "mental cultivation (Samadhi), and liberating wisdom (Panna). Rather than relying "
            "on blind dogma or superstition, the Dhamma invites every human being to examine "
            "experience rationally, practice non-discrimination, and cultivate boundless "
            "loving-kindness (Metta) and compassion (Karuna) for the welfare of society."
        ),
    )
    mission_statement = models.TextField(
        _("Mission Statement"),
        default=(
            "To foster accessible Dhamma education, ethical leadership, meditation practice, "
            "and scientific thinking across communities—empowering dedicated teachers and "
            "learners to live with dignity, equality, and compassion."
        ),
    )
    vision_statement = models.TextField(
        _("Vision Statement"),
        default=(
            "A compassionate, rational, and egalitarian society free from discrimination and "
            "superstition, guided by universal human values and the timeless wisdom of "
            "Gautama Buddha."
        ),
    )

    # About Us Page Editable Sections
    about_introduction = models.TextField(
        _("About Us — Organization Introduction"),
        default=(
            "100% HUMANITY is a community-focused educational initiative dedicated to studying, "
            "practicing, and sharing the teachings of Gautama Buddha. We focus on practical "
            "Dhamma education that uplifts individuals and strengthens social harmony through "
            "moral integrity, mindfulness, and rational inquiry."
        ),
    )
    about_purpose_of_dhamma = models.TextField(
        _("About Us — Purpose of Dhamma Education"),
        default=(
            "The purpose of Dhamma education is to cultivate clear understanding, ethical "
            "conduct, and emotional balance in daily life. By training capable, compassionate "
            "Dhamma teachers who communicate clearly in local languages, we help communities "
            "apply the Five Precepts, mindfulness meditation, and critical thinking to everyday challenges."
        ),
    )
    about_equality_compassion = models.TextField(
        _("About Us — Equality and Compassion"),
        default=(
            "Rooted in the egalitarian spirit of Gautama Buddha and the transformative historical "
            "insight of Dr. Babasaheb Ambedkar's Navayana movement, 100% HUMANITY affirms the "
            "equal dignity and worth of every person regardless of caste, gender, background, "
            "or status. True spirituality is measured by how humanely and justly we treat one another."
        ),
    )
    about_scientific_thinking = models.TextField(
        _("About Us — Scientific Thinking & Social Awareness"),
        default=(
            "Dhamma encourages questioning, verification through experience, and understanding "
            "cause and effect. We promote scientific temperament, digital literacy, and constructive "
            "social awareness so learners can reject superstition and contribute thoughtfully to community welfare."
        ),
    )
    about_educational_objectives = models.TextField(
        _("About Us — Educational Objectives (One per line)"),
        default=(
            "Develop well-trained, ethical Dhamma teachers grounded in the 15 foundational principles.\n"
            "Encourage regular mindfulness and vipassana-inspired meditation practice for mental clarity.\n"
            "Promote scientific thinking, rational inquiry, and freedom from superstition.\n"
            "Uphold human equality, non-discrimination, and compassionate community service.\n"
            "Provide accessible study materials, public talks, and multilingual learning in English, Marathi, and Hindi."
        ),
    )

    # Community Participation Section
    community_participation_title = models.CharField(
        _("Community Participation Heading"),
        max_length=200,
        default="Participate in Study Circles, Meditation & Dhamma Learning",
    )
    community_participation_text = models.TextField(
        _("Community Participation Text"),
        default=(
            "Whether you are beginning your study of Buddha Dhamma, practicing meditation, or "
            "preparing to serve as a community Dhamma teacher, we welcome your participation. "
            "Reach out to connect with upcoming study sessions, lectures, and educational resources."
        ),
    )

    # Contact & Identity Details (Strictly matching verified prompt details)
    contact_person = models.CharField(
        _("Contact Person"),
        max_length=120,
        default="Arvind Betkar",
    )
    contact_email = models.EmailField(
        _("Contact Email"),
        default="arvindbet12@gmail.com",
    )
    contact_phone = models.CharField(
        _("Contact Phone"),
        max_length=30,
        default="8983087210",
    )
    contact_address = models.TextField(
        _("Address / Location Note (Optional)"),
        blank=True,
        default="",
        help_text=_("Leave blank until an official physical address is provided. Do not fabricate addresses."),
    )

    # Social & External Links
    youtube_channel_name = models.CharField(
        _("YouTube Channel Name"),
        max_length=120,
        default="100% HUMANITY",
    )
    youtube_channel_url = models.URLField(
        _("YouTube Channel URL"),
        blank=True,
        default="",
        help_text=_("Paste the official 100% HUMANITY YouTube channel URL here when available."),
    )
    facebook_url = models.URLField(_("Facebook Page URL (Optional)"), blank=True, default="")
    instagram_url = models.URLField(_("Instagram URL (Optional)"), blank=True, default="")
    telegram_url = models.URLField(_("Telegram Group/Channel URL (Optional)"), blank=True, default="")

    # SEO Defaults
    meta_description = models.CharField(
        _("Default Meta Description"),
        max_length=300,
        default=(
            "100% HUMANITY — Educational initiative dedicated to Gautama Buddha's teachings, "
            "Buddha Dhamma, equality, compassion, meditation, scientific thinking, and social awareness."
        ),
    )
    footer_note = models.CharField(
        _("Footer Note"),
        max_length=255,
        default="Dedicated to Buddha Dhamma, Human Equality, Compassion, and Rational Inquiry.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Site Settings & Page Content")
        verbose_name_plural = _("Site Settings & Page Content")

    def __str__(self):
        return f"{self.site_name} — Global Configuration"

    def clean(self):
        if SiteSettings.objects.exclude(pk=self.pk).exists():
            raise ValidationError(_("Only one SiteSettings instance is permitted. Please edit the existing record."))

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @property
    def objectives_list(self):
        """Returns educational objectives split cleanly by line."""
        return [
            line.strip()
            for line in (self.about_educational_objectives or "").splitlines()
            if line.strip()
        ]

    @classmethod
    def get_solo(cls):
        """Returns the active SiteSettings record or initializes defaults safely."""
        try:
            obj, _ = cls.objects.get_or_create(
                pk=1,
                defaults={
                    "site_name": getattr(settings, "DEFAULT_SITE_NAME", "100% HUMANITY"),
                    "contact_person": getattr(settings, "DEFAULT_CONTACT_PERSON", "Arvind Betkar"),
                    "contact_email": getattr(settings, "DEFAULT_CONTACT_EMAIL", "arvindbet12@gmail.com"),
                    "contact_phone": getattr(settings, "DEFAULT_CONTACT_PHONE", "8983087210"),
                    "youtube_channel_name": getattr(settings, "DEFAULT_YOUTUBE_CHANNEL_NAME", "100% HUMANITY"),
                    "youtube_channel_url": getattr(settings, "DEFAULT_YOUTUBE_CHANNEL_URL", ""),
                },
            )
            return obj
        except Exception:
            # Fallback if database migrations have not run yet
            return cls(
                site_name=getattr(settings, "DEFAULT_SITE_NAME", "100% HUMANITY"),
                contact_person=getattr(settings, "DEFAULT_CONTACT_PERSON", "Arvind Betkar"),
                contact_email=getattr(settings, "DEFAULT_CONTACT_EMAIL", "arvindbet12@gmail.com"),
                contact_phone=getattr(settings, "DEFAULT_CONTACT_PHONE", "8983087210"),
                youtube_channel_name=getattr(settings, "DEFAULT_YOUTUBE_CHANNEL_NAME", "100% HUMANITY"),
                youtube_channel_url=getattr(settings, "DEFAULT_YOUTUBE_CHANNEL_URL", ""),
            )
