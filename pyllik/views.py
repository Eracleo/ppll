from django.shortcuts import render
from django.template import RequestContext, loader
from .models import Paquete, Empresa, Reserva, ReservaDetalle
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, EmpresaForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
@login_required
def index(request):
    id_user = request.user.id
    empresa = Empresa.objects.get(user_id = id_user)
    return render(request,'information.html',{'obj':empresa})
# EMPRESA
@login_required
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
    return render(request,'paquete/list.html',{'objs':paquetes})
@login_required
def paqueteDetail(request, id):
    id_user = request.user.id
    paquete = Paquete.objects.get(id=id,user_id = id_user)
    return render(request,'paquete/detail.html',{'obj':paquete})
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
@login_required
def reservaList(request):
    id_user = request.user.id
    objs = Reserva.objects.filter(user_id = id_user)
    return render(request,'reserva/list.html',{'objs':objs})
@login_required
def reservaDetail(request, id):
    id_user = request.user.id
    reserva = Reserva.objects.get(id=id,user_id = id_user)
    reservaDetail = ReservaDetalle.objects.filter(reserva_id=id)
    return render(request,'reserva/detail.html',{'obj':reserva,'detail':reservaDetail })