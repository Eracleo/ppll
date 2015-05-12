# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.context import RequestContext
from pyllik.models import Empresa, Rubro, Trabajador,Paquete
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from forms import SignUpForm, EditForm, EmpresaForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
@login_required()
def main(request):
    request.session["empresa"]=1
    del request.session["empresa"]
    return render(request,'user/main.html')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/user/login')
def signup(request):
    if request.method == 'POST':
        signupF = SignUpForm(request.POST)
        empresaF = EmpresaForm(request.POST)
        if signupF.is_valid() and empresaF.is_valid():
            username = signupF.cleaned_data["username"]
            password = signupF.cleaned_data["password"]
            email = signupF.cleaned_data["email"]
            user = User.objects.create_user(username, email, password)

            empresa = empresaF.save()

            trabajador = Trabajador(user_id=user.id,empresa_id=empresa.id)
            trabajador.save()

            paquete = Paquete()
            paquete.sku = empresa.abreviatura + "001"
            paquete.nombre = "Paquete Inicial"
            paquete.estado = False
            paquete.empresa = empresa
            paquete.save()

            contenido = 'Estimado(a) '
            contenido += username
            contenido += "\n\nGracias por su interes en Negotu.com\n\n\nTu cuenta fue creado.\n"
            contenido += "\n\nSu Cuenta:\nURL: https://quipu.negotu.com/user/\nUsuario: " + username +"\nPassword: "+ password +"\n\n\nLlika Inversiones E.I.R.L\n www.llika.com\nhttp://www.negotu.com\nTelefono: 051 084 232460"
            correo = EmailMessage('Cuenta creada en Negotu', contenido, to=[email])
            correo.send()
            messages.success(request, 'Cuenta creada con exito. Revise su correo')
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.warning(request, 'Verifique su Información.')
    else:
        signupF = SignUpForm()
        empresaF = EmpresaForm()
    ctx = {
        'signup': signupF,
        'empresa': empresaF,
    }
    return render(request,'user/signup.html', ctx)
@login_required()
def home(request):
    empresa_logo = request.session["logo"]
    return render(request,'user/perfil.html', {'user': request.user,'logo':empresa_logo})
@login_required()
def config(request):
    try:
        id_user = request.user.id
        empresa = Trabajador.objects.get(user_id = id_user).empresa
        request.session["email"] = request.user.email
        request.session["empresa"] = empresa.id
        request.session["abreviatura"] = empresa.abreviatura
        request.session["razon_social"] = empresa.razon_social
        request.session["logo"] = empresa.logo.url_150x50
        return HttpResponseRedirect('/crm')
    except Trabajador.DoesNotExist:
        messages.info(request, 'Informacion de empresa falta crear')
        return HttpResponseRedirect('/crm/information')

@login_required()
def cambiar(request):
    if request.method == 'POST':
        user = request.user
        passa = request.POST['password']
        newpass=request.POST['next']
        success = user.check_password(passa)
        if success :
            user.set_password(newpass)
            user.save()
            messages.success(request, 'Su contraseña se ha cambiado satisfactoriamente.')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, 'Ingrese Correctamente su contraseña. Por favor intenta otra vez..')
            return render(request,'user/cambiarpass.html', {'user': request.user})
    else:
        messages.info(request,'Por favor, introduzca su contraseña antigua, por seguridad, y después introduzca la nueva contraseña dos veces para verificar que la ha escrito correctamente.')
        return render(request,'user/cambiarpass.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Bienvenido.')
                return config(request)
            else:
                messages.warning(request, 'Su cuenta no esta activado')
                return HttpResponseRedirect('/user/login')
        else:
            messages.warning(request, 'Cuenta no existe')
            return HttpResponseRedirect('/user/login')
    else:
        next = ''
        if 'next' in request.GET:
            next = request.GET['next']
        return render(request,'user/login.html',{'next':next})
@login_required()
def edit(request):
    user = request.user
    empresa_logo = request.session["logo"]
    if request.method == 'POST':
        frm = EditForm(request.POST)
        if frm.is_valid():
            user.email = frm.cleaned_data['email']
            user.first_name = frm.cleaned_data['first_name']
            user.last_name = frm.cleaned_data['last_name']
            user.save()
            messages.success(request, 'Datos Actualizados')
            return HttpResponseRedirect('/user')
    if request.method == 'GET':
        form = EditForm(initial=
            {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            })
    ctx = {'form':form,'logo':empresa_logo}
    return render(request,'user/edit.html',ctx)
