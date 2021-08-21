import json
from platform import platform

from conreq.core.server_settings.models import ConreqConfig
from conreq.utils import log
from conreq.utils.debug import performance_metrics
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader

_logger = log.get_logger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def server_settings(request):
    template = loader.get_template("viewport/server_settings.html")
    context = {"os_platform": platform()}
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
            if message["setting_name"] == "Conreq Custom CSS":
                conreq_config.conreq_custom_css = message["value"]

            elif message["setting_name"] == "Conreq Custom JS":
                conreq_config.conreq_custom_js = message["value"]

            elif message["setting_name"] == "Conreq Automatically Resolve Issues":
                conreq_config.conreq_auto_resolve_issues = message["value"]

            elif message["setting_name"] == "Conreq Allow TV Specials":
                conreq_config.conreq_allow_tv_specials = message["value"]

            elif message["setting_name"] == "Conreq Simple/Minimal Poster Cards":
                conreq_config.conreq_simple_posters = message["value"]

            elif message["setting_name"] == "Conreq HTTP Auth":
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
