from django.conf.urls import patterns, include, url
from reservar import views
urlpatterns = patterns('',
    url(r'^$','reservar.views.index', name='index'),
    url(r'^reservar$','reservar.views.index', name='index'),
    url(r'^paquete.html$','reservar.views.detalle', name='detalle'),
    url(r'^dato.html$','reservar.views.persona', name='persona'),
)