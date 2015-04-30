from django.contrib import admin
from .models import Rubro, Pais, Empresa, EstadoPago,Paquete
# Register your models here.
admin.site.register(Paquete)
admin.site.register(EstadoPago)
admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Empresa)