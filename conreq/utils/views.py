"""Any function that assists in views"""
from inspect import isclass

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from conreq.types import AuthLevel


class SuccessCurrentUrlMixin:
    """Mixin for UpdateView to return success at the current URL, if
    a success_url is not set."""

    # pylint: disable=too-few-public-methods

    def get_success_url(self):
        params = self.request.GET.copy()
        params["success"] = True
        self.success_url = f"{self.request.path}?{params.urlencode()}"
        return super().get_success_url()


class CurrentUserMixin:
    """Mixin for `FormView`, `UpdateView`, and `DeleteView` to utilize the current
    user as the object. Forms utilized in these views must be a `ModelForm`."""

    # pylint: disable=too-few-public-methods

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if isinstance(self, FormView):
            kwargs["instance"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        # pylint: disable=unused-argument
        return self.request.user


class ObjectInParamsMixin:
    """Mixin for any Django view to get an object by ID in the
    URL params."""

    # pylint: disable=too-few-public-methods

    def get_object(self, queryset=None):
        # pylint: disable=unused-argument
        return self.model.objects.get(id=self.request.GET["id"])


class SaveFormViewMixin:
    """Adds a `save()` action to a `FormView`'s post behavior."""

    # pylint: disable=too-few-public-methods

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)
        form.save()
        return self.form_valid(form)


def login_required(view, login_url=None, redirect_field_name=None):
    # Class view
    if isclass(view):
        return method_decorator(
            user_passes_test(
                lambda user: user.is_authenticated,
                login_url=login_url,
                redirect_field_name=redirect_field_name,
            ),
            name="dispatch",
        )(view)

    # Function view
    return user_passes_test(
        lambda user: user.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )(view)


def staff_required(view, login_url=None, redirect_field_name=None):
    # Class view
    if isclass(view):
        return method_decorator(
            user_passes_test(
                lambda user: user.is_staff,
                login_url=login_url,
                redirect_field_name=redirect_field_name,
            ),
            name="dispatch",
        )(view)

    # Function view
    return user_passes_test(
        lambda user: user.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )(view)


def authenticated(view, auth_level: AuthLevel = AuthLevel.user):
    if auth_level == AuthLevel.user:
        return login_required(view)
    if auth_level == AuthLevel.admin:
        return staff_required(view)
    return view


def stub(request, *args, **kwargs):
    """Placeholder view function intended for debugging or development."""
    return HttpResponse(
        f"{__name__}: This is a stub for a view that has not yet been defined."
    )
