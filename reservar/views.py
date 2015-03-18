from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView
from pyllik.models import Paquete, Pais, Reserva,Persona
from reservar.forms import PostForm
#from reservar.forms import PersonaForm
#from reservar.forms import PersonaFormset
#from reservar.forms import ReservaaForm
from reservar.forms import PostForm, ContactoForm
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
from pyllik.models import Reserva, Persona

 

def index(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = form.cleaned_data['created_at']
            post = m.Post.objects.create(content=content,
                                         created_at=created_at)
            return HttpResponseRedirect(reverse('post_detail',
                                                kwargs={'post_id': post.id}))
            #return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post.id}))
    return render(request, 'f_reservar.html', {
        'form': form,
    })
def detalle(request, id):
    paquete = Paquete.objects.get(id=id)
    if request.method == 'GET':
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
        HttpResponseRedirect('/')


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

#Correo de Confirmacion
def confircorreo(request):
    if request.method=='POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            titulo = 'Mensaje des pagos en LLIKA EIRL'
            contenido = formulario.cleaned_data['mensaje'] + "\n"
            contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
            correo = EmailMessage(titulo, contenido, to=['aridni81@gmail.com'])
            correo.send()
            return HttpResponseRedirect('/')
    else:
        formulario = ContactoForm()
    return render_to_response('confirmar.html',{'formulario':formulario}, context_instance=RequestContext(request))



def personasa(request):
    # Creando formulario registro personas con comboBox pais-gfgd
    paquete_id =  request.POST.get('paquete_id')
    paquete = Paquete.objects.get(id=paquete_id)
    cantidad_personas = request.POST.get('cantidad')
    fecha_viaje = request.POST.get('fecha')
    monto = request.POST.get('id_monto')

    class PersonaForm(forms.ModelForm):
        class Meta:
            model = Persona

    #PersonaFormset= formset_factory(PersonaForm,extra=2,max_num=3)
    PersonaFormset= formset_factory(PersonaForm, extra=int(cantidad_personas), max_num=int(cantidad_personas))

    class ReservaaForm(forms.Form):

        paquete= forms.CharField(max_length=100)    
        viajeros= PersonaFormset()

    
    if request.method == 'POST':        
        form = ReservaaForm(request.POST)
        #user_id = request.user.id
        
        form.viajeros_instances = PersonaFormset(request.POST)
        if form.is_valid():
            #reserva = Reserva() #model class
            #reserva.paquete= form.cleaned_data() 
            paquete=Paquete.objects.get(id=paquete_id)

            reserva = Reserva(paquete=paquete, cantidad_personas=cantidad_personas, fecha_viaje=fecha_viaje, precio=monto,user=request.user)
            #reserva.user_instances=user_id
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