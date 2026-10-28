"""
Database model and canonical seed data for the 15 Principles for Developing Good Dhamma Teachers.
No fabricated scriptural quotations are used; explanations focus on authentic pedagogical and ethical practice.
"""
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


DEFAULT_DHAMMA_PRINCIPLES = [
    {
        "principle_number": 1,
        "title": "Strong knowledge of Buddha Dhamma",
        "slug": "strong-knowledge-of-buddha-dhamma",
        "summary": "A clear, grounded understanding of the Four Noble Truths, the Eightfold Path, Dependent Origination (Paticcasamuppada), and the Three Trainings (Sila, Samadhi, Panna).",
        "detailed_explanation": (
            "An effective Dhamma teacher studies the foundational teachings of Gautama Buddha systematically. "
            "Rather than relying on hearsay or superficial interpretations, the teacher understands how ethical "
            "conduct, mental discipline, and experiential wisdom work together to alleviate suffering and promote "
            "human flourishing."
        ),
        "practical_guidance": "Dedicate regular time to structured study of primary Dhamma discourses and Dr. Babasaheb Ambedkar's 'The Buddha and His Dhamma', verifying concepts through reflection and dialogue.",
        "learning_resources": "The Buddha and His Dhamma (Dr. B.R. Ambedkar); Introductory study circles on the Noble Eightfold Path.",
        "is_featured": True,
    },
    {
        "principle_number": 2,
        "title": "Good character and ethical conduct",
        "slug": "good-character-and-ethical-conduct",
        "summary": "Integrity, honesty, non-harming, and moral uprightness in personal, family, and public life.",
        "detailed_explanation": (
            "Ethical conduct (Sila) is the bedrock of Buddha Dhamma. A teacher's character builds trust within "
            "the community. When speech and actions consistently reflect truthfulness, kindness, and fairness, "
            "students learn the value of moral responsibility through direct observation."
        ),
        "practical_guidance": "Practice conscientiousness in speech, livelihood, and interpersonal relationships, treating every individual with respect and honesty.",
        "learning_resources": "Study of Right Speech, Right Action, and Right Livelihood.",
        "is_featured": True,
    },
    {
        "principle_number": 3,
        "title": "Regular meditation practice",
        "slug": "regular-meditation-practice",
        "summary": "Consistent cultivation of mindfulness (Satipatthana), calm awareness (Samatha), and loving-kindness (Metta).",
        "detailed_explanation": (
            "Dhamma is not merely intellectual theory; it is an experiential discipline of training the mind. "
            "Regular meditation cultivates emotional steadiness, clarity of attention, and patience, enabling "
            "a teacher to respond to difficult questions and life situations with equanimity."
        ),
        "practical_guidance": "Maintain a daily personal sitting practice focusing on mindfulness of breathing (Anapanasati) and loving-kindness (Metta Bhavana).",
        "learning_resources": "Guided mindfulness of breathing and Metta meditation workshops.",
        "is_featured": True,
    },
    {
        "principle_number": 4,
        "title": "Effective public speaking",
        "slug": "effective-public-speaking",
        "summary": "Speaking with clarity, warmth, structured organization, and respectful engagement before diverse audiences.",
        "detailed_explanation": (
            "A Dhamma teacher communicates complex philosophical and ethical ideas in a calm, confident, and "
            "resonant voice. Effective public speaking avoids harsh rhetoric, arrogance, or confusion, keeping "
            "listeners engaged and inspired to apply the teachings in daily life."
        ),
        "practical_guidance": "Prepare clear outlines before every talk, modulate tone with warmth, respect audience time limits, and invite thoughtful questions.",
        "learning_resources": "Community speaker training sessions and structured talk outlines.",
        "is_featured": False,
    },
    {
        "principle_number": 5,
        "title": "Good teaching and explanation skills",
        "slug": "good-teaching-and-explanation-skills",
        "summary": "Breaking down profound concepts into relatable, practical lessons suited to children, youth, and adults.",
        "detailed_explanation": (
            "Good pedagogy meets learners where they are. By using everyday examples, patient dialogue, and "
            "clear step-by-step explanations, a teacher ensures that everyone—from beginners to advanced "
            "students—can grasp the relevance of Dhamma in modern life."
        ),
        "practical_guidance": "Use real-life analogies, encourage active questions, summarize key takeaways, and check for student comprehension.",
        "learning_resources": "Pedagogical lesson plans for youth and adult study groups.",
        "is_featured": False,
    },
    {
        "principle_number": 6,
        "title": "Scientific thinking and rational inquiry",
        "slug": "scientific-thinking-and-rational-inquiry",
        "summary": "Examining cause and effect objectively, rejecting blind superstition, and encouraging evidence-based reasoning.",
        "detailed_explanation": (
            "Buddha Dhamma emphasizes causal understanding and experiential verification rather than blind faith "
            "or ritualism. A good Dhamma teacher nurtures a scientific temperament, helping communities distinguish "
            "verified truth from superstition and dogmatism."
        ),
        "practical_guidance": "Encourage critical inquiry in classes, explain teachings through cause-and-effect reasoning, and support scientific education.",
        "learning_resources": "Workshops on rational inquiry, causality, and freedom from superstition.",
        "is_featured": True,
    },
    {
        "principle_number": 7,
        "title": "Equality and non-discrimination",
        "slug": "equality-and-non-discrimination",
        "summary": "Upholding the equal human dignity of all people without distinction of caste, gender, class, or background.",
        "detailed_explanation": (
            "Gautama Buddha rejected birth-based hierarchy and affirmed that human worth is determined by deeds "
            "and character, not lineage. Teachers must actively model non-discrimination, ensuring learning spaces "
            "welcome women, men, youth, and elders as equals."
        ),
        "practical_guidance": "Ensure inclusive participation in all events and study circles, challenging discriminatory attitudes with calm reason and solidarity.",
        "learning_resources": "Historical studies on equality in the Sangha and constitutional human rights.",
        "is_featured": True,
    },
    {
        "principle_number": 8,
        "title": "Compassion and humanity",
        "slug": "compassion-and-humanity",
        "summary": "Practicing active empathy (Karuna) and loving-kindness (Metta) toward all living beings and supporting those in distress.",
        "detailed_explanation": (
            "Knowledge without compassion becomes cold and disconnected. The heart of 100% HUMANITY is active "
            "care for human wellbeing—listening empathetically, supporting educational upliftment, and standing "
            "beside those facing hardship."
        ),
        "practical_guidance": "Combine educational instruction with practical community care, active listening, and mutual support.",
        "learning_resources": "Practice guides on the Four Brahmaviharas (Metta, Karuna, Mudita, Upekkha).",
        "is_featured": True,
    },
    {
        "principle_number": 9,
        "title": "Knowledge of Buddhist history, including Dr. Babasaheb Ambedkar and Navayana Buddhism",
        "slug": "knowledge-of-buddhist-history-and-navayana-buddhism",
        "summary": "Understanding the historical evolution of Buddhism in India and its modern revival led by Dr. B.R. Ambedkar.",
        "detailed_explanation": (
            "To teach effectively in the contemporary context, a teacher needs accurate historical perspective: "
            "the social conditions during Gautama Buddha's life, the spread of educational viharas across ancient "
            "India, and Dr. Babasaheb Ambedkar's historic 1956 revival of Navayana Buddhism centered on liberty, "
            "equality, and fraternity."
        ),
        "practical_guidance": "Study verified historical texts, biographies, and Dr. Ambedkar's writings on Dhamma as a social and moral reconstruction.",
        "learning_resources": "The Buddha and His Dhamma; Historical essays on ancient Indian Buddhist education and the 1956 Diksha.",
        "is_featured": False,
    },
    {
        "principle_number": 10,
        "title": "Understanding and practicing the Five Precepts",
        "slug": "understanding-and-practicing-the-five-precepts",
        "summary": "Living by Panchsheel: abstaining from harming life, taking what is not given, sexual misconduct, false speech, and intoxicants.",
        "detailed_explanation": (
            "The Five Precepts (Panchsheel) are voluntary ethical commitments that protect personal peace and "
            "social trust. A teacher not only explains their meaning in positive terms—respect for life, generosity, "
            "respectful relationships, truthful speech, and mental clarity—but embodies them daily."
        ),
        "practical_guidance": "Reflect daily on the Five Precepts and explain how mental clarity (freedom from intoxicants) protects families and communities.",
        "learning_resources": "Panchsheel study guide for families and youth.",
        "is_featured": False,
    },
    {
        "principle_number": 11,
        "title": "Leadership and community-building",
        "slug": "leadership-and-community-building",
        "summary": "Organizing inclusive study groups, fostering cooperation, and resolving conflicts constructively.",
        "detailed_explanation": (
            "Dhamma flourishes in a supportive community (Sangha/fellowship). Good teachers practice servant "
            "leadership—sharing responsibilities, mentoring younger teachers, maintaining transparency, and "
            "building unity across neighborhoods."
        ),
        "practical_guidance": "Establish collaborative study circles, rotate facilitation duties, and make decisions transparently.",
        "learning_resources": "Community organizing and democratic facilitation guidelines.",
        "is_featured": False,
    },
    {
        "principle_number": 12,
        "title": "Digital media and technology skills",
        "slug": "digital-media-and-technology-skills",
        "summary": "Using digital tools, online video, and responsible media literacy to share authentic Dhamma education widely.",
        "detailed_explanation": (
            "In the modern era, digital platforms allow quality educational talks, articles, and event updates "
            "to reach learners everywhere at zero cost. Teachers should know how to record clear lectures, share "
            "verified resources online, and help students verify digital information responsibly."
        ),
        "practical_guidance": "Learn basic audio/video recording, presentation structure, and fact-checking before sharing online content.",
        "learning_resources": "100% HUMANITY YouTube video library and digital literacy workshops.",
        "is_featured": False,
    },
    {
        "principle_number": 13,
        "title": "Discipline and consistency",
        "slug": "discipline-and-consistency",
        "summary": "Punctuality, steady preparation, and long-term commitment to learning and community service.",
        "detailed_explanation": (
            "Lasting educational transformation requires steady effort over time rather than occasional bursts "
            "of enthusiasm. Punctuality at events, thorough preparation before lectures, and reliable follow-through "
            "inspire discipline across the entire learning community."
        ),
        "practical_guidance": "Maintain a consistent weekly schedule for reading, meditation, and community teaching sessions.",
        "learning_resources": "Personal study and teaching planner templates.",
        "is_featured": False,
    },
    {
        "principle_number": 14,
        "title": "Ability to teach in local languages",
        "slug": "ability-to-teach-in-local-languages",
        "summary": "Communicating Dhamma clearly in Marathi, Hindi, English, and local vernaculars so everyone can understand.",
        "detailed_explanation": (
            "Gautama Buddha encouraged teaching in the everyday language of the people so that wisdom is never "
            "locked behind elitist barriers. Explaining key Pali terms accurately in clear Marathi, Hindi, and "
            "English ensures elders, youth, and families connect deeply with the teachings."
        ),
        "practical_guidance": "Build a bilingual/trilingual glossary of core Dhamma concepts in Marathi, Hindi, and English.",
        "learning_resources": "Multilingual Dhamma terminology reference sheets (Marathi / Hindi / English).",
        "is_featured": False,
    },
    {
        "principle_number": 15,
        "title": "Living as an example of Dhamma in everyday life",
        "slug": "living-as-an-example-of-dhamma-in-everyday-life",
        "summary": "Harmonizing words and deeds at home, at work, and in society so one's life becomes the clearest teaching.",
        "detailed_explanation": (
            "The highest test of Dhamma education is how one lives when off the stage—showing patience within "
            "the family, fairness at work, humility in success, and resilience in adversity. A teacher who lives "
            "the Dhamma inspires genuine transformation without needing grand claims."
        ),
        "practical_guidance": "Practice daily self-reflection, humility, and gratitude, aligning public teaching with private conduct.",
        "learning_resources": "Daily mindfulness and ethical reflection journal.",
        "is_featured": False,
    },
]


