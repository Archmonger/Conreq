from django.shortcuts import render

from conreq.utils.environment import get_base_url

from . import apps

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
        "manifest.json",
        {
            setting_name: getattr(apps, setting_name)
            for setting_name in dir(apps)
            if setting_name.startswith("PWA_")
        },
        content_type="application/json",
    )


def offline(request):
    return render(request, "offline.html")
