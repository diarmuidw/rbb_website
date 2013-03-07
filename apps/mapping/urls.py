from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from mapping import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^json$', views.getjson, name='json'),
   
)