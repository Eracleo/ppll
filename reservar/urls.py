from django.conf.urls import patterns, include, url
from reservar import views
urlpatterns = patterns('',
    url(r'^paquete/(?P<sku>[^/]+)$','reservar.views.detalle', name='detalle'),
    #url(r'^pasajeros/(?P<id>\d+)$','reservar.views.pasajeros', name='pasajeros'),
   # url(r'^guardar/$','reservar.views.guaradarpasajeros', name='viajeros'),
    url(r'^agregara/$','reservar.views.personasa', name='Persona'),
    url(r'^pagar/(?P<id>\d+)$','reservar.views.pagar', name='pagar'),
    url(r'^paypal/$','reservar.views.dePaypal', name='dePaypal'),
    url(r'^confirmado/$','reservar.views.confirmado', name='confirmado'),
    url(r'^cancelado/$','reservar.views.cancelado', name='cancelado'),
)
