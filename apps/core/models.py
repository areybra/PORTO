from django.db import models
from django.core.validators import RegexValidator


class SiteProfile(models.Model):
    """Singleton profile for AREYBRA — Brunelle style editorial studio."""
    site_name = models.CharField(max_length=50, default="AREYBRA")
    tagline = models.CharField(max_length=120, default="Desainer Produk & Creative Technologist")
    hero_name = models.CharField(max_length=100, default="Areta Y. Radjawali")
    hero_title = models.CharField(max_length=100, default="Junior Web Development")
    hero_description = models.TextField(
        default="Membangun sistem digital terukur, kejernihan arsitektur antarmuka, dan pengalaman web visceral yang dirancang pada titik temu keindahan estetika dan presisi rekayasa kode."
    )
    hero_image_url = models.URLField(
        blank=True,
        default="https://lh3.googleusercontent.com/aida/AEtjO1UEoiyjmRKUBIc9t_Fndn02qah9zD4YxMOclwvCsw3RgF04tBa7qBJtB3e-J04xQLKcvUDjFs3W9OGpRH2ONio9YqP3AFOlbnf_VADprquwDe9nBnqaSBN4w2LlKcPBqpkEODL3pzu4GkgxG44ucGQRBvUR2HQGWMBjGgDsHFLRA1U1NAfAjAKRmAirn9ZaUcwEP-OH1rfpqF-1S_JV3Za18csDTh8B6C7BX43cPLUS05jJpemociIHRQPo",
        help_text="URL gambar profil (gunakan URL eksternal untuk hemat storage, mis. https://...)",
        verbose_name="Foto Profil URL",
    )
    hero_image = models.ImageField(upload_to="profile/", blank=True, null=True, editable=False)  # deprecated, kept for migration
    email = models.EmailField(default="aretaradjawali@gmail.com")
    whatsapp_number = models.CharField(
        max_length=20,
        default="6282142961010",
        validators=[RegexValidator(r"^62\d{9,14}$", "Format 62xxxxxxxxxxx")],
        help_text="Format 62 tanpa + (contoh 6282142961010)",
    )
    location = models.CharField(max_length=100, default="Kabupaten Probolinggo & Jawa Timur")
    timezone_label = models.CharField(max_length=50, default="WIB (UTC+7) · Jakarta, Indonesia")
    availability_text = models.CharField(max_length=120, default="Tersedia untuk proyek baru Q2/Q3 2025")
    availability_active = models.BooleanField(default=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)
    footer_description = models.TextField(
        default="Studio desain produk independen yang memadukan keanggunan tipografi editorial, arsitektur perangkat lunak presisi, dan filosofi interaksi modern."
    )
    # About page narrative
    about_quote = models.TextField(
        blank=True,
        default='"Berasal dari Kab. Probolinggo, kini menempuh pendidikan SLTA di SMK Nurul Jadid dalam bidang keahlian Rekayasa Perangkat Lunak. Selain meminati Web Development juga tertarik dengan Cyber Security."',
    )
    about_vision = models.TextField(
        blank=True,
        default="Menjadi arsitek solusi digital dan Data Analyst yang mampu mengurai kompleksitas data menjadi keputusan bernilai, aman dari celah siber.",
    )
    github_username = models.CharField(max_length=50, default="aretaradjawali")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com")
    github_url = models.URLField(blank=True, default="https://github.com")
    dribbble_url = models.URLField(blank=True, default="https://dribbble.com")
    readcv_url = models.URLField(blank=True, default="https://read.cv")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("project_detail", args=[self.slug])

    class Meta:
        verbose_name = "Site Profile"
        verbose_name_plural = "Site Profile"

    def __str__(self):
        return f"{self.site_name} — {self.hero_name}"

    @property
    def hero_image_effective(self):
        if self.hero_image_url:
            return self.hero_image_url
        if self.hero_image and hasattr(self.hero_image, "url"):
            try:
                return self.hero_image.url
            except Exception:
                pass
        return ""

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("dribbble", "Dribbble"),
        ("readcv", "Read.cv"),
        ("email", "Email"),
        ("telegram", "Telegram/WA"),
        ("other", "Other"),
    ]
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="github")
    label = models.CharField(max_length=50, help_text="Contoh: GitHub / @aretaradjawali")
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True, help_text="Material Symbol name, ex: code, work")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Social Link"

    def __str__(self):
        return f"{self.label} ({self.platform})"


class Service(models.Model):
    """Layanan & Praktik — footer col & about matrix."""
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Material symbol")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Trait(models.Model):
    """Pilar karakter tentang-saya: 4 cards."""
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="traits")
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=20, help_text="Pilar I / II")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=30, default="flag")
    footer_label = models.CharField(max_length=50, blank=True)
    footer_value = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default="primary", help_text="primary / tertiary")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class SkillCategory(models.Model):
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="skill_categories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=30, default="dns")
    domain_label = models.CharField(max_length=20, default="Domain 01")
    order = models.PositiveIntegerField(default=0)
    tools_text = models.CharField(max_length=120, blank=True, help_text="Postman, Docker, Git Bash")

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    LEVEL_CHOICES = [
        ("mahir", "Mahir"),
        ("kompeten", "Kompeten"),
        ("menengah", "Menengah"),
        ("riset", "Riset Aktif"),
        ("aspirasi", "Aspirasi Utama"),
    ]
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=150, blank=True)
    icon = models.CharField(max_length=30, default="code")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="kompeten")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class FAQ(models.Model):
    profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="faqs", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"

    def __str__(self):
        return self.question[:60]
