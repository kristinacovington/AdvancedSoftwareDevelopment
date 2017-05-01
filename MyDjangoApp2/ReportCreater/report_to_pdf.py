from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.units import cm

#from .models import Report

def convert(report):
    response = HttpResponse(content_type='application/pdf')
    response.status_code = 200
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % report.report_name

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=pagesizes.A4)
    (width, height) = (pagesizes.A4)
    #21.0x29.7 cm page size

    xpos = width/2
    ypos = height - 50
    text =  "Report #%s, %s" % (report.id,report)
    p.drawCentredString(xpos, ypos, text)

    xpos = 75
    p.drawString(xpos, 700, "Company Name: " )
    p.drawString(xpos, 650, "Company's Location: ")
    p.drawString(xpos, 600, "Company Phone Number: ")
    p.drawString(xpos, 550, "Company Industry: ")
    p.drawString(xpos, 500, "Company Sector: ")
    p.drawString(xpos, 450, "Current Projects: ")

    xpos = 250
    p.drawString(xpos, 700, report.company_name)
    p.drawString(xpos, 650, report.company_location + ", " + report.company_country)
    p.drawString(xpos, 600, report.phone_number)
    p.drawString(xpos, 550, report.industry)
    p.drawString(xpos, 500, report.sector)
    p.drawString(xpos, 450, report.current_projects)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response