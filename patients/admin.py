from django.contrib import admin
from .models import DiagnosticTest, Patient, FactorsInDiagnosticTest, DefaultFactorValues, TestReport, TestReportResult
from django import forms
from django.utils.html import format_html
# Register your models here.
admin.site.register(DiagnosticTest)
admin.site.register(FactorsInDiagnosticTest)
admin.site.register(TestReport)
admin.site.register(TestReportResult)
admin.site.register(DefaultFactorValues)
# admin.site.register(TestRequest)





# ========================================================================================
# This is for generating payment slip
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "total_price", "download_receipt")

    def download_receipt(self, obj):
        return format_html(f'<a href="/patient/receipt/{obj.id}/" target="_blank">Download</a>')

    download_receipt.short_description = "Receipt"

admin.site.register(Patient, PatientAdmin)




