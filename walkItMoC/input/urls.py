from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^stop/$', views.stop, name='stop'),
    url(r'^walk/$', views.walk, name='walk'),
    url(r'^paper/$', views.paper, name='paper'),
    url(r'^coffee/$', views.coffee, name='coffee'),
    url(r'^about/$', views.about, name='about'),
]