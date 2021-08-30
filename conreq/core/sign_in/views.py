from django.contrib.auth.views import LoginView

from conreq import app
from conreq.utils.debug import performance_metrics


@performance_metrics()
def sign_in(request):
    return LoginView.as_view(template_name=app.config.sign_in_template)(request)
