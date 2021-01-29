from secrets import token_hex

from conreq.utils.apps import generate_context
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.template import loader

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60

# Create your views here.
def invite_code(request):
    template = loader.get_template("registration/sign_up.html")
    context = generate_context({})
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_invite_code(request):
    invite_code_created = False

    # Create an invite code that isn't already active
    while not invite_code_created:
        new_code = token_hex(12)
        cache_key = "invite_code" + new_code

        if cache.get(cache_key) is None:
            cache.set(cache_key, True, INVITE_CODE_DURATION)
            invite_code_created = True

    return JsonResponse({"invite_code": new_code})
