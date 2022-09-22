from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView, FormView, UpdateView

from conreq._core.user_settings.forms import (
    ChangePasswordForm,
    DeleteMyAccountForm,
    UserSettingsForm,
)
from conreq.utils.views import CurrentUserMixin, SuccessCurrentUrlMixin


class UserSettingsView(CurrentUserMixin, SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/form.html"
    form_class = UserSettingsForm


class ChangePasswordView(SuccessCurrentUrlMixin, PasswordChangeView):
    template_name = "conreq/form.html"
    form_class = ChangePasswordForm


class DeleteMyAccountView(CurrentUserMixin, FormView):
    template_name = "conreq/form.html"
    form_class = DeleteMyAccountForm
    success_url = reverse_lazy("delete_my_account_confirm")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_subtitle"] = "Confirm your password to delete your account."
        return context


class DeleteMyAccountConfirmView(CurrentUserMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    success_url = reverse_lazy("delete_my_account_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Are you sure you want to delete your account?"
        return context


def delete_my_account_success(request):
    return render(request, "conreq/refresh_parent_frame.html")
