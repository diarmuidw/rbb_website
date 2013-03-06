from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mapping.forms import CustomerForm
from mapping.models import Customer

import anyjson
@csrf_exempt
def index(request):
    form = CustomerForm() # An unbound form
    return render_to_response('mapping/index.html', {'form':form
    })
    
    
    
@csrf_exempt
def search(request):
    print "search"
    if request.method == 'POST': # If the form has been submitted...
            form = CustomerForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
                print request.POST
                customer_name = ''
                
                try:
                    customer_name = request.POST['customer_name']
                   
                except:
                    customer_name = ''
                    pass
                billing_active = '0'
                try:
                    billing_active = request.POST['billing_active']
                   
                except:
                    billing_active = ''
                    pass   
                    
                show_online = '0'
                try:
                    print 'aaaaaaaaaaaaaaaaaaa'
                    show_online = request.POST['show_online']
                   
                except:
                    online = ''
                    pass   
                    
                                        
                                     
                qs = 'customer_name=%s&billing_active=%s&show_online=%s'%(customer_name, billing_active,show_online)
                print qs
                return render(request, 'mapping/index.html', {
                'form': form, 'qs': qs
                })
    else:
        form = CustomerForm() # An unbound form
    
    #j = '{"markers": [{"name": "Rosaleen Mc Carthy", "long": 9.1066, "lat": 51.627, "data1": "1", "id": "2", "data2": "1"}, {"name": "Brian + Louise  Elphick", "long": 8.9751, "lat": 51.6123, "data1": "1", "id": "3", "data2": "2"}, {"name": "Graham and Sally Crowley", "long": 3.15, "lat": 51.548, "data1": "1", "id": "6", "data2": "3"}, {"name": "Eithne O Donovan", "long": 9.0942, "lat": 51.5588, "data1": "1", "id": "9", "data2": "1"}, {"name": "Declan and Rita Carroll", "long": 3.1333, "lat": 51.5881, "data1": "1", "id": "12", "data2": "1"}]}'
    print form
    return render(request, 'mapping/index.html', {
        'form': form, 'qs': ''
    })
    
    
    
@csrf_exempt   
def getjson(request):
    print request.GET
    #j = '{"markers": [{"name": "ssss", "long": 9.1066, "lat": 51.627, "data1": "1", "id": "2", "data2": "1"}, {"name": "cccccc", "long": 8.9751, "lat": 51.6123, "data1": "1", "id": "3", "data2": "2"}, {"name": "jjjjj", "long": 3.15, "lat": 51.548, "data1": "1", "id": "6", "data2": "3"}, {"name": "jj;lk;k;", "long": 9.0942, "lat": 51.5588, "data1": "1", "id": "9", "data2": "1"}, {"name": "iiiii", "long": 3.1333, "lat": 51.5881, "data1": "1", "id": "12", "data2": "1"}]}'
    
    #data = Customer.objects.filter(gps_longitude__lte = -9.0).filter(voip_number__startswith='0')
    data = Customer.objects.filter(voip_number__startswith='0')
    try:
        name = request.GET['customer_name']
        data = Customer.objects.filter(last_name__contains=name)
    except:
        data = Customer.objects.all()
        pass
     
    try:
        billing_active = request.GET['billing_active']
        if billing_active == 'on':
            data = data.filter(billing_active__exact='1')
        else:
            data = data.filter(billing_active__exact='0')
        
    except:
        
        pass        
    try:
        show_online = request.GET['show_online']
        print 'online'
        if show_online == 'on':
            data = data.filter(ip__contains='9')
        else:
            pass
        
        
    except:
        pass     
    #data = Customer.objects.all()
    markers = {}
    rows = []
    for d in data:
        a = {}
        a['name'] = "%s %s"%(   d.first_name, d.last_name)
        a['long'] = d.gps_longitude
        a['lat'] = d.gps_latitude
        a['id'] = str(d.customer_id)
        a['data1'] = str(1)
        a['data2'] = str(2)
        a['billing'] = str(d.billing_active)
        a['ip'] = str(d.ip)
        a['voip'] = str(d.voip_number)
        rows.append(a)
        

    markers['markers'] = rows
    markers = anyjson.serialize(markers)

    return render(request, 'mapping/json.html', {
        "json":markers
    })