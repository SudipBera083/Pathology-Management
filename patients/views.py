from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.http import FileResponse
from .utils import generate_receipt
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, DiagnosticTest, FactorsInDiagnosticTest, DefaultFactorValues, TestReport, TestReportResult
from .forms import PatientForm, DiagnosticTestForm, FactorsInDiagnosticTestForm, DefaultFactorValuesForm

def dashboard(request):
    patients = Patient.objects.all()
    tests = DiagnosticTest.objects.all()
    factors = FactorsInDiagnosticTest.objects.all()
    default_values = DefaultFactorValues.objects.all()

    return render(request, "./dashboard.html", {
        "patients": patients,
        "tests": tests,
        "factors": factors,
        "default_values": default_values
    })

# Add & Edit Patient
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = PatientForm()
    return render(request, "./patient/add_patient.html", {"form": form})

def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = PatientForm(instance=patient)
    return render(request, "./patient/edit_patient.html", {"form": form})

def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect("dashboard")

# Add & Edit Diagnostic Test
def add_test(request):
    if request.method == "POST":
        form = DiagnosticTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = DiagnosticTestForm()
    return render(request, "./test/add_test.html", {"form": form})






# Add Factor to Test

def add_factor(request, test_id=None):
    tests = DiagnosticTest.objects.all()
    selected_test = None

    if test_id:
        selected_test = get_object_or_404(DiagnosticTest, id=test_id)  # Get the selected test

    if request.method == "POST":
        form = FactorsInDiagnosticTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # Redirect after saving
    else:
        form = FactorsInDiagnosticTestForm(initial={"test_name": selected_test})  # Pre-fill test_name

    return render(request, "./factor/add_factor.html", {"form": form, "tests": tests, "test_id": test_id})




def edit_factor(request, factor_id):
    factor = get_object_or_404(FactorsInDiagnosticTest, id=factor_id)

    if request.method == "POST":
        form = FactorsInDiagnosticTestForm(request.POST, instance=factor)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # Redirect to the dashboard after saving
    else:
        form = FactorsInDiagnosticTestForm(instance=factor)

    return render(request, "./factor/edit_factor.html", {"form": form, "factor": factor})

def delete_factor(request, factor_id):
    factor = get_object_or_404(FactorsInDiagnosticTest, id=factor_id)
    
    # if request.method == "POST":
    factor.delete()
    return redirect("dashboard")  # Redirect after deletion

    # return render(request, "confirm_delete.html", {"factor": factor})




# Add Default Factor Value
def add_default_value(request):
    if request.method == "POST":
        form = DefaultFactorValuesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = DefaultFactorValuesForm()
    return render(request, "add_edit_default_value.html", {"form": form})



def download_receipt(request, patient_id):
    buffer = generate_receipt(patient_id)
    if buffer:
        return FileResponse(buffer, as_attachment=True, filename=f"Receipt_{patient_id}.pdf")
    return HttpResponse("Patient not found", status=404)

def set_default_values(request, factor_id):
    factor = get_object_or_404(FactorsInDiagnosticTest, id=factor_id)

    if request.method == "POST":
        min_ages = request.POST.getlist("min_age[]")
        min_age_units = request.POST.getlist("min_age_unit[]")

        max_ages = request.POST.getlist("max_age[]")
        max_age_units = request.POST.getlist("max_age_unit[]")

        min_values = request.POST.getlist("min_value[]")
        max_values = request.POST.getlist("max_value[]")
        units = request.POST.getlist("unit[]")

        # Loop through all received form values and create multiple records
        for i in range(len(min_ages)):
            DefaultFactorValues.objects.create(
                test_name=factor.test_name,  # Ensure correct test association
                factor_name=factor,  
                min_age=int(min_ages[i]) if min_ages[i] else 0,
                min_age_unit=min_age_units[i],
                max_age=int(max_ages[i]) if max_ages[i] else 0,
                max_age_unit=max_age_units[i],
                min_value=int(min_values[i]) if min_values[i] else None,
                max_value=int(max_values[i]) if max_values[i] else None,
                unit=units[i] if units[i] else ""
            )

        return redirect("dashboard")  # Redirect after saving all values

    return redirect("dashboard")



def edit_default_value(request, value_id):
    default_value = get_object_or_404(DefaultFactorValues, id=value_id)

    if request.method == "POST":
        default_value.min_age = request.POST["min_age"]
        default_value.min_age_unit = request.POST["min_age_unit"]
        default_value.max_age = request.POST["max_age"]
        default_value.max_age_unit = request.POST["max_age_unit"]
        default_value.min_value = request.POST["min_value"]
        default_value.max_value = request.POST["max_value"]
        default_value.unit = request.POST["unit"]
        default_value.save()
        return redirect("dashboard")  # Change to actual view

    return render(request, "./factor/edit_default_value.html", {"default_value": default_value})



