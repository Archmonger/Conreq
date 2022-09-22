from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig

from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management.forms import UserEditForm
from conreq._core.user_management.tables import UserInviteTable, UsersTable
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin


class EditUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/form.html"
    form_class = UserEditForm
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit User"
        return context


class DeleteUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    model = get_user_model()


def manage_users(request):
    table = UsersTable(get_user_model().objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})


def manage_invites(request):
    table = UserInviteTable(InviteCode.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    return render(request, "conreq/table.html", {"table": table})
