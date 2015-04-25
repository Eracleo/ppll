from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from pyllik.models import Reserva
def index(request):
    return render(request,'index.html')
def reserva(request,id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="reserva.pdf"'
    response = HttpResponse(content_type='application/pdf')
    obj = Reserva.objects.get(id=id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 20)
    p.drawString(50,730,obj.empresa.razon_social)
    p.setFont('Helvetica', 13)
    p.drawString(50,715,obj.empresa.direccion)
    p.setFont('Helvetica', 18)
    p.drawString(280,690,obj.paquete.nombre)
    p.setFont('Helvetica', 13)

    p.drawString(280,670,'Price per Person USD$')
    p.drawString(480,670,str(obj.pre_pago))
    p.drawString(280,650,'Number of passenger')
    p.drawString(480,650,str(obj.cantidad_personas))
    p.drawString(280,630,'Total Price USD$')
    p.drawString(480,630,str(obj.cantidad_personas*obj.pre_pago))
    p.drawString(280,610,'Travel Date')
    p.drawString(480,610,str(obj.fecha_viaje))

    p.drawString(50,550,'Reserve by:')
    p.drawString(130,550,obj.email)
    p.drawString(50,530,'Date:')
    p.drawString(130,530,str(obj.creado))
    p.line(50,500,560,500)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response