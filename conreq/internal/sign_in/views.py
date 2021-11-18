from django.contrib.auth.views import LoginView

import conreq
from conreq.app import register


@register.sign_in_view()
def sign_in(request):
    return LoginView.as_view(template_name=conreq.config.sign_in_template)(request)
