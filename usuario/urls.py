from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from usuario import views

urlpatterns = patterns('',
    url(r'^$', 'usuario.views.home', name='home'),
    url(r'^config$', 'usuario.views.config',name='config'),
    url(r'^usuario$', 'usuario.views.main',name='main'),
    url(r'^signup$', 'usuario.views.signup', name='signup'),
    url(r'^login$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout$', logout, {'template_name': 'main.html', }, name="logout"),
    url(r'^cambiar$', 'usuario.views.cambiar', name="cambiar"),

)