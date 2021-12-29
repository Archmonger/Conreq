from django.views.generic.edit import UpdateView

from conreq import config
from conreq.app import register
from conreq.internal.user_settings.forms import UserSettingsForm
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import SuccessCurrentUrlMixin

# TODO: Tabs for general, delete user, and change password


def change_password(request):
    pass


def delete_my_account(request):
    pass


@register.tabs.user_settings("Basic Settings")
@django_to_idom()
class UserSettingsView(SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = UserSettingsForm

    def get_object(self, queryset=None):
        return self.request.user


def user_settings(websocket, viewport_state, set_viewport_state):
    # TODO: Create some way for `tabbed_viewport` to access the viewport state
    return tabbed_viewport(websocket, config.tabs.user_settings)