def delete_default_value(request, value_id):
    value = get_object_or_404(DefaultFactorValues, id=value_id)
    value.delete()
    return redirect('dashboard')  # Replace with your actual dashboard view name





# ============================================================================================
# Report generation


def save_test_report(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)

        for test in patient.tests.all():
            test_report = TestReport.objects.create(patient=patient, test=test)

            for factor in FactorsInDiagnosticTest.objects.filter(test_name=test):
                value = request.POST.get(f'factor_{factor.id}')
                if value:
                    TestReportResult.objects.create(
                        report=test_report,
                        factor=factor.factors,
                        tested_value=float(value),
                        min_value=0,  # Set default values or fetch from DefaultFactorValues
                        max_value=100,  # Example range, update this as needed
                        unit="Unit"
                    )

        return redirect('some_success_page')

    return redirect('generate_report', patient_id=patient_id)





from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, DiagnosticTest, FactorsInDiagnosticTest, TestReport, TestReportResult

def select_test(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    tests = patient.tests.all()

    if request.method == "POST":
        test_id = request.POST.get("test_id")
        test = get_object_or_404(DiagnosticTest, id=test_id)
        predefined_header = request.POST.get("predefined_header")  # Will be 'on' if checked, None if unchecked

       


        # Create a new TestReport
        report = TestReport.objects.create(test=test, patient=patient)

        # Loop through posted factors
        for key, value in request.POST.items():
            if key.startswith("factor_"):  # Check if the input belongs to a factor
                factor_id = key.split("_")[1]  # Extract factor ID
                factor = get_object_or_404(FactorsInDiagnosticTest, id=factor_id)

                # Save the test result
                TestReportResult.objects.create(
                    report=report,
                    factor=factor,
                    tested_value=float(value) if value else 0.0  # Default to 0 if empty
                )


        if predefined_header:
            return redirect("generate_report", report_id=report.id)  # Redirect after saving
        else:
            return redirect("generate_custom_report", report_id=report.id)  # Redirect after saving
        

    return render(request, "./testReport/generate_report.html", {"patient": patient, "tests": tests})




# def generate_report(request, patient_id):
#     patient = get_object_or_404(Patient, id=patient_id)
#     return render(request, 'generate_report.html', {'patient': patient})



# ==============================================================

def takeResponse(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    tests = patient.tests.all() 
    if request.method == "POST":
        test_id = request.POST.get("test_id")
        test = get_object_or_404(DiagnosticTest, id=test_id)
        
        # Capture all factor values
        factor_values = {}
        for factor in test.factorsindiagnostictest_set.all():
            factor_input_name = f"factor_{factor.id}"
            factor_value = request.POST.get(factor_input_name)
            if factor_value:
                factor_values[factor.factors] = factor_value
    
    return JsonResponse({

                "test":test_id,
                "factor":factor_value
            })


# ================================================================


# Pathology Details
PATHOLOGY_NAME = "XYZ Pathology Lab"
PATHOLOGY_ADDRESS = "123, Medical Road, City Center, New Delhi, India - 110001"
PATHOLOGY_CONTACT = "+91 98765 43210 | Email: support@xyzpathology.com"


def generate_diagnostic_report(request, report_id):
    try:
        report = TestReport.objects.get(id=report_id)
        patient = report.patient
        test_results = TestReportResult.objects.filter(report=report)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Diagnostic_Report_{patient.name}.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle(f"Diagnostic Report - {patient.name}")

        # **Header Section**
        pdf.setFont("Helvetica-Bold", 18)
        pdf.setFillColor(colors.darkblue)
        pdf.drawString(180, 770, "XYZ Pathology Lab")

        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 750, "123, Medical Road, City Center, New Delhi, India - 110001")
        pdf.drawString(180, 735, "+91 98765 43210 | Email: support@xyzpathology.com")

        # **Diagnostic Report Title**
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.black)
        pdf.drawString(220, 700, "DIAGNOSTIC REPORT")

        # **Patient Details**
        y_position = 670
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Patient Details:")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(60, y_position - 20, f"Name: {patient.name}")
        pdf.drawString(60, y_position - 40, f"Gender: {patient.gender}")
        pdf.drawString(60, y_position - 60, f"Age: {patient.age} {patient.age_unit}")
        pdf.drawString(60, y_position - 80, f"Phone: {patient.phone}")
        pdf.drawString(60, y_position - 100, f"Test Name: {report.test.name}")
        pdf.drawString(60, y_position - 120, f"Report Date: {report.report_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # **Test Results Table**
        y_position -= 140
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Test Results:")

        # **Fixed Table Widths for Proper Alignment**
        col_widths = [140, 90, 160, 70, 70]  # Adjusted column widths

        table_data = [["Factor", "Tested Value", "Normal Range (Age-based)", "Unit", "Status"]]

        for result in test_results:
            try:
                factor_values = DefaultFactorValues.objects.filter(
                    test_name=report.test, factor_name=result.factor,
                    min_age__lte=patient.age, max_age__gte=patient.age
                ).order_by('-min_age', 'max_age').first()

                if factor_values:
                    normal_range = f"{factor_values.min_value} - {factor_values.max_value} ({factor_values.min_age}-{factor_values.max_age} {factor_values.min_age_unit})"
                    unit = factor_values.unit
                    status = "Normal" if factor_values.min_value <= result.tested_value <= factor_values.max_value else "Abnormal"
                else:
                    normal_range, unit, status = "N/A", "N/A", "N/A"

            except DefaultFactorValues.DoesNotExist:
                normal_range, unit, status = "N/A", "N/A", "N/A"

            table_data.append([result.factor.factors, result.tested_value, normal_range, unit, status])

        # **Create Styled Table**
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # **Ensure Proper Margin & Centering**
        table.wrapOn(pdf, 50, y_position)
        table.drawOn(pdf, 50, y_position - (25 * len(table_data)))

        # **Footer**
        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.darkgray)
        # pdf.drawString(50, y_position - 80, "Thank you for choosing XYZ Pathology Lab.")
        # pdf.drawString(50, y_position - 100, "For queries, contact: support@xyzpathology.com")
        pdf.setFillColor(colors.black)

        pdf.save()
        return response

    except TestReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)
    


    # =======================================================================================
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from .models import TestReport, TestReportResult, DefaultFactorValues

