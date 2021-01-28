from conreq.utils.apps import generate_context
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page


# Create your views here.
@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    template = loader.get_template("viewport/manage_users.html")
    users = get_user_model().objects.values()
    context = generate_context({"users": users})
    return HttpResponse(template.render(context, request))
