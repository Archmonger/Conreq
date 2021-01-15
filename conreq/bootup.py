from conreq.apps.settings.models import ConreqConfig
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.core.search import Search

TMDB_KEY = "112fd4c96274603f68620c78067d5422"

conreq_config = ConreqConfig.get_solo()

sonarr_url = conreq_config.sonarr_url
sonarr_key = conreq_config.sonarr_api_key
radarr_url = conreq_config.radarr_url
radarr_key = conreq_config.radarr_api_key

content_discovery = ContentDiscovery()
content_manager = ContentManager(sonarr_url, sonarr_key, radarr_url, radarr_key)
searcher = Search(sonarr_url, sonarr_key, radarr_url, radarr_key)
