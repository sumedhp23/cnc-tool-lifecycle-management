from django.contrib import admin
from django.urls import path
from cnc_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lifecycle_form, name="lifecycle_form"),
    path('success/', views.success_page, name="success"),
    path("reports/", views.reports_table, name="reports_table"),
    path("export-reports/", views.export_reports_excel, name="export_reports"),
    path("upload-excel/", views.upload_excel, name="upload_excel"),
    path("confirm-upload/", views.confirm_upload, name="confirm_upload"),
]