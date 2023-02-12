"""Any function that assists in views"""
from inspect import isclass

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from conreq.types import AuthLevel


class CurrentUserOrAdminMixin:
    """Mixin for any class based view to block access if the user is not the current
    user or an admin.

    To validate the user is modifying a page related to his user ID, you must set
    `self.user_id`, or you can set the user ID as a URL parameter.

    By default, the URL parameter is `id`, but can be configured by setting the
    `user_id_param` attribute."""

    user_id = None
    user_id_param = "id"

    def dispatch(self, request, *args, **kwargs):
        if self.user_id is None:
            user_id_string = getattr(request, request.method).get(self.user_id_param)
            self.user_id = (
                int(user_id_string)
                if isinstance(user_id_string, str) and user_id_string.isnumeric()
                else ""
            )

        if request.user.is_superuser or request.user.id == self.user_id:
            return super().dispatch(request, *args, **kwargs)  # type: ignore

        return HttpResponse(status=403)


class SuccessCurrentUrlMixin:
    """Mixin for `UpdateView` to return success at the current URL, if
    a success_url is not set."""

    # pylint: disable=too-few-public-methods

    def get_success_url(self):
        params = self.request.GET.copy()  # type: ignore
        params["success"] = True
        self.success_url = f"{self.request.path}?{params.urlencode()}"  # type: ignore
        return super().get_success_url()  # type: ignore


class UserInstanceMixin:
    """Mixin for `FormView`, `UpdateView`, and `DeleteView` to utilize the current
    user as the object. Forms utilized in these views must be a `ModelForm`."""

    # pylint: disable=too-few-public-methods

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()  # type: ignore
        if isinstance(self, FormView):
            kwargs["instance"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        # pylint: disable=unused-argument
        return self.request.user  # type: ignore


class ObjectInParamsMixin:
    """Mixin for any Django class based view to get an object by ID in the
    URL params."""

    # pylint: disable=too-few-public-methods

    def get_object(self, queryset=None):
        # pylint: disable=unused-argument
        return self.model.objects.get(id=self.request.GET["id"])  # type: ignore


class SaveFormViewMixin:
    """Adds a `save()` action to a `FormView`'s post behavior."""

    # pylint: disable=too-few-public-methods

    def post(self, request, *args, **kwargs):
        form = self.get_form()  # type: ignore
        if not form.is_valid():
            return self.form_invalid(form)  # type: ignore
        form.full_clean()
        form.save()
        return self.form_valid(form)  # type: ignore


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
                lambda user: user.is_staff,  # type: ignore
                login_url=login_url,
                redirect_field_name=redirect_field_name,
            ),
            name="dispatch",
        )(view)

    # Function view
    return user_passes_test(
        lambda user: user.is_staff,  # type: ignore
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )(view)


def authenticated(view, auth_level: str = AuthLevel.user):
    if auth_level == AuthLevel.user:
        return login_required(view)
    return staff_required(view) if auth_level == AuthLevel.admin else view


def stub(request, *args, **kwargs):
    """Placeholder view function intended for debugging or development."""
    return HttpResponse(
        f"{__name__}: This is a stub for a view that has not yet been defined."
    )
