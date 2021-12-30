from django.contrib.auth import get_user_model
from django.views.generic.edit import DeleteView, UpdateView

from conreq.internal.manage_users.forms import UserEditForm
from conreq.utils.views import ObjectInParamsMixin, SuccessCurrentUrlMixin

User = get_user_model()

# TODO: Split up manage_users.css into a generic, reusable file(s)
# TODO: Create SimpleTable and SimpleForm abstractions
# TODO: Figure out some way to integrate user invites into this


class EditUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, UpdateView):
    template_name = "conreq/manage_users/edit_user.html"
    form_class = UserEditForm
    model = User


class DeleteUserView(SuccessCurrentUrlMixin, ObjectInParamsMixin, DeleteView):
    template_name = "conreq/manage_users/delete_user_confirm.html"
    model = User
