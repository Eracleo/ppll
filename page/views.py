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
    ref = "http://127.0.0.1:8000"+obj.empresa.logo.url

    y = 700
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.drawImage(ref, 50, y, 90,45)
    y  = y - 20

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
    p.drawString(480,y,str(obj.cantidad_pasajeros))
    y = y - 20
    p.drawString(280,y,'Total Price USD$') # 630
    p.drawString(480,y,str(obj.cantidad_pasajeros*obj.pre_pago))
    y = y - 20
    p.drawString(280,y,'Travel Date') # 610
    p.drawString(480,y,str(obj.fecha_viaje))

    p.drawString(50,500,'Reserve by:')
    p.drawString(130,500,obj.cliente.email)
    p.drawString(50,480,'Date:')
    p.drawString(130,480,str(obj.creado))
    p.line(50,470,560,470)
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
    ref = "http://127.0.0.1:8000"+obj.empresa.logo.url

    y = 700
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.drawImage(ref, 50, y, 90,45)
    y  = y - 20

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
    p.drawString(480,y,str(obj.cantidad_pasajeros))
    y = y - 20
    p.drawString(280,y,'Total Price USD$') # 630
    p.drawString(480,y,str(obj.cantidad_pasajeros*obj.pre_pago))
    y = y - 20
    p.drawString(280,y,'Travel Date') # 610
    p.drawString(480,y,str(obj.fecha_viaje))

    p.drawString(50,500,'Reserve by:')
    p.drawString(130,500,obj.cliente.email)
    p.drawString(50,480,'Date:')
    p.drawString(130,480,str(obj.creado))
    p.line(50,470,560,470)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response