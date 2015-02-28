from django.contrib import admin
from .models import Persona, Paquete, Reserva, ReservaDetalle, Rubro, Pais, Empresa
# Register your models here.
admin.site.register(Persona)
admin.site.register(Paquete)
admin.site.register(Reserva)
admin.site.register(ReservaDetalle)
admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Empresa)