from django.conf.urls import patterns, include, url
from usuario import views

urlpatterns = patterns('',
    url(r'^$', 'usuario.views.home', name='home'),
    url(r'^config$', 'usuario.views.config',name='config'),
    url(r'^usuario$', 'usuario.views.main',name='main'),
    url(r'^signup$', 'usuario.views.signup', name='signup'),
    url(r'^login$', 'usuario.views.login_view', name='login_view'),
    url(r'^logout$', 'usuario.views.logout_view', name='logout_view'),

)