"""Automated tests for SiteSettings singleton, Home, About Us, robots.txt, sitemap, and production security."""
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from apps.core.models import SiteSettings
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
