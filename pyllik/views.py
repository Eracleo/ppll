# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Paquete, Empresa, Reserva, Pasajero, Cliente
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, PaqueteEditForm, EmpresaForm, EmpresaFormEdit,PaypalAccountForm,PasajeroForm,ClienteForm,EmpresaFormEditLogo,BuscarReservaForm,BuscarClienteForm,ReservaEstadoForm,ReservaForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count
from collections import defaultdict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import uuid
@login_required
def index(request):
    return empresaDetail(request)
# EMPRESA
@login_required
def empresaDetail(request):
    try:
        id_user = request.user.id
        empresa = Empresa.objects.get(owner = id_user)
        request.session["empresa"] = empresa.id
        empresa_logo = request.session["logo"]
    except Empresa.DoesNotExist:
        if request.method == 'POST':
            usuario = Empresa(owner=request.user)
            abrev = request.POST['abreviatura']
            nro = request.POST['nro']
            if Empresa.objects.filter(abreviatura=abrev):
                formAgregar = EmpresaForm(request.POST,request.FILES, instance=usuario)
                messages.success(request, 'Información de empresa creado.')
                return render(request,'empresa/add.html', {'form':formAgregar,'abres':'si','nro':int(nro)+1})
            else:
                formAgregar = EmpresaForm(request.POST,request.FILES, instance=usuario)
                if formAgregar.is_valid():
                    empresa = formAgregar.save()
                    empresa.code = uuid.uuid1().hex
                    empresa.save()
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
        return render(request,'empresa/add.html', {'form':formAgregar})
    return render(request,'empresa/detail.html',{'obj':empresa,'logo':empresa_logo})
