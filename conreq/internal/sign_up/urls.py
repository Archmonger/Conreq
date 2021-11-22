from django.urls import path

from .views import sign_up

app_name = "sign_up"

urlpatterns = [
    path("", sign_up, name="sign_up"),
]