def generate_custom_report(request, report_id):
    try:
        report = TestReport.objects.get(id=report_id)
        patient = report.patient
        test_results = TestReportResult.objects.filter(report=report)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Diagnostic_Report_{patient.name}.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle(f"Diagnostic Report - {patient.name}")

        # **Page Dimensions**
        page_width, page_height = letter  # (612, 792) in points
        middle_y = page_height / 2  # Center point (396)

        # **Start Content in Middle**
        start_y = middle_y + 100  # Adjust upward slightly for balance

        # **Diagnostic Report Title**
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.black)
        pdf.drawString(220, start_y, "DIAGNOSTIC REPORT")

        # **Patient Details**
        y_position = start_y - 40  # Shift downward for spacing
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Patient Details:")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(60, y_position - 20, f"Name: {patient.name}")
        pdf.drawString(60, y_position - 40, f"Gender: {patient.gender}")
        pdf.drawString(60, y_position - 60, f"Age: {patient.age} {patient.age_unit}")
        pdf.drawString(60, y_position - 80, f"Phone: {patient.phone}")
        pdf.drawString(60, y_position - 100, f"Test Name: {report.test.name}")
        pdf.drawString(60, y_position - 120, f"Report Date: {report.report_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # **Test Results Table**
        y_position -= 150  # Space before the table
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Test Results:")

        # **Fixed Table Widths for Proper Alignment**
        col_widths = [140, 90, 160, 70, 70]

        table_data = [["Factor", "Tested Value", "Normal Range (Age-based)", "Unit", "Status"]]

        for result in test_results:
            try:
                factor_values = DefaultFactorValues.objects.filter(
                    test_name=report.test, factor_name=result.factor,
                    min_age__lte=patient.age, max_age__gte=patient.age
                ).order_by('-min_age', 'max_age').first()

                if factor_values:
                    normal_range = f"{factor_values.min_value} - {factor_values.max_value} ({factor_values.min_age}-{factor_values.max_age} {factor_values.min_age_unit})"
                    unit = factor_values.unit
                    status = "Normal" if factor_values.min_value <= result.tested_value <= factor_values.max_value else "Abnormal"
                else:
                    normal_range, unit, status = "N/A", "N/A", "N/A"

            except DefaultFactorValues.DoesNotExist:
                normal_range, unit, status = "N/A", "N/A", "N/A"

            table_data.append([result.factor.factors, result.tested_value, normal_range, unit, status])

        # **Create Styled Table**
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # **Ensure Proper Margin & Centering**
        table.wrapOn(pdf, 50, y_position)
        table.drawOn(pdf, 50, y_position - (25 * len(table_data)))

        # **Footer**
        # pdf.setFont("Helvetica", 10)
        # pdf.setFillColor(colors.darkgray)
        # pdf.drawString(50, y_position - 80, "Thank you for choosing XYZ Pathology Lab.")
        # pdf.drawString(50, y_position - 100, "For queries, contact: support@xyzpathology.com")
        # pdf.setFillColor(colors.black)

        pdf.save()
        return response

    except TestReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)
