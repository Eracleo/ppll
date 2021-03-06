# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.context import RequestContext
from pyllik.models import Empresa
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

@login_required()
def main(request):
    request.session["empresa"]=1
    del request.session["empresa"]
    return render(request,'main.html')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/user/login')
def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SignUpForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()
            titulo = 'Cuenta Creada Negotu'
            contenido = 'Estimado(a) '
            contenido += first_name
            contenido += "\n\nGracias por su interes en Negotu.com\n\n\nTu cuenta fue creado.\n"
            contenido += "\n\nSu Cuenta:\nURL: https://quipu.negotu.com/user/\nUsuario: " + username +"\nPassword: "+ password +"\n\n\nLlika Inversiones E.I.R.L\n www.llika.com\nhttp://www.negotu.com\nTelefono: 051 084 232460"
            correo = EmailMessage(titulo, contenido, to=[email])
            correo.send()
            messages.success(request, 'Cuenta creada con exito. Revise su correo')
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.warning(request, 'Verifique su Información.')
    else:
        form = SignUpForm()
    data = {
        'form': form,
    }

    return render(request,'signup.html', data)
@login_required()
def home(request):
    empresa_logo = request.session["logo"]
    return render(request,'perfil.html', {'user': request.user,'logo':empresa_logo})
@login_required()
def config(request):
    try:
        id_user = request.user.id
        empresa = Empresa.objects.get(user_id = id_user)
        request.session["email"] = request.user.email
        request.session["empresa"] = empresa.id
        request.session["abreviatura"] = empresa.abreviatura
        request.session["razon_social"] = empresa.razon_social
        request.session["logo"] = empresa.logo.url
        return HttpResponseRedirect('/user')
    except Empresa.DoesNotExist:
        messages.info(request, 'Informacion de empresa falta crear')
        return HttpResponseRedirect('/empresa/information')

@login_required()
def cambiar(request):
    if request.method == 'POST':
        name = request.POST['username']
        user = User.objects.get(username=name)
        passa = request.POST['password']
        newpass=request.POST['next']
        success = user.check_password(passa)
        if success :
            # do your email changing magic
            user.set_password(newpass)
            user.save()
            messages.success(request, 'Su contraseña se ha cambiado satisfactoriamente.')
            return HttpResponseRedirect('/user')
        else:
            return render(request,'cambiarpass.html', {'user': request.user,'mensaje':'si'})
    else:
        return render(request,'cambiarpass.html', {'user': request.user})

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
        return render(request,'login.html',{'next':next})
def edit(request):
    return HttpResponseRedirect('/user')
