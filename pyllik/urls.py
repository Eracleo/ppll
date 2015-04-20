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
    # Persona
    url(r'^persona/detail/(?P<id>\d+)$','pyllik.views.personaDetail', name='personaDetail'),
    url(r'^personas$','pyllik.views.personas', name='personas'),
)
