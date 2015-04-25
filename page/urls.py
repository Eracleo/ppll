from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^books/(?P<id>\d+)-reserve-(\d{4})-(\d{2})-(\d+).pdf$','page.views.reserva', name='reserva'),
)
