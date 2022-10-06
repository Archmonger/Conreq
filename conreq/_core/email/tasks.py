from typing import Iterable

from django.core.mail import send_mail as django_send_email
from django.core.mail.backends import smtp
from huey.contrib.djhuey import db_task

from conreq._core.email import utils
from conreq._core.email.types import Email
from conreq.app.models import EmailSettings


@db_task()
def send_email(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
):
    django_send_email(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=fail_silently,
        auth_user=auth_user,
        auth_password=auth_password,
        connection=connection,
        html_message=html_message,
    )


@db_task()
def send_mass_email(
    connection: smtp.EmailBackend, emails: Iterable[Email], email_config: EmailSettings
):
    return utils.send_mass_email(connection, emails, email_config)
