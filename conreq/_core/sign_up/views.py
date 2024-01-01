from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils import timezone

from conreq import config
from conreq._core.sign_up.forms import UserForm
from conreq._core.sign_up.models import InviteCode

LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")


# TODO: Add page for invalid invite codes
def sign_up(request, invite_code=None):
    # No invite code was provided
    if not invite_code:
        return redirect("conreq:landing")

    # Check if the invite code is valid
    try:
        code: InviteCode = InviteCode.objects.get(code=invite_code)
        if not code.is_valid:
            # TODO: This should give a meaningful error message
            return redirect("conreq:landing")
    except (
        InviteCode.DoesNotExist,  # pylint: disable=no-member
        InviteCode.MultipleObjectsReturned,  # pylint: disable=no-member
    ):
        return redirect("conreq:landing")

    # User submitted the registration form
    if request.method == "POST":
        # Check if form submission is clean
        form = UserForm(request.POST)

        # Submission wasn't valid, so return the error codes
        if not form.is_valid():
            return render(
                request,
                config.templates.sign_up,
                {"form": form, "initial_email": code.email},
            )

        # Create and login the user
        form.full_clean()
        form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        code.used_by = user  # type: ignore
        code.used_at = timezone.now()
        code.full_clean()
        code.save()
        login(request, user)
        return redirect(LOGIN_REDIRECT_URL)

    # User needs to fill out registration form
    return render(request, config.templates.sign_up, {"initial_email": code.email})
