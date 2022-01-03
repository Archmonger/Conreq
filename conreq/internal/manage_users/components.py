from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq import config
from conreq.app import register
from conreq.app.selectors import AuthLevel
from conreq.internal.manage_users.forms import UserEditForm
from conreq.internal.manage_users.tables import UsersTable
from conreq.internal.utils import tab_constructor
from conreq.utils.components import tabbed_viewport, view_to_component
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin, stub

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)
# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this
# TODO: Protect all of these pages with auth level admin


@view_to_component(name="edit_user", auth_level=AuthLevel.admin)
class EditUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/manage_users/edit_user.html"
    form_class = UserEditForm
    model = User


@view_to_component(name="delete_user", auth_level=AuthLevel.admin)
class DeleteUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    model = User


@register.component.manage_users()
@view_to_component(name="manage_users", auth_level=AuthLevel.admin)
def manage_users_table(request):
    table = UsersTable(User.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    context = {"table": table}
    return render(request, "conreq/manage_users/user_table.html", context)


# pylint: disable=protected-access
def user_management(websocket, state, set_state):
    return tabbed_viewport(
        websocket,
        state,
        set_state,
        config.tabs.manage_users,
        top_tabs=config._tabs.manage_users,
    )


config._homepage.admin_nav_tabs[0] = tab_constructor("User Management", user_management)
config._tabs.manage_users["Manage Users"] = {"component": manage_users_table}
config._tabs.manage_users["User Invites"] = {"component": view_to_component()(stub)}
