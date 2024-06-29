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
    def _check_availability(content: dict):
        """Checks the availability of one item. For use within check_availability()"""
        statistics: dict = content.get("statistics", {})
        percent_available: int | None = statistics.get("percentOfEpisodes")
        grabbed: bool | None = statistics.get("grabbed")

        ##### "Unavailable" #####
        # Sonarr/Radarr: Check if an individual movie or episode does not exist
        if "hasFile" in content and not content["hasFile"]:
            content["availability"] = "Unavailable"
            return content
        # Sonarr: Check if a season or series is completely unavailable
        if statistics and percent_available == 0:
            content["availability"] = "Unavailable"
            return content

        ##### "Partial" #####
        # Sonarr: Check if season or series is partially downloaded
        if statistics and percent_available and percent_available < 100:
            content["availability"] = "Partial"
            return content
        # Radarr: Check if a movie is being downloaded.
        if grabbed is True and statistics and statistics.get("movieFileCount") == 0:
            content["availability"] = "Partial"
            return content

        ##### "Available" #####
        # Sonarr: Check if a season or series is fully downloaded
        if statistics and percent_available == 100:
            content["availability"] = "Available"
            return content
        # Sonarr/Radarr: Check if an individual movie or individual episode exists
        if "hasFile" in content and content["hasFile"]:
            content["availability"] = "Available"
            return content

        ##### "Unknown" #####
        # This should never be reached except with Sonarr/Raddarr API changes
        content["availability"] = "Unknown"
        return content
