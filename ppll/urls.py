from django.conf.urls import patterns, include, url
from django.contrib import admin
from pyllik import views
from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^$',views.index,name='index'),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^user/', include('usuario.urls')),
        url(r'^empresa/', include('pyllik.urls')),
        url(r'^logos/', include('pyllik.urls')),
        url(r'^reservar/', include('reservar.urls')),
        url(r'^carga/(?P<path>.*)$', 'django.views.static.serve',
           {'document_root': settings.MEDIA_ROOT, } ),  
    #url(r'^agregarpaquete/$' , views.AgregarPaquete , name="agregar_paquete"),
    #url(r'^listarpaquetes/$' , views.ListarPaquetes , name="listar_paquetes"),
    #url(r'^listarpaquetes/editar_paquetes/(?P<paquete_id>\d+)/$', views.editar_paquetes, name="editar_paquetes"),
)
