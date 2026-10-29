"""Automated tests for SiteSettings singleton, Home, About Us, robots.txt, sitemap, and production security."""
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from apps.core.models import SiteSettings, EnvironmentSetting, BackgroundMusic
from apps.events.models import Event


class CoreViewsAndSettingsTests(TestCase):
    @override_settings(DEFAULT_YOUTUBE_CHANNEL_URL="")
    def test_site_settings_singleton_defaults(self):
        site = SiteSettings.get_solo()
        self.assertEqual(site.site_name, "100% HUMANITY")
        self.assertEqual(site.contact_person, "Arvind Betkar")
        self.assertEqual(site.contact_email, "arvindbet12@gmail.com")
        self.assertEqual(site.contact_phone, "8983087210")
        self.assertEqual(site.youtube_channel_name, "100% HUMANITY")
        self.assertEqual(site.youtube_channel_url, "")

    def test_site_settings_prevents_second_instance(self):
        SiteSettings.get_solo()
        second = SiteSettings(site_name="Duplicate")
        with self.assertRaises(ValidationError):
            second.clean()

    def test_home_page_renders_with_identity(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100% HUMANITY")
        self.assertContains(response, "Arvind Betkar")
        self.assertContains(response, "8983087210")

    def test_home_shows_ongoing_event_that_started_before_today(self):
        today = timezone.localdate()
        Event.objects.create(
            title="Ongoing Dhamma Study Retreat",
            description="A multi-day study retreat that is still in progress.",
            start_date=today - timedelta(days=1),
            end_date=today + timedelta(days=1),
            venue="Community Vihara Hall",
            status=Event.Status.PUBLISHED,
        )
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ongoing Dhamma Study Retreat")

    def test_about_page_renders(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Purpose of Dhamma Education")
        self.assertContains(response, "Equality")

    def test_robots_txt_and_sitemap(self):
        robots_res = self.client.get(reverse("robots_txt"))
        self.assertEqual(robots_res.status_code, 200)
        self.assertIn("Disallow: /admin/", robots_res.content.decode())

        sitemap_res = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        self.assertEqual(sitemap_res.status_code, 200)

    @override_settings(DEBUG=False)
    def test_security_headers_and_settings_present(self):
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.X_FRAME_OPTIONS, "DENY")
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)

    def test_environment_settings_singleton_and_sync(self):
        env_obj = EnvironmentSetting.get_solo()
        self.assertEqual(env_obj.pk, 1)
        self.assertTrue(env_obj.active_database_engine)
        self.assertTrue(env_obj.cloudinary_status)

        # Test in-memory synchronization
        env_obj.cloudinary_cloud_name = "test-cloud-123"
        env_obj.cloudinary_api_key = "test-key-456"
        env_obj.cloudinary_api_secret = "test-secret-789"
        env_obj.save()

        self.assertEqual(settings.CLOUDINARY_CLOUD_NAME, "test-cloud-123")
        self.assertEqual(settings.CLOUDINARY_API_KEY, "test-key-456")
        self.assertEqual(settings.CLOUDINARY_API_SECRET, "test-secret-789")
        self.assertIn("Active", env_obj.cloudinary_status)

        # Duplicate clean check
        second = EnvironmentSetting(database_url="postgresql://fake")
        with self.assertRaises(ValidationError):
            second.clean()

    def test_background_music_model_and_active_switching(self):
        track1 = BackgroundMusic.objects.create(
            title="Track One",
            audio_url="https://example.com/one.mp3",
            is_active=True,
            is_enabled=True,
            default_volume=35,
        )
        self.assertEqual(BackgroundMusic.get_active_track(), track1)

        # Creating or saving track2 as active should deactivate track1
        track2 = BackgroundMusic.objects.create(
            title="Track Two",
            audio_url="https://example.com/two.mp3",
            is_active=True,
            is_enabled=True,
            default_volume=40,
        )
        track1.refresh_from_db()
        self.assertFalse(track1.is_active)
        self.assertTrue(track2.is_active)
        self.assertEqual(BackgroundMusic.get_active_track(), track2)

    def test_floating_music_widget_renders_on_pages(self):
        BackgroundMusic.objects.create(
            title="Buddham Saranam Gacchami Ambient",
            audio_url="https://example.com/meditation.mp3",
            is_active=True,
            is_enabled=True,
            default_volume=30,
        )
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="music-floating-widget"')
        self.assertContains(response, 'id="bg-audio-player"')
        self.assertContains(response, 'Buddham Saranam Gacchami Ambient')
        self.assertContains(response, 'id="music-volume-slider"')

    def test_google_analytics_script_renders_when_configured(self):
        site = SiteSettings.get_solo()
        site.google_analytics_id = "G-TEST123456"
        site.save()

        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "googletagmanager.com/gtag/js?id=G-TEST123456")
        self.assertContains(response, "gtag('config', 'G-TEST123456');")

    def test_google_search_console_verification_meta_renders(self):
        site = SiteSettings.get_solo()
        site.google_site_verification = "test-search-console-verification-token-123"
        site.save()

        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<meta name="google-site-verification" content="test-search-console-verification-token-123" />')

    def test_google_search_console_token_cleaner_from_full_html_tag(self):
        site = SiteSettings.get_solo()
        site.google_site_verification = '<meta name="google-site-verification" content="xyz987token" />'
        self.assertEqual(site.clean_google_site_verification, "xyz987token")
