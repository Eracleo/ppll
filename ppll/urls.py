from django.conf.urls import patterns, include, url
from django.contrib import admin
from pyllik import views
from django.conf import settings

handler404 = 'pyllik.views.error404'
handler403 = 'pyllik.views.error403'
handler500 = 'pyllik.views.error500'

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('usuario.urls')),
    url(r'^empresa/', include('pyllik.urls')),
    url(r'^logos/', include('pyllik.urls')),
    url(r'^reservar/', include('reservar.urls')),
    url(r'^pdf/', include('page.urls')),
    url(r'^carga/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': settings.MEDIA_ROOT, } ),
)
