from django import template

register = template.Library()


@register.simple_tag
def server_name():
    # TODO: Get this from the database
    return "Conreq"


@register.simple_tag
def app_description():
    # TODO: Get this from the database
    return "A hub for great things."
