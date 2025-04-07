from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO
from .models import Patient

# Pathology Details
PATHOLOGY_NAME = "XYZ Pathology Lab"
PATHOLOGY_ADDRESS = "123, Medical Road, City Center, New Delhi, India - 110001"
PATHOLOGY_CONTACT = "+91 98765 43210 | Email: support@xyzpathology.com"


def generate_receipt(patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Receipt_{patient.name}")

    # **Header Section**
    y_position = 750
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(170, y_position, PATHOLOGY_NAME)

    pdf.setFont("Helvetica", 11)
    pdf.drawString(120, y_position - 20, PATHOLOGY_ADDRESS)
    pdf.drawString(180, y_position - 40, PATHOLOGY_CONTACT)

    # **Receipt Title**
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(230, y_position - 70, "Payment Receipt")

    # **Patient Details Section**
    y_position -= 100
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y_position, "Patient Details:")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, y_position - 20, f"Name: {patient.name}")
    pdf.drawString(60, y_position - 40, f"Phone: {patient.phone}")
    pdf.drawString(60, y_position - 60, f"Referred Doctor: {patient.referred_doctor if patient.referred_doctor else 'N/A'}")
    pdf.drawString(60, y_position - 80, f"Age: {patient.age} {patient.age_unit}")
    pdf.drawString(60, y_position - 100, f"Gender: {patient.gender}")

    # **Test Details Section**
    y_position -= 130
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y_position, "Tests Conducted:")

    # Table Header
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(80, y_position - 20, "Test Name")
    pdf.drawString(380, y_position - 20, "Price (₹)")
    pdf.line(50, y_position - 25, 550, y_position - 25)  # Horizontal line for table header

    # List Tests
    y_position -= 40
    pdf.setFont("Helvetica", 11)
    total_price = 0

    for test in patient.tests.all():
        pdf.drawString(80, y_position, f"{test.name}")
        pdf.drawString(400, y_position, f"₹{test.price}")
        total_price += test.price
        y_position -= 20  # Move to next row

    # **Total Amount**
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y_position - 20, "Total Amount Paid:")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(colors.red)
    pdf.drawString(400, y_position - 20, f"₹{total_price}")
    pdf.setFillColor(colors.black)

    # **Footer**
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.darkgray)
    pdf.drawString(50, y_position - 50, "Thank you for choosing XYZ Pathology Lab.")
    pdf.drawString(50, y_position - 70, "For any queries, contact us at support@xyzpathology.com")
    pdf.setFillColor(colors.black)

    # Save PDF
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
