from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^books/(?P<id>\d+)-reserve-(\d{4})-(\d+)-(\d+).pdf$','page.views.reserva', name='reserva'),
    url(r'^books/(?P<id>\d+)-(?P<tx>\w+)-reserve-(\d{4})-(\d+)-(\d+).pdf$','page.views.reserve', name='reserve'),
)
