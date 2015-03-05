from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView
from pyllik.models import Paquete, Pais, Reserva
from reservar.forms import PostForm
from django.http import HttpResponseRedirect
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
            #'cantidad_personas':cantidad_personas,
            #'fecha_viaje':fecha_viaje,
            #'monto':monto
        }
        return render(request,'detalle.html',context)
    else :
        HttpResponseRedirect('/')

# Creando formulario registro personas con comboBox pais-
def persona(request):
    if request.POST :
        cantidad_personas = request.POST.get('cantidad_personas')
        listapais = Pais.objects.all()
        context = {
            'cantidad_personas':cantidad_personas,
            'paises': listapais,
            'range':range(int(cantidad_personas))
        }
        return render(request,'persona.html',context)
    else :
        HttpResponseRedirect('/')
def pasajeros(request,id):
    reserva = Reserva.objects.get(id=id)
    return render(request,'pasajeros.html',{'reserva':reserva})