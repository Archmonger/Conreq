from django.urls import path

from . import views

app_name = "issue_reporting"
urlpatterns = [
    path("", views.report_issue, name="report_issue"),
    path("manage_issue/", views.manage_issue, name="manage_issue"),
    path("issue_modal/", views.report_issue_modal, name="report_issue_modal"),
    path("all_issues/", views.all_issues, name="all_issues"),
    path("my_issues/", views.my_issues, name="my_issues"),
]
