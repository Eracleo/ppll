from django.shortcuts import render
from .forms import PasajeroForm
from pyllik.models import Paquete, Pais, Reserva,Pasajero, Cliente
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.core.mail import EmailMessage
from django import forms
import paypal
def get_ip(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip
def detalle(request, sku):
    paquete = Paquete.objects.get(sku=sku)
    request.session["logo_pago"] = paquete.empresa.logo.url
    empresa_logo = request.session["logo_pago"]
    if request.method == 'GET' and paquete.estado:
        context = {
            'paquete':paquete,
            'range':xrange(1,16),
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
            cliente = Cliente()
            cliente.email = email
            cliente.save()
            reserva = Reserva(paquete=paquete, cantidad_pasajeros=cantidad_pasajeros, fecha_viaje=fecha_viaje, cliente=cliente,ip=ip)
            reserva.save()
            if form.viajeros_instances.cleaned_data is not None:
                for item in form.viajeros_instances.cleaned_data:
                    pasajero = Pasajero()
                    pasajero.nombre= item['nombre']
                    pasajero.apellidos= item['apellidos']
                    pasajero.doc_tipo= item['doc_tipo']
                    pasajero.doc_nro= item['doc_nro']
                    pasajero.pais= item['pais']
                    pasajero.telefono= item['telefono']
                    pasajero.email= item['email']
                    pasajero.empresa = reserva.empresa
                    pasajero.save()
                    reserva.pasajeros.add(pasajero)
            # Send message
            title = 'LLIKA EIRL - Negotu.com'
            body = 'Reserva creada correctamente' + "\n"
            body +='Paquete: ' + paquete.nombre + "\n"
            body +='Viajeros:' + cantidad_pasajeros + "\n"
            body +='Total a pagar: ' + monto
            correo = EmailMessage(title, body, to=[email])
            correo.send()

            return HttpResponseRedirect('/reservar/pagar/'+str(reserva.id))
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
        return HttpResponseRedirect('reservar/paquete/BIB002')
def pagar(request,id):
    obj = Reserva.objects.get(id=id)
    request.session["logo_pago"] = ''
    empresa_logo = obj.empresa.logo.url
    request.session["logo_pago"] = empresa_logo
    # Datos a enviar
    paypal = {
        'paypal_url':"https://www.sandbox.paypal.com/cgi-bin/webscr",
        'paypal_pdt_url':"https://www.sandbox.paypal.com/au/cgi-bin/webscr",
        'return_url':"https://quipu.negotu.com/reservar/paypal/",
        'cancel_url':"https://quipu.negotu.com/reservar/cancelado/",
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

    reserva = Reserva.objects.get(id=ir)
    at = reserva.empresa.paypal_at

    success,pdt = paypal.paypal_check(tx,at)
    if success :
        if reserva.id == int(pdt['item_number']):
            if float(pdt['payment_gross']) >= reserva.cantidad_pasajeros * reserva.pre_pago:
                reserva.tx = tx
                reserva.pago_estado = 'ad'
            else :
                reserva.pago_estado = 'in'
            reserva.save()
            # Send message
            title = "Negotu.com"
            body = "Detalles de pago de su reserva\n"
            body +="Paquete: " + str(reserva.paquete) + "\n"
            body +="Viajeros: " + str(reserva.cantidad_pasajeros) + "\n"
            body +="Detalles de tus reserva: https://quipu.negotu.com/pdf/books/"+str(reserva.id)+"-"+reserva.tx+"-reserve-"+str(reserva.fecha_viaje.year)+"-"+str(reserva.fecha_viaje.month)+"-"+str(reserva.fecha_viaje.day)+".pdf\n"
            body +="Total a pagar: " + str(reserva.pre_pago)
            correo = EmailMessage(title, body, to=[reserva.email])
            correo.send()

            return HttpResponseRedirect("/reservar/confirmado/?id="+str(reserva.id)+"&y="+str(reserva.fecha_viaje.year)+"&m="+str(reserva.fecha_viaje.month)+"&d="+str(reserva.fecha_viaje.day)+"&tx="+tx)
    return HttpResponseRedirect('/reservar/cancelado/')
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