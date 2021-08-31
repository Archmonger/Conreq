from django.urls import path

from conreq import app
from conreq.utils.environment import get_home_url

app_name = "landing"

HOME_URL = get_home_url(prepend_slash=False)

urlpatterns = [
    path("", app.config.landing_view, name="main"),
]
