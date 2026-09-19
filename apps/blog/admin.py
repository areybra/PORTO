from django.contrib import admin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "is_featured", "status", "read_time", "published_at", "image_preview"]
    list_filter = ["category", "status", "is_featured"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_featured", "status"]
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at", "image_preview"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "tags", "excerpt", "content", "read_time", "is_featured", "featured_order")}),
        ("Gambar (URL - hemat storage)", {"fields": ("cover_url", "image_preview"), "description": 'Tempel URL cover (https://...).'}),
        ("Meta", {"fields": ("status", "published_at", "views_count", "created_at", "updated_at")}),
    )

    def image_preview(self, obj):
        url = obj.image_url if obj and obj.pk else ""
        if url:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height:120px; border-radius:12px;" /><br><a href="{}" target="_blank" style="font-size:11px; word-break:break-all;">{}</a>', url, url, url)
        return "— tanpa cover —"
    image_preview.short_description = "Preview"
