from django.shortcuts import render
from apps.portfolio.models import Project
from apps.blog.models import Post
from .models import SiteProfile
from .seo import build_meta, json_ld_website, json_ld_person, json_ld_organization, json_ld_breadcrumb, to_jsonld
from django.conf import settings


def landing(request):
    profile = SiteProfile.get_solo()
    featured_projects = Project.objects.filter(status="published", featured=True).select_related("category").prefetch_related("technologies")[:3]
    if not featured_projects:
        featured_projects = Project.objects.filter(status="published").select_related("category").prefetch_related("technologies")[:3]
    featured_posts = Post.objects.filter(status="published", is_featured=True).select_related("category")[:4]
    if not featured_posts:
        featured_posts = Post.objects.filter(status="published").select_related("category")[:4]
    latest_posts = Post.objects.filter(status="published").select_related("category")[:6]

    # SEO & GEO — cover aliases for generative
    seo = build_meta(
        request,
        title="Areybra — Areta Y. Radjawali | Areta Ybei Radjawali | Junior Web Developer & Data Analyst",
        description="Portofolio resmi Areta Y. Radjawali — juga dikenal sebagai Areta Ybei Radjawali / Areybra. Junior Web Developer SMK Nurul Jadid RPL, spesialis Django, Tailwind CSS, MySQL, Linux, Cyber Security & Data Analyst. Jakarta & Probolinggo.",
        keywords="Areta Y Radjawali, Areta Ybei Radjawali, Areybra, AREYBRA, Areta Radjawali, Areybra Studio, Junior Web Developer, Django Developer, SMK Nurul Jadid, Portfolio Django",
        og_image=getattr(settings, "DEFAULT_OG_IMAGE", ""),
        canonical_path=request.path,
    )
    json_ld = to_jsonld(
        json_ld_website(request),
        json_ld_person(),
        json_ld_organization(),
        json_ld_breadcrumb([("Beranda", "/")]),
    )

    return render(request, "pages/landing.html", {
        "profile": profile,
        "featured_projects": featured_projects,
        "featured_posts": featured_posts,
        "latest_posts": latest_posts,
        "seo": seo,
        "json_ld": json_ld,
    })


def tentang_saya(request):
    profile = SiteProfile.get_solo()
    traits = profile.traits.all()
    skill_categories = profile.skill_categories.prefetch_related("skills").all()

    seo = build_meta(
        request,
        title="Tentang Areta Y. Radjawali (Areta Ybei Radjawali / Areybra) — Profil & Keahlian",
        description="Mengenal Areta Y. Radjawali — alias Areta Ybei Radjawali, brand Areybra. Siswa RPL SMK Nurul Jadid, Kab. Probolinggo. Visi: arsitek solusi digital & Data Analyst. Keahlian Django, MySQL, Linux, Cyber Security.",
        keywords="Tentang Areta Y Radjawali, Areta Ybei Radjawali, Areybra, Profil Areybra, SMK Nurul Jadid RPL, Junior Web Developer",
        canonical_path=request.path,
    )
    json_ld = to_jsonld(
        json_ld_person(),
        json_ld_breadcrumb([("Beranda", "/"), ("Tentang Saya", "/tentang-saya/")]),
    )

    return render(request, "pages/tentang_saya.html", {
        "profile": profile,
        "traits": traits,
        "skill_categories": skill_categories,
        "seo": seo,
        "json_ld": json_ld,
    })
