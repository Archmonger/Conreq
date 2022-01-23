from django.urls import path

from conreq import config

urlpatterns = [
    path("", config.views.sign_up, name="sign_up"),
    path("<invite_code>", config.views.sign_up, name="sign_up_invite"),
]
