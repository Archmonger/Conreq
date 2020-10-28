# from django.shortcuts import render
from conreq.apps.helpers import generate_context
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def login(request):
    template = loader.get_template("login.html")

    context = generate_context({})
    return HttpResponse(template.render(context, request))
