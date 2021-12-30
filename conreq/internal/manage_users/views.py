from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq.app import register
from conreq.internal.manage_users.forms import UserEditForm
from conreq.internal.manage_users.tables import UsersTable
from conreq.utils.components import django_to_idom
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)
# TODO: Create SimpleTable and SimpleForm abstractions
# TODO: Figure out some way to integrate user invites into this


class UserEditView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/manage_users/edit_user.html"
    form_class = UserEditForm
    model = User


class UserDeleteView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/manage_users/delete_user_confirm.html"
    model = User


@register.homepage.nav_tab("Manage Users", "Admin")
@register.component.manage_users()
@django_to_idom()
def manage_users(request):
    if request.GET.get("edit"):
        return UserEditView.as_view()(request)

    if request.GET.get("delete"):
        return UserDeleteView.as_view()(request)

    table = UsersTable(User.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    context = {"table": table}
    return render(request, "conreq/manage_users/user_table.html", context)
