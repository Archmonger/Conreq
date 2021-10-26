from django.contrib.auth.views import LoginView

from conreq.app import register


@register.sign_in_view()
def sign_in(request):
    return LoginView.as_view(template_name=app.config.sign_in_template)(request)
