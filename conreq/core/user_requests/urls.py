from django.urls import path
from . import views

app_name = "user_requests"
urlpatterns = [
    path("", views.request_content, name="request_content"),
    path("my_requests/", views.my_requests, name="my_requests"),
    path("all_requests/", views.all_requests, name="all_requests"),
]
