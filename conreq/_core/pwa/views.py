from django.shortcuts import render

from conreq import config
from conreq._core.pwa.apps import PwaConfig


def service_worker(request):
    return render(
        request,
        "conreq/serviceworker.js",
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
