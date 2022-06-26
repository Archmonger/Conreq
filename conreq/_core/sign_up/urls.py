from django.urls import path

from conreq.config import view_wrappers

urlpatterns = [
    path("", view_wrappers.sign_up, name="sign_up"),
    path("<invite_code>", view_wrappers.sign_up, name="sign_up_invite"),
]
