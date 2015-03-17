from django.conf.urls import patterns, include, url
from reservar import views
urlpatterns = patterns('',
    url(r'^$','reservar.views.index', name='index'),
    url(r'^reservar$','reservar.views.index', name='index'),
    url(r'^paquete/(?P<id>\d+)$','reservar.views.detalle', name='detalle'),
    url(r'^pasajeros/(?P<id>\d+)$','reservar.views.pasajeros', name='pasajeros'),
    url(r'^dato.html$','reservar.views.persona', name='persona'),
    url(r'^confirmar/$','reservar.views.confircorreo', name='ConfirmarCorreo'),
)