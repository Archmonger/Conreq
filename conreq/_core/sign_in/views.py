from django.contrib.auth.views import LoginView

from conreq import config
from conreq.app import register


@register.view.sign_in()
def sign_in(request):
    return LoginView.as_view(template_name=config.templates.sign_in)(request)
