from django.shortcuts import render
from .forms import PersonaForm
from django.views.generic import ListView
from pyllik.models import Paquete, Pais, Reserva,Persona
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from  django.forms.models  import  modelformset_factory
from  django.forms.models  import  inlineformset_factory
from django.template import RequestContext
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

            titulo = 'LLIKA EIRL - Negotu.com'
            contenido = 'Reserva creada correctamente' + "\n"
            contenido +='Paquete: ' + paquete.nombre + "\n"
            contenido +='Viajeros:' + cantidad_personas + "\n"
            contenido +='Total a pagar: ' + monto
            correo = EmailMessage(titulo, contenido, to=[email])
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
        'return_url':"http://127.0.0.1:8000/reservar/paypal/",
        'cancel_url':"http://127.0.0.1:8000/reservar/cancelado/",
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
            return HttpResponseRedirect('/reservar/confirmado/')
        else :
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/reservar/cancelado/')
def confirmado(request):
    empresa_logo = request.session["logo_pago"]
    del request.session["logo_pago"]
    return render(request,'confirmation.html',{'logo':empresa_logo})
def cancelado(request):
    empresa_logo = request.session["logo_pago"]
    return render(request,'cancelado.html',{'logo':empresa_logo})

