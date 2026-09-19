from .models import SiteProfile


def site_profile(request):
    try:
        profile = SiteProfile.get_solo()
    except Exception:
        profile = None
    return {"site_profile": profile}
