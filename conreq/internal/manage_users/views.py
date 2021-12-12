import django_tables2 as tables
from django.contrib.auth import get_user_model

# from django_tables2 import SingleTableView
from django.shortcuts import render

User = get_user_model()


class UsersTable(tables.Table):
    delete = tables.TemplateColumn(template_name="manage_users/delete_btn.html")
    edit = tables.TemplateColumn(template_name="manage_users/edit_btn.html")

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = (
            "username",
            "email",
            "date_joined",
            "last_login",
            "is_staff",
            "edit",
            "delete",
        )
        order_by = "date_joined"


def manage_users(request):
    if request.GET.get("edit"):
        return render(request, "manage_users/edit_user.html", {})
    if request.GET.get("delete"):
        return render(request, "manage_users/delete_user.html", {})

    table = UsersTable(User.objects.all())
    table.paginate(
        page=request.GET.get("page", 1),
        per_page=request.GET.get("per_page", 25),
    )
    context = {"table": table}
    return render(request, "manage_users/user_table.html", context)
