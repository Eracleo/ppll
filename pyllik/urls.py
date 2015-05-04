from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    # Paquetes
    url(r'^paquetes$','pyllik.views.paqueteList', name='paqueteList'),
    url(r'^paquete/detail/(?P<id>\d+)$','pyllik.views.paqueteDetail', name='paqueteDetail'),
    url(r'^paquete/edit/(?P<id>\d+)$','pyllik.views.paqueteEdit', name='paqueteEdit'),
    url(r'^paquete/add/$','pyllik.views.paqueteAdd', name='paqueteAdd'),
    # Empresa
    url(r'^$','pyllik.views.index', name='index'),
    url(r'^information/$','pyllik.views.empresaDetail', name='empresaDetail'),
    url(r'^edit/$','pyllik.views.empresaEdit', name='empresaEdit'),
    url(r'^edit/paypal_account$','pyllik.views.paypal_account', name='paypal_account'),
    # Reservas
    url(r'^reservas$','pyllik.views.reservaList', name='reservaList'),
    url(r'^reserva/detail/(?P<id>\d+)$','pyllik.views.reservaDetail', name='reservaDetail'),
    #rl(r'^reserva/edit/(?P<id>\d+)$','pyllik.views.reservaEdit', name='reservaEdit'),
    #rl(r'^reserva/add$','pyllik.views.reservaAdd', name='reservaAdd'),
    # Pasajeros
    url(r'^pasajeros$','pyllik.views.pasajeros', name='pasajeros'),
    url(r'^pasajero/add$','pyllik.views.pasajeroAdd', name='pasajeroAdd'),
    url(r'^pasajero/detail/(?P<id>\d+)$','pyllik.views.pasajeroDetail', name='pasajeroDetail'),
    url(r'^pasajero/edit/(?P<id>\d+)$','pyllik.views.pasajeroEdit', name='pasajeroEdit'),
    # Clientes
    url(r'^clientes$','pyllik.views.clientes', name='clientes'),
    url(r'^cliente/add/$','pyllik.views.clienteAdd', name='clienteAdd'),
    url(r'^cliente/detail/(?P<id>\d+)$','pyllik.views.clienteDetail', name='clienteDetail'),
    url(r'^cliente/edit/(?P<id>\d+)$','pyllik.views.clienteEdit', name='clienteEdit'),
)
