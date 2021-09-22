from django.shortcuts import render

from conreq.utils.environment import get_base_url

from .apps import PwaConfig

BASE_URL = get_base_url()


def service_worker(request):
    return render(
        request,
        "serviceworker.js",
        {"base_url": BASE_URL},
        content_type="application/javascript",
    )


def manifest(request):
    return render(
        request,
        "site.webmanifest",
        {"pwa": PwaConfig.__dict__},
        content_type="application/json",
    )


def offline(request):
    return render(request, "offline.html")
