from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote
from django.conf import settings
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "domain", "timeline", "scope", "is_read", "whatsapp_link", "created_at"]
    list_filter = ["domain", "timeline", "scope", "is_read", "whatsapp_sent"]
    search_fields = ["name", "email", "message"]
    list_editable = ["is_read"]
    readonly_fields = ["created_at", "whatsapp_link_display"]
    date_hierarchy = "created_at"

    def whatsapp_link(self, obj):
        wa = getattr(settings, "WHATSAPP_NUMBER", "6282142961010")
        text = quote(obj.build_whatsapp_text())
        url = f"https://wa.me/{wa}?text={text}"
        return format_html('<a href="{}" target="_blank">Buka WA</a>', url)

    whatsapp_link.short_description = "WhatsApp"

    def whatsapp_link_display(self, obj):
        return self.whatsapp_link(obj)

    whatsapp_link_display.short_description = "WhatsApp Link"
