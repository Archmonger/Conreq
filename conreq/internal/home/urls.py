from django.urls import path

import conreq
from conreq.utils.environment import get_home_url

app_name = "home"

HOME_URL = get_home_url(append_slash=False, prepend_slash=False)

urlpatterns = [
    path(HOME_URL, conreq.config.home_view, name="home"),
]
