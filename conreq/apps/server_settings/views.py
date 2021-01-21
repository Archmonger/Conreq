# from django.shortcuts import render
from platform import platform

from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader

__logger = log.get_logger(__name__)

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_staff)
def server_settings(request):
    template = loader.get_template("viewport/server_settings.html")

    # Database values
    conreq_config = ConreqConfig.get_solo()

    # Obtain sonarr and radarr information
    content_manger = ContentManager()
    sonarr_quality_profiles = []
    current_sonarr_anime_quality_profile = ""
    current_sonarr_tv_quality_profile = ""
    sonarr_folders = []
    current_sonarr_anime_folder = ""
    current_sonarr_tv_folder = ""
    radarr_quality_profiles = []
    current_radarr_anime_quality_profile = ""
    current_radarr_movies_quality_profile = ""
    radarr_folders = []
    current_radarr_anime_folder = ""
    current_radarr_movies_folder = ""

    if conreq_config.sonarr_enabled:
        # Sonarr Quality Profiles
        try:
            for profile in content_manger.sonarr_quality_profiles():
                # Current anime profile
                if conreq_config.sonarr_anime_quality_profile == profile["id"]:
                    current_sonarr_anime_quality_profile = profile["name"]
                # Current TV profile
                if conreq_config.sonarr_tv_quality_profile == profile["id"]:
                    current_sonarr_tv_quality_profile = profile["name"]
                # List of all dropdown entries
                sonarr_quality_profiles.append(
                    {"id": profile["id"], "label": profile["name"]}
                )
        except:
            log.handler(
                "Failed to obtain Sonarr Quality Profiles!", log.ERROR, __logger
            )

        # Sonarr Folder Paths
        try:
            for path in content_manger.sonarr_root_dirs():
                # Current anime dirs
                if conreq_config.sonarr_anime_folder == path["id"]:
                    current_sonarr_anime_folder = path["path"]
                # Current TV dirs
                if conreq_config.sonarr_anime_folder == path["id"]:
                    current_sonarr_tv_folder = path["path"]
                # List of all dropdown entries
                sonarr_folders.append({"id": path["id"], "label": path["path"]})
        except:
            log.handler("Failed to obtain Sonarr Folder Paths!", log.ERROR, __logger)

    if conreq_config.radarr_enabled:
        # Radarr Quality Profiles
        try:
            for profile in content_manger.radarr_quality_profiles():
                # Current anime movies profile
                if conreq_config.radarr_anime_quality_profile == profile["id"]:
                    current_radarr_anime_quality_profile = profile["name"]
                # Current TV profile
                if conreq_config.radarr_movies_quality_profile == profile["id"]:
                    current_radarr_movies_quality_profile = profile["name"]
                # List of all dropdown entries
                radarr_quality_profiles.append(
                    {"id": profile["id"], "label": profile["name"]}
                )
        except:
            log.handler(
                "Failed to obtain Radarr Quality Profiles!", log.ERROR, __logger
            )

        # Radarr Folder Paths
        try:
            for path in content_manger.radarr_root_dirs():
                # Current anime movies dirs
                if conreq_config.radarr_anime_folder == path["id"]:
                    current_radarr_anime_folder = path["path"]
                # Current TV dirs
                if conreq_config.radarr_anime_folder == path["id"]:
                    current_radarr_movies_folder = path["path"]
                # List of all dropdown entries
                radarr_folders.append({"id": path["id"], "label": path["path"]})
        except:
            log.handler("Failed to obtain Radarr Folder Paths!", log.ERROR, __logger)

    context = {
        "os_platform": platform(),
        "sonarr_quality_profiles": sonarr_quality_profiles,
        "current_sonarr_anime_quality_profile": current_sonarr_anime_quality_profile,
        "current_sonarr_tv_quality_profile": current_sonarr_tv_quality_profile,
        "sonarr_folders": sonarr_folders,
        "current_sonarr_anime_folder": current_sonarr_anime_folder,
        "current_sonarr_tv_folder": current_sonarr_tv_folder,
        "radarr_quality_profiles": radarr_quality_profiles,
        "current_radarr_anime_quality_profile": current_radarr_anime_quality_profile,
        "current_radarr_movies_quality_profile": current_radarr_movies_quality_profile,
        "radarr_folders": radarr_folders,
        "current_radarr_anime_folder": current_radarr_anime_folder,
        "current_radarr_movies_folder": current_radarr_movies_folder,
    }

    return HttpResponse(template.render(context, request))
