from django.views.generic.edit import UpdateView

from conreq.internal.user_settings.forms import UserSettingsForm
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import SuccessCurrentUrlMixin

# TODO: Tabs for general, delete user, and change password


def change_password(request):
    pass


def delete_self(request):
    pass


class GeneralSettingsView(SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = UserSettingsForm

    def get_object(self, queryset=None):
        return self.request.user


def user_settings(websocket, current_tab, set_current_tab):
    return tabbed_viewport(websocket, user_tabs)


# TODO: Remove this later.
user_tabs = {
    "General Settings": {"component": django_to_idom()(GeneralSettingsView)},
    "Change Password": {"component": lambda: print("placeholder")},
    "Delete My Account": {"component": lambda: print("placeholder")},
}
