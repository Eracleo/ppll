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

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()
            titulo = 'LLIKA EIRL - Negotu.com'
            contenido = 'Bienvenido...'
            contenido += first_name
            contenido += ' gracias por crear su cuenta en Negotu.com' + "\n"
            contenido +='Usuario: ' + username + "\n"
            correo = EmailMessage(titulo, contenido, to=[email])
            correo.send()
            return HttpResponseRedirect(reverse('main'))
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
                return config(request)
            else:
                return HttpResponseRedirect('/user/login')
        else:
            return HttpResponseRedirect('/user/login')
    else:
        next = ''
        if 'next' in request.GET:
            next = request.GET['next']
        return render(request,'login.html',{'next':next})
def edit(request):
    return HttpResponseRedirect('/user')
