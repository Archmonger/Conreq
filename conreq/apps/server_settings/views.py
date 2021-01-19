# from django.shortcuts import render
from platform import platform

from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_manager import ContentManager
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_staff)
def server_settings(request):
    template = loader.get_template("viewport/server_settings.html")

    # Database values
    conreq_config = ConreqConfig.get_solo()

    # Obtain sonarr and radarr information
    content_manger = ContentManager()

    # Sonarr Anime Quality Profiles
    sonarr_quality_profiles = []
    current_sonarr_quality_profile = ""
    for profile in content_manger.sonarr_quality_profiles():
        if conreq_config.sonarr_anime_quality_profile == profile["id"]:
            current_sonarr_quality_profile = profile["name"]
        sonarr_quality_profiles.append({"id": profile["id"], "label": profile["name"]})

    context = {
        "os_platform": platform(),
        "sonarr_quality_profiles": sonarr_quality_profiles,
        "current_sonarr_quality_profile": current_sonarr_quality_profile,
    }

    return HttpResponse(template.render(context, request))
