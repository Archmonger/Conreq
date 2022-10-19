from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq import config
from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management.forms import CreateInviteForm, UserEditForm
from conreq._core.user_management.tables import UserInviteTable, UsersTable
from conreq.utils.views import (
    CurrentUserOrAdminMixin,
    ObjectInParamsMixin,
    SuccessCurrentUrlMixin,
)


class EditUserView(
    SuccessCurrentUrlMixin, ObjectInParamsMixin, CurrentUserOrAdminMixin, UpdateView
):
    template_name = config.templates.edit_user
    form_class = UserEditForm
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit User"
        return context


class DeleteUserView(
    SuccessCurrentUrlMixin, ObjectInParamsMixin, CurrentUserOrAdminMixin, DeleteView
):
    template_name = config.templates.delete_user
    model = get_user_model()


def manage_users(request):
    table = UsersTable(get_user_model().objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},  # type: ignore
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


def manage_invites(request):
    table = UserInviteTable(InviteCode.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},  # type: ignore
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


class CreateInvite(SuccessCurrentUrlMixin, CurrentUserOrAdminMixin, CreateView):
    template_name = config.templates.create_invite
    model = InviteCode
    form_class = CreateInviteForm

    def get_success_url(self):
        invite_code: InviteCode = getattr(self, "object")
        return reverse(
            "create_invite_success", kwargs={"invite_code": invite_code.code}
        )


class CreateInviteSuccess(TemplateView):
    template_name = config.templates.create_invite_success