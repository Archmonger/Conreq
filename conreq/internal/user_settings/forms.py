from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.forms import CharField, ModelForm, PasswordInput
from django.urls import reverse_lazy

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


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class DeleteMyAccountForm(ModelForm):
    password = CharField(widget=PasswordInput())
    confirm_password = CharField(widget=PasswordInput())
    success_url = reverse_lazy("delete_my_account_confirm")

    class Meta:
        model = User
        fields = ("password",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Delete My Account", css_class="btn btn-danger")
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Password does not match.")

        if not check_password(password, self.instance.password):
            self.add_error("password", "Incorrect password.")
