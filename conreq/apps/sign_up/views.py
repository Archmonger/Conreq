from secrets import token_hex

from conreq.apps.sign_up.forms import UserForm
from conreq.utils.apps import generate_context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.template import loader

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60

# Create your views here.
def invite(request):
    # User submitted the registration form
    if request.method == "POST":
        form = UserForm(request.POST)

        # Create the user
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            user.save()
            login(request, user)
            return redirect("homepage:index")

        # Form data wasn't valid, so return the error codes
        template = loader.get_template("registration/sign_up.html")
        return HttpResponse(template.render({"form": form}, request))

    # User needs to fill out registration form, so check if the invite code exists
    invite_code = request.GET.get("invite_code", None)
    cache_key = "invite_code" + invite_code
    if invite_code is not None and cache.get(cache_key) is not None:
        template = loader.get_template("registration/sign_up.html")
        context = generate_context({})
        return HttpResponse(template.render(context, request))

    # User tried to use an invalid invite code!
    return HttpResponseForbidden()


@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_invite_code(request):
    invite_code_created = False

    # Create an invite code that isn't already active
    while not invite_code_created:
        invite_code = token_hex(12)
        cache_key = "invite_code" + invite_code

        if cache.get(cache_key) is None:
            cache.set(cache_key, True, INVITE_CODE_DURATION)
            invite_code_created = True

    return JsonResponse({"invite_code": invite_code})
