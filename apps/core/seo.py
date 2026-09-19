"""
SEO & GEO helpers — supports entity aliases for generative search:
Areta Y. Radjawali / Areta Ybei Radjawali / Areybra
"""
import json
from django.conf import settings

ALIASES = ["Areta Y. Radjawali", "Areta Ybei Radjawali", "Areybra", "Areta Radjawali", "AREYBRA Studio"]
PRIMARY_NAME = "Areta Y. Radjawali"
ALIAS_YBEI = "Areta Ybei Radjawali"
BRAND = "Areybra"

def site_url():
    return getattr(settings, "SITE_URL", "https://areybra.vercel.app").rstrip("/")

def absolute_url(path="/"):
    base = site_url()
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return base + path

def build_meta(request, title=None, description=None, keywords=None, og_image=None, og_type="website", canonical_path=None):
    """
    Returns dict for base.html SEO.
    canonical_path: if None, uses request.path
    """
    base = site_url()
    path = canonical_path if canonical_path is not None else request.path
    canonical = absolute_url(path)
    # also handle query trim for canonical
    if "?" in canonical:
        canonical = canonical.split("?")[0]

    default_desc = getattr(settings, "DEFAULT_META_DESCRIPTION", "")
    default_kw = getattr(settings, "DEFAULT_META_KEYWORDS", "")
    default_img = getattr(settings, "DEFAULT_OG_IMAGE", "")

    # ensure alias coverage in description/keywords for GEO
    # append alias hint if not already present
    if description and ALIAS_YBEI not in description and BRAND not in description:
        # keep description clean but ensure one alias mention for generative
        pass

    meta = {
        "title": title or f"{BRAND} — {PRIMARY_NAME} | {ALIAS_YBEI} | Junior Web Developer & Data Analyst",
        "description": description or default_desc,
        "keywords": keywords or default_kw,
        "canonical": canonical,
        "og_title": title or f"{BRAND} — {PRIMARY_NAME}",
        "og_description": description or default_desc,
        "og_image": og_image or default_img,
        "og_url": canonical,
        "og_type": og_type,
        "og_site_name": BRAND,
        "twitter_card": "summary_large_image",
        "robots": "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
        "aliases": ALIASES,
    }
    return meta

def json_ld_website(request):
    base = site_url()
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND,
        "alternateName": ALIASES,
        "url": base + "/",
        "inLanguage": "id-ID",
        "publisher": {"@type": "Organization", "name": BRAND, "url": base + "/"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": base + "/blog/?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }

def json_ld_person():
    base = site_url()
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": PRIMARY_NAME,
        "alternateName": [ALIAS_YBEI, BRAND, "Areta Radjawali"],
        "givenName": "Areta",
        "familyName": "Radjawali",
        "additionalName": "Ybei",
        "disambiguatingDescription": "Junior Web Developer & Data Analyst, SMK Nurul Jadid RPL, juga dikenal sebagai Areybra / Areta Ybei Radjawali",
        "url": base + "/tentang-saya/",
        "image": getattr(settings, "DEFAULT_OG_IMAGE", ""),
        "jobTitle": "Junior Web Development & Data Analyst",
        "affiliation": {"@type": "EducationalOrganization", "name": "SMK Nurul Jadid"},
        "address": {"@type": "PostalAddress", "addressLocality": "Kabupaten Probolinggo", "addressRegion": "Jawa Timur", "addressCountry": "ID"},
        "knowsAbout": ["Django", "Python", "Tailwind CSS", "MySQL", "Linux", "Cyber Security", "Data Analysis", "Web Development"],
        "sameAs": [
            "https://github.com/aretaradjawali",
            "https://linkedin.com/in/areta-y-radjawali",
        ],
        "mainEntityOfPage": base + "/"
    }

def json_ld_organization():
    base = site_url()
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "alternateName": ALIASES[2:],
        "url": base + "/",
        "logo": getattr(settings, "DEFAULT_OG_IMAGE", ""),
        "founder": {"@type": "Person", "name": PRIMARY_NAME, "alternateName": ALIAS_YBEI},
        "description": getattr(settings, "DEFAULT_META_DESCRIPTION", ""),
        "address": {"@type": "PostalAddress", "addressLocality": "Jakarta", "addressCountry": "ID"}
    }

def json_ld_breadcrumb(items):
    """
    items: list of (name, url_path)
    """
    base = site_url()
    lst = []
    for i, (name, path) in enumerate(items, start=1):
        lst.append({"@type": "ListItem", "position": i, "name": name, "item": absolute_url(path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

def json_ld_faq(faqs):
    # faqs: queryset or list of objects with question/answer
    qas = []
    for f in faqs:
        q = getattr(f, "question", str(f[0]) if isinstance(f, (list, tuple)) else "")
        a = getattr(f, "answer", str(f[1]) if isinstance(f, (list, tuple)) else "")
        if q and a:
            qas.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    if not qas:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qas}

def to_jsonld(*objects):
    # filter None
    objs = [o for o in objects if o]
    if len(objs) == 1:
        return json.dumps(objs[0], ensure_ascii=False)
    return json.dumps(objs, ensure_ascii=False)
