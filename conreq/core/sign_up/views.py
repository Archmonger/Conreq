from secrets import token_hex

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader

from conreq.core.sign_up.forms import UserForm
from conreq.utils.profiling import performance_metrics

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60


@performance_metrics()
def sign_up(request):
    # User submitted the registration form
    invite_code = request.GET.get("invite_code", "")
    invite_key = "invite_code" + invite_code

    if request.method == "POST":
        # Check if the invite code was valid
        if cache.get(invite_key):
            # Check if form submission is clean
            form = UserForm(request.POST)
            if form.is_valid():
                # Remove the invite code, then create & login the user
                cache.delete(invite_key)
                form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("base:landing")

        # Invite code invalid!
        else:
            return redirect("base:landing")

        # Submission wasn't valid, so return the error codes
        template = loader.get_template("registration/sign_up.html")
        return HttpResponse(template.render({"form": form}, request))

    # User needs to fill out registration form, so check if the invite code exists
    if cache.get(invite_key):
        template = loader.get_template("registration/sign_up.html")
        return HttpResponse(template.render({}, request))

    # User tried to use an invalid invite code!
    return redirect("base:landing")


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def generate_invite_code(request):
    # Create an invite code that doesn't already exist
    while True:
        invite_code = token_hex(12)
        cache_key = "invite_code" + invite_code
        if cache.get(cache_key) is None:
            cache.set(cache_key, True, INVITE_CODE_DURATION)
            break

    return JsonResponse({"invite_code": invite_code})
