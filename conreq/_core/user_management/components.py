from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq import AuthLevel, config
from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management.forms import UserEditForm
from conreq._core.user_management.tables import UserInviteTable, UsersTable
from conreq._core.utils import tab_constructor
from conreq.app.components import tabbed_viewport
from conreq.types import Tab
from conreq.utils.components import view_to_component
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin

# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this


@view_to_component(name="edit_user", auth_level=AuthLevel.admin)
class EditUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/form.html"
    form_class = UserEditForm
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit User"
        return context


@view_to_component(name="delete_user", auth_level=AuthLevel.admin)
class DeleteUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    model = get_user_model()


@view_to_component(name="manage_users", auth_level=AuthLevel.admin)
def manage_users_table(request):
    table = UsersTable(get_user_model().objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


@view_to_component(name="user_invites", auth_level=AuthLevel.admin)
def user_invites(request):
    table = UserInviteTable(InviteCode.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


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
config._tabs.manage_users.append(Tab(name="Manage Users", component=manage_users_table))
config._tabs.manage_users.append(Tab(name="User Invites", component=user_invites))
