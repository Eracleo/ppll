from django.conf.urls import patterns, include, url
from django.contrib import admin
from pyllik import views

from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.contrib.auth.views import login, logout
from usuario import views

urlpatterns = patterns('',
    url(r'^usuario$', 'usuario.views.main',name='main'),
    url(r'^signup$', 'usuario.views.signup', name='signup'),
    url(r'^login$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^home$', 'usuario.views.home', name='home'),
    url(r'^logout$', logout, {'template_name': 'main.html', }, name="logout"),
)