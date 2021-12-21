from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import RequestConfig, Table, TemplateColumn

from conreq.internal.manage_users.forms import UserEditForm
from conreq.internal.manage_users.tables import UsersTable

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)
# TODO: Create SimpleTable and SimpleForm abstractions


class UserEditView(UpdateView):
    template_name = "conreq/manage_users/edit_user.html"
    form_class = UserEditForm
    model = User

    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.GET["user"])


class UserDeleteView(DeleteView):
    template_name = "conreq/manage_users/delete_user_confirm.html"
    model = User

    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.GET["user"])


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
