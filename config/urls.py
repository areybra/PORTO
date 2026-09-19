from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticSitemap, ProjectSitemap, PostSitemap
from apps.core.views import landing, tentang_saya
from apps.core.views_seo import robots_txt, humans_txt, llms_txt
from apps.portfolio.views import project_list, project_detail
from apps.blog.views import post_list, post_detail
from apps.contact.views import contact_view

sitemaps = {"static": StaticSitemap, "projects": ProjectSitemap, "posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("tentang-saya/", tentang_saya, name="tentang_saya"),
    path("proyek/", project_list, name="project_list"),
    path("proyek/<slug:slug>/", project_detail, name="project_detail"),
    path("blog/", post_list, name="blog_list"),
    path("blog/<slug:slug>/", post_detail, name="blog_detail"),
    path("kontak/", contact_view, name="contact"),
    # SEO / GEO
    path("robots.txt", robots_txt, name="robots_txt"),
    path("humans.txt", humans_txt, name="humans_txt"),
    path("llms.txt", llms_txt, name="llms_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
