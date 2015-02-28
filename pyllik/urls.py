from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','pyllik.views.index', name='index'),
    url(r'^paquete.html$','pyllik.views.detalle', name='detalle'),
    # Paquetes
    url(r'^paquetes$','pyllik.views.paqueteListar', name='paqueteListar'),
    url(r'^paquete/detalle/(?P<id>\d+)$','pyllik.views.paqueteDetalle', name='paqueteDetalle'),
    url(r'^paquete/edit/(?P<id>\d+)$','pyllik.views.paqueteEdit', name='paqueteEdit'),
    url(r'^paquete/add$','pyllik.views.paqueteAdd', name='paqueteAdd'),
    # Empresa
    url(r'^empresa$','pyllik.views.empresaDetalle', name='empresaDetalle'),
    url(r'^empresa/edit/(?P<id>\d+)$','pyllik.views.empresaEdit', name='empresaEdit'),
    # Reservas
    url(r'^reservas$','pyllik.views.reservaListar', name='reservaListar'),
    url(r'^reserva/detalle/(?P<id>\d+)$','pyllik.views.reservaDetalle', name='reservaDetalle'),
    url(r'^reserva/edit/(?P<id>\d+)$','pyllik.views.reservaEdit', name='reservaEdit'),
    url(r'^reserva/add$','pyllik.views.reservaAdd', name='reservaAdd'),
)