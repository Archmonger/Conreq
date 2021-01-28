from secrets import token_hex

from conreq.utils import cache
from conreq.utils.apps import generate_context
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page


# Create your views here.
@cache_page(60 * 60)
def invite_code(request):
    pass


@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_invite_code(request):
    pass
