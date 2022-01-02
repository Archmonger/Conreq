from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq import config
from conreq.app import register
from conreq.internal.manage_users.forms import UserEditForm
from conreq.internal.manage_users.tables import UsersTable
from conreq.internal.utils import tab_constructor
from conreq.utils.components import django_to_idom
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)
# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this
# TODO: Protect all of these pages with auth level admin


@django_to_idom(name="edit_user")
class EditUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/manage_users/edit_user.html"
    form_class = UserEditForm
    model = User


@django_to_idom(name="delete_user")
class DeleteUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    model = User


@register.component.manage_users()
@django_to_idom(name="manage_users")
def manage_users(request):
    table = UsersTable(User.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    context = {"table": table}
    return render(request, "conreq/manage_users/user_table.html", context)


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[0] = tab_constructor("Manage Users", manage_users)
