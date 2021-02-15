import json
import secrets
from platform import platform

from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from django.views.decorators.cache import cache_page

_logger = log.get_logger(__name__)


@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
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
            log.handler("Failed to obtain Sonarr Quality Profiles!", log.ERROR, _logger)

        # Sonarr Folder Paths
        try:
            for path in content_manger.sonarr_root_dirs():
                # Current anime dirs
                if conreq_config.sonarr_anime_folder == path["id"]:
                    current_sonarr_anime_folder = path["path"]
                # Current TV dirs
                if conreq_config.sonarr_tv_folder == path["id"]:
                    current_sonarr_tv_folder = path["path"]
                # List of all dropdown entries
                sonarr_folders.append({"id": path["id"], "label": path["path"]})
        except:
            log.handler("Failed to obtain Sonarr Folder Paths!", log.ERROR, _logger)

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
            log.handler("Failed to obtain Radarr Quality Profiles!", log.ERROR, _logger)

        # Radarr Folder Paths
        try:
            for path in content_manger.radarr_root_dirs():
                # Current anime movies dirs
                if conreq_config.radarr_anime_folder == path["id"]:
                    current_radarr_anime_folder = path["path"]
                # Current TV dirs
                if conreq_config.radarr_movies_folder == path["id"]:
                    current_radarr_movies_folder = path["path"]
                # List of all dropdown entries
                radarr_folders.append({"id": path["id"], "label": path["path"]})
        except:
            log.handler("Failed to obtain Radarr Folder Paths!", log.ERROR, _logger)

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


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def update_settings(request):
    if request.method == "POST":
        response = {
            "success": True,
        }
        message = json.loads(request.body.decode("utf-8"))
        try:
            # Database values
            conreq_config = ConreqConfig.get_solo()

            # Basic Configuration
            if message["setting_name"] == "Conreq Application Name":
                conreq_config.conreq_app_name = message["value"]

            elif message["setting_name"] == "Conreq Application URL/Web Domain":
                conreq_config.conreq_app_url = message["value"]

            elif message["setting_name"] == "Conreq API Key":
                conreq_config.conreq_api_key = secrets.token_hex(16)
                response["command_name"] = "new conreq api key"
                response["value"] = conreq_config.conreq_api_key

            elif message["setting_name"] == "Conreq Language":
                conreq_config.conreq_language = message["value"]

            elif message["setting_name"] == "Conreq Custom CSS":
                conreq_config.conreq_custom_css = message["value"]

            elif message["setting_name"] == "Conreq Custom JS":
                conreq_config.conreq_custom_js = message["value"]

            elif message["setting_name"] == "Conreq Automatically Resolve Issues":
                conreq_config.conreq_auto_resolve_issues = message["value"]

            elif message["setting_name"] == "Conreq Allow Guest Login/Requests":
                conreq_config.conreq_guest_login = message["value"]

            elif message["setting_name"] == "Conreq Simple/Minimal Poster Cards":
                conreq_config.conreq_simple_posters = message["value"]

            elif message["setting_name"] == "Conreq Dark Theme":
                conreq_config.conreq_dark_theme = message["value"]

            elif message["setting_name"] == "Conreq Organizr User Authentication":
                conreq_config.conreq_http_header_auth = message["value"]

            # Sonarr Settings
            elif message["setting_name"] == "Sonarr URL":
                conreq_config.sonarr_url = message["value"]

            elif message["setting_name"] == "Sonarr API Key":
                conreq_config.sonarr_api_key = message["value"]

            elif message["setting_name"] == "Sonarr Anime Quality Profile":
                conreq_config.sonarr_anime_quality_profile = message["value"]

            elif message["setting_name"] == "Sonarr TV Quality Profile":
                conreq_config.sonarr_tv_quality_profile = message["value"]

            elif message["setting_name"] == "Sonarr Anime Folder Path":
                conreq_config.sonarr_anime_folder = message["value"]

            elif message["setting_name"] == "Sonarr TV Folder Path":
                conreq_config.sonarr_tv_folder = message["value"]

            elif message["setting_name"] == "Enable Sonarr":
                conreq_config.sonarr_enabled = message["value"]

            elif message["setting_name"] == "Sonarr Season Folders":
                conreq_config.sonarr_season_folders = message["value"]

            # Radarr Settings
            elif message["setting_name"] == "Radarr URL":
                conreq_config.radarr_url = message["value"]

            elif message["setting_name"] == "Radarr API Key":
                conreq_config.radarr_api_key = message["value"]

            elif message["setting_name"] == "Radarr Anime Quality Profile":
                conreq_config.radarr_anime_quality_profile = message["value"]

            elif message["setting_name"] == "Radarr Movies Quality Profile":
                conreq_config.radarr_movies_quality_profile = message["value"]

            elif message["setting_name"] == "Radarr Anime Folder Path":
                conreq_config.radarr_anime_folder = message["value"]

            elif message["setting_name"] == "Radarr Movies Folder Path":
                conreq_config.radarr_movies_folder = message["value"]

            elif message["setting_name"] == "Enable Radarr":
                conreq_config.radarr_enabled = message["value"]

            # Unhandled setting failure
            else:
                log.handler(
                    'Server setting "'
                    + message["setting_name"]
                    + '" is currently not handled!',
                    log.WARNING,
                    _logger,
                )
                response["success"] = False
                response["error_message"] = "Unhandled server setting!"
                return JsonResponse(response)

            # Model fails validation schema
            try:
                conreq_config.clean_fields()
            except ValidationError as error:
                for field, message in dict(error).items():
                    response["success"] = False
                    response["error_message"] = field + ": " + message[0]
                    # Send a message to the user
                    return JsonResponse(response)

            # Save the model if it passes all checks
            if response["success"]:
                conreq_config.save()
                log.handler(
                    message,
                    log.INFO,
                    _logger,
                )
                return JsonResponse(response)

        # Unknown exception occured
        except:
            response["success"] = False
            response["error_message"] = "Unknown error!"
            log.handler(
                "Unknown error has occurred within server websocket!",
                log.ERROR,
                _logger,
            )
            return JsonResponse(response)

    return HttpResponseBadRequest()
