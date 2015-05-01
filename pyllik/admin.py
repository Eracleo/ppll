from django.contrib import admin
from .models import Rubro, Pais, Empresa, EstadoPago,Cliente,Pasajero
# Register your models here.
admin.site.register(EstadoPago)
admin.site.register(Cliente)
admin.site.register(Pasajero)
admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Empresa)