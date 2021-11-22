from django.urls import path

import conreq
from conreq.utils.environment import get_home_url

app_name = "landing"

HOME_URL = get_home_url(prepend_slash=False)

urlpatterns = [
    path("", conreq.config.landing_view, name="landing"),
]
