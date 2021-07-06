from conreq.utils.testing import performance_metrics
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(1)
@login_required
@performance_metrics()
def manage_users(request):
    if request.method == "POST":
        # Ensure non-admins aren't trying to edit other accounts
        original_username = request.POST.get("username_original")
        if not request.user.is_staff and original_username != request.user.username:
            return HttpResponseForbidden()

        # Fetch the user from DB
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
                user.set_password(password1)
            except ValidationError as issues:
                return JsonResponse({"success": False, "message": " ".join(issues)})

        # Set other user fields
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email

        # Fields only modifiable by an admin
        if request.user.is_staff:
            staff_status = request.POST.get("staff")
            if staff_status == "on":
                user.is_staff = True
            elif staff_status == "off":
                user.is_staff = False

        # Save the user
        try:
            user.clean_fields()
            user.save()
            return JsonResponse({"success": True})
        except ValidationError as issues:
            issue_list = list(dict(issues).values())
            issue_list = [item for sublist in issue_list for item in sublist]
            return JsonResponse({"success": False, "message": " ".join(issue_list)})

    # Render the HTTP page
    if request.user.is_staff:
        template = loader.get_template("viewport/manage_users.html")
        users = get_user_model().objects.all()
        context = {"users": users}
        return HttpResponse(template.render(context, request))

    return HttpResponseForbidden()


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
