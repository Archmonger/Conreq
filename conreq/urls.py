"""Conreq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path(
        "signin/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="signin",
    ),
    path("signout/", auth_views.logout_then_login, name="signout"),
    path("admin/", admin.site.urls),
    path("discover/", include("conreq.apps.discover.urls")),
    path("more_info/", include("conreq.apps.more_info.urls")),
    path("search/", include("conreq.apps.search.urls")),
    path("settings/", include("conreq.apps.settings.urls")),
    path("", include("conreq.apps.homepage.urls")),
]