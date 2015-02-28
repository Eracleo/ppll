from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from .models import Paquete, Empresa
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, EmpresaForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# EMPRESA
def empresaDetail(request):
    id_user = request.user.id
    empresa = Empresa.objects.get(user_id = id_user)
    return render(request,'information.html',{'obj':empresa})
@login_required
def empresaEdit(request):
    id_user = request.user.id
    empresa = Empresa.objects.get(user_id = id_user)
    if request.method == 'POST':
        empresa_form = EmpresaForm(request.POST,request.FILES)
        if empresa_form.is_valid():
            empresa.razon_social = empresa_form.cleaned_data['razon_social']
            paquete.save()
            return HttpResponseRedirect('/empresa/paquetes')
    if request.method == 'GET':
        empresa_form = EmpresaForm(initial=
            {
                'razon_social':empresa.razon_social,
                'ruc':empresa.ruc,
            })
    ctx = {'empresa_form':empresa_form,'empresa':empresa}
    return render(request,'edit.html', ctx)
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
            paquete.nombre = paquete_form.cleaned_data['nombre']
            paquete.precio = paquete_form.cleaned_data['precio']
            paquete.descripcion = paquete_form.cleaned_data['descripcion']
            paquete.estado = paquete_form.cleaned_data['estado']
            paquete.save()
            return HttpResponseRedirect('/empresa/paquetes')
    if request.method == 'GET':
        paquete_form = PaqueteForm(initial=
            {
                'nombre':paquete.nombre,
                'precio':paquete.precio,
                'descripcion':paquete.descripcion,
                #'user':paquete.user,
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