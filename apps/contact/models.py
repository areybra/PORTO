from django.db import models


class ContactMessage(models.Model):
    DOMAIN_CHOICES = [
        ("web-django", "Pengembangan Web (Django/Tailwind)"),
        ("security-audit", "Audit & Konsultasi Keamanan"),
        ("data-analysis", "Analisis & Visualisasi Data"),
        ("academic", "Undangan Diskusi / Kolaborasi Akademik"),
        ("other", "Eksplorasi Ide / Diskusi Lainnya"),
    ]
    TIMELINE_CHOICES = [
        ("fleksibel", "Jadwal Fleksibel / Tahap Eksplorasi"),
        ("segera", "Segera (1-4 Minggu ke Depan)"),
        ("q2-2025", "Kuartal Q2 (Apr - Jun 2025)"),
        ("q3-2025", "Kuartal Q3 (Jul - Sep 2025)"),
    ]
    SCOPE_CHOICES = [
        ("akademik", "Riset Terbuka / Institusi Pendidikan"),
        ("mvp", "< IDR 5M (Protipe MVP / Audit Skala Kecil)"),
        ("growth", "IDR 5M - 15M (Sistem Penuh / Dashboard)"),
        ("enterprise", "> IDR 15M (Infrastruktur Komprehensif)"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, default="web-django")
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, default="fleksibel")
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default="akademik")
    message = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.name} — {self.get_domain_display()} ({self.created_at:%Y-%m-%d})"

    def build_whatsapp_text(self):
        return (
            f"Halo Areta, saya {self.name} ({self.email})\n"
            f"Domain: {self.get_domain_display()}\n"
            f"Timeline: {self.get_timeline_display()} | Skala: {self.get_scope_display()}\n"
            f"Pesan:\n{self.message}"
        )
