from django.conf.urls import patterns, url
from reservar import views
urlpatterns = patterns('',
    url(r'^paquete/precio/$','reservar.views.cancelado', name='cancelado'),
)
