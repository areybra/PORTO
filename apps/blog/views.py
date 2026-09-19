from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category
from apps.core.seo import build_meta, json_ld_breadcrumb, json_ld_person, to_jsonld
from django.conf import settings

def post_list(request):
    qs = Post.objects.filter(status="published").select_related("category").prefetch_related("tags")
    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category")

    if category_slug and category_slug != "all":
        qs = qs.filter(category__slug=category_slug)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))

    featured = qs.filter(is_featured=True).first()
    if featured:
        qs_rest = qs.exclude(pk=featured.pk)
    else:
        qs_rest = qs

    paginator = Paginator(qs_rest, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    from django.db.models import Count
    from django.db.models.functions import ExtractYear
    archive = Post.objects.filter(status="published").annotate(year=ExtractYear("published_at")).values("year").annotate(count=Count("id")).order_by("-year")

    seo = build_meta(
        request,
        title="Blog Areta Y. Radjawali (Areybra) — Wawasan Kode, Keamanan Siber & Data",
        description="Esai Areta Y. Radjawali / Areta Ybei Radjawali (Areybra): Django anti-brute force, SQL injection, Linux VPS hardening, Pandas telemetri, tipografi editorial. 18 naskah kolektif.",
        keywords="Blog Areybra, Areta Ybei Radjawali Blog, Areta Y Radjawali, Django Blog, Cyber Security",
        canonical_path=request.path,
    )
    json_ld = to_jsonld(
        json_ld_breadcrumb([("Beranda", "/"), ("Blog", "/blog/")]),
        json_ld_person(),
    )

    return render(request, "pages/blog_list.html", {
        "featured": featured,
        "page_obj": page_obj,
        "categories": categories,
        "q": q,
        "category_slug": category_slug or "all",
        "archive": archive,
        "total_count": Post.objects.filter(status="published").count(),
        "seo": seo,
        "json_ld": json_ld,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("category").prefetch_related("tags"), slug=slug, status="published")
    Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)
    related = Post.objects.filter(status="published").exclude(pk=post.pk)
    if post.category:
        related = related.filter(category=post.category)[:3]
    else:
        related = related[:3]

    seo = build_meta(
        request,
        title=f"{post.title} — Esai Areta Y. Radjawali (Areybra)",
        description=post.excerpt[:160] if post.excerpt else post.content[:160],
        keywords=f"{post.title}, Areta Ybei Radjawali, Areybra, {post.category.name if post.category else ''}",
        og_image=post.image_url or getattr(settings, "DEFAULT_OG_IMAGE", ""),
        og_type="article",
        canonical_path=request.path,
    )
    base = getattr(settings, "SITE_URL", "https://areybra.vercel.app")
    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt,
        "author": {"@type": "Person", "name": "Areta Y. Radjawali", "alternateName": ["Areta Ybei Radjawali", "Areybra"]},
        "publisher": {"@type": "Organization", "name": "Areybra", "logo": {"@type": "ImageObject", "url": getattr(settings, "DEFAULT_OG_IMAGE", "")}},
        "datePublished": post.published_at.isoformat() if post.published_at else post.created_at.isoformat(),
        "dateModified": post.updated_at.isoformat() if post.updated_at else post.created_at.isoformat(),
        "image": post.image_url or getattr(settings, "DEFAULT_OG_IMAGE", ""),
        "mainEntityOfPage": base + request.path,
        "keywords": ", ".join([t.name for t in post.tags.all()]),
        "inLanguage": "id-ID",
    }
    json_ld = to_jsonld(
        article,
        json_ld_breadcrumb([("Beranda", "/"), ("Blog", "/blog/"), (post.title, request.path)]),
    )
    return render(request, "pages/blog_detail.html", {"post": post, "related": related, "seo": seo, "json_ld": json_ld})
