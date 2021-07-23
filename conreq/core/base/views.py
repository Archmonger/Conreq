from channels.db import database_sync_to_async
from conreq.core.base.forms import InitializationForm
from conreq.core.server_settings.models import ConreqConfig
from conreq.utils.generic import get_base_url, get_debug_from_env
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .helpers import initialize_conreq

base_url = get_base_url()
debug = get_debug_from_env()


# @performance_metrics()
async def main(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""
    conreq_config = await database_sync_to_async(ConreqConfig.get_solo)()
    user_model = await database_sync_to_async(get_user_model)()
    user_objects = user_model.objects

    # Authenticate using Organizr headers
    organizr_username = request.headers.get("X-WEBAUTH-USER")
    if conreq_config.conreq_http_header_auth and organizr_username:
        # Configure the user parameters
        organizr_email = request.headers.get("X-WEBAUTH-EMAIL")
        organizr_group = int(request.headers.get("X-WEBAUTH-GROUP"))
        get_or_create_user = await database_sync_to_async(user_objects.get_or_create)(
            username=organizr_username,
        )
        user = get_or_create_user[0]
        user.email = organizr_email
        user.is_staff = False
        if organizr_group == 0:
            user.is_superuser = True
        if organizr_group == 0 or organizr_group == 1:
            user.is_staff = True
        if user.has_usable_password():
            user.set_unusable_password()
        await database_sync_to_async(user.save)()

        # Make sure the user is labeled as a HTTP auth user
        if not user.profile.externally_authenticated:
            user.profile.externally_authenticated = True
            await database_sync_to_async(user.save)()

        await database_sync_to_async(login)(request, user)

    # Run the first time initialization if needed
    if conreq_config.conreq_initialized is False:

        # User submitted the first time setup form
        if request.method == "POST":

            form = InitializationForm(request.POST)

            # Create the superuser and set up the database if the form is valid
            if await database_sync_to_async(form.is_valid)():
                await database_sync_to_async(form.save)()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = await database_sync_to_async(authenticate)(
                    username=username, password=password
                )
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                await database_sync_to_async(user.save)()
                await database_sync_to_async(login)(request, user)
                await database_sync_to_async(initialize_conreq)(conreq_config, form)
                return redirect("base:index")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(
                await database_sync_to_async(template.render)({"form": form}, request)
            )

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(await database_sync_to_async(template.render)({}, request))

    # Render the base
    return await database_sync_to_async(login_required(render))(
        request, "primary/base_app.html", {"base_url": base_url, "debug": debug}
    )
