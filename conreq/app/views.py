from django.views.generic.edit import UpdateView

from conreq.utils.views import SuccessCurrentUrlMixin


class SingletonUpdateView(SuccessCurrentUrlMixin, UpdateView):
    """Update view intended for `SingletonModel`."""

    template_name = "conreq/form.html"

    def get_object(self, queryset=None):
        return self.model.get_solo()
