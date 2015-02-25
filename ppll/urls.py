from django.conf.urls import patterns, include, url
from django.contrib import admin
from pyllik import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('usuario.urls')),
    url(r'^reservar/', include('pyllik.urls')),
)