from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils import timezone

from conreq import config
from conreq._core.sign_up.forms import UserForm
from conreq._core.sign_up.models import InviteCode
from conreq.app import register

LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")


@register.view.sign_up()
def sign_up(request, invite_code=None):
    # No invite code was provided
    if not invite_code:
        return redirect("landing")

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
            return render(request, config.templates.sign_up, {"form": form})

        # Create and login the user
        form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        code.used_by = user
        code.used_at = timezone.now()
        code.save()
        login(request, user)
        return redirect(LOGIN_REDIRECT_URL)

    # User needs to fill out registration form
    return render(request, config.templates.sign_up)
