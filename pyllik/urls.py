from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','pyllik.views.index', name='index'),
    url(r'^paquete.html$','pyllik.views.detalle', name='detalle'),
)