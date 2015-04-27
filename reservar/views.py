from django.shortcuts import render
from .forms import PersonaForm
from pyllik.models import Paquete, Pais, Reserva,Persona
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
def personas(request):
    empresa_logo = request.session["logo_pago"]
    # Creando formulario registro personas con comboBox pais-gfgd
    paquete_id =  request.POST.get('paquete_id')
    paquete = Paquete.objects.get(id=paquete_id)

    cantidad_personas = request.POST.get('cantidad')
    fecha_viaje = request.POST.get('fecha')
    monto = request.POST.get('id_monto')
    email=request.POST.get('email')
    ip=get_ip(request)

    PersonaFormset= formset_factory(PersonaForm, extra=int(cantidad_personas), max_num=int(cantidad_personas))

    class ReservarForm(forms.Form):
        paquete= forms.CharField(widget=forms.HiddenInput(),max_length=10)
        viajeros= PersonaFormset()

    if request.method == 'POST':
        form = ReservarForm(request.POST)
        form.viajeros_instances = PersonaFormset(request.POST)
        if form.is_valid():
            reserva = Reserva(paquete=paquete, cantidad_personas=cantidad_personas, fecha_viaje=fecha_viaje, email=email,ip=ip)
            reserva.save()
            if form.viajeros_instances.cleaned_data is not None:
                for item in form.viajeros_instances.cleaned_data:
                    persona = Persona()
                    persona.nombre= item['nombre']
                    persona.apellidos= item['apellidos']
                    persona.doc_tipo= item['doc_tipo']
                    persona.doc_nro= item['doc_nro']
                    persona.pais= item['pais']
                    persona.telefono= item['telefono']
                    persona.email= item['email']
                    persona.empresa = reserva.empresa
                    persona.save()
                    reserva.viajeros.add(persona)

            # Send message
            title = 'LLIKA EIRL - Negotu.com'
            body = 'Reserva creada correctamente' + "\n"
            body +='Paquete: ' + paquete.nombre + "\n"
            body +='Viajeros:' + cantidad_personas + "\n"
            body +='Total a pagar: ' + monto
            correo = EmailMessage(title, body, to=[email])
            correo.send()

            return HttpResponseRedirect('/reservar/pagar/'+str(reserva.id))
        else:
            form = ReservarForm()
            form.viajeros_instances = PersonaFormset()

            context = {
                'paquete_id':paquete_id,
                'paquete':paquete,
                'cantidad_personas':cantidad_personas,
                'fecha_viaje':fecha_viaje,
                'monto':monto,
                'form':form,
                'email':email,
                'logo': empresa_logo,
                'precio_total': int(cantidad_personas) * paquete.precio,
                'precio_total_pre': int(cantidad_personas) * paquete.pre_pago,
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
        'quantity':obj.cantidad_personas,
        'precio':obj.precio,
        'amount':obj.pre_pago,
        'total':obj.pre_pago*obj.cantidad_personas,
        'fecha':obj.fecha_viaje,
        'viajeros':obj.viajeros,
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
            if float(pdt['payment_gross']) >= reserva.cantidad_personas * reserva.pre_pago:
                reserva.tx = tx
                reserva.pago_estado = 'ad'
            else :
                reserva.pago_estado = 'in'
            reserva.save()
            # Send message
            title = "Negotu.com"
            body = "Detalles de pago de su reserva\n"
            body +="Paquete: " + str(reserva.paquete) + "\n"
            body +="Viajeros: " + str(reserva.cantidad_personas) + "\n"
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