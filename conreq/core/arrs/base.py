"""Conreq Content Manager: Talks with Sonarr/Radarr in order to add/remove content."""

# Days, Hours, Minutes, Seconds
# Library is refreshed every minute as a background task
# This value is just a fail-safe.
ARR_LIBRARY_CACHE_TIMEOUT = 24 * 60 * 60


class ArrBase:
    """Adds and removes content from Sonarr and Radarr, and can return the request state."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    def _set_content_attributes(content_type, content_source, results):
        # Set a list of results
        if isinstance(results, list):
            for result in results:
                result["content_type"] = content_type
                result["content_source"] = content_source
        # # Set a single media item
        else:
            results["content_type"] = content_type
            results["content_source"] = content_source

    @staticmethod
    def _determine_availability(content: dict):
        """Checks the availability of one item using fuzzy logic."""
        # TODO: Rewrite this into separate methods for Sonarr season, Sonarr series, Radarr movie, etc.
        statistics: dict = content.get("statistics") or content or {}
        percent_available: int | None = statistics.get("percentOfEpisodes")
        monitored: bool | None = statistics.get("monitored") or content.get("monitored")

        ##### "Unavailable" #####
        # Sonarr/Radarr: Check if an individual movie or episode does not exist and isn't monitored
        if content.get("hasFile") is False and not monitored:
            content["availability"] = "Unavailable"
            return
        # Sonarr: Check if a season or series is completely unavailable
        if percent_available == 0 and not monitored:
            content["availability"] = "Unavailable"
            return

        ##### "Available" #####
        # Sonarr: Check if a season or series is fully downloaded
        if percent_available == 100:
            content["availability"] = "Available"
            return
        # Sonarr/Radarr: Check if an individual movie or individual episode exists
        if content.get("hasFile"):
            content["availability"] = "Available"
            return

        ##### "Partial" #####
        # Sonarr: Check if season or series is partially downloaded
        if percent_available and percent_available < 100:
            content["availability"] = "Partial"
            return
        # Sonarr/Radarr: Check if a content is being monitored.
        if monitored:
            content["availability"] = "Partial"
            return

        ##### "Unknown" #####
        # This should never be reached except with Sonarr/Raddarr API changes
        content["availability"] = "Unknown"
        return
