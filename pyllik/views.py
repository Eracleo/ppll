# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Paquete, Empresa, Reserva, Persona
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, PaqueteEditForm, EmpresaForm, EmpresaFormEdit,PaypalAccountForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count
from collections import defaultdict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

@login_required
def index(request):
    return empresaDetail(request)
# EMPRESA
@login_required
def empresaDetail(request):
    try:
        id_user = request.user.id
        empresa = Empresa.objects.get(user_id = id_user)
        request.session["empresa"] = empresa.id
        empresa_logo = request.session["logo"]
    except Empresa.DoesNotExist:
        if request.method == 'POST':
            usuario = Empresa(user=request.user)
            abrev = request.POST['abreviatura']
            nro = request.POST['nro']
            if Empresa.objects.filter(abreviatura=abrev):
                formAgregar = EmpresaForm(request.POST,request.FILES, instance=usuario)
                messages.success(request, 'Información de empresa creado.')
                return render(request,'empresa/add.html', {'formAgregar':formAgregar,'abres':'si','nro':int(nro)+1})
            else:
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
                    return HttpResponseRedirect('/user/config')
        else:
            formAgregar = EmpresaForm()
        return render(request,'empresa/add.html', {'formAgregar':formAgregar})
    return render(request,'empresa/detail.html',{'obj':empresa,'logo':empresa_logo})

@login_required
def empresaEdit(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(user_id = user_id)
    #Guarda el formulario en la BD
    if request.method == 'POST':
        empresa_form = EmpresaFormEdit(request.POST,request.FILES)
        if empresa_form.is_valid():
            empresa.razon_social = empresa_form.cleaned_data['razon_social']
            empresa.rubro = empresa_form.cleaned_data['rubro']
            empresa.direccion = empresa_form.cleaned_data['direccion']
            empresa.ruc = empresa_form.cleaned_data['ruc']
            empresa.web = empresa_form.cleaned_data['web']
            empresa.telefono = empresa_form.cleaned_data['telefono']
            empresa.terminos_condiciones = empresa_form.cleaned_data['terminos_condiciones']
            #empresa.nro_paquetes = empresa_form.cleaned_data['nro_paquetes']
            empresa.save()
            messages.success(request, 'Información de empresa actualizado.')
            return HttpResponseRedirect('/empresa/information')
    if request.method == 'GET':
        empresa_form = EmpresaFormEdit(initial=
            {
                'rubro':empresa.rubro,
                'razon_social':empresa.razon_social,
                'ruc':empresa.ruc,
                'razon_social':empresa.razon_social,
                'ruc':empresa.ruc,
                'direccion':empresa.direccion,
                'web':empresa.web,
                'telefono':empresa.telefono,
                'terminos_condiciones':empresa.terminos_condiciones,
            })
    ctx = {'empresa_form':empresa_form,'empresa':empresa,}
    return render(request,'empresa/edit.html', ctx)
@login_required
def paypal_account(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(user_id = user_id)
    #Guarda el formulario en la BD
    if request.method == 'POST':
        empresa_form = PaypalAccountForm(request.POST,request.FILES)
        if empresa_form.is_valid():
            empresa.paypal_email = empresa_form.cleaned_data['paypal_email']
            empresa.paypal_at = empresa_form.cleaned_data['paypal_at']
            empresa.save()
            messages.success(request, 'Información de empresa actualizado.')
            return HttpResponseRedirect('/empresa/information')
    if request.method == 'GET':
        empresa_form = PaypalAccountForm(initial=
            {
                'paypal_email':empresa.paypal_email,
                'paypal_at':empresa.paypal_at,
            })
    ctx = {'empresa_form':empresa_form,'empresa':empresa,'titulo':"Editar"}
    return render(request,'form.html', ctx)

@login_required
def paqueteList(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    objs_list = Paquete.objects.filter(empresa_id = empresa_id).order_by('-id')
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        paquetes = paginator.page(page)
    except PageNotAnInteger:
        paquetes = paginator.page(1)
    except EmptyPage:
        paquetes = paginator.page(paginator.num_pages)

    return render(request,'paquete/list.html',{'objs':paquetes,'logo':empresa_logo})
@login_required
def paqueteDetail(request, id):
    empresa_id = request.session["empresa"]
    paquete = Paquete.objects.get(id=id,empresa_id = empresa_id)
    empresa_logo = request.session["logo"]
    return render(request,'paquete/detail.html',{'obj':paquete,'logo':empresa_logo})
@login_required
def paqueteEdit(request, id):
    empresa_id = request.session["empresa"]
    paquete = Paquete.objects.get(id=id,empresa_id = empresa_id)
    empresa_logo = request.session["logo"]
    if request.method == 'POST':
        paquete_form = PaqueteEditForm(request.POST)
        if paquete_form.is_valid():
            paquete.nombre = paquete_form.cleaned_data['nombre']
            paquete.precio = paquete_form.cleaned_data['precio']
            paquete.porcentaje = paquete_form.cleaned_data['porcentaje']
            paquete.pre_pago = paquete_form.cleaned_data['pre_pago']
            paquete.descripcion = paquete_form.cleaned_data['descripcion']
            paquete.estado = paquete_form.cleaned_data['estado']
            paquete.link = paquete_form.cleaned_data['link']
            paquete.save()
            return HttpResponseRedirect('/empresa/paquetes')
        else:
            messages.warning(request, 'Datod no validos')
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
    ctx = {'form':paquete_form,'Paquete':paquete,'logo':empresa_logo}
    return render(request,'paquete/edit.html', ctx)
@login_required
def paqueteAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    ultimo = Paquete.objects.filter(empresa_id = empresa_id).latest('id')
    nombre_empresa = Paquete(empresa_id=empresa_id)
    if request.method == 'POST':
        formAgregar = PaqueteForm(request.POST,instance=nombre_empresa)
        if formAgregar.is_valid():
            formAgregar.save()
            messages.success(request, 'Paquete creado.')
            return HttpResponseRedirect('/empresa/paquetes')
        else:
            messages.warning(request, 'Verefique los campos.')
            ctx = {
            'ultimo':ultimo.sku,
            'formAgregar':formAgregar,
            'logo':empresa_logo,}
            return render(request,'paquete/add.html', ctx)
    else:
        formAgregar=PaqueteForm()
        ctx = {
            'ultimo':ultimo.sku,
            'form':formAgregar,
            'logo':empresa_logo,}
        return render(request,'paquete/add.html', ctx)
@login_required
def reservaList(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    objs_list = Reserva.objects.filter(empresa_id = empresa_id).order_by('-id')
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'reserva/list.html',{'objs':objs,'logo':empresa_logo})
@login_required
def reservaDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    return render(request,'reserva/detail.html',{'obj':reserva,'logo':empresa_logo})
# PERSONA
@login_required
def personaDetail(request, id):
    empresa_id = request.session["empresa"]
    persona = Persona.objects.get(id=id,empresa_id = empresa_id)
    empresa_logo = request.session["logo"]
    return render(request,'persona/detail.html',{'obj':persona,'logo':empresa_logo})
@login_required
def personas(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    objs_list = Persona.objects.filter(empresa_id = empresa_id)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'persona/list.html',{'objs':objs,'logo':empresa_logo})
def error404(request):
    return render(request,'errors/404.html')
def error403(request):
    return render(request,'errors/403.html')
def error500(request):
    return render(request,'errors/500.html')
