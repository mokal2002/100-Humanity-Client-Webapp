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

    # SEO & Analytics Defaults
    meta_description = models.CharField(
        _("Default Meta Description"),
        max_length=300,
        default=(
            "100% HUMANITY — Educational initiative dedicated to Gautama Buddha's teachings, "
            "Buddha Dhamma, equality, compassion, meditation, scientific thinking, and social awareness."
        ),
    )
    google_analytics_id = models.CharField(
        _("Google Analytics Measurement ID (GA4)"),
        max_length=30,
        blank=True,
        default="G-QRLSPJ2R6J",
        help_text=_(
            "Your Google Analytics 4 Measurement ID starting with 'G-' (e.g. G-XXXXXXXXXX). "
            "Leave blank if not using Google Analytics."
        ),
    )
    google_site_verification = models.CharField(
        _("Google Search Console Verification Token / Tag"),
        max_length=150,
        blank=True,
        default="",
        help_text=_(
            "Paste your Google Search Console verification token or full meta tag "
            "(e.g. 'abc123xyz' or <meta name='google-site-verification' content='...' />)."
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
    def clean_google_site_verification(self):
        """Extracts the verification token cleanly if the user pasted the entire HTML tag."""
        val = (self.google_site_verification or "").strip()
        if 'content="' in val:
            try:
                return val.split('content="')[1].split('"')[0].strip()
            except Exception:
                pass
        if "content='" in val:
            try:
                return val.split("content='")[1].split("'")[0].strip()
            except Exception:
                pass
        return val

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


class EnvironmentSetting(models.Model):
    """
    Singleton model for managing system environment variables, API keys,
    and database connection strings directly from Django Admin without backend shell access.
    Automatically synchronizes with runtime settings and the .env file.
    """
    database_url = models.CharField(
        _("Database Connection URL (DATABASE_URL)"),
        max_length=500,
        blank=True,
        default="",
        help_text=_(
            "PostgreSQL connection URL (e.g. Neon, Supabase, Railway). "
            "Leave blank to use local SQLite (db.sqlite3)."
        ),
    )

    # Cloudinary Image Storage
    cloudinary_cloud_name = models.CharField(
        _("Cloudinary Cloud Name"),
        max_length=120,
        blank=True,
        default="",
        help_text=_("From your Cloudinary dashboard: https://console.cloudinary.com/"),
    )
    cloudinary_api_key = models.CharField(
        _("Cloudinary API Key"),
        max_length=120,
        blank=True,
        default="",
    )
    cloudinary_api_secret = models.CharField(
        _("Cloudinary API Secret"),
        max_length=150,
        blank=True,
        default="",
    )
    cloudinary_folder = models.CharField(
        _("Cloudinary Upload Folder"),
        max_length=100,
        default="100_humanity",
        help_text=_("Folder name in Cloudinary where photos will be organized."),
    )

    # YouTube API / Integration
    youtube_api_key = models.CharField(
        _("YouTube API Key (Optional)"),
        max_length=150,
        blank=True,
        default="",
        help_text=_("Google Cloud YouTube Data API v3 key if automated playlist fetching is needed."),
    )

    # Django Core Security & Hosts
    secret_key = models.CharField(
        _("Django Secret Key (SECRET_KEY)"),
        max_length=255,
        blank=True,
        default="",
        help_text=_("Cryptographic signing key. Leave blank to preserve current key."),
    )
    allowed_hosts = models.CharField(
        _("Allowed Hosts (ALLOWED_HOSTS)"),
        max_length=500,
        default="127.0.0.1,localhost,testserver,.onrender.com,.vercel.app,.pythonanywhere.com",
        help_text=_("Comma-separated domains permitted to connect to this server."),
    )
    csrf_trusted_origins = models.CharField(
        _("CSRF Trusted Origins (CSRF_TRUSTED_ORIGINS)"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Comma-separated HTTPS origins (e.g. https://100humanity.org,https://my-app.onrender.com)."),
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Environment & API Setting (.env)")
        verbose_name_plural = _("Environment & API Settings (.env)")

    def __str__(self):
        return "System Environment & API Configuration"

    @property
    def active_database_engine(self):
        """Displays currently active database engine and host safely."""
        from django.db import connection
        engine = connection.settings_dict.get("ENGINE", "").split(".")[-1]
        name = connection.settings_dict.get("NAME", "")
        return f"{engine.upper()} ({name})"

    @property
    def cloudinary_status(self):
        """Displays whether Cloudinary credentials are fully configured."""
        if self.cloudinary_cloud_name and self.cloudinary_api_key and self.cloudinary_api_secret:
            return f"Active (Cloud: {self.cloudinary_cloud_name}, Folder: {self.cloudinary_folder})"
        return "Not Configured (Missing Cloud Name, Key, or Secret)"

    def clean(self):
        if EnvironmentSetting.objects.exclude(pk=self.pk).exists():
            raise ValidationError(_("Only one EnvironmentSetting instance is permitted."))

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        self.sync_to_runtime_and_env()

    def sync_to_runtime_and_env(self):
        """Updates in-memory Django settings and writes changes to the local .env file."""
        from django.conf import settings
        from pathlib import Path

        # 1. In-memory settings synchronization
        if self.cloudinary_cloud_name:
            settings.CLOUDINARY_CLOUD_NAME = self.cloudinary_cloud_name
        if self.cloudinary_api_key:
            settings.CLOUDINARY_API_KEY = self.cloudinary_api_key
        if self.cloudinary_api_secret:
            settings.CLOUDINARY_API_SECRET = self.cloudinary_api_secret
        if self.cloudinary_folder:
            settings.CLOUDINARY_FOLDER = self.cloudinary_folder

        if self.cloudinary_cloud_name and self.cloudinary_api_key and self.cloudinary_api_secret:
            try:
                import cloudinary
                cloudinary.config(
                    cloud_name=self.cloudinary_cloud_name,
                    api_key=self.cloudinary_api_key,
                    api_secret=self.cloudinary_api_secret,
                    secure=True,
                )
            except Exception:
                pass

        if self.allowed_hosts:
            settings.ALLOWED_HOSTS = [h.strip() for h in self.allowed_hosts.split(",") if h.strip()]

        if self.csrf_trusted_origins:
            settings.CSRF_TRUSTED_ORIGINS = [u.strip() for u in self.csrf_trusted_origins.split(",") if u.strip()]

        # 2. Write to .env file
        env_path = Path(settings.BASE_DIR) / ".env"
        try:
            existing = {}
            if env_path.exists():
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            parts = line.split("=", 1)
                            existing[parts[0].strip()] = parts[1].strip()

            if self.database_url:
                existing["DATABASE_URL"] = self.database_url
            if self.cloudinary_cloud_name:
                existing["CLOUDINARY_CLOUD_NAME"] = self.cloudinary_cloud_name
            if self.cloudinary_api_key:
                existing["CLOUDINARY_API_KEY"] = self.cloudinary_api_key
            if self.cloudinary_api_secret:
                existing["CLOUDINARY_API_SECRET"] = self.cloudinary_api_secret
            if self.cloudinary_folder:
                existing["CLOUDINARY_FOLDER"] = self.cloudinary_folder
            if self.youtube_api_key:
                existing["YOUTUBE_API_KEY"] = self.youtube_api_key
            if self.allowed_hosts:
                existing["ALLOWED_HOSTS"] = self.allowed_hosts
            if self.csrf_trusted_origins:
                existing["CSRF_TRUSTED_ORIGINS"] = self.csrf_trusted_origins
            if self.secret_key:
                existing["SECRET_KEY"] = self.secret_key

            with open(env_path, "w", encoding="utf-8") as f:
                f.write("# Generated and updated via Django Admin (Environment & API Settings)\n")
                for k, v in existing.items():
                    f.write(f"{k}={v}\n")
        except Exception:
            pass

    @classmethod
    def get_solo(cls):
        """Returns the active EnvironmentSetting record or initializes from existing env/settings."""
        from django.conf import settings
        import os
        try:
            raw_hosts = getattr(settings, "ALLOWED_HOSTS", [])
            allowed_hosts_str = ",".join(raw_hosts) if isinstance(raw_hosts, list) else str(raw_hosts)
            raw_csrf = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])
            csrf_str = ",".join(raw_csrf) if isinstance(raw_csrf, list) else str(raw_csrf)

            obj, _ = cls.objects.get_or_create(
                pk=1,
                defaults={
                    "database_url": os.environ.get("DATABASE_URL", ""),
                    "cloudinary_cloud_name": getattr(settings, "CLOUDINARY_CLOUD_NAME", ""),
                    "cloudinary_api_key": getattr(settings, "CLOUDINARY_API_KEY", ""),
                    "cloudinary_api_secret": getattr(settings, "CLOUDINARY_API_SECRET", ""),
                    "cloudinary_folder": getattr(settings, "CLOUDINARY_FOLDER", "100_humanity"),
                    "youtube_api_key": os.environ.get("YOUTUBE_API_KEY", ""),
                    "secret_key": getattr(settings, "SECRET_KEY", ""),
                    "allowed_hosts": allowed_hosts_str or "127.0.0.1,localhost,testserver,.onrender.com,.vercel.app,.pythonanywhere.com",
                    "csrf_trusted_origins": csrf_str,
                },
            )
            return obj
        except Exception:
            return cls(pk=1)


class BackgroundMusic(models.Model):
    """
    Background meditation audio and music tracks for 100% HUMANITY.
    Allows administrators to upload audio files (MP3/WAV/OGG) or specify external audio URLs,
    preview and audition playback in the admin dashboard, set default volume, and designate
    the active track playing across all pages with a floating mute/play control.
    """
    title = models.CharField(
        _("Track Title"),
        max_length=150,
        default="Buddham Saranam Gacchami — Flute Meditation",
        help_text=_("Display title of the ambient or meditation track."),
    )
    artist_credit = models.CharField(
        _("Artist / Credit"),
        max_length=150,
        blank=True,
        default="Traditional Buddhist Chant & Flute Meditation",
        help_text=_("Artist, composer, or copyright credit."),
    )
    audio_file = models.FileField(
        _("Audio File (Upload MP3 / WAV / OGG)"),
        upload_to="audio/",
        blank=True,
        null=True,
        help_text=_("Upload an audio file (MP3, WAV, or OGG). Max 20 MB."),
    )
    audio_url = models.URLField(
        _("External Audio URL (Stream / CDN)"),
        blank=True,
        default="",
        help_text=_(
            "Or enter a direct URL to an MP3/OGG audio stream (e.g., Cloudinary, CDN, archive.org). "
            "Used if no audio file is uploaded."
        ),
    )
    is_active = models.BooleanField(
        _("Active Website Track"),
        default=False,
        help_text=_(
            "Check to set this as the active background track across the entire website. "
            "Selecting this automatically deactivates other tracks."
        ),
    )
    is_enabled = models.BooleanField(
        _("Enabled Globally"),
        default=True,
        help_text=_("Master toggle: Uncheck to temporarily mute/disable background music on the website."),
    )
    default_volume = models.PositiveSmallIntegerField(
        _("Default Volume (%)"),
        default=30,
        help_text=_("Default playback volume percentage (1 to 100). Recommended: 25%–35% for soothing background sound."),
    )
    loop = models.BooleanField(
        _("Loop Playback"),
        default=True,
        help_text=_("Continuously repeat the track when it finishes."),
    )
    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Background Music Track")
        verbose_name_plural = _("Background Music Tracks")
        ordering = ["-is_active", "order", "-created_at"]

    def __str__(self):
        active_indicator = " [ACTIVE ON SITE]" if self.is_active else ""
        return f"{self.title}{active_indicator}"

    @property
    def effective_audio_url(self):
        """Returns the local uploaded file URL, or the external URL, or static fallback."""
        if self.audio_file:
            try:
                return self.audio_file.url
            except Exception:
                pass
        if self.audio_url and self.audio_url.strip():
            return self.audio_url.strip()
        from django.templatetags.static import static
        return static("audio/meditation-ambient.wav")

    def clean(self):
        if self.default_volume > 100:
            self.default_volume = 100
        elif self.default_volume < 1:
            self.default_volume = 1

    def save(self, *args, **kwargs):
        # Enforce that only one track is active at any time
        if self.is_active:
            BackgroundMusic.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_track(cls):
        """Returns the currently active and enabled track, or fallback default."""
        try:
            track = cls.objects.filter(is_active=True, is_enabled=True).first()
            if not track:
                track = cls.objects.filter(is_enabled=True).first()
            return track
        except Exception:
            return None
