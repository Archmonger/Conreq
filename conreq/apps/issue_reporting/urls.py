from django.urls import path

from . import views

app_name = "issue_reporting"
urlpatterns = [
    path("", views.report_issue, name="report_issue"),
    path("issue_modal", views.report_issue_modal, name="report_issue_modal"),
]
