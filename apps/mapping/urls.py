from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from mapping import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^json$', views.getjson, name='json'),
    url(r'^sectorjson$', views.getsectorjson, name='getsectorjson'),
    url(r'^data$', views.getdata, name='data'),
    url(r'^outlasthour$', views.outlasthour, name='outlasthour'),
    url(r'^out$', views.out, name='out'),
    url(r'^viewmap$', views.viewmap, name='viewmap'),
    url(r'^viewsectors$', views.viewsectors, name='viewsectors'),
    url(r'^phoneoutrun$', views.phoneoutrun, name='phoneoutrun'),
    url(r'^chart$', views.chart, name='chart'),
    url(r'^test$', views.test, name='test'),
)


