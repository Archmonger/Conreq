from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone

from conreq import config
from conreq.app import register
from conreq.internal.sign_up.forms import UserForm
from conreq.internal.sign_up.models import InviteCode

LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")


@register.sign_up_view()
def sign_up_with_invite(request, invite_code):
    # Check if the invite code is valid
    try:
        code: InviteCode = InviteCode.objects.get(code=invite_code)
        if not code.is_valid:
            return redirect("landing")
    except (InviteCode.DoesNotExist, InviteCode.MultipleObjectsReturned):
        return redirect("landing")

    # User submitted the registration form
    if request.method == "POST":
        # Check if form submission is clean
        form = UserForm(request.POST)

        # Submission wasn't valid, so return the error codes
        if not form.is_valid():
            template = loader.get_template(config.sign_up_template)
            return HttpResponse(template.render({"form": form}, request))

        # Create and login the user
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        code.used_by = user
        code.used_at = timezone.now()
        code.save()
        login(request, user)
        return redirect(LOGIN_REDIRECT_URL)

    # User needs to fill out registration form
    template = loader.get_template(config.sign_up_template)
    return HttpResponse(template.render({}, request))
