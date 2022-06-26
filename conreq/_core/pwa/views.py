from django.shortcuts import render

from conreq import config
from conreq._core.pwa.apps import PwaConfig
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url()


def service_worker(request):
    return render(
        request,
        "conreq/serviceworker.js",
        {"base_url": BASE_URL},
        content_type="application/javascript",
    )


def web_manifest(request):
    return render(
        request,
        "conreq/site.webmanifest",
        {"pwa": PwaConfig.__dict__},
        content_type="application/manifest+json",
    )


def offline(request):
    return render(request, config.templates.offline)
