from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    icon = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Technologies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    technologies = models.ManyToManyField(Technology, blank=True, related_name="projects")
    excerpt = models.CharField(max_length=300, blank=True)
    description = models.TextField(help_text="Deskripsi lengkap studi kasus")
    thumbnail_url = models.URLField(blank=True, help_text="URL gambar thumbnail (eksternal, hemat storage). Kosongkan untuk pakai placeholder SVG.")
    thumbnail = models.ImageField(upload_to="projects/%Y/", blank=True, null=True, editable=False)  # deprecated
    # fallback SVG mock type for templates without image
    mock_type = models.CharField(max_length=30, blank=True, help_text="kroma / aura / chronos etc for SVG placeholder")

    @property
    def image_url(self):
        if self.thumbnail_url:
            return self.thumbnail_url
        if self.thumbnail and hasattr(self.thumbnail, "url"):
            try:
                return self.thumbnail.url
            except Exception:
                pass
        return ""
    year = models.PositiveIntegerField(default=2024)
    reference_code = models.CharField(max_length=30, blank=True, help_text="#KRM-01")
    featured = models.BooleanField(default=False, help_text="Tampil di landing hero/spotlight")
    featured_order = models.PositiveIntegerField(default=0)
    is_spotlight = models.BooleanField(default=False, help_text="Spotlight di halaman proyek (Kroma OS)")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.9)
    rating_count = models.CharField(max_length=20, default="8.1k")
    badge_text = models.CharField(max_length=80, blank=True, help_text="Healthtech Core / Security Tooling")
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    views_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "featured_order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
