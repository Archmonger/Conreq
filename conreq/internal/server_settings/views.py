from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.forms import ModelForm
from django.views.generic.edit import UpdateView

from conreq.internal.server_settings.models import GeneralSettings


class GeneralSettingsForm(ModelForm):
    class Meta:
        model = GeneralSettings
        fields = ("server_name", "server_description", "app_store_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
        self.helper.add_input(Button("clear-cache", "Clear Cache"))


class GeneralSettingsView(UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = GeneralSettingsForm
    model = GeneralSettings

    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

    def get_object(self, queryset=None):
        return GeneralSettings.get_solo()


def server_settings(request):
    return GeneralSettingsView.as_view()(request)
