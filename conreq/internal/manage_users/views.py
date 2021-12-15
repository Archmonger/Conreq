from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django_tables2 import RequestConfig, Table, TemplateColumn

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)


class UsersTable(Table):
    edit = TemplateColumn(
        template_name="manage_users/edit_btn.html",
        orderable=False,
    )

    class Meta:
        model = User
        # TODO: PR a template for Bootstrap 5
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = (
            "username",
            "email",
            "date_joined",
            "last_login",
            "is_staff",
            "edit",
        )
        order_by = "date_joined"


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
        self.helper.add_input(
            Button(
                "delete",
                "Delete",
                css_class="btn-danger",
                onclick="window.location.href = window.location.href.replace('edit','delete');",
            )
        )
        self.helper.add_input(Button("back", "Back", onclick="history.back()"))


class UserEditView(UpdateView):
    template_name = "manage_users/edit_user.html"
    form_class = UserEditForm
    model = User

    def form_valid(self, *args, **kwargs) -> None:
        self.success_url = self.request.path
        return super().form_valid(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.GET["user"])


class UserDeleteView(DeleteView):
    template_name = "manage_users/delete_user_confirm.html"
    model = User

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
    return render(request, "manage_users/user_table.html", context)
