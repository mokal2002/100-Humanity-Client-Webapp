"""Automated tests for YouTube URL parsing, iframe injection rejection, and video pages."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from apps.videos.models import Video, VideoCategory
from apps.videos.validators import extract_youtube_video_id


class YouTubeValidatorAndModelTests(TestCase):
    def test_extracts_standard_watch_url(self):
        vid = extract_youtube_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_extracts_short_youtu_be_url(self):
        vid = extract_youtube_video_id("https://youtu.be/dQw4w9WgXcQ?si=12345")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_extracts_youtube_shorts_url(self):
        vid = extract_youtube_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_rejects_raw_iframe_html_and_non_youtube_domains(self):
        with self.assertRaises(ValidationError):
            extract_youtube_video_id('<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ"></iframe>')
        with self.assertRaises(ValidationError):
            extract_youtube_video_id("https://malicious-site.example.com/watch?v=dQw4w9WgXcQ")

    def test_video_model_populates_video_id_and_embed_url(self):
        cat = VideoCategory.objects.create(name="Dhamma Talks")
        video = Video.objects.create(
            title="Introduction to the Five Precepts",
            youtube_url="https://youtu.be/dQw4w9WgXcQ",
            category=cat,
            is_published=True,
        )
        self.assertEqual(video.video_id, "dQw4w9WgXcQ")
        self.assertEqual(
            video.embed_url,
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ?rel=0",
        )
        res = self.client.get(reverse("videos:video_detail", kwargs={"slug": video.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "youtube-nocookie.com/embed/dQw4w9WgXcQ")

    def test_video_search_keeps_selected_category(self):
        cat = VideoCategory.objects.create(name="Meditation Guidance")
        Video.objects.create(
            title="Breath Awareness Practice",
            youtube_url="https://youtu.be/dQw4w9WgXcQ",
            category=cat,
            is_published=True,
        )
        res = self.client.get(reverse("videos:video_list"), {"category": cat.slug})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="category"')
        self.assertContains(res, cat.slug)
