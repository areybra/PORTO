from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.portfolio.models import Project
from apps.blog.models import Post

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return ["landing", "tentang_saya", "project_list", "blog_list", "contact"]

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Project.objects.filter(status="published")

    def location(self, obj):
        from django.urls import reverse
        return reverse("project_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Post.objects.filter(status="published")

    def location(self, obj):
        from django.urls import reverse
        return reverse("blog_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at