@login_required
def logo(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(owner = user_id)
    if request.method == 'POST':
        form = EmpresaFormEditLogo(request.POST,request.FILES,instance=empresa)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Logo de la empresa actualizado.')
                return HttpResponseRedirect('/user/config')
    form = EmpresaFormEditLogo(instance=empresa)
    ctx = {'form':form,'empresa':empresa,}
    return render(request,'empresa/logo.html', ctx)
@login_required
def empresaEdit(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(owner = user_id)
    if request.method == 'POST':
        form = EmpresaFormEdit(request.POST,request.FILES,instance=empresa)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Información de empresa actualizado.')
                return HttpResponseRedirect('/empresa/information')
    if request.method == 'GET':
        form = EmpresaFormEdit(instance=empresa)
    ctx = {'form':form,'empresa':empresa,}
    return render(request,'edit.html', ctx)
@login_required
def paypal_account(request):
    user_id = request.user.id
    empresa = Empresa.objects.get(owner = user_id)
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
    ctx = {'form':empresa_form,'empresa':empresa}
    return render(request,'edit.html', ctx)
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
def paquetesRendimiento(request):
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
    return render(request,'paquete/rendimiento.html',{'objs':paquetes,'logo':empresa_logo})
@login_required
def paqueteDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        paquete = Paquete.objects.get(id=id,empresa_id = empresa_id)
    except Paquete.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    return render(request,'paquete/detail.html',{'obj':paquete,'logo':empresa_logo})
@login_required
def paqueteEdit(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        paquete = Paquete.objects.get(id=id,empresa_id = empresa_id)
    except Paquete.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        form = PaqueteEditForm(request.POST,instance=paquete)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Datos actualizados.')
                return HttpResponseRedirect('/empresa/paquetes')
        else:
            messages.warning(request, 'Datos no validos')
    if request.method == 'GET':
        form = PaqueteForm(instance=paquete)
    ctx = {'form':form,'obj':paquete,'logo':empresa_logo}
    return render(request,'paquete/edit.html', ctx)
@login_required
def paqueteAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    ultimo = Paquete.objects.filter(empresa_id = empresa_id).latest('id')
    paquete = Paquete(empresa_id=empresa_id)
    if request.method == 'POST':
        form = PaqueteForm(request.POST,instance=paquete)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paquete creado.')
            return HttpResponseRedirect('/empresa/paquetes')
        else:
            messages.warning(request, 'Verefique los campos.')
            ctx = {
            'ultimo':ultimo.sku,
            'formAgregar':form,
            'logo':empresa_logo,}
            return render(request,'paquete/add.html', ctx)
    else:
        form=PaqueteForm()
        ctx = {
            'ultimo':ultimo.sku,
            'form':form,
            'logo':empresa_logo,}
        return render(request,'paquete/add.html', ctx)
@login_required
def reservaList(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    filtro = {}
    filtro['empresa_id'] = empresa_id
    if request.GET.get('estado'):
        filtro['estado_id'] = request.GET.get('estado');
    if request.GET.get('estado_pago'):
        filtro['estado_pago_id'] = request.GET.get('estado_pago');
    if request.GET.get('fecha_viaje'):
        filtro['fecha_viaje'] = request.GET.get('fecha_viaje');
    reserva = Reserva(**filtro)
    form = BuscarReservaForm(instance=reserva)
    objs_list = Reserva.objects.filter(**filtro).order_by('-id')
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'reserva/list.html',{'objs':objs,'logo':empresa_logo,'form':form})
@login_required
def reservaDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    except Reserva.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    return render(request,'reserva/detail.html',{'obj':reserva,'logo':empresa_logo})
@login_required
def reservaPaquete(request,sku):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        paquete = Paquete.objects.get(sku=sku,empresa_id = empresa_id)
    except Paquete.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            cliente = Cliente.objects.get(email = email,empresa_id=paquete.empresa_id)
        except Cliente.DoesNotExist:
            cliente = Cliente()
            cliente.email = email
            cliente.empresa = paquete.empresa
            cliente.save()
        obj = Reserva(empresa_id=empresa_id,paquete_id=paquete.id,cliente_id=cliente.id)
        form = ReservaForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Reserva creado.')
                return HttpResponseRedirect('/empresa/reservas')
        else:
            messages.warning(request, 'Verefique los campos.')
            ctx = {
            'form':form,
            'paquete':paquete,
            'logo':empresa_logo,}
            return render(request,'reserva/paquete.html', ctx)
    form=ReservaForm()
    ctx = {
        'paquete':paquete,
        'form':form,
        'logo':empresa_logo,}
    return render(request,'reserva/paquete.html', ctx)
@login_required
def reservaEstado(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    except Reserva.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        form = ReservaEstadoForm(request.POST,instance=reserva)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Estados actualizado')
                return HttpResponseRedirect('/empresa/reserva/detail/'+str(reserva.id))
        else:
            messages.warning(request, 'Datos no validos')
    if request.method == 'GET':
        form = ReservaEstadoForm(instance=reserva)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
# Pasajero
@login_required
def pasajeroDetail(request, id):
    empresa_id = request.session["empresa"]
    try:
        obj = Pasajero.objects.get(id=id,empresa_id = empresa_id)
    except Reserva.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    empresa_logo = request.session["logo"]
    return render(request,'pasajero/detail.html',{'obj':obj,'logo':empresa_logo})
@login_required
def pasajeroEdit(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        pasajero = Pasajero.objects.get(id=id,empresa_id = empresa_id)
    except Pasajero.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        form = PasajeroForm(request.POST,instance=pasajero)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Actualizado')
                return HttpResponseRedirect('/empresa/pasajeros')
        else:
            messages.warning(request, 'Datos no validos')
    if request.method == 'GET':
        form = PasajeroForm(instance=pasajero)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def pasajeros(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    objs_list = Pasajero.objects.filter(empresa_id = empresa_id)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'pasajero/list.html',{'objs':objs,'logo':empresa_logo})
@login_required
def pasajeroAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    if request.method == 'POST':
        obj = Pasajero(empresa_id=empresa_id)
        form = PasajeroForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Pasajero creado.')
                return HttpResponseRedirect('/empresa/pasajeros')
        else:
            messages.warning(request, 'Verefique los campos.')
            ctx = {
            'form':form,
            'logo':empresa_logo,}
            return render(request,'add.html', ctx)
    form=PasajeroForm()
    ctx = {
        'form':form,
        'logo':empresa_logo,}
    return render(request,'add.html', ctx)
# Cliente
@login_required
def clienteDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        obj = Cliente.objects.get(id=id,empresa_id = empresa_id)
    except Cliente.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    reservas = obj.reserva_set.all()
    return render(request,'cliente/detail.html',{'obj':obj,'logo':empresa_logo,'reservas':reservas})
@login_required
def clienteEdit(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        obj = Cliente.objects.get(id=id,empresa_id = empresa_id)
    except Cliente.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        form = ClienteForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Actualizado')
                return HttpResponseRedirect('/empresa/clientes')
        else:
            messages.warning(request, 'Datos no validos')
    if request.method == 'GET':
        form = ClienteForm(instance=obj)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def clientes(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    filtro = {}
    filtro['empresa_id'] = empresa_id
    if request.GET.get('email'):
        filtro['email'] = request.GET.get('email');
    if request.GET.get('pais'):
        filtro['pais_id'] = request.GET.get('pais');
    cliente =Cliente(**filtro)
    form = BuscarClienteForm(instance=cliente)
    objs_list = Cliente.objects.filter(**filtro)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'cliente/list.html',{'objs':objs,'logo':empresa_logo,'form':form})
@login_required
def clienteAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    if request.method == 'POST':
        obj = Cliente(empresa_id=empresa_id)
        form = ClienteForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Cliente creado.')
                return HttpResponseRedirect('/empresa/clientes')
        else:
            messages.warning(request, 'Verefique los campos.')
            ctx = {
            'form':form,
            'logo':empresa_logo,}
            return render(request,'add.html', ctx)
    form=ClienteForm()
    ctx = {
        'form':form,
        'logo':empresa_logo,}
    return render(request,'add.html', ctx)
def error404(request):
    return render(request,'errors/404.html')
def error403(request):
    return render(request,'errors/403.html')
def error500(request):
    return render(request,'errors/500.html')