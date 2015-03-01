from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Paquetes
    url(r'^paquetes$','pyllik.views.paqueteList', name='paqueteList'),
    url(r'^paquete/detail/(?P<id>\d+)$','pyllik.views.paqueteDetail', name='paqueteDetail'),
    url(r'^paquete/edit/(?P<id>\d+)$','pyllik.views.paqueteEdit', name='paqueteEdit'),
    url(r'^paquete/add/$','pyllik.views.paqueteAdd', name='paqueteAdd'),
    # Empresa
    url(r'^information/$','pyllik.views.empresaDetail', name='empresaDetail'),
    url(r'^edit/$','pyllik.views.empresaEdit', name='empresaEdit'),
    # Reservas
    url(r'^reservas$','pyllik.views.reservaList', name='reservaList'),
    url(r'^reserva/detail/(?P<id>\d+)$','pyllik.views.reservaDetail', name='reservaDetail'),
    #rl(r'^reserva/edit/(?P<id>\d+)$','pyllik.views.reservaEdit', name='reservaEdit'),
    #rl(r'^reserva/add$','pyllik.views.reservaAdd', name='reservaAdd'),
)