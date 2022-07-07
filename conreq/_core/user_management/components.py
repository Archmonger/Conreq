from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig
from idom import component, html

from conreq import AuthLevel, config
from conreq._core.components import tabbed_viewport
from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management.forms import UserEditForm
from conreq._core.user_management.tables import UserInviteTable, UsersTable
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
def manage_users(request):
    table = UsersTable(get_user_model().objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


@view_to_component(name="user_invites", auth_level=AuthLevel.admin)
def manage_invites(request):
    table = UserInviteTable(InviteCode.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


@component
def create_invite(state, set_state):
    return html.div("Under Construction")


# pylint: disable=protected-access
@component
def user_management(state, set_state):
    return tabbed_viewport(
        state,
        set_state,
        tabs=config.tabs.user_management.installed,
        top_tabs=config._internal_tabs.user_management,
    )
