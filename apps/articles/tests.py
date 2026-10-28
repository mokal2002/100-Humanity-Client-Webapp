"""Automated tests for Article publication visibility, Unicode support (Marathi/Hindi), and HTML escaping."""
from django.test import TestCase
from django.urls import reverse
from apps.articles.models import Article, ArticleCategory


class ArticlePublishingTests(TestCase):
    def setUp(self):
        self.category = ArticleCategory.objects.create(name="Buddha Dhamma & Rationality")
        self.published_article = Article.objects.create(
            title="समता आणि करुणा — Equality and Compassion in Buddha Dhamma",
            author_name="Arvind Betkar",
            category=self.category,
            summary="Exploring how Gautama Buddha taught universal human dignity.",
            content="Buddha Dhamma teaches प्रज्ञा (wisdom), शील (ethics), and करुणा (compassion).\n<script>alert('xss')</script>",
            status=Article.Status.PUBLISHED,
        )
        self.draft_article = Article.objects.create(
            title="Unpublished Draft Essay",
            author_name="Arvind Betkar",
            category=self.category,
            summary="Draft summary.",
            content="Draft content.",
            status=Article.Status.DRAFT,
        )

    def test_published_article_visible_and_draft_hidden(self):
        list_res = self.client.get(reverse("articles:article_list"))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, "समता आणि करुणा")
        self.assertNotContains(list_res, "Unpublished Draft Essay")

        draft_detail = self.client.get(
            reverse("articles:article_detail", kwargs={"slug": self.draft_article.slug})
        )
        self.assertEqual(draft_detail.status_code, 404)

    def test_untrusted_html_is_escaped_on_article_detail(self):
        detail_res = self.client.get(
            reverse("articles:article_detail", kwargs={"slug": self.published_article.slug})
        )
        self.assertEqual(detail_res.status_code, 200)
        self.assertNotContains(detail_res, "<script>alert('xss')</script>")
        self.assertContains(detail_res, "&lt;script&gt;")
