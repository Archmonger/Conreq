from django.urls import path
from . import views

app_name = "user_requests"
urlpatterns = [
    path("", views.request_content, name="request_content"),
]
