"""Conreq URL Configuration"""


from django.urls import include, path
from django.views.generic.base import RedirectView

from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)
HOME_URL = get_home_url(prepend_slash=False)

external_urls = [
    path("reactpy/", include("reactpy_django.http.urls")),
]
"""Any URL patterns not contained within the Conreq namespace, such as URLs made by user apps or external packages."""

urlpatterns = [
    path(
        BASE_URL, include("conreq._core.base.urls", namespace="conreq"), name="base_url"
    ),
    path(BASE_URL, include(external_urls)),
]
"""Conreq's root URL configuration."""


if BASE_URL:
    urlpatterns.insert(0, path("", RedirectView.as_view(url=BASE_URL)))  # type: ignore
