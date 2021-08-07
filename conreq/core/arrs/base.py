"""Conreq Content Manager: Talks with Sonarr/Radarr in order to add/remove content."""

# Days, Hours, Minutes, Seconds
# Library is refreshed every minute as a background task
# This value is just a fail-safe.
ARR_LIBRARY_CACHE_TIMEOUT = 24 * 60 * 60


class ArrBase:
    """Adds and removes content from Sonarr and Radarr, and can return the request state."""

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
    def _check_availability(content):
        """Checks the availability of one item. For use within check_availability()"""
        #####################
        ### "Unavailable" ###
        #####################
        # Check if an individual movie or episode does not exist (Sonarr and Radarr)
        try:
            if not content["hasFile"]:
                content["availability"] = "Unavailable"
                return content
        except:
            pass

        # Check if a season or series is completely unavailable (Sonarr)
        try:
            if content["episodeFileCount"] == 0:
                content["availability"] = "Unavailable"
                return content
        except:
            pass

        #################
        ### "Partial" ###
        #################
        # Check if season or series is partially downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] < content["episodeCount"]
                ):
                    content["availability"] = "Partial"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] > content["episodeCount"]
            ):
                content["availability"] = "Partial"
                return content
        except:
            pass

        ###################
        ### "Available" ###
        ###################
        # Check if a season is fully downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] >= content["episodeCount"]
                ):
                    content["availability"] = "Available"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] <= content["episodeCount"]
            ):
                content["availability"] = "Available"
                return content
        except:
            pass

        # Check if an individual movie or individual episode exists (Sonarr & Radarr)
        try:
            if content["hasFile"]:
                content["availability"] = "Available"
                return content
        except:
            pass

        content["availability"] = "Unknown"
        return content
