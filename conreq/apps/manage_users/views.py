from channels.db import database_sync_to_async as convert_to_async
from conreq.utils.apps import generate_context
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page


# Create your views here.
@convert_to_async
@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    template = loader.get_template("viewport/manage_users.html")
    users = get_user_model().objects.values()
    context = generate_context({"users": users})
    return HttpResponse(template.render(context, request))


@convert_to_async
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request):
    if request.method == "POST":
        try:
            username = request.GET.get("username", None)
            user = get_user_model().objects.get(username=username)

            # Don't allow staff members to delete eachother
            if user.is_staff and not request.user.is_superuser:
                return JsonResponse({"success": False})

            user.delete()

        except:
            return JsonResponse({"success": False})

        return JsonResponse({"success": True})

    return HttpResponseForbidden()
