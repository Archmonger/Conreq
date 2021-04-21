from conreq.utils.testing import performance_metrics
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def manage_users(request):
    if request.method == "POST":
        # Fetch the user from DB
        original_username = request.POST.get("username_original")
        try:
            user = get_user_model().objects.get(username=original_username)
        except:
            return JsonResponse(
                {
                    "success": False,
                    "message": "User " + original_username + " does not exist!",
                }
            )

        # Password validation
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 and password2:
            if password1 != password2:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Passwords do not match!",
                    }
                )
            try:
                validate_password(password1)
                user.password = password1
            except Exception as error:
                return JsonResponse(
                    {
                        "success": False,
                        "message": " ".join(error),
                    }
                )

        # Set other user fields
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.is_staff = True if request.POST.get("staff") else False

        # Save the user
        try:
            user.clean_fields()
            user.save()
            return JsonResponse({"success": True})
        except Exception as error:
            return JsonResponse(
                {
                    "success": False,
                    "message": str(error),
                }
            )

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
