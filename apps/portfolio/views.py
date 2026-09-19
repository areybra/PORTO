from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, Category
from apps.core.seo import build_meta, json_ld_breadcrumb, json_ld_person, to_jsonld
from django.conf import settings

def project_list(request):
    qs = Project.objects.filter(status="published").select_related("category").prefetch_related("technologies")
    category_slug = request.GET.get("category")
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")

    if category_slug and category_slug != "all":
        qs = qs.filter(category__slug=category_slug)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(description__icontains=q))

    if sort == "popular":
        qs = qs.order_by("-views_count", "-created_at")
    elif sort == "complexity":
        qs = qs.order_by("-technologies__id")
    else:
        qs = qs.order_by("-featured", "featured_order", "-created_at")

    spotlight = qs.filter(is_spotlight=True).first()
    if spotlight:
        qs = qs.exclude(pk=spotlight.pk)

    paginator = Paginator(qs, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    seo = build_meta(
        request,
        title="Proyek Areta Y. Radjawali (Areybra) — Django, MySQL, Linux & Data",
        description="Arsip karya Areta Y. Radjawali / Areta Ybei Radjawali (Areybra) — 36 dokumen: Django & Tailwind, MySQL clustering, Linux VPS, Cyber Security, Data Science. Lihat studi kasus Kroma OS, Aura Health, Sentinel Shield.",
        keywords="Proyek Areybra, Areta Y Radjawali Project, Areta Ybei Radjawali, Django Portfolio, MySQL, Linux",
        canonical_path=request.path,
    )
    json_ld = to_jsonld(
        json_ld_breadcrumb([("Beranda", "/"), ("Proyek", "/proyek/")]),
        json_ld_person(),
    )

    return render(request, "pages/proyek_list.html", {
        "spotlight": spotlight,
        "page_obj": page_obj,
        "categories": categories,
        "q": q,
        "category_slug": category_slug or "all",
        "sort": sort,
        "seo": seo,
        "json_ld": json_ld,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.select_related("category").prefetch_related("technologies"), slug=slug, status="published")
    Project.objects.filter(pk=project.pk).update(views_count=project.views_count + 1)
    related = Project.objects.filter(status="published").exclude(pk=project.pk)
    if project.category:
        related = related.filter(category=project.category)[:3]
    else:
        related = related[:3]

    # SEO per project
    seo = build_meta(
        request,
        title=f"{project.title} — Proyek Areta Y. Radjawali (Areybra)",
        description=(project.excerpt or project.description)[:160],
        keywords=f"{project.title}, Areta Y Radjawali, Areybra, {project.category.name if project.category else ''}, {', '.join([t.name for t in project.technologies.all()[:3]])}",
        og_image=project.image_url or getattr(settings, "DEFAULT_OG_IMAGE", ""),
        og_type="article",
        canonical_path=request.path,
    )
    # JSON-LD CreativeWork
    base = getattr(settings, "SITE_URL", "https://areybra.vercel.app")
    creative = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": project.title,
        "description": project.excerpt or project.description[:200],
        "author": {"@type": "Person", "name": "Areta Y. Radjawali", "alternateName": "Areta Ybei Radjawali"},
        "publisher": {"@type": "Organization", "name": "Areybra"},
        "datePublished": project.created_at.isoformat() if project.created_at else None,
        "image": project.image_url or getattr(settings, "DEFAULT_OG_IMAGE", ""),
        "url": base + request.path,
        "keywords": ", ".join([t.name for t in project.technologies.all()]),
    }
    json_ld = to_jsonld(
        creative,
        json_ld_breadcrumb([("Beranda", "/"), ("Proyek", "/proyek/"), (project.title, request.path)]),
    )
    return render(request, "pages/proyek_detail.html", {"project": project, "related": related, "seo": seo, "json_ld": json_ld})
