from django.contrib.auth import get_user_model
from django_tables2 import Table, TemplateColumn

User = get_user_model()


class UsersTable(Table):
    edit = TemplateColumn(
        template_name="conreq/manage_users/edit_btn.html",
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
