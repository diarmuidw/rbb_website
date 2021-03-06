from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mapping.forms import CustomerForm
from mapping.models import Customer, Detail, Sector
from django.conf import settings
import anyjson

import logging

import google_chart
import sys, math
from math import radians, cos, sin, asin, atan,atan2, sqrt, pi, degrees, floor

from google_gis import SrtmTiff
s = SrtmTiff(settings.SRTM_FILE)




#import  google_map


# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    form = CustomerForm() # An unbound form
    return render_to_response('mapping/index.html', {'form':form,  'qs': ''
    })
    
@csrf_exempt
def out(request):
    form = CustomerForm() # An unbound form
    return render_to_response('mapping/out.html', {'form':form,  'qs': ''
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

            phone_out = 'off'
            try:
               
                phone_out = request.POST['phone_out']
               
            except:
                phone_out = 'off'
                pass  
                                
            has_phone = 'all'
            try:
                has_phone = request.POST['has_phone']
            except:
                has_phone = 'all'
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
            
            last_check_in = 'off'
            try:
               
                last_check_in = request.POST['last_check_in']
               
            except:
                last_check_in = 'off'
                pass 
                        
            display_sectors = 'off'
            try:
               
                display_sectors = request.POST['display_sectors']
               
            except:
                display_sectors = 'off'
                pass 

#form params for date range on phone reg 

            last_check_in_start_date = ''
            try:
                last_check_in_start_date = request.POST['last_check_in_start_date']
            except:
                last_check_in_start_date = ''
                pass 
    
            last_check_in_end_date = ''
            try:
                last_check_in_end_date = request.POST['last_check_in_end_date']
            except:
                last_check_in_end_date = ''
                pass 

            last_check_in_start_time = 0
            try:
                last_check_in_start_time = request.POST['last_check_in_start_time']
            except:
                last_check_in_start_time = 0
                pass 
    
            last_check_in_end_time = 0
            try:
                last_check_in_end_time = request.POST['last_check_in_end_time']
            except Exception, ex:
                last_check_in_end_time = 0
                print ex
                pass
            qs = 'last_check_in_start_date=%s&last_check_in_start_time=%s&last_check_in_end_date=%s&last_check_in_end_time=%s'%(last_check_in_start_date,last_check_in_start_time,last_check_in_end_date, last_check_in_end_time)
            
            qs = qs +'&' +'display_sectors=%s&last_check_in=%s&phone_out=%s&has_phone=%s&phone_active=%s&no_gps=%s&will_come_back=%s&customer_name=%s&billing_active=%s&show_online=%s&customer_id=%s&sector_id=%s'%(display_sectors,last_check_in,phone_out,has_phone,phone_active,no_gps,will_come_back,customer_name, billing_active,show_online,customer_id, sector_id)
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
    
    #print 'filter_data'
    #data = Customer.objects.filter(gps_longitude__lte = -9.0).filter(voip_number__startswith='0')
    data = Customer.objects.all()
    try:
        name = request.GET['customer_name']
        logger.debug( "name %s "%name)
        if name!='':
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
        has_phone = request.GET['has_phone']
        logger.debug( "has_phone %s "%has_phone)
        if has_phone == 'on':
            data = data.filter(voip_number__startswith='0')
        elif has_phone == "off":
            data = data.filter(voip_number__isnull=True)
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
            ##print details
            try:
                data = data.filter(detail__time_stamp__range=(an_hour_ago, now)).distinct()
                ##print data
            except Exception, ex:
                print ex
                pass
    except:
        pass  

    #now a tricky one
    #find phones that have a voip number but exclude those that were active in phone_out
    try:
        phone_out = request.GET['phone_out']
        logger.debug( "phone_out %s "%phone_out)
        if phone_out != 'off':
            #print 'doing phone out'
            from datetime import datetime, timedelta
            now = datetime.now()
            #print 'doing active phones'
            time_period = now - timedelta(hours=int(phone_out))
            try:
                activedata = Customer.objects.filter(detail__time_stamp__range=(time_period, now)).distinct()
                ##print activedata
            except Exception, ex:
                print ex       
            #print 'doing week phones'
            #now find phones active in the past week
            a_week_ago=  now - timedelta(hours=24*7)
            try:
                active_in_past_week = Customer.objects.filter(detail__time_stamp__range=(a_week_ago, now)).distinct()
                ##print active_in_past_week
            except Exception, ex:
                print ex    
                
##            d_4_days =  now - timedelta(hours=24*4)   
##             
##            try:
##                dd = Customer.objects.filter(detail__time_stamp__range=(a_week_ago, time_period)).distinct()
##                ##print activedata
##            except Exception, ex:
##                print ex   
                
            #print 'convert to list'
            try:
                activephones = list(activedata.values_list('customer_id', flat=True))
            except Exception, ex:
                print ex
            #print 'doing weekphones'
            weekphones = list(active_in_past_week.values_list('customer_id', flat=True))
            #ddd = list(dd.values_list('customer_id', flat=True))
            
            #print len(activephones)
            #print len(weekphones)
            ##print len(ddd)
            #print 'after active phones'
            
            for x in activephones:
                try:    
                    weekphones.remove(x)
                except Exception, ex:
                    pass
                    
##            for x in ddd:
##                try:    
##                    weekphones.remove(x)
##                except Exception, ex:
##                    pass
##            
                       
            data = data.filter(customer_id__in=[o for o in weekphones])
            
            #print 'after exclude'
    except Exception, ex:
        print ex
        pass  
    
    olddata = data
    print olddata
    
    #now do phone range
    try:
        last_check_in = request.GET['last_check_in']
        logger.debug( "last_check_in %s "%last_check_in)
        if last_check_in != 'off':
            #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            from datetime import datetime, timedelta
            now = datetime.now()
            start_range = 0
            end_range = 0
            if last_check_in == '0.25':
                start_range = now - timedelta(hours=0.25)
                end_range = now
            elif last_check_in == '0.5':
                start_range = now - timedelta(hours=0.5)
                end_range = now
            elif last_check_in == '1':
                start_range = now - timedelta(hours=int(1))
                end_range = now
            elif last_check_in == '2':
                start_range = now - timedelta(hours=int(2))
                end_range = now - timedelta(hours=int(1))
            elif last_check_in == '6':
                start_range = now - timedelta(hours=int(6))
                end_range = now - timedelta(hours=int(2))
            elif last_check_in == '12':
                start_range = now - timedelta(hours=int(12))
                end_range = now - timedelta(hours=int(6))
            elif last_check_in == '24':
                start_range = now - timedelta(hours=int(24))
                end_range = now - timedelta(hours=int(12))
            elif last_check_in == '48':
                start_range = now - timedelta(hours=int(48))
                end_range = now - timedelta(hours=int(24))
            elif last_check_in == '96':
                start_range = now - timedelta(hours=int(96))
                end_range = now - timedelta(hours=int(48))
            #print 'start_range %s'%start_range
            #print 'end_range  %s'%end_range
            
            try:
                data = Customer.objects.filter(latest__time_stamp__range=(start_range, end_range))
                ##print data
            except Exception, ex:
                print ex        
            activephones = list(data.values_list('customer_id', flat=True))
            ##print len(activephones)      
            
        

    except Exception, ex:
        print ex
        pass  
    
    #do a query based on the start and end date and time
    try:
        last_check_in_start_date = request.GET['last_check_in_start_date']
        last_check_in_start_time = request.GET['last_check_in_start_time']
        last_check_in_end_date = request.GET['last_check_in_end_date']
        last_check_in_end_time = request.GET['last_check_in_end_time']
        logger.debug( "last_check_in_start_date %s "%last_check_in_start_date)
        if last_check_in_start_date != '':
            #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            from datetime import datetime, timedelta
            now = datetime.now()
            start_range = 0
            end_range = 0
            start_range = now - timedelta(hours=0.25)
            end_range = now
           
            import time
            start_range = time.strptime(last_check_in_start_date + " " + last_check_in_start_time, "%Y-%m-%d %H")  
            start_range = datetime.fromtimestamp(time.mktime(start_range))
            if last_check_in_end_date != '':
                end_range = time.strptime(last_check_in_end_date + " " + last_check_in_end_time, "%Y-%m-%d %H")  
                end_range = datetime.fromtimestamp(time.mktime(end_range))
            else:
                end_range = now
            print start_range, end_range
            
            try:
                data = Customer.objects.filter(latest__time_stamp__range=(start_range, end_range))
                ##print data
            except Exception, ex:
                print ex        
            activephones = list(data.values_list('customer_id', flat=True))
            ##print len(activephones)      

    except Exception, ex:
        print ex
        pass  

    lastreg = list(data.values_list('customer_id', flat=True))
    data = olddata.filter(customer_id__in=[o for o in lastreg])
    
    
    l =  list(data.values_list('customer_id', flat=True))

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
    #print (rows)
    markers = anyjson.serialize(markers)

    return render(request, 'mapping/json.html', {
        "json":markers
    })

    
@csrf_exempt   
def getsectorjson(request):
    
    logger.debug('getsectorjson')
    logger.debug( request.GET)
    display_sectors = request.GET['display_sectors']
    data = Sector.objects.all()
    markers = {}
    rows = []
    for d in data:
        a = {}
        a['name'] = "%s"%(   d.name)
        a['long'] = d.gps_longitude
        a['lat'] = d.gps_latitude
        a['direction'] = d.direction
        a['angle'] = d.angle
        a['distance'] = d.distance
        a['color'] = d.color

        rows.append(a)
        
    markers['count'] = len(rows)
    markers['markers'] = rows
    
    markers = anyjson.serialize(markers)
    #print markers
    if display_sectors == 'off':
        markers = []
    return render(request, 'mapping/json.html', {
        "json":markers
    })
    
    
@csrf_exempt   
def viewmap(request):
    
    logger.debug('viewmap')
    logger.debug( request.GET)
    #print dir(request.GET)
    qs = ''
    for k in request.GET.keys():
        #print k, request.GET[k]
        qs = "%s&%s=%s"%(qs,k,request.GET[k])
    #print qs
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

    return render(request, 'mapping/map.html', {
        "json":markers, 'qs': qs
    })



    
def generate_sector_diagram(sectornumber, orig_lon, orig_lat, direction, sweepangle, range_, tower_height):
    R = 6378.1 #Radius of the Earth
    brng = 0 #Bearing is 90 degrees converted to radians.
    d = 3 #Distance in 

    start_angle = direction - sweepangle/2.0;
    end_angle = direction + sweepangle/2.0;

    elev_orig = s.get_elevation(orig_lat, orig_lon) + tower_height
    lat1 = math.radians(orig_lat) #Current lat point converted to radians
    lon1 = math.radians(orig_lon) #Current long point converted to radians


    ##print elev_orig

    coords = ''
    coords = coords + "var sector%s = ["%sectornumber

    north_lat = 0
    north_lon = 0
    north_d = 0
    coords = coords + "new google.maps.LatLng(%s, %s),\n"%(orig_lat,orig_lon)
    for brng in range(int(math.floor(start_angle)), int(math.ceil(end_angle)),1):
        #print brng, start_angle, direction, sweepangle
        brng = brng * math.pi/180
        previous_lon = 0
        previous_lat = 0
        still_visible = True
        previous_elev = 0
        max_elev = 0
        previous_d = 0
        for d in range(20,range_ *10):
            
            d = d/10.0
            lat2 = math.asin( math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R)*math.cos(brng))
            
            lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R) * math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
            
            lon2 = math.degrees(lon2)
        
            
            lat2 = math.degrees(lat2)
            ##print(lat2)
            try:
                elev = s.get_elevation(lat2, lon2)
            except:
                elev = 0
            if elev > max_elev and still_visible:
                max_elev = elev

            #and elev != -32768.0
            if still_visible:
                if (elev < elev_orig and elev <= max_elev )  or elev > previous_elev:
                    still_visible = True
                    previous_lon = lon2
                    previous_lat = lat2
                    previous_elev = elev
                    previous_d = d
                else:
                    still_visible= False
                
        #\#print(brng, d, lon2, lat2, elev)

        if brng == 0.0:
            north_lat = previous_lat 
            north_lon = previous_lon
            
        ##print(brng, previous_d, previous_lon, previous_lat, previous_elev)    
          
        ##print("new google.maps.LatLng(%s, %s),"%(previous_lat,previous_lon))
        coords = coords + "new google.maps.LatLng(%s, %s),\n"%(previous_lat,previous_lon)
    coords = coords + "new google.maps.LatLng(%s, %s),\n"%(orig_lat,orig_lon)  
    #coords = coords +  "new google.maps.LatLng(%s, %s),\n"%(north_lat,north_lon)
    coords = coords +  "];"

    return coords



