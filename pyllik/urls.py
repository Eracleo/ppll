from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','pyllik.views.index', name='index'),
    url(r'^paquete.html$','pyllik.views.detalle', name='detalle'),
    # Paquetes
    url(r'^paquetes$','pyllik.views.paqueteList', name='paqueteList'),
    url(r'^paquete/detail/(?P<id>\d+)$','pyllik.views.paqueteDetail', name='paqueteDetail'),
    url(r'^paquete/edit/(?P<id>\d+)$','pyllik.views.paqueteEdit', name='paqueteEdit'),
    url(r'^paquete/add$','pyllik.views.paqueteAdd', name='paqueteAdd'),
    # Empresa
    #rl(r'^infomacion/$','pyllik.views.empresaDetalle', name='empresaDetalle'),
    #rl(r'^empresa/edit/(?P<id>\d+)$','pyllik.views.empresaEdit', name='empresaEdit'),
    # Reservas
    #rl(r'^reservas$','pyllik.views.reservaListar', name='reservaListar'),
    #rl(r'^reserva/detail/(?P<id>\d+)$','pyllik.views.reservaDetalle', name='reservaDetalle'),
    #rl(r'^reserva/edit/(?P<id>\d+)$','pyllik.views.reservaEdit', name='reservaEdit'),
    #rl(r'^reserva/add$','pyllik.views.reservaAdd', name='reservaAdd'),
)