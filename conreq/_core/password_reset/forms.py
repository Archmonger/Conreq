from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as _SetPasswordForm
from django.contrib.auth.forms import _unicode_ci_compare  # type: ignore
from django.db.models import Q
from django.forms import CharField, TextInput
from django.utils.translation import gettext_lazy as _


class PasswordResetForm(_PasswordResetForm):
    email = CharField(
        label=_("Email"),
        max_length=254,
        widget=TextInput(
            attrs={"autocomplete": "email", "placeholder": "Username or Email"}
        ),
    )

    def get_users(self, username_or_email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        # pylint: disable=arguments-renamed, protected-access
        active_users = get_user_model().objects.filter(
            Q(email__iexact=username_or_email) | Q(username__iexact=username_or_email),
            is_active=True,
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and (
                _unicode_ci_compare(username_or_email, getattr(u, "email"))
                or _unicode_ci_compare(username_or_email, getattr(u, "username")),
            )
        )


class SetPasswordForm(_SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "New Password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Confirm New Password",
            }
        ),
    )
