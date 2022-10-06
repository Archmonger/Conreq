from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.urls import reverse_lazy

from conreq._core.sign_up.models import InviteCode


class UserEditForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
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
                onclick=f"location.href = '{reverse_lazy('delete_user')}?id=' + new URLSearchParams(window.location.search).get('id')",
            )
        )
        self.helper.add_input(Button("back", "Back", onclick="history.back()"))


class CreateInviteForm(ModelForm):
    class Meta:
        model = InviteCode
        fields = ("name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Invite"))