def generateSectorRangeOverlay():
    #print 'generateSectorRangeOverlay'
    data = Sector.objects.all()
    i = 0
    js = ''
    setmap = ''
    cmd = '''var flightPath = new google.maps.Polyline({
    path: sector%s,
    strokeColor: '#%s',
    strokeOpacity: 1.0,
    strokeWeight: 2
  })\n;
flightPath.setMap(map);\n
'''

  
    for d in data:
        i = i +1
        a = {}
        a['name'] = "%s"%(   d.name)
        a['long'] = d.gps_longitude
        a['lat'] = d.gps_latitude
        a['direction'] = d.direction
        a['angle'] = d.angle
        a['distance'] = d.distance
        a['color'] = d.color
        
        coords = generate_sector_diagram(i,float(d.gps_longitude), float(d.gps_latitude), int(d.direction), int(d.angle), int(d.distance), 10)
        js =  js + coords + '\n'
        setmap = setmap + cmd%(i,d.color)
    return js +'\n' +setmap
    
    
   

@csrf_exempt   
def viewsectors(request):
    js = generateSectorRangeOverlay()
    logger.debug('viewmap')
    logger.debug( request.GET)
    #print dir(request.GET)
    qs = ''
    for k in request.GET.keys():
        #print k, request.GET[k]
        qs = "%s&%s=%s"%(qs,k,request.GET[k])
    #print qs
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

    return render(request, 'mapping/sectors.html', {
        "json":markers, 'qs': qs, 'js':js
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
        
    #rows = sorted(rows)
    markers['markers'] = rows
    markers = anyjson.serialize(markers)
    #print markers
    return render(request, 'mapping/data.html', {
        "data":rows
    })
    
    
@csrf_exempt   
def outlasthour(request):
    
    logger.debug('outlasthour')
    logger.debug( request.GET)
    from datetime import datetime, timedelta

    now = datetime.now()

 
    an_hour_ago = now - timedelta(hours=1)
    #details = Detail.objects.filter(time_stamp__range=(an_hour_ago, now))
    ##print details
    #this gets all phones active in last hour
    try:
        data = Customer.objects.filter(detail__time_stamp__range=(an_hour_ago, now)).distinct()
        ##print data
    except Exception, ex:
        print ex        
    activephones = list(data.values_list('customer_id', flat=True))
    
    ##print activephones
    #print len(activephones)

    try:
        outdata = Customer.objects.filter(voip_number__startswith='0').exclude(customer_id__in=[o for o in activephones])
        #print outdata
    except Exception, ex:
        print ex
    #print len(outdata)
    
    markers = {}
    rows = []
    for d in outdata:
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
        ##print a['id'], a['long'], a['lat']
    
    markers['count'] = len(rows)
    markers['markers'] = rows
    markers = anyjson.serialize(markers)
    
    ##print markers
    ##print rows
    return render(request, 'mapping/json.html', {
        "json":markers
    })
    
    
   
def phoneoutrun(request):
    logger.debug('phoneoutrun')
    logger.debug( request.GET)
    from datetime import datetime, timedelta

    now = datetime.now()

    an_hour_ago = now - timedelta(hours=16)
    #details = Detail.objects.filter(time_stamp__range=(an_hour_ago, now))
    ##print details
    #this gets all phones active in last hour
    try:
        data = Customer.objects.filter(latest__time_stamp__range=(an_hour_ago, now))
        ##print data
    except Exception, ex:
        print ex        
    activephones = list(data.values_list('customer_id', flat=True))
    #print len(activephones)
##    ##print activephones
##    #print len(activephones)
##    #print 'phoneoutrun'
##    try:
##        allphones = Customer.objects.filter(voip_number__startswith='0')#.exclude(customer_id__in=[o for o in activephones])
##        ##print outdata
##    except Exception, ex:
##        print ex
##    #print 
##    #print 'len of allphones = %s'%len(allphones)    
##    
##    for p in allphones:
##        #now do calcs for each phone
##        pass
##        
##    return allphones



#def calcBearing(lat1, lon1, lat2, lon2):
#    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#    dLon = lon2 - lon1
#    y = sin(dLon) * cos(lat2)
#    x = cos(lat1) * sin(lat2) \
#        - sin(lat1) * cos(lat2) * cos(dLon)
#    return degrees(atan2(y, x))
#
#Bearing = calcBearing(start_lat, start_lon, end_lat, end_lon)
#
#
##print "Bearing --> %s"%Bearing

def calculate_initial_compass_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing between two points.

 
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    pointA = (lat1,lon1)
    pointB = (lat2, lon2)
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180 to + 180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    b = dlat/dlon
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    
    c = 2 * asin(sqrt(a)) 
    km = 6367.1 * c
    return km 


def Generate_chart(start_lat, start_lon, end_lat, end_lon):
    logger.debug('Generate_chart')
    R = 6378.1
    try:
        hav =  haversine(start_lon, start_lat, end_lon, end_lat)
    except Exception, ex:
        logger.debug( ex)
        hav = 0
    #print "Distance --> %s"%hav
    Bearing2 = calculate_initial_compass_bearing(start_lat, start_lon, end_lat, end_lon)
    #print "Bearing2 --> %s"%Bearing2
    brng = radians(Bearing2)
    coords = []
    d = 0
    lat1 = math.radians(start_lat) #Current lat point converted to radians
    lon1 = math.radians(start_lon) #Current long point converted to radians
    #print lat1
    #print lon1
    logger.debug('before interval')
    interval = settings.ELEVATION_CHART_INTERVAL
    d = interval
    while d < hav:
        #print d
        lat2 = math.asin( math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R)*math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R) * math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
        lon2 = math.degrees(lon2)
        lat2 = math.degrees(lat2)
        ##print(lat2)
        try:
            elev = s.get_elevation(lat2, lon2)
        except Exception, ex:
            logger.debug( ex)
            elev = 0
            pass 
        ##print '%s, %s, %s, %s'%(lat2, lon2, d, elev)
        
        coord = {}
        coord['d'] = math.ceil(d * 100.0)/100.0
        coord['h'] = floor(elev)
        coords.append(coord)
        d = d + interval
    print 'print coords count', len(coords)
    ##print coords
    js = "['x','LOS', 'height'],\n"

    #put in first coord
    elev = s.get_elevation(start_lat, start_lon)
    start_elev = elev
    end_elev = coords[len(coords)-1]['h']
    print start_elev, end_elev
    #calc increment
    increment = (end_elev - start_elev)/float(len(coords))
    if  elev < 0:
        elev = 0
    js = js + "['%s', %s, %s],\n"%(0, start_elev , floor(elev))
    ##print js
    numberofsteps = 0.0
    for c in coords:
        if c['h'] < 0:
            c['h'] = 0
        if c['h'] > 1000:
            c['h'] = 0
        numberofsteps = numberofsteps + 1
        js = js + "['%s', %s,  %s],\n"%(c['d'],start_elev + increment*numberofsteps, c['h'])

    js = js + ']);'

    return js

@csrf_exempt   
def chart(request):
    logger.debug( 'starting chart')
    logger.debug( request.GET)
    lat_start = request.GET['lat1']
    logger.debug(lat_start)
    lng_start = request.GET['lon1']
    logger.debug(lng_start)
    lat_end = request.GET['lat2']
    logger.debug(lat_end)
    lng_end = request.GET['lon2']
    logger.debug(lng_end)
    logger.debug( 'chart - after requests')
    try:
        js = Generate_chart(float(lat_start),float(lng_start), float(lat_end),float(lng_end));
    except Exception, ex:
        logger.debug( ex)
    
    html = google_chart.start_html + js + google_chart.end_html
    logger.debug(html)
    return render(request, 'mapping/chart.html', {
        "html1":html
    }) 


    
@csrf_exempt   
def test(request):
    
    logger.debug('viewmap')
    logger.debug( request.GET)
    #print dir(request.GET)
    qs = ''
    for k in request.GET.keys():
        #print k, request.GET[k]
        qs = "%s&%s=%s"%(qs,k,request.GET[k])
    #print qs
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
    form = CustomerForm() # An unbound form
    return render(request, 'mapping/map2.html', {
        "json":markers, 'qs': qs, 'form':form
    })

