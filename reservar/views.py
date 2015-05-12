from django.shortcuts import render
from .forms import PasajeroForm
from pyllik.models import Paquete, Pais,TipoDocumento,Reserva,Pasajero, Cliente,EstadoReserva,FormaPago,EstadoPago,ReservadoMediante,Pago
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.core.mail import EmailMessage
from django import forms
import paypal
import datetime
def get_ip(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip
def detalle(request, sku):
    try:
        paquete = Paquete.objects.get(sku=sku)
    except Paquete.DoesNotExist:
        return render(request,'404-reservar.html')
    request.session["logo_pago"] = paquete.empresa.logo.url
    empresa_logo = request.session["logo_pago"]
    if request.method == 'GET' and paquete.estado:
        context = {
            'paquete':paquete,
            'logo': empresa_logo,
        }
        return render(request,'product.html',context)
    else :
        empresa = paquete.empresa
        return render(request,'deshabilitado.html',{'empresa':empresa})
def pasajeros(request):
    empresa_logo = request.session["logo_pago"]
    paquete_id =  request.POST.get('paquete_id')
    paquete = Paquete.objects.get(id=paquete_id)

    cantidad_pasajeros = request.POST.get('cantidad')
    fecha_viaje = request.POST.get('fecha')
    monto = request.POST.get('id_monto')
    email=request.POST.get('email')
    ip=get_ip(request)

    PasajeroFormset= formset_factory(PasajeroForm, extra=int(cantidad_pasajeros), max_num=int(cantidad_pasajeros))

    class ReservarForm(forms.Form):
        paquete= forms.CharField(widget=forms.HiddenInput(),max_length=10)
        viajeros= PasajeroFormset()

    if request.method == 'POST':
        form = ReservarForm(request.POST)
        form.viajeros_instances = PasajeroFormset(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente.objects.get(email = email,empresa_id=paquete.empresa_id)
            except Cliente.DoesNotExist:
                cliente = Cliente()
                cliente.email = email
                cliente.empresa = paquete.empresa
                cliente.save()

            reserva = Reserva(paquete=paquete, cantidad_pasajeros=cantidad_pasajeros, fecha_viaje=fecha_viaje, cliente=cliente,ip=ip)
            reserva.estado_id = 1
            reserva.forma_pago_id = 2
            reserva.estado_pago_id = 1
            reserva.reservado_mediante_id = 2
            reserva.save()
            if form.viajeros_instances.cleaned_data is not None:
                for item in form.viajeros_instances.cleaned_data:
                    pasajero = Pasajero()
                    pasajero.nombre= item['nombre']
                    pasajero.apellidos= item['apellidos']
                    pasajero.doc_tipo = item['doc_tipo']
                    pasajero.doc_nro= item['doc_nro']
                    pasajero.pais= item['pais']
                    pasajero.telefono= item['telefono']
                    pasajero.email= item['email']
                    pasajero.empresa = reserva.empresa
                    pasajero.save()
                    reserva.pasajeros.add(pasajero)
            # Send message
            empresa = reserva.empresa
            title = empresa.razon_social + " - INVOICE "+ str(reserva.id)
            body = "<img heigth='50' src='httpw://quipu.negotu.com"+empresa.logo.url+"'>"
            body += "<h3>"+empresa.razon_social + "</h3><p>" + empresa.direccion + "<br>" + empresa.web + "</p>"
            body += "<h2>INVOICE CREATED Nro "+reserva.empresa.abreviatura+"-"+str(reserva.id)+"</h2><table>"
            body += "<tr><td width='160px'>Tour Name </td><td>: " + paquete.nombre
            body += "<tr><td width='160px'>Tour Date </td><td>: " + str(reserva.fecha_viaje)
            body += "</td></tr><tr><td>Tour price per Person</td><td>: USD $ " + str(reserva.precio)
            body += "</td></tr><tr><td>Number of Travelers</td><td>: " + str(reserva.cantidad_pasajeros)
            body += "</td></tr><tr><td>Total Price</td><td>:  USD $ " + str(reserva.precioTotal())
            body += "</td></tr><tr><td>Advance's mount ("+str(paquete.porcentaje)+"%)</td><td>:  USD $ " + str(reserva.precioTotalPrePago())
            body += "</td></tr><tr><td>Tax</td><td>: 0.00"
            body += "</td></tr><tr><td><p>Total payment</p></td><td>: USD $ " + str(reserva.precioTotalPrePago())
            code = str(reserva.id)+str(reserva.code)
            body += "</td></tr><tr><td>Link of Payment</td><td>: https://quipu.negotu.com/reservar/pagar/" + code
            body += "</td><tr><td>Booked by</td><td>: " + email
            body += "</td></tr></table>"
            body += "<br><br><p><b>Terms & Conditions:</b></p>" + empresa.terminos_condiciones
            body += "<br><br><p align='right'> Power by:<b><a href='http://negotu.com'>negotu.com</a></b></p>"
            msg = EmailMessage(title, body, to=[email,empresa.email])
            msg.content_subtype = "html"
            msg.send()

            return HttpResponseRedirect('/reservar/pagar/'+code)
        else:
            form = ReservarForm()
            form.viajeros_instances = PasajeroFormset()

            context = {
                'paquete_id':paquete_id,
                'paquete':paquete,
                'cantidad_pasajeros':cantidad_pasajeros,
                'fecha_viaje':fecha_viaje,
                'monto':monto,
                'form':form,
                'email':email,
                'logo': empresa_logo,
                'precio_total': int(cantidad_pasajeros) * paquete.precio,
                'precio_total_pre': int(cantidad_pasajeros) * paquete.pre_pago,
            }
        return render(request,'passenger.html',context)
    else:
        return HttpResponseRedirect('reservar/paquete/'+paquete.sku)
def pagar(request,id,code):
    try:
        obj = Reserva.objects.get(id=id,code=code)
    except Reserva.DoesNotExist:
        return render(request,'404-reservar.html')
    request.session["logo_pago"] = ''
    empresa_logo = obj.empresa.logo.url
    request.session["logo_pago"] = empresa_logo
    if obj.estado_pago_id > 1:
        empresa = obj.empresa
        ctx = {
            'logo':empresa_logo,
            'empresa':empresa,
        }
        return render(request,'pagado.html',ctx)
    # Datos a enviar
    paypal = {
        'paypal_url':"https://www.sandbox.paypal.com/cgi-bin/webscr",
        'paypal_pdt_url':"https://www.sandbox.paypal.com/au/cgi-bin/webscr",
        'return_url':"http://127.0.0.1:8000/reservar/paypal/",
        'cancel_url':"http://127.0.0.1:8000/reservar/cancelado/",
    }
    # Recuperar datos de la agencia
    agencia = obj.empresa
    acount = {
        'business':agencia.paypal_email,
    }
    reserve = {
        'quantity':obj.cantidad_pasajeros,
        'precio':obj.precio,
        'amount':obj.pre_pago,
        'total':obj.pre_pago*obj.cantidad_pasajeros,
        'fecha':obj.fecha_viaje,
        'pasajeros':obj.pasajeros,
        'item_name':obj.paquete,
        'item_number':obj.id,
        'currency_code':"USD",
    }
    context = {
        'paypal':paypal,
        'acount':acount,
        'reserve':reserve,
        'logo':empresa_logo,
    }
    return render(request,'payments.html',context)
def dePaypal(request):
    tx = request.GET.get('tx')
    ir = request.GET.get('item_number')
    try:
        reserva = Reserva.objects.get(id=ir)
    except Reserva.DoesNotExist:
        return render(request,'404-reservar.html')
    at = reserva.empresa.paypal_at

    success,pdt = paypal.paypal_check(tx,at)
    reserva.estado_pago_id=4
    reserva.save()

    if success :
        if reserva.id == int(pdt['item_number']):
            if float(pdt['payment_gross']) >= reserva.cantidad_pasajeros * reserva.pre_pago:
                reserva.estado_pago_id=3
                reserva.estado_id=2
            else :
                reserva.estado_pago_id=4
                reserva.estado_id=3
            #reserva.tx = tx
            #reserva.fecha_pago = datetime.datetime.now()
            reserva.save()

            pago = Pago(reserva_id=reserva.id)
            pago.precio = float(pdt['payment_gross'])
            pago.empresa_id = reserva.empresa_id
            pago.tx = tx
            pago.ip = get_ip(request)
            pago.forma_pago_id = 2
            pago.save()
            empresa = reserva.empresa
            title = empresa.razon_social + " - INVOICE "+ str(reserva.id)
            body = "<img heigth='50' src='httpw://quipu.negotu.com"+empresa.logo.url+"'>"
            body += "<h3>"+empresa.razon_social + "</h3><p>" + empresa.direccion + "<br>" + empresa.web + "</p>"
            body += "<h2>RECEIPT</h2><table>"
            body += "<tr><td width='160px'>Tour Name </td><td>: " + str(reserva.paquete)
            body += "<tr><td>Tour Date </td><td>: " + str(reserva.fecha_viaje)
            body += "</td></tr><tr><td>Tour price per Person</td><td>: USD $ " + str(reserva.precio)
            body += "</td></tr><tr><td>Number of Travelers</td><td>: " + str(reserva.cantidad_pasajeros)
            body += "</td></tr><tr><td>Total Price</td><td>:  USD $ " + str(int(reserva.cantidad_pasajeros)*reserva.precio)
            body += "</td></tr><tr><td>Advance's mount (%)</td><td>:  USD $ " + str(int(reserva.cantidad_pasajeros)*reserva.pre_pago)
            body += "</td></tr><tr><td>Tax</td><td>: 0.00"
            body += "</td></tr><tr><td><p>Total payment</p></td><td>: USD $ " + str(int(reserva.cantidad_pasajeros)*reserva.pre_pago)
            body += "</td></tr><tr><td>Date of paymet</td><td>: " + str(reserva.fecha_pago)
            body += "</td></tr><tr><td>Paymet form</td><td>: Paypal"
            body += "</td></tr><tr><td>Transaction ID</td><td>: " + tx
            body += "</td><tr><td>Booked by</td><td>: " + str(reserva.cliente)
            body += "</td></tr></table>"
            body += "<br><br><p><b>Terms & Conditions:</b></p>" + empresa.terminos_condiciones
            body += "<br><br><p align='right'> Power by:<b><a href='http://negotu.com'>negotu.com</a></b></p>"
            msg = EmailMessage(title, body, to=[str(reserva.cliente),empresa.email])
            msg.content_subtype = "html"
            msg.send()

            return HttpResponseRedirect("/reservar/confirmado/?id="+str(reserva.id)+"&y="+str(reserva.fecha_viaje.year)+"&m="+str(reserva.fecha_viaje.month)+"&d="+str(reserva.fecha_viaje.day)+"&tx="+tx)
        else:
            return render(request,'404-reservar.html')
    else :
        return render(request,'500-reservar.html')
    #return HttpResponseRedirect('/reservar/cancelado/')
def confirmado(request):
    empresa_logo = request.session["logo_pago"]
    ctx = {
        'logo':empresa_logo,
        'id':request.GET.get('id'),
        'y':request.GET.get('y'),
        'm':request.GET.get('m'),
        'd':request.GET.get('d'),
        'tx':request.GET.get('tx'),
        }
    return render(request,'confirmation.html',ctx)
def cancelado(request):
    empresa_logo = request.session["logo_pago"]
    return render(request,'cancelado.html',{'logo':empresa_logo})