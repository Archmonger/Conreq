from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_tables2 import RequestConfig

from conreq import config
from conreq.app import register
from conreq.internal.manage_users.tables import UsersTable
from conreq.internal.manage_users.views import DeleteUserView, EditUserView
from conreq.internal.utils import tab_constructor
from conreq.utils.components import django_to_idom

User = get_user_model()


@register.component.manage_users()
@django_to_idom()
def manage_users(request):
    if request.GET.get("edit"):
        return EditUserView.as_view()(request)

    if request.GET.get("delete"):
        return DeleteUserView.as_view()(request)

    table = UsersTable(User.objects.all())
    RequestConfig(
        request,
        paginate={"per_page": request.GET.get("per_page", 25)},
    ).configure(table)
    context = {"table": table}
    return render(request, "conreq/manage_users/user_table.html", context)


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[0] = tab_constructor("Manage Users", manage_users)
