from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.forms import _unicode_ci_compare
from django.db.models import Q
from django.forms import CharField, TextInput
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PasswordResetForm(_PasswordResetForm):
    email = CharField(
        label=_("Email"),
        max_length=254,
        widget=TextInput(
            attrs={"autocomplete": "email", "placeholder": "Email or Username"}
        ),
    )

    def get_users(self, username_or_email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        # pylint: disable=arguments-renamed, protected-access
        active_users = User.objects.filter(
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
