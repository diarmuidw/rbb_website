from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mapping.forms import CustomerForm
from mapping.models import Customer, Detail

import anyjson

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    form = CustomerForm() # An unbound form
    return render_to_response('mapping/index.html', {'form':form,  'qs': ''
    })
    
    
    
@csrf_exempt
def search(request):
    logger.debug( "search")
    if request.method == 'POST': # If the form has been submitted...
        form = CustomerForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
            logger.debug(request.POST)
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

            will_come_back = 'off'
            try:
               
                will_come_back = request.POST['will_come_back']
               
            except:
                will_come_back = 'off'
                pass   
                
            no_gps = 'off'
            try:
               
                no_gps = request.POST['no_gps']
               
            except:
                no_gps = 'off'
                pass 
                
            phone_active = 'off'
            try:
               
                phone_active = request.POST['phone_active']
               
            except:
                phone_active = 'off'
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
                                                    
            qs = 'phone_active=%s&no_gps=%s&will_come_back=%s&customer_name=%s&billing_active=%s&show_online=%s&customer_id=%s&sector_id=%s'%(phone_active,no_gps,will_come_back,customer_name, billing_active,show_online,customer_id, sector_id)
            logger.debug( qs)
            return render(request, 'mapping/index.html', {
            'form': form, 'qs': qs
            })
    else:
        form = CustomerForm() # An unbound form
    

    return render(request, 'mapping/index.html', {
        'form': form, 'qs': ''
    })
    
def filter_data(request):
    
    #data = Customer.objects.filter(gps_longitude__lte = -9.0).filter(voip_number__startswith='0')
    data = Customer.objects.filter(voip_number__startswith='0')
    try:
        name = request.GET['customer_name']
        logger.debug( "name %s "%name)
        data = Customer.objects.filter(last_name__contains=name)
    except:
        data = Customer.objects.all()
        pass
     
    try:
        billing_active = request.GET['billing_active']
        logger.debug( "billing_active %s "%billing_active)
        if billing_active == 'on':
            data = data.filter(billing_active__exact='1')
        elif billing_active == 'off':
            data = data.filter(billing_active__exact='0')
        
    except:
        
        pass        
    try:
        show_online = request.GET['show_online']
        logger.debug( "show_online %s "%show_online)
        if show_online == 'on':
            data = data.filter(ip__contains='9')
        elif show_online == 'off':
            data = data.filter(ip__isnull=True)
            pass
    except:
        pass    
 
    try:
        will_come_back = request.GET['will_come_back']
        logger.debug( "will_come_back %s "%will_come_back)
        if will_come_back == 'on':
            data = data.filter(will_come_back__exact='1')
        else: 
            pass
    except:
        pass 

    try:
        no_gps = request.GET['no_gps']
        logger.debug( "no_gps %s "%no_gps)
        if no_gps == 'on':
            data = data.filter(gps_latitude__exact='0')
        else: 
            pass
    except:
        pass 
                
    try:
        customer_id = request.GET['customer_id']
        logger.debug( "customer_id %s "%customer_id)
        if customer_id != '':
            data = data.filter(customer_id__iexact=customer_id)
            print data
        else:
            pass
    except:
        pass 
    
    try:
        
        sector_id = request.GET['sector_id']
        logger.debug( "Sector_id %s "%sector_id)
        if sector_id != 'all':
            data = data.filter(sector_id__exact=sector_id)
        
    except:
        pass  
        
    

    try:
        
        phone_active = request.GET['phone_active']
        logger.debug( "phone_active %s "%phone_active)
        if sector_id != 'off':
            from datetime import datetime, timedelta

            now = datetime.now()
            an_hour_ago = now - timedelta(hours=int(phone_active))
            #details = Detail.objects.filter(time_stamp__range=(an_hour_ago, now))
            #print details
            try:
                data = Customer.objects.filter(detail__time_stamp__range=(an_hour_ago, now)).distinct()
                print data
            except Exception, ex:
                print ex
        
    except:
        pass  
        
    return data    
    
@csrf_exempt   
def getjson(request):
    logger.debug('getjson')
    logger.debug( request.GET)
    
    data = filter_data(request)
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
        
    markers['count'] = len(rows)
    markers['markers'] = rows
   
    markers = anyjson.serialize(markers)

    return render(request, 'mapping/json.html', {
        "json":markers
    })
    
    
    
    
@csrf_exempt   
def getdata(request):
    logger.debug( request.GET)

    data = filter_data(request)
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
    #print markers
    return render(request, 'mapping/data.html', {
        "data":rows
    })
    
    
@csrf_exempt   
def lasthour(request):
    logger.debug('lasthour')
    logger.debug( request.GET)
    from datetime import datetime, timedelta

    now = datetime.now()

 
    an_hour_ago = now - timedelta(hours=100)
    #details = Detail.objects.filter(time_stamp__range=(an_hour_ago, now))
    #print details
    try:
        data = Customer.objects.filter(detail__time_stamp__range=(an_hour_ago, now)).distinct()
        print data
    except Exception, ex:
        print ex

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
    #print markers
    return render(request, 'mapping/index.html', {
        "data":rows
    })