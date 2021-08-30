"""Any function that assists in views"""
from django.http import HttpResponse


def stub(request, *args, **kwargs):
    """Empty view function."""
    return HttpResponse(__name__ + ": This is a view stub!")
