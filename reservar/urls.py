from django.conf.urls import patterns, include, url
from reservar import views
urlpatterns = patterns('',
    url(r'^$','reservar.views.index', name='index'),
    url(r'^reservar$','reservar.views.index', name='index'),
    url(r'^paquete/(?P<id>\d+)$','reservar.views.detalle', name='detalle'),
    url(r'^pasajeros/(?P<id>\d+)$','reservar.views.pasajeros', name='pasajeros'),
   # url(r'^guardar/$','reservar.views.guaradarpasajeros', name='viajeros'),
    url(r'^agregara/$','reservar.views.personasa', name='Persona'),
    url(r'^success/$','reservar.views.Success', name='Success'),
    url(r'^failure/$','reservar.views.Failure', name='Failure'),
    url(r'^detalle/(?P<id>\d+)$','reservar.views.Detalle', name='Detalle1'),
   # url(r'^dato.html$','reservar.views.persona', name='persona'),
    url(r'^confirmar/$','reservar.views.confircorreo', name='ConfirmarCorreo'),'),
)
