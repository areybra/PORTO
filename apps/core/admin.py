from django.contrib import admin
from .models import SiteProfile, SocialLink, Service, Trait, SkillCategory, Skill, FAQ


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ["site_name", "hero_name", "email", "whatsapp_number", "hero_preview"]
    readonly_fields = ["hero_preview"]
    inlines = [SocialLinkInline, ServiceInline, FAQInline]
    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "email", "whatsapp_number", "location", "timezone_label", "availability_text", "availability_active", "footer_description")}),
        ("Hero / Foto Profil", {"fields": ("hero_name", "hero_title", "hero_description", "hero_image_url", "hero_preview", "cv_file"), "description": "Gunakan URL gambar (https://...) untuk hemat storage. Preview akan muncul dibawah."}),
        ("Tentang", {"fields": ("about_quote", "about_vision", "github_username", "linkedin_url", "github_url", "dribbble_url", "readcv_url")}),
    )

    def hero_preview(self, obj):
        url = obj.hero_image_effective if obj and obj.pk else ""
        if url:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height:120px; border-radius:12px; border:1px solid #e3e2e3;" /><br><a href="{}" target="_blank" style="font-size:11px;">{}</a>', url, url, url)
        return "— belum ada foto —"
    hero_preview.short_description = "Preview Foto"


@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ["title", "label", "profile", "order", "color"]
    list_editable = ["order"]
    list_filter = ["profile"]


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "profile", "order", "domain_label"]
    list_editable = ["order"]
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "level", "order"]
    list_filter = ["category", "level"]
    list_editable = ["order", "level"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "profile", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["label", "platform", "profile", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "profile", "order"]
    list_editable = ["order"]
