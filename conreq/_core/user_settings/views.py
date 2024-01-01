from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, FormView, UpdateView

from conreq._core.user_settings.forms import (
    ChangePasswordForm,
    DeleteMyAccountForm,
    UserSettingsForm,
)
from conreq.utils.views import SuccessCurrentUrlMixin, UserInstanceMixin


@method_decorator(user_passes_test(lambda u: u.is_authenticated), name="dispatch")
class UserSettingsView(UserInstanceMixin, SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/form.html"
    form_class = UserSettingsForm


@method_decorator(user_passes_test(lambda u: u.is_authenticated), name="dispatch")
class ChangePasswordView(SuccessCurrentUrlMixin, PasswordChangeView):
    template_name = "conreq/form.html"
    form_class = ChangePasswordForm


@method_decorator(user_passes_test(lambda u: u.is_authenticated), name="dispatch")
class DeleteMyAccountView(UserInstanceMixin, FormView):
    template_name = "conreq/form.html"
    form_class = DeleteMyAccountForm
    success_url = reverse_lazy("conreq:delete_my_account_confirm")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_subtitle"] = "Confirm your password to delete your account."
        return context


@method_decorator(user_passes_test(lambda u: u.is_authenticated), name="dispatch")
class DeleteMyAccountConfirmView(UserInstanceMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    success_url = reverse_lazy("conreq:delete_my_account_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Are you sure you want to delete your account?"
        return context


def delete_my_account_success(request):
    return render(request, "conreq/refresh_parent_frame.html")
