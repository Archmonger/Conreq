from django.urls import reverse
from reactpy import component, html


@component
def sign_out():
    return html.script(f"location.href = '{reverse('conreq:sign_out')}';")
