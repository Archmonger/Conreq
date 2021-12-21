"""Any function that assists in views"""
from django.http import HttpResponse
from django.views.generic.edit import UpdateView


class SingletonUpdateView(UpdateView):
    """Update view intended for `SingletonModel`."""

    template_name = "conreq/simple_form.html"

    def get_success_url(self):
        self.success_url = (
            getattr(self, "success_url", None) or self.request.path + "?success=true"
        )
        return super().get_success_url()

    def get_object(self, queryset=None):
        return self.model.get_solo()


def stub(request, *args, **kwargs):
    """Placeholder view function intended for debugging or development."""
    return HttpResponse(
        __name__ + ": This is a stub for a view that has not yet been defined."
    )
