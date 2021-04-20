from conreq.utils.testing import performance_metrics
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def manage_users(request):
    template = loader.get_template("viewport/manage_users.html")
    users = get_user_model().objects.all()
    context = {"users": users}
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def delete_user(request):
    if request.method == "POST":
        try:
            username = request.GET.get("username", None)
            user = get_user_model().objects.get(username=username)
            user.delete()

        except:
            return JsonResponse({"success": False})

        return JsonResponse({"success": True})

    return HttpResponseForbidden()


@login_required
@performance_metrics()
def manage_modal(request):
    template = loader.get_template("modal/manage_user.html")
    username = request.GET.get("username", None)
    user = None
    try:
        user = get_user_model().objects.get(username=username)

    except:
        pass

    context = {"account": user}
    return HttpResponse(template.render(context, request))
