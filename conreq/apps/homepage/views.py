from conreq.apps.helpers import generate_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
def homepage(request):
    template = loader.get_template("primary/base.html")
    context = generate_context({})
    return HttpResponse(template.render(context, request))
