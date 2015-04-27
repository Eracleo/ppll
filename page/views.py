from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from pyllik.models import Reserva
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'index.html')
@login_required
def reserva(request,id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="reserva.pdf"'
    response = HttpResponse(content_type='application/pdf')
    empresa_id = request.session["empresa"]
    obj = Reserva.objects.get(id=id,empresa_id = empresa_id)

    y = 730
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 20)
    p.drawString(50,y,obj.empresa.razon_social)
    p.setFont('Helvetica', 13)
    y=y-15
    p.drawString(50,y,obj.empresa.direccion)
    p.setFont('Helvetica', 18)
    y=y-25
    p.drawString(280,y,obj.paquete.nombre) #690
    p.setFont('Helvetica', 13)
    y=y-20
    p.drawString(280,y,'Price per Person USD$')
    p.drawString(480,y,str(obj.pre_pago))
    y=y-20
    p.drawString(280,y,'Number of passenger') # 650
    p.drawString(480,y,str(obj.cantidad_personas))
    y = y - 20
    p.drawString(280,y,'Total Price USD$') # 630
    p.drawString(480,y,str(obj.cantidad_personas*obj.pre_pago))
    y = y - 20
    p.drawString(280,y,'Travel Date') # 610
    p.drawString(480,y,str(obj.fecha_viaje))

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
def reserve(request,id,tx):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="reserva.pdf"'
    response = HttpResponse(content_type='application/pdf')
    obj = Reserva.objects.get(id=id,tx=tx)

    y = 730
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 20)
    p.drawString(50,y,obj.empresa.razon_social)
    p.setFont('Helvetica', 13)
    y=y-15
    p.drawString(50,y,obj.empresa.direccion)
    p.setFont('Helvetica', 18)
    y=y-25
    p.drawString(280,y,obj.paquete.nombre) #690
    p.setFont('Helvetica', 13)
    y=y-20
    p.drawString(280,y,'Price per Person USD$')
    p.drawString(480,y,str(obj.pre_pago))
    y=y-20
    p.drawString(280,y,'Number of passenger') # 650
    p.drawString(480,y,str(obj.cantidad_personas))
    y = y - 20
    p.drawString(280,y,'Total Price USD$') # 630
    p.drawString(480,y,str(obj.cantidad_personas*obj.pre_pago))
    y = y - 20
    p.drawString(280,y,'Travel Date') # 610
    p.drawString(480,y,str(obj.fecha_viaje))

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
