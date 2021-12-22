from django.views.generic.edit import UpdateView

from conreq.internal.user_settings.forms import UserSettingsForm
from conreq.utils.views import SuccessCurrentUrlMixin

# TODO: Tabs for general, delete user, and change password


def change_password(request):
    pass


def delete_self(request):
    pass


class UserSettingsView(SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = UserSettingsForm

    def get_object(self, queryset=None):
        return self.request.user


def user_settings(request):
    return UserSettingsView.as_view()(request)
