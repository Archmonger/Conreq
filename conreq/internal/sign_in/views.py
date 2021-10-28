from django.contrib.auth.views import LoginView

from conreq.app import config, register


@register.sign_in_view()
def sign_in(request):
    return LoginView.as_view(template_name=config.sign_in_template)(request)
