from django import template

register = template.Library()


@register.simple_tag
def server_name():
    # TODO: Get server name from the database
    return "Conreq"


@register.simple_tag
def app_description():
    # TODO: Get server description from the database
    return "A hub for great things."
