from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            # TODO: Fetch more settings via conreq.config object
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
        self.helper.add_input(Button("change-password", "Change Password"))
