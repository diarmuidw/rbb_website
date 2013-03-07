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
                    
                billing_active = 'all'
                try:
                    billing_active = request.POST['billing_active']
                   
                except:
                    billing_active = 'all'
                    pass   
                    
                show_online = '0'
                try:
                   
                    show_online = request.POST['show_online']
                   
                except:
                    show_online = ''
                    pass   

                customer_id = '0'
                try:
                   
                    customer_id = request.POST['customer_id']
                   
                except:
                    customer_id = ''
                    pass                      
                                        
                sector_id = 'all'
                try:
                   
                    sector_id = request.POST['sector_id']
                   
                except:
                    sector_id = 'all'
                    pass
                                                        
                qs = 'customer_name=%s&billing_active=%s&show_online=%s&customer_id=%s&sector_id=%s'%(customer_name, billing_active,show_online,customer_id, sector_id)
                print qs
                return render(request, 'mapping/index.html', {
                'form': form, 'qs': qs
                })
    else:
        form = CustomerForm() # An unbound form
    

    return render(request, 'mapping/index.html', {
        'form': form, 'qs': ''
    })
    
    
    
@csrf_exempt   
def getjson(request):
    print request.GET

    #data = Customer.objects.filter(gps_longitude__lte = -9.0).filter(voip_number__startswith='0')
    data = Customer.objects.filter(voip_number__startswith='0')
    try:
        name = request.GET['customer_name']
        print "name %s "%name
        data = Customer.objects.filter(last_name__contains=name)
    except:
        data = Customer.objects.all()
        pass
     
    try:
        billing_active = request.GET['billing_active']
        print "billing_active %s "%billing_active
        if billing_active == 'on':
            data = data.filter(billing_active__exact='1')
        elif billing_active == 'off':
            data = data.filter(billing_active__exact='0')
        
    except:
        
        pass        
    try:
        show_online = request.GET['show_online']
        print "show_online %s "%show_online
        if show_online == 'on':
            data = data.filter(ip__contains='9')
        elif show_online == 'off':
            data = data.filter(ip__isnull=True)
            pass
    except:
        pass    
         
    try:
        customer_id = request.GET['customer_id']
        print "customer_id %s "%customer_id
        if customer_id != '':
            data = data.filter(customer_id__iexact=customer_id)
            print data
        else:
            pass
    except:
        pass 
    
    try:
        
        sector_id = request.GET['sector_id']
        print "Sector_id %s "%sector_id
        if sector_id != 'all':
            data = data.filter(sector_id__exact=sector_id)
        
    except:
        pass  

    #data = data.filter(sector_id__exact='AP-Skibb')

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