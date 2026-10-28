from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("site_name", models.CharField(default="100% HUMANITY", max_length=120, verbose_name="Website Name")),
                ("tagline", models.CharField(default="Walking the Path of Buddha Dhamma: Equality, Compassion, Scientific Inquiry & Humanity", max_length=255, verbose_name="Site Tagline")),
                ("hero_title", models.CharField(default="Awakening Minds Through Buddha Dhamma, Compassion & Rational Inquiry", max_length=200, verbose_name="Homepage Hero Title")),
                ("hero_subtitle", models.TextField(default="100% HUMANITY is an educational initiative dedicated to sharing Gautama Buddha's teachings of pragmatic wisdom, universal equality, ethical conduct, mindfulness meditation, scientific temperament, and social awareness.", verbose_name="Homepage Hero Subtitle")),
                ("dhamma_intro_title", models.CharField(default="Understanding Buddha Dhamma as a Living Educational Path", max_length=200, verbose_name="Buddha Dhamma Introduction Heading")),
                ("dhamma_intro_text", models.TextField(default="Buddha Dhamma is grounded in direct observation, ethical responsibility (Sila), mental cultivation (Samadhi), and liberating wisdom (Panna). Rather than relying on blind dogma or superstition, the Dhamma invites every human being to examine experience rationally, practice non-discrimination, and cultivate boundless loving-kindness (Metta) and compassion (Karuna) for the welfare of society.", verbose_name="Buddha Dhamma Introduction Content")),
                ("mission_statement", models.TextField(default="To foster accessible Dhamma education, ethical leadership, meditation practice, and scientific thinking across communities—empowering dedicated teachers and learners to live with dignity, equality, and compassion.", verbose_name="Mission Statement")),
                ("vision_statement", models.TextField(default="A compassionate, rational, and egalitarian society free from discrimination and superstition, guided by universal human values and the timeless wisdom of Gautama Buddha.", verbose_name="Vision Statement")),
                ("about_introduction", models.TextField(default="100% HUMANITY is a community-focused educational initiative dedicated to studying, practicing, and sharing the teachings of Gautama Buddha. We focus on practical Dhamma education that uplifts individuals and strengthens social harmony through moral integrity, mindfulness, and rational inquiry.", verbose_name="About Us — Organization Introduction")),
                ("about_purpose_of_dhamma", models.TextField(default="The purpose of Dhamma education is to cultivate clear understanding, ethical conduct, and emotional balance in daily life. By training capable, compassionate Dhamma teachers who communicate clearly in local languages, we help communities apply the Five Precepts, mindfulness meditation, and critical thinking to everyday challenges.", verbose_name="About Us — Purpose of Dhamma Education")),
                ("about_equality_compassion", models.TextField(default="Rooted in the egalitarian spirit of Gautama Buddha and the transformative historical insight of Dr. Babasaheb Ambedkar's Navayana movement, 100% HUMANITY affirms the equal dignity and worth of every person regardless of caste, gender, background, or status. True spirituality is measured by how humanely and justly we treat one another.", verbose_name="About Us — Equality and Compassion")),
                ("about_scientific_thinking", models.TextField(default="Dhamma encourages questioning, verification through experience, and understanding cause and effect. We promote scientific temperament, digital literacy, and constructive social awareness so learners can reject superstition and contribute thoughtfully to community welfare.", verbose_name="About Us — Scientific Thinking & Social Awareness")),
                ("about_educational_objectives", models.TextField(default="Develop well-trained, ethical Dhamma teachers grounded in the 15 foundational principles.\nEncourage regular mindfulness and vipassana-inspired meditation practice for mental clarity.\nPromote scientific thinking, rational inquiry, and freedom from superstition.\nUphold human equality, non-discrimination, and compassionate community service.\nProvide accessible study materials, public talks, and multilingual learning in English, Marathi, and Hindi.", verbose_name="About Us — Educational Objectives (One per line)")),
                ("community_participation_title", models.CharField(default="Participate in Study Circles, Meditation & Dhamma Learning", max_length=200, verbose_name="Community Participation Heading")),
                ("community_participation_text", models.TextField(default="Whether you are beginning your study of Buddha Dhamma, practicing meditation, or preparing to serve as a community Dhamma teacher, we welcome your participation. Reach out to connect with upcoming study sessions, lectures, and educational resources.", verbose_name="Community Participation Text")),
                ("contact_person", models.CharField(default="Arvind Betkar", max_length=120, verbose_name="Contact Person")),
                ("contact_email", models.EmailField(default="arvindbet12@gmail.com", max_length=254, verbose_name="Contact Email")),
                ("contact_phone", models.CharField(default="8983087210", max_length=30, verbose_name="Contact Phone")),
                ("contact_address", models.TextField(blank=True, default="", help_text="Leave blank until an official physical address is provided. Do not fabricate addresses.", verbose_name="Address / Location Note (Optional)")),
                ("youtube_channel_name", models.CharField(default="100% HUMANITY", max_length=120, verbose_name="YouTube Channel Name")),
                ("youtube_channel_url", models.URLField(blank=True, default="", help_text="Paste the official 100% HUMANITY YouTube channel URL here when available.", verbose_name="YouTube Channel URL")),
                ("facebook_url", models.URLField(blank=True, default="", verbose_name="Facebook Page URL (Optional)")),
                ("instagram_url", models.URLField(blank=True, default="", verbose_name="Instagram URL (Optional)")),
                ("telegram_url", models.URLField(blank=True, default="", verbose_name="Telegram Group/Channel URL (Optional)")),
                ("meta_description", models.CharField(default="100% HUMANITY — Educational initiative dedicated to Gautama Buddha's teachings, Buddha Dhamma, equality, compassion, meditation, scientific thinking, and social awareness.", max_length=300, verbose_name="Default Meta Description")),
                ("footer_note", models.CharField(default="Dedicated to Buddha Dhamma, Human Equality, Compassion, and Rational Inquiry.", max_length=255, verbose_name="Footer Note")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Site Settings & Page Content",
                "verbose_name_plural": "Site Settings & Page Content",
            },
        ),
    ]
