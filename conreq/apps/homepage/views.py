import os

from conreq.apps.helpers import generate_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

BASE_URL = SECRET_KEY = os.environ.get("BASE_URL", "")
if isinstance(BASE_URL, str) and BASE_URL and not BASE_URL.endswith("/"):
    BASE_URL = BASE_URL + "/"

# Create your views here.
@login_required
def homepage(request):
    # Redirect the user to the base URL if he came here from "/"
    if request.path[1:] != BASE_URL:
        return redirect("/" + BASE_URL)

    template = loader.get_template("primary/base.html")
    context = generate_context({})
    return HttpResponse(template.render(context, request))
