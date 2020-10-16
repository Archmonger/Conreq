# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def login(request):
    template = loader.get_template("login.html")

    context = {}
    return HttpResponse(template.render(context, request))
