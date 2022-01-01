"""Any function that assists in views"""
from django.http import HttpResponse
from django.views.generic.edit import FormView, UpdateView


class SuccessCurrentUrlMixin:
    """Mixin for UpdateView to return success at the current URL, if
    a success_url is not set."""

    def get_success_url(self):
        self.success_url = (
            getattr(self, "success_url", None) or self.request.path + "?success=true"
        )
        return super().get_success_url()


class CurrentUserMixin:
    """Mixin for `FormView`, `UpdateView`, and `DeleteView` to utilize the current
    user as the object. Forms utilized in these views must be a `ModelForm`."""

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

    def get_object(self, queryset=None):
        # pylint: disable=unused-argument
        return self.model.objects.get(id=self.request.GET["id"])


class SingletonUpdateView(SuccessCurrentUrlMixin, UpdateView):
    """Update view intended for `SingletonModel`."""

    template_name = "conreq/simple_form.html"

    def get_object(self, queryset=None):
        return self.model.get_solo()


def stub(request, *args, **kwargs):
    """Placeholder view function intended for debugging or development."""
    return HttpResponse(
        __name__ + ": This is a stub for a view that has not yet been defined."
    )
