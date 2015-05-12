# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Paquete, Empresa, Reserva, Pasajero, Cliente,TipoDocumento,Trabajador,Pago
from django.contrib.auth.decorators import login_required
from forms import PaqueteForm, PaqueteEditForm, EmpresaForm, EmpresaFormEdit,PaypalAccountForm,PasajeroForm,ClienteForm,TrabajadorForm,UserForm,EmpresaFormEditLogo,BuscarReservaForm,BuscarClienteForm,ReservaEstadoForm,ReservaForm,BuscarPasajeroForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms.formsets import formset_factory
from django import forms
def get_ip(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip
@login_required
def index(request):
    return empresaDetail(request)
# EMPRESA
@login_required
def empresaDetail(request):
    try:
        id_user = request.user.id
        empresa = Trabajador.objects.get(user_id = id_user).empresa
        request.session["empresa"] = empresa.id
        empresa_logo = request.session["logo"]
    except Trabajador.DoesNotExist:
        return HttpResponseRedirect('/user/logout')
    return render(request,'empresa/detail.html',{'obj':empresa,'logo':empresa_logo})
@login_required
def logo(request):
    empresa_logo = request.session["logo"]
    empresa_id = request.session["empresa"]
    empresa = Empresa.objects.get(id = empresa_id)
    if request.method == 'POST':
        form = EmpresaFormEditLogo(request.POST,request.FILES,instance=empresa)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Logo de la empresa actualizado.')
                return HttpResponseRedirect('/user/config')
    form = EmpresaFormEditLogo(instance=empresa)
    ctx = {'form':form,'empresa':empresa,'logo':empresa_logo}
    return render(request,'empresa/logo.html', ctx)
@login_required
def empresaEdit(request):
    empresa_logo = request.session["logo"]
    empresa_id = request.session["empresa"]
    empresa = Empresa.objects.get(id = empresa_id)
    if request.method == 'POST':
        form = EmpresaFormEdit(request.POST,request.FILES,instance=empresa)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Información de empresa actualizado.')
                return HttpResponseRedirect('/crm/information')
    if request.method == 'GET':
        form = EmpresaFormEdit(instance=empresa)
    ctx = {'form':form,'empresa':empresa,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def paypal_account(request):
    empresa_logo = request.session["logo"]
    empresa_id = request.session["empresa"]
    empresa = Empresa.objects.get(id = empresa_id)
    if request.method == 'POST':
        empresa_form = PaypalAccountForm(request.POST,request.FILES)
        if empresa_form.is_valid():
            empresa.paypal_email = empresa_form.cleaned_data['paypal_email']
            empresa.paypal_at = empresa_form.cleaned_data['paypal_at']
            empresa.save()
            messages.success(request, 'Información de empresa actualizado.')
            return HttpResponseRedirect('/crm/information')
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
                return HttpResponseRedirect('/crm/paquetes')
        else:
            messages.warning(request, 'Datos no validos')
    else:
        form = PaqueteForm(instance=paquete)
    ctx = {'form':form,'obj':paquete,'logo':empresa_logo}
    return render(request,'paquete/edit.html', ctx)
@login_required
def paqueteAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    paquete = Paquete(empresa_id=empresa_id)
    if request.method == 'POST':
        form = PaqueteForm(request.POST,instance=paquete)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paquete creado.')
            return HttpResponseRedirect('/crm/paquetes')
        else:
            messages.warning(request, 'Verefique los campos.')
    else:
        form=PaqueteForm()
    ctx = {
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
    if request.GET.get('paquete'):
        filtro['paquete_id'] = request.GET.get('paquete');
    if request.GET.get('estado_pago'):
        filtro['estado_pago_id'] = request.GET.get('estado_pago');
    if request.GET.get('fecha_viaje'):
        filtro['fecha_viaje'] = request.GET.get('fecha_viaje');
    reserva = Reserva(**filtro)
    form = BuscarReservaForm(empresa_id,instance=reserva)
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
def reservaConfirmadas(request):
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
    objs_list = Reserva.objects.filter(**filtro).order_by('-fecha_viaje')
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'reserva/confirmadas.html',{'objs':objs,'logo':empresa_logo,'form':form})
@login_required
def reservaDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    except Reserva.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    pagos = Pago.objects.filter(reserva_id=reserva.id)
    return render(request,'reserva/detail.html',{'obj':reserva,'logo':empresa_logo,'pagos':pagos})
@login_required
def reservaAddPasajero(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        reserva = Reserva.objects.get(id=id,empresa_id = empresa_id)
    except Reserva.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})

    PasajeroFormset= formset_factory(PasajeroForm, extra=reserva.cantidad_pasajeros, max_num=int(reserva.cantidad_pasajeros))

    if request.method == 'POST':
        form = PasajeroFormset(request.POST)
        if form.is_valid():
            for item in form:
                pasajero = Pasajero()
                pasajero.nombre= item['nombre'].value()
                pasajero.apellidos= item['apellidos'].value()
                pasajero.doc_tipo_id = item['doc_tipo'].value()
                pasajero.doc_nro= item['doc_tipo'].value()
                pasajero.pais_id= item['pais'].value()
                pasajero.telefono= item['telefono'].value()
                pasajero.email= item['email'].value()
                pasajero.empresa = reserva.empresa
                pasajero.save()
                reserva.pasajeros.add(pasajero)
            reserva.estado_id = 3
            reserva.save()
            messages.success(request, 'Pasajeros agregados')
        return HttpResponseRedirect('/crm/reserva/detail/'+str(reserva.id))
    else:
        form = PasajeroFormset()
        return render(request,'add.html',{'obj':reserva,'logo':empresa_logo,'form':form})
@login_required
def reservaPaquete(request,sku):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        paquete = Paquete.objects.get(sku=sku,empresa_id = empresa_id)
    except Paquete.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        ip=get_ip(request)
        email = request.POST.get('email')
        try:
            cliente = Cliente.objects.get(email = email,empresa_id=paquete.empresa_id)
        except Cliente.DoesNotExist:
            cliente = Cliente()
            cliente.email = email
            cliente.empresa = paquete.empresa
            cliente.save()
        obj = Reserva(empresa_id=empresa_id,paquete_id=paquete.id,cliente_id=cliente.id,ip=ip)
        form = ReservaForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Reserva creado.')
                return HttpResponseRedirect('/crm/reservas')
        else:
            messages.warning(request, 'Verefique los campos.')
    else:
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
                return HttpResponseRedirect('/crm/reserva/detail/'+str(reserva.id))
    else:
        form = ReservaEstadoForm(instance=reserva)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def pagos(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    filtro = {}
    filtro['empresa_id'] = empresa_id
    pago =Pago(**filtro)
    objs_list = Pago.objects.filter(**filtro)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'pago/list.html',{'objs':objs,'logo':empresa_logo})
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
                return HttpResponseRedirect('/crm/pasajeros')
        else:
            messages.warning(request, 'Datos no validos')
    else:
        form = PasajeroForm(instance=pasajero)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def pasajeros(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    filtro = {}
    filtro['empresa_id'] = empresa_id
    if request.GET.get('doc_nro'):
        filtro['doc_nro'] = request.GET.get('doc_nro');
    if request.GET.get('pais'):
        filtro['pais_id'] = request.GET.get('pais');
    pasajero =Pasajero(**filtro)
    form = BuscarPasajeroForm(instance=pasajero)
    objs_list = Pasajero.objects.filter(**filtro)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'pasajero/list.html',{'objs':objs,'logo':empresa_logo,'form':form})
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
                return HttpResponseRedirect('/crm/pasajeros')
        else:
            messages.warning(request, 'Verefique los campos.')
    else:
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
                return HttpResponseRedirect('/crm/clientes')
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
                return HttpResponseRedirect('/crm/clientes')
        else:
            messages.warning(request, 'Verefique los campos.')
    else:
        form=ClienteForm()
    ctx = {
        'form':form,
        'logo':empresa_logo,}
    return render(request,'add.html', ctx)
# Trabajadores
@login_required
def trabajadorDetail(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        obj = Trabajador.objects.get(user_id=id,empresa_id = empresa_id)
    except Trabajador.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    return render(request,'trabajador/detail.html',{'obj':obj,'logo':empresa_logo})
@login_required
def trabajadorEdit(request, id):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    try:
        obj = Trabajador.objects.get(user_id=id,empresa_id = empresa_id)
    except Trabajador.DoesNotExist:
        return render(request,'404-admin.html',{'logo':empresa_logo})
    if request.method == 'POST':
        form = TrabajadorForm(request.POST,instance=obj)
        if form.is_valid():
            if form.cleaned_data:
                form.save()
                messages.success(request, 'Actualizado')
                return HttpResponseRedirect('/crm/trabajadores')
        else:
            messages.warning(request, 'Datos no validos')
    if request.method == 'GET':
        form = TrabajadorForm(instance=obj)
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'edit.html', ctx)
@login_required
def trabajadores(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    filtro = {}
    filtro['empresa_id'] = empresa_id
    if request.GET.get('email'):
        filtro['email'] = request.GET.get('email');
    trabajador =Trabajador(**filtro)
    objs_list = Trabajador.objects.filter(**filtro)
    paginator = Paginator(objs_list, 30)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    return render(request,'trabajador/list.html',{'objs':objs,'logo':empresa_logo})
@login_required
def trabajadorAdd(request):
    empresa_id = request.session["empresa"]
    empresa_logo = request.session["logo"]
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = User.objects.create_user(username, email, password)
            obj = Trabajador(user_id=user.id,empresa_id=empresa_id)
            obj.save()
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, 'Trabajador creado.')
            return HttpResponseRedirect('/crm/trabajadores')
        else:
            messages.warning(request, 'Verefique los campos.')
    else:
        form=UserForm()
    ctx = {
        'form':form,
        'logo':empresa_logo,}
    return render(request,'trabajador/add.html', ctx)
def error404(request):
    return render(request,'errors/404.html')
def error403(request):
    return render(request,'errors/403.html')
def error500(request):
    return render(request,'errors/500.html')