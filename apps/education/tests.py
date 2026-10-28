"""Automated tests for the 15 Dhamma Education Principles."""
from django.test import TestCase
from django.urls import reverse
from apps.education.models import DhammaPrinciple


class DhammaEducationTests(TestCase):
    def test_all_15_principles_seeded_and_rendered(self):
        response = self.client.get(reverse("education:principle_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DhammaPrinciple.objects.count(), 15)
        self.assertContains(response, "Strong knowledge of Buddha Dhamma")
        self.assertContains(response, "Dr. Babasaheb Ambedkar and Navayana Buddhism")
        self.assertContains(response, "Living as an example of Dhamma in everyday life")

    def test_unpublished_principle_hidden_from_public(self):
        p1 = DhammaPrinciple.objects.get(principle_number=1)
        p1.is_published = False
        p1.save()
        response = self.client.get(reverse("education:principle_list"))
        self.assertNotContains(response, "Strong knowledge of Buddha Dhamma")
