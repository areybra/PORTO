from django.contrib import admin
from .models import Category, Technology, Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "year", "featured", "is_spotlight", "status", "views_count", "image_preview"]
    list_filter = ["category", "status", "featured", "is_spotlight", "year"]
    search_fields = ["title", "reference_code"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["featured", "is_spotlight", "status"]
    filter_horizontal = ["technologies"]
    readonly_fields = ["created_at", "updated_at", "image_preview"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "technologies", "excerpt", "description")}),
        ("Gambar (URL - hemat storage)", {"fields": ("thumbnail_url", "image_preview", "mock_type"), "description": 'Tempel URL gambar (https://...). Contoh: https://lh3.googleusercontent.com/... atau https://images.unsplash.com/...'}),
        ("Meta", {"fields": ("year", "reference_code", "badge_text", "rating", "rating_count", "featured", "featured_order", "is_spotlight", "github_url", "demo_url", "status", "views_count", "created_at", "updated_at")}),
    )

    def image_preview(self, obj):
        url = obj.image_url if obj and obj.pk else ""
        if url:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height:120px; border-radius:12px;" /><br><a href="{}" target="_blank" style="font-size:11px; word-break:break-all;">{}</a>', url, url, url)
        return "— pakai placeholder SVG —"
    image_preview.short_description = "Preview"
