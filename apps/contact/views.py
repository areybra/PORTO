from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from urllib.parse import quote
from .forms import ContactMessageForm
from apps.core.models import SiteProfile, FAQ
from apps.core.seo import build_meta, json_ld_breadcrumb, json_ld_faq, json_ld_person, to_jsonld


def contact_view(request):
    profile = SiteProfile.get_solo()
    faqs = FAQ.objects.filter(is_active=True).order_by("order")[:6]

    # SEO & GEO for kontak — include FAQ JSON-LD for generative
    seo = build_meta(
        request,
        title="Kontak Areta Y. Radjawali (Areta Ybei Radjawali / Areybra) — Hubungi via WhatsApp",
        description="Hubungi Areta Y. Radjawali — alias Areta Ybei Radjawali (Areybra). Konsultasi Django, Tailwind, MySQL, Linux, Cyber Security & Data Analyst. WhatsApp 6282142961010, email aretaradjawali@gmail.com. Probolinggo & Jakarta.",
        keywords="Kontak Areybra, Areta Ybei Radjawali Kontak, Areta Y Radjawali WhatsApp 6282142961010, Hubungi Areybra",
        canonical_path=request.path,
    )
    json_ld = to_jsonld(
        json_ld_person(),
        json_ld_breadcrumb([("Beranda", "/"), ("Kontak", "/kontak/")]),
        json_ld_faq(faqs),
        {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": "Kontak Areta Y. Radjawali — Areybra",
            "description": "Form kontak → WhatsApp 6282142961010",
            "url": getattr(settings, "SITE_URL", "https://areybra.vercel.app") + "/kontak/",
        }
    )

    if request.method == "POST":
        if request.POST.get("footer_subscribe"):
            email = request.POST.get("email", "").strip()
            if email:
                from .models import ContactMessage
                msg = ContactMessage.objects.create(
                    name="Subscriber",
                    email=email,
                    domain="other",
                    message="Permintaan konsultasi via footer subscribe",
                )
                messages.success(request, "Terima kasih! Tim akan menghubungi via email.")
                wa = getattr(settings, "WHATSAPP_NUMBER", profile.whatsapp_number)
                text = quote(f"Halo Areta (Areybra), saya tertarik konsultasi. Email saya {email}. Mohon info lanjut.")
                return redirect(f"https://wa.me/{wa}?text={text}")
            messages.error(request, "Email tidak valid.")
            return redirect("contact")

        form = ContactMessageForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Pesan berhasil dikirim! Mengalihkan ke WhatsApp...")
            wa = getattr(settings, "WHATSAPP_NUMBER", profile.whatsapp_number)
            text = quote(obj.build_whatsapp_text())
            wa_url = f"https://wa.me/{wa}?text={text}"
            obj.whatsapp_sent = True
            obj.save(update_fields=["whatsapp_sent"])
            return redirect(wa_url)
        else:
            messages.error(request, "Periksa kembali isian form.")
    else:
        form = ContactMessageForm()

    return render(request, "pages/kontak.html", {"form": form, "profile": profile, "faqs": faqs, "seo": seo, "json_ld": json_ld})
