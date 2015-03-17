from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView
from pyllik.models import Paquete, Pais, Reserva,Persona
from reservar.forms import PostForm, ContactoForm
from django.http import HttpResponseRedirect
from  django.forms.models  import  modelformset_factory 
from  django.shortcuts  import  render_to_response 
from  django.forms.models  import  inlineformset_factory 
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.mail import EmailMessage
 

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
# Creando formulario registro personas con comboBox pais-gfgd
def persona(request):
    if request.POST : 
        cantidad_personas = request.POST.get('cantidad')
        paquete_id = request.POST.get('paquete_id')
        fecha_viaje = request.POST.get('fecha')
        monto_total = request.POST.get('id_monto')
        AuthorFormSet  =  modelformset_factory ( Persona, extra=int(cantidad_personas) ) 
        formset  =  AuthorFormSet
        listapais = Pais.objects.all()
        context = {
            'cantidad':cantidad_personas,
            'paquete_id':paquete_id,
            'fecha':fecha_viaje,
            'monto':monto_total,
            'paises': listapais,
            'range':range(int(cantidad_personas)),
            'formset':formset
        }  
        return render(request,'persona.html',context)
    else :
        HttpResponseRedirect('/')   



def pasajeros(request,id):
    reserva = Reserva.objects.get(id=id)
    return render(request,'pasajeros.html',{'reserva':reserva})

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
