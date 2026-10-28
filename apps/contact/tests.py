"""Automated tests for Contact form validation, honeypot spam rejection, and admin protection."""
from django.test import TestCase
from django.urls import reverse
from apps.contact.forms import ContactForm
from apps.contact.models import ContactSubmission


class ContactSubmissionTests(TestCase):
    def test_valid_contact_submission_saved_with_new_status(self):
        form = ContactForm(
            data={
                "full_name": "Rahul Jadhav",
                "email": "rahul@example.com",
                "phone": "9876543210",
                "subject": "Study Circle Inquiry",
                "message": "I would like to join the upcoming Sunday Dhamma study circle.",
                "website_url_honeypot": "",
            }
        )
        self.assertTrue(form.is_valid())
        submission = form.save()
        self.assertEqual(submission.status, ContactSubmission.Status.NEW)

    def test_honeypot_spam_field_rejects_bot_submission(self):
        form = ContactForm(
            data={
                "full_name": "Spam Bot",
                "email": "bot@example.com",
                "message": "Buy cheap links now!",
                "website_url_honeypot": "http://spam.example.com",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("website_url_honeypot", form.errors)

    def test_short_message_rejected(self):
        form = ContactForm(
            data={
                "full_name": "Test User",
                "email": "user@example.com",
                "message": "Too short",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_admin_contact_list_protected_from_anonymous_users(self):
        res = self.client.get("/admin/contact/contactsubmission/")
        self.assertEqual(res.status_code, 302)
