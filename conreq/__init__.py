import json
import os

from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.core.search import Search
from conreq.settings import DATA_DIR, DEBUG
from django.core.cache import cache


TMDB_KEY = "112fd4c96274603f68620c78067d5422"

try:
    credentials_file = open(os.path.join(DATA_DIR, "credentials.json"))
    credentials = json.load(credentials_file)
except:
    print("Could not open credentials.json!")
    quit()

try:
    sonarr_url = credentials["sonarr_url"]
    sonarr_key = credentials["sonarr_key"]
    radarr_url = credentials["radarr_url"]
    radarr_key = credentials["radarr_key"]
except:
    raise

content_discovery = ContentDiscovery(TMDB_KEY)
content_manager = ContentManager(sonarr_url, sonarr_key, radarr_url, radarr_key)
searcher = Search(sonarr_url, sonarr_key, radarr_url, radarr_key)
credentials_file.close()

if DEBUG:
    cache.clear()
