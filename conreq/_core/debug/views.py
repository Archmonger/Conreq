from health_check.views import MainView as HealthCheckView


class HealthCheck(HealthCheckView):
    template_name = "conreq/health_check.html"
