"""Helpers for Base"""


def initialize_conreq(conreq_config, form):
    """Sets up the initial database values during Conreq's first run sequence."""
    # Obtain the sonarr/radarr parameters
    conreq_config.sonarr_url = form.cleaned_data.get("sonarr_url")
    conreq_config.sonarr_api_key = form.cleaned_data.get("sonarr_api_key")
    conreq_config.radarr_url = form.cleaned_data.get("radarr_url")
    conreq_config.radarr_api_key = form.cleaned_data.get("radarr_api_key")

    # Enable Sonarr if URL and API key is configured
    if conreq_config.sonarr_url and conreq_config.sonarr_api_key:
        conreq_config.sonarr_enabled = True

    # Enable Radarr if URL and API key is configured
    if conreq_config.radarr_url and conreq_config.radarr_api_key:
        conreq_config.radarr_enabled = True

    # Remember that the database has been initialized
    conreq_config.conreq_initialized = True
    conreq_config.save()
