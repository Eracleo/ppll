from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from .models import Paquete
from pyllik.forms import PostForm
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# PAQUETES
@login_required
def paqueteList(request):
    id_user = request.user.id
    paquetes = Paquete.objects.filter(user_id = id_user)
    return render(request,'paquete/list.html',{'paquetes':paquetes})
@login_required
def paqueteDetail(request, id):
    id_user = request.user.id
    paquete = Paquete.objects.get(id=id,user_id = id_user)
    return render(request,'paquete/detail.html',{'paquete':paquete})
@login_required
def paqueteEdit(request, id):
    paquete = Paquete.objects.get(id=id)
    if request.method == 'POST':
        paquete_form = PaqueteForm(request.POST,request.FILES)
        if paquete_form.is_valid():
            nombre = paquete_form.cleaned_data['nombre']
            precio = paquete_form.cleaned_data['precio']
            descripcion = paquete_form.cleaned_data['descripcion']
            user = paquete_form.cleaned_data['user']
            estado = paquete_form.cleaned_data['estado']
            paquete.nombre = nombre
            paquete.precio = precio
            paquete.descripcion = descripcion
            paquete.estado = estado
            paquete.save() #Guardar el modelo editar
            return HttpResponseRedirect('/empresa/paquetes')
    if request.method == 'GET':
        paquete_form = PaqueteForm(initial=
            {
                'nombre':paquete.nombre,
                'precio':paquete.precio,
                'descripcion':paquete.descripcion,
                'user':paquete.user,
                'estado':paquete.estado,
            })
    ctx = {'paquete_form':paquete_form,'Paquete':paquete}
    return render(request,'paquete/edit.html', ctx)
@login_required
def paqueteAdd(request):
    if request.method == 'POST':
        formAgregar = PaqueteForm(request.POST,request.FILES)
        if formAgregar.is_valid():
            formAgregar.save()
            return HttpResponseRedirect('/empresa/paquetes')
    else:
        formAgregar = PaqueteForm()
    return render(request,'paquete/add.html', {'formAgregar':formAgregar})

#Nuevo formularios
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
def detalle(request):
    if request.POST :
        paquete_id =  request.POST.get('Paquete_Id')
        paquete = Paquete.objects.get(id=paquete_id)
        cantidad_personas = request.POST.get('Cantidad_Personas')
        fecha_viaje = request.POST.get('Fecha')
        monto = int(cantidad_personas) * int(paquete.precio)
        context = {
            'paquete':paquete,
            'cantidad_personas':cantidad_personas,
            'fecha_viaje':fecha_viaje,
            'monto':monto
        }
        return render(request,'detalle.html',context)
    else :
        HttpResponseRedirect('/')
# Vistas para Gestionar Paquetes
# Editar Paquetes
@login_required
def editar_paquetes(request, paquete_id):
    	paquete = Paquete.objects.get(id=paquete_id)
    	if request.method == 'POST':
    		paquete_form = PaqueteForm(request.POST,request.FILES)
    		if paquete_form.is_valid():
    			nombre = paquete_form.cleaned_data['nombre']
    			precio = paquete_form.cleaned_data['precio']
    			descripcion = paquete_form.cleaned_data['descripcion']
    			user = paquete_form.cleaned_data['user']
    			estado = paquete_form.cleaned_data['estado']
    			paquete.nombre = nombre
    			paquete.precio = precio
    			paquete.descripcion = descripcion
    			paquete.estado = estado
    			paquete.save() #Guardar el modelo editar
    			return HttpResponseRedirect('/listarpaquetes/')
    	if request.method == 'GET':
        	paquete_form = PaqueteForm(initial=
        		{
        			'nombre':paquete.nombre,
        			'precio':paquete.precio,
        			'descripcion':paquete.descripcion,
        			'user':paquete.user,
        			'estado':paquete.estado,
        		})
        ctx = {'paquete_form':paquete_form,'Paquete':paquete}

	return render_to_response('layout/editar_paquete.html', ctx, context_instance=RequestContext(request))
