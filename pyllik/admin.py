from django.contrib import admin
from .models import Rubro, Pago,Pais, Empresa, EstadoPago,Cliente,Pasajero,Trabajador,Paquete
# Register your models here.
class EmpresaAdmin(admin.ModelAdmin):
    list_filter = ('creado','rubro')
    list_display = ('razon_social','ruc',)
    search_fields =('razon_social',)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('nombre','sku',)
admin.site.register(Trabajador)
admin.site.register(Pago)
admin.site.register(Paquete,PaqueteAdmin)
admin.site.register(EstadoPago)
admin.site.register(Cliente)
admin.site.register(Pasajero)
admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Empresa,EmpresaAdmin)