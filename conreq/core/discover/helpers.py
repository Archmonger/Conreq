from conreq.core.tmdb.preset_filters import (
    anime_only_values,
    no_anime_values,
)


def preset_filter_extras(request):
    """Obtains any values that need to be added to a preset filter."""
    filter_type = request.GET.get("type", "")
    if filter_type == "anime":
        return anime_only_values
    if filter_type == "no-anime":
        return no_anime_values
    return ()
