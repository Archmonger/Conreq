import json
from platform import platform

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader

from conreq.core.server_settings.models import ConreqConfig
from conreq.utils import log
from conreq.utils.debug import performance_metrics

_logger = log.get_logger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def server_settings(request):
    template = loader.get_template("viewport/server_settings.html")
    context = {"os_platform": platform()}
    return HttpResponse(template.render(context, request))
