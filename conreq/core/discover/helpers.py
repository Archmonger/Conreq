from threading import Thread

from conreq.core.arrs.radarr import RadarrManager
from conreq.core.arrs.sonarr import SonarrManager
from conreq.core.server_settings.models import ConreqConfig
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.tmdb.preset_filters import anime_only_values, no_anime_values
from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list

_logger = log.get_logger(__name__)


def preset_filter_extras(request):
    """Obtains any values that need to be added to a preset filter."""
    filter_type = request.GET.get("type", "")
    if filter_type == "anime":
        return anime_only_values
    if filter_type == "no-anime":
        return no_anime_values
    return ()


def __set_many_availability(card, radarr_library, sonarr_library):
    """Threaded portion of set_many_availability."""
    # TMDB TV card
    if card.__contains__("name"):
        if (
            sonarr_library is not None
            and card.__contains__("tvdb_id")
            and sonarr_library.__contains__(str(card["tvdb_id"]))
        ):
            card["availability"] = sonarr_library[str(card["tvdb_id"])]["availability"]

    # TMDB movie card
    elif card.__contains__("title"):
        if radarr_library is not None and radarr_library.__contains__(str(card["id"])):
            card["availability"] = radarr_library[str(card["id"])]["availability"]


def set_many_availability(results):
    """Sets the availabily on list of cards."""
    # Fetch Sonarr and Radarr libraries
    radarr_library = cache.handler(
        "radarr library",
    )
    sonarr_library = cache.handler(
        "sonarr library",
    )

    # Generate the availability if possible, or get the external ID if a TVDB ID is needed
    thread_list = []
    if isinstance(results, list):
        for card in results:
            thread = Thread(
                target=__set_many_availability,
                args=[card, radarr_library, sonarr_library],
            )
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()
    else:
        log.handler(
            "set_many_availability did not recieve a List!",
            log.WARNING,
            _logger,
        )

    return results


def set_single_availability(card):
    """Sets the availabily on a single card."""
    content_discovery = TmdbDiscovery()
    try:
        # Compute the availability of TV show
        if card.__contains__("name"):
            external_id = content_discovery.get_external_ids(card["id"], "tv")
            content = SonarrManager().get(tvdb_id=external_id["tvdb_id"])
            if content is not None:
                card["availability"] = content["availability"]

        # Compute the availability of movie
        elif card.__contains__("title"):
            content = RadarrManager().get(tmdb_id=card["id"])
            if content is not None:
                card["availability"] = content["availability"]

        # Something unexpected was passed in
        else:
            log.handler(
                "Card did not contain content_type, title, or name!",
                log.WARNING,
                _logger,
            )
            return card

    except:
        log.handler(
            "Could not determine the availability of card!\n" + str(card),
            log.ERROR,
            _logger,
        )
        return card


def obtain_sonarr_parameters(
    tmdb_id=None,
    tvdb_id=None,
):
    """Returns the common parameters needed for adding a series to Sonarr."""
    content_discovery = TmdbDiscovery()
    sonarr_manager = SonarrManager()
    conreq_config = ConreqConfig.get_solo()

    # Attempt to convert TVDB to TMDB if possible
    if tmdb_id is None:
        conversion = content_discovery.get_by_tvdb_id(tvdb_id)
        if conversion.__contains__("tv_results") and conversion["tv_results"]:
            tmdb_id = conversion["tv_results"][0]["id"]

    # Determine series type, root directory, and profile ID
    is_anime = False
    if tmdb_id is not None:
        is_anime = content_discovery.is_anime(tmdb_id, "tv")

    season_folders = conreq_config.sonarr_season_folders
    all_root_dirs = sonarr_manager.sonarr_root_dirs()

    # Generate parameters
    if is_anime:
        series_type = "Anime"
        sonarr_root = is_key_value_in_list(
            "id", conreq_config.sonarr_anime_folder, all_root_dirs, return_item=True
        )["path"]
        sonarr_profile_id = conreq_config.sonarr_anime_quality_profile

    else:
        series_type = "Standard"
        sonarr_root = is_key_value_in_list(
            "id", conreq_config.sonarr_tv_folder, all_root_dirs, return_item=True
        )["path"]
        sonarr_profile_id = conreq_config.sonarr_tv_quality_profile

    return {
        "sonarr_profile_id": sonarr_profile_id,
        "sonarr_root": sonarr_root,
        "series_type": series_type,
        "season_folders": season_folders,
    }


def obtain_radarr_parameters(
    tmdb_id=None,
):
    """Returns the common parameters needed for adding a series to Radarr."""
    content_discovery = TmdbDiscovery()
    radarr_manager = RadarrManager()
    conreq_config = ConreqConfig.get_solo()

    is_anime = content_discovery.is_anime(tmdb_id, "movie")
    all_root_dirs = radarr_manager.radarr_root_dirs()

    if is_anime:
        radarr_root = is_key_value_in_list(
            "id", conreq_config.radarr_anime_folder, all_root_dirs, return_item=True
        )["path"]
        radarr_profile_id = conreq_config.radarr_anime_quality_profile

    else:
        radarr_root = is_key_value_in_list(
            "id", conreq_config.radarr_movies_folder, all_root_dirs, return_item=True
        )["path"]
        radarr_profile_id = conreq_config.radarr_movies_quality_profile

    return {
        "radarr_profile_id": radarr_profile_id,
        "radarr_root": radarr_root,
    }
