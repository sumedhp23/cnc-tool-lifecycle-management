from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import *


# -------------------------
# INLINE FOR DYNAMIC FIELDS
# -------------------------
class FormSubmissionInline(admin.TabularInline):
    model = FormSubmission
    extra = 0


# -------------------------
# BASIC REGISTRATIONS
# -------------------------
admin.site.register(FieldOption)


# -------------------------
# DYNAMIC FIELD ADMIN
# -------------------------
@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ("field_name", "field_type")
    list_filter = ("field_type",)


# -------------------------
# TOOL LIFECYCLE REPORT ADMIN
# -------------------------
@admin.register(ToolLifecycleReport)
class ToolLifecycleReportAdmin(admin.ModelAdmin):

    list_display = (
        "serial_no",
        "date",
        "shift",
        "cell_no",
        "stage",
        "tool_no",
        "machine_number",
        "stage_tool",
        "target_life",
        "actual_life",
    )

    search_fields = (
        "cell_no",
        "stage",
        "tool_no",
        "machine_number",
        "sap_code",
    )

    list_filter = (
        "cell_no",
        "stage",
        "tool_no",
        "shift",
    )

    ordering = ("-serial_no",)

    # 👇 THIS IS THE FIX
    inlines = [FormSubmissionInline]


# -------------------------
# REPORTS DASHBOARD
# -------------------------
def reports_dashboard(request):

    reports = ToolLifecycleReport.objects.all()
    dynamic_fields = DynamicField.objects.all()

    context = dict(
        admin.site.each_context(request),
        reports=reports,
        dynamic_fields=dynamic_fields
    )

    return TemplateResponse(
        request,
        "reports_table.html",
        context
    )


# -------------------------
# CUSTOM ADMIN URL
# -------------------------
def get_admin_urls(urls):

    def get_urls():

        custom_urls = [
            path(
                "reports-dashboard/",
                admin.site.admin_view(reports_dashboard),
                name="reports-dashboard",
            ),
        ]

        return custom_urls + urls

    return get_urls


admin.site.get_urls = get_admin_urls(admin.site.get_urls())