from django.shortcuts import render
from django.template import RequestContext, loader
from .models import Paquete, Empresa, Reserva, Persona
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, EmpresaForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count
from collections import defaultdict
@login_required
def index(request):
    return empresaDetail(request)
# EMPRESA
@login_required
def empresaDetail(request):
    context_instance = RequestContext(request)
    try:
        id_user = request.user.id
        empresa = Empresa.objects.get(user_id = id_user)
        request.session["empresa"] = empresa.id
    except Empresa.DoesNotExist:
        if request.method == 'POST':
            usuario = Empresa(user=request.user)
            formAgregar = EmpresaForm(request.POST,request.FILES, instance=usuario)
            if formAgregar.is_valid():
                empresa = formAgregar.save()
                paquete = Paquete()
                paquete.sku = empresa.abreviatura + "001"
                paquete.nombre = "Paquete Inicial"
                paquete.descripcion = "Este es un paquete inicial de prueba, puede editar su contenido!"
                paquete.precio = "0"
                paquete.porcentaje = "0"
                paquete.pre_pago = "0"
                paquete.empresa = empresa
                paquete.link = ""
                paquete.estado = False
                paquete.save()
                return HttpResponseRedirect('/empresa/information')
        else:
            formAgregar = EmpresaForm()
        return render(request,'add.html', {'formAgregar':formAgregar})
    return render(request,'information.html',{'obj':empresa})

@login_required
def empresaEdit(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(user_id = user_id)
    #Guarda el formulario en la BD
    if request.method == 'POST':
        empresa_form = EmpresaForm(request.POST,request.FILES)
        if empresa_form.is_valid():
            empresa.razon_social = empresa_form.cleaned_data['razon_social']
            empresa.rubro = empresa_form.cleaned_data['rubro']
            empresa.direccion = empresa_form.cleaned_data['direccion']
            empresa.ruc = empresa_form.cleaned_data['ruc']
            empresa.web = empresa_form.cleaned_data['web']
            empresa.paypal_email = empresa_form.cleaned_data['paypal_email']
            empresa.paypal_code = empresa_form.cleaned_data['paypal_code']
            #empresa.nro_paquetes = empresa_form.cleaned_data['nro_paquetes']
            empresa.logo = empresa_form.cleaned_data['logo']
            #empresa.user = empresa_form.cleaned_data['user']
            empresa.abreviatura = empresa_form.cleaned_data['abreviatura']
            #empresa.creado = empresa_form.cleaned_data['creado']
            #empresa.editado = empresa_form.cleaned_data['editado']
            empresa.save()
            return HttpResponseRedirect('/empresa/information')
    #Recupera los datos de la BD
    if request.method == 'GET':
        empresa_form = EmpresaForm(initial=
            {
                'rubro':empresa.rubro,
                'razon_social':empresa.razon_social,
                'ruc':empresa.ruc,
                'razon_social':empresa.razon_social,
                'ruc':empresa.ruc,
                'direccion':empresa.direccion,
                'web':empresa.web,
                'paypal_email':empresa.paypal_email,
                'paypal_code':empresa.paypal_code,
                'abreviatura':empresa.abreviatura,
                'logo':empresa.logo,
            })
    ctx = {'empresa_form':empresa_form,'empresa':empresa}
    return render(request,'edit.html', ctx)

@login_required
def paqueteList(request):
    empresa_id = request.session["empresa"]
    paquetes = Paquete.objects.filter(empresa_id = empresa_id)
    return render(request,'paquete/list.html',{'objs':paquetes})
@login_required
def paqueteDetail(request, id):
    empresa_id = request.session["empresa"]
    paquete = Paquete.objects.get(id=id,empresa_id = empresa_id)
    return render(request,'paquete/detail.html',{'obj':paquete})
@login_required
def paqueteEdit(request, id):
    paquete = Paquete.objects.get(id=id)
    if request.method == 'POST':
        paquete_form = PaqueteForm(request.POST)
        if paquete_form.is_valid():
            paquete.sku = paquete_form.cleaned_data['sku']
            paquete.nombre = paquete_form.cleaned_data['nombre']
            paquete.precio = paquete_form.cleaned_data['precio']
            paquete.porcentaje = paquete_form.cleaned_data['porcentaje']
            paquete.pre_pago = paquete_form.cleaned_data['pre_pago']
            paquete.descripcion = paquete_form.cleaned_data['descripcion']
            paquete.estado = paquete_form.cleaned_data['estado']
            paquete.link = paquete_form.cleaned_data['link']
            paquete.save()
            return HttpResponseRedirect('/empresa/paquetes')
    if request.method == 'GET':
        paquete_form = PaqueteForm(initial=
            {
                'sku':paquete.sku,
                'nombre':paquete.nombre,
                'precio':paquete.precio,
                'descripcion':paquete.descripcion,
                'estado':paquete.estado,
                'porcentaje':paquete.porcentaje,
                'pre_pago':paquete.pre_pago,
                'link':paquete.link,
            })
    ctx = {'paquete_form':paquete_form,'Paquete':paquete}
    return render(request,'paquete/edit.html', ctx)
@login_required
def paqueteAdd(request):
    context_instance = RequestContext(request)
    empresa_id = request.session["empresa"]
    ultimo = Paquete.objects.filter(empresa_id = empresa_id).latest('id')
    nombre_empresa = Paquete(empresa_id=empresa_id)
    if request.method == 'POST':
        formAgregar = PaqueteForm(request.POST,instance=nombre_empresa)
        if formAgregar.is_valid():
            formAgregar.save()
            return HttpResponseRedirect('/empresa/paquetes')
    if request.method == 'GET':
        formAgregar=PaqueteForm()
        ctx =   {   'ultimo':ultimo.sku,
                    'formAgregar':formAgregar,
                }
    else:
        formAgregar = PaqueteForm()
    return render(request,'paquete/add.html', ctx)
@login_required
def reservaList(request):
    empresa_id = request.session["empresa"]
    objs = Reserva.objects.filter(empresa_id = empresa_id)
    return render(request,'reserva/list.html',{'objs':objs})
@login_required
def reservaDetail(request, id):
    empresa_id = request.session["empresa"]
    reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    return render(request,'reserva/detail.html',{'obj':reserva})
# PERSONA
@login_required
def personaDetail(request, id):
    persona = Persona.objects.get(id=id)
    return render(request,'persona/detail.html',{'obj':persona})