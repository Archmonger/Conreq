# from django.shortcuts import render
from platform import platform

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def server_settings(request):
    template = loader.get_template("viewport/server_settings.html")

    context = {"os_platform": platform()}

    return HttpResponse(template.render(context, request))