class DhammaPrinciple(models.Model):
    """
    Stores each of the 15 principles for developing good Dhamma teachers.
    Administrators can edit, reorder, feature, publish, or update them via Django Admin.
    """
    principle_number = models.PositiveSmallIntegerField(
        _("Principle Number"),
        unique=True,
        help_text=_("Canonical principle number (1 to 15+)."),
    )
    title = models.CharField(_("Principle Title"), max_length=220)
    slug = models.SlugField(_("URL Slug"), max_length=240, unique=True)
    summary = models.TextField(
        _("Brief Summary"),
        help_text=_("Concise 1-2 sentence overview shown on cards."),
    )
    detailed_explanation = models.TextField(
        _("Detailed Explanation"),
        help_text=_("Full educational explanation of why this principle matters."),
    )
    practical_guidance = models.TextField(
        _("Practical Application for Teachers"),
        blank=True,
        default="",
        help_text=_("Actionable steps for practicing and applying this principle."),
    )
    learning_resources = models.TextField(
        _("Recommended Learning Resources (Optional)"),
        blank=True,
        default="",
        help_text=_("Optional study topics, books, or workshop references."),
    )
    display_order = models.PositiveSmallIntegerField(
        _("Display Order"),
        default=1,
        db_index=True,
        help_text=_("Controls ordering on the Dhamma Education page (lowest number first)."),
    )
    is_featured = models.BooleanField(
        _("Feature on Homepage"),
        default=False,
        db_index=True,
    )
    is_published = models.BooleanField(
        _("Published"),
        default=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "principle_number"]
        verbose_name = _("Dhamma Education Principle")
        verbose_name_plural = _("Dhamma Education Principles")
        indexes = [
            models.Index(fields=["is_published", "display_order"]),
        ]

    def __str__(self):
        return f"Principle {self.principle_number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.principle_number}-{self.title}")[:240]
        super().save(*args, **kwargs)
