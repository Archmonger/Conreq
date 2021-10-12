from django.urls import path

from conreq import app
from conreq.utils.environment import get_home_url

app_name = "home"

HOME_URL = get_home_url(prepend_slash=False)

urlpatterns = [
    path(HOME_URL, app.config.home_view, name="main"),
]
