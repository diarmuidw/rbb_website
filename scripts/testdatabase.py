from django.core.management import setup_environ
import sys
sys.path.append('../../')
sys.path.append('../apps/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rbb_website.settings'

import rbb_website.settings
setup_environ(rbb_website.settings)

import anyjson

#
#from django.core.serializers import serialize
#from django.utils.simplejson import dumps, loads, JSONEncoder
#from django.db.models.query import QuerySet
#from django.utils.functional import curry
#
#class DjangoJSONEncoder(JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, QuerySet):
#            # `default` must return a python serializable
#            # structure, the easiest way is to load the JSON
#            # string produced by `serialize` and return it
#            return loads(serialize('json', obj))
#        return JSONEncoder.default(self,obj)
#    
#    

from rbb_website.apps.mapping.models import Customer

#
#data = Customer.objects.filter(gps_latitude__gte = "0")
#
#print data
##
##a = {}
##a['aaaa'] ='234'
##a['bbbbb'] = 'abc'
## 
###dumps = curry(dumps, cls=DjangoJSONEncoder)
##
###print dumps(a)
#a = {}
#for d in data:
#    #print d.dict()
#    a[d.gps_longitude] = d.dict()
#print a  
##print anyjson.serialize(a)


data = Customer.objects.filter(gps_longitude__lte = -9.2)
markers = []
for d in data:
    a = {}
    a['name'] = d
    a['long'] = d.gps_longitude
    a['lat'] = d.gps_latitude
    a['id'] = d.customer_id
    markers.append(a)

print markers