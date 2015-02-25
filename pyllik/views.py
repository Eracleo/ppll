from django.shortcuts import render
from django.views.generic import ListView
from .models import Paqu

def index(request):
    return render(request,'index.html')
# Create your views here.
def ListarPaquetes(request):
	paquetes = Paquete.objects.all()
	return render(request,'layout/listarpaquetes.html',{'paquetes':paquetes})
