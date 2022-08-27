from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path("user-token/", views.obtain_auth_token, name="user-token"),
]
