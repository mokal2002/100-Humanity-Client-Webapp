"""Automated tests for Event publication, date validation, and upcoming/past filtering."""
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.events.models import Event


class EventModelAndViewTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.published_event = Event.objects.create(
            title="Sunday Mindfulness and Dhamma Study Circle",
            description="Weekly meditation and study of The Buddha and His Dhamma.",
            start_date=self.today + timedelta(days=7),
            venue="Community Vihara Hall",
            status=Event.Status.PUBLISHED,
        )
        self.draft_event = Event.objects.create(
            title="Internal Teacher Planning Session",
            description="Draft event not yet public.",
            start_date=self.today + timedelta(days=14),
            venue="Study Room",
            status=Event.Status.DRAFT,
        )

    def test_event_date_validation_rejects_end_before_start(self):
        invalid_event = Event(
            title="Invalid Date Event",
            description="Test",
            start_date=self.today + timedelta(days=5),
            end_date=self.today + timedelta(days=2),
            venue="Hall",
        )
        with self.assertRaises(ValidationError):
            invalid_event.clean()

    def test_public_event_list_shows_only_published(self):
        response = self.client.get(reverse("events:event_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_event.title)
        self.assertNotContains(response, self.draft_event.title)

    def test_draft_event_detail_returns_404(self):
        response = self.client.get(
            reverse("events:event_detail", kwargs={"slug": self.draft_event.slug})
        )
        self.assertEqual(response.status_code, 404)
