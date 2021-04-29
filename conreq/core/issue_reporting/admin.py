from django.contrib import admin
from conreq.core.issue_reporting.models import ReportedIssue

# Register your models here.
@admin.register(ReportedIssue)
class AllReportedIssues(admin.ModelAdmin):
    pass
