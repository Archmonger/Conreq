from django.urls import path

from conreq.config.wrappers import views

urlpatterns = [
    path("", views.sign_up, name="sign_up"),
    path("<invite_code>", views.sign_up, name="sign_up_invite"),
]
