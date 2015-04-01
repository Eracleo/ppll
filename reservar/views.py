from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView
from pyllik.models import Paquete, Pais, Reserva,Persona
from reservar.forms import PostForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from  django.forms.models  import  modelformset_factory
from  django.shortcuts  import  render_to_response
from  django.forms.models  import  inlineformset_factory
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.mail import EmailMessage
from django import forms
import paypal
def detalle(request, sku):
    paquete = Paquete.objects.get(sku=sku)
    if request.method == 'GET' and paquete.estado:
    #if request.POST :
        #paquete_nombre =  request.GET.get('paquete_id')
        #paquete = Paquete.objects.get(id=paquete_nombre)
        #cantidad_personas = request.POST.get('Cantidad_Personas')
        #fecha_viaje = request.POST.get('Fecha')
        #monto = int(cantidad_personas) * int(paquete.precio)
        context = {
            'paquete':paquete,
            'range':xrange(1,16)
            #'cantidad_personas':cantidad_personas,
            #'fecha_viaje':fecha_viaje,
            #'monto':monto
        }
        return render(request,'detalle.html',context)
    else :
        empresa = paquete.empresa
        return render(request,'deshabilitado.html',{'empresa':empresa})
def pasajeros(request,id):
    reserva = Reserva.objects.get(id=id)
    return render(request,'pasajeros.html',{'reserva':reserva})

def Post(request):
        form = ReservaaForm(request.POST)
        form.viajeros_instances = PersonaFormset(request.POST)
        if form.is_valid():
            #reserva = Reserva() #model class
            #reserva.paquete= form.cleaned_data()
            paquete=Paquete.objects.get(id=1)
            reserva = Reserva(paquete=paquete, cantidad_personas="2", fecha_viaje="2014-04-23", precio="1200")
            reserva.save()
            if form.viajeros_instances.cleaned_data is not None:
                for item in form.viajeros_instances.cleaned_data:
                    persona = Persona() #Product model class
                    persona.nombre= item['nombre']
                    persona.apellidos= item['apellidos']
                    persona.doc_tipo= item['doc_tipo']
                    persona.doc_nro= item['doc_nro']
                    persona.pais= item['pais']
                    persona.email= item['email']
                    persona.save()
                    reserva.viajeros.add(persona)

            return HttpResponseRedirect('/reservar/success')
        return HttpResponseRedirect('/reservar/failure')

def Failure(request):
    form = ReservaaForm()
    form.persona_instances = PersonaFormset()
    return render(request,'persona.html',{'form':form})
def Success(request):
    reserva = Reserva.objects.all()
    return render(request,'lista.html',{'reserva':reserva})
def Detalle(request,id):
    reserva = Reserva.objects.get(id=id)
    viajeros = reserva.viajeros.all()
    return render(request,'detalle1.html',{'Reserva':reserva, 'viajeros':viajeros})

def personasa(request):
    # Creando formulario registro personas con comboBox pais-gfgd
    paquete_id =  request.POST.get('paquete_id')
    paquete = Paquete.objects.get(id=paquete_id)
    cantidad_personas = request.POST.get('cantidad')
    fecha_viaje = request.POST.get('fecha')
    monto = request.POST.get('id_monto')
    email=request.POST.get('email')

    class PersonaForm(forms.ModelForm):
        class Meta:
            model = Persona

    #PersonaFormset= formset_factory(PersonaForm,extra=2,max_num=3)
    PersonaFormset= formset_factory(PersonaForm, extra=int(cantidad_personas), max_num=int(cantidad_personas))

    class ReservaaForm(forms.Form):

        paquete= forms.CharField(widget=forms.HiddenInput(),max_length=10)
        viajeros= PersonaFormset()

    if request.method == 'POST':
        form = ReservaaForm(request.POST)
        #user_id = request.user.id

        form.viajeros_instances = PersonaFormset(request.POST)
        if form.is_valid():
            titulo = 'LLIKA EIRL - Negotu.com'
            contenido = 'Reserva creada correctamente' + "\n"
            contenido +='Paquete: ' + paquete.nombre + "\n"
            contenido +='Viajeros:' + cantidad_personas + "\n"
            contenido +='Total a pagar: ' + monto
            correo = EmailMessage(titulo, contenido, to=[email])
            correo.send()
            reserva = Reserva(paquete=paquete, cantidad_personas=cantidad_personas, fecha_viaje=fecha_viaje, email=email)
            reserva.save()
            if form.viajeros_instances.cleaned_data is not None:
                for item in form.viajeros_instances.cleaned_data:
                    persona = Persona()
                    persona.nombre= item['nombre']
                    persona.apellidos= item['apellidos']
                    persona.doc_tipo= item['doc_tipo']
                    persona.doc_nro= item['doc_nro']
                    persona.pais= item['pais']
                    persona.email= item['email']
                    persona.save()
                    reserva.viajeros.add(persona)
            return HttpResponseRedirect('/reservar/pagar/'+str(reserva.id))
        else:
            form = ReservaaForm()
            form.viajeros_instances = PersonaFormset()

            context = {
                'paquete_id':paquete_id,
                'paquete':paquete,
                'cantidad_personas':cantidad_personas,
                'fecha_viaje':fecha_viaje,
                'monto':monto,
                'form':form,
                'email':email,
            }
        return render(request,'persona.html',context)
    else:
        form = ReservaaForm()
        form.viajeros_instances = PersonaFormset()

        context = {
            'paquete_id':paquete_id,
            'cantidad_personas':cantidad_personas,
            'fecha_viaje':fecha_viaje,
            'monto':monto,
            'form':form
        }
        return render(request,'jajaj.html',context)
def pagar(request,id):
    obj = Reserva.objects.get(id=id)
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
        'pdt_token':"2E-ni3FGiArjF6alEy8gu_SQ4BmlhzFYs09slOuer2XOrtnsHsWnIdR7hFO",
        'business':agencia.paypal_email,
        'merchant':"TG484VU34FSW6",
    }
    reserve = {
        'quantity':obj.cantidad_personas,
        'precio':obj.precio,
        'amount':obj.pre_pago,
        'item_name':obj.paquete,
        'item_number':obj.id,
        'currency_code':"USD",
    }
    context = {
        'paypal':paypal,
        'acount':acount,
        'reserve':reserve,
    }
    return render(request,'pagar.html',context)
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
    return HttpResponseRedirect('/reservar/cancelado/')
def confirmado(request):
    return render(request,'confirmado.html')
def cancelado(request):
    return render(request,'cancelado.html')