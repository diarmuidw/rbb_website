from django.shortcuts import render_to_response
from django.shortcuts import render

from mapping.forms import CustomerForm

def index(request):

    return render_to_response('mapping/index.html', {
    })
    
def search(request):
    print "search"
    if request.method == 'POST': # If the form has been submitted...
            form = CustomerForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
                return render_to_response("hey hey")
    else:
        form = CustomerForm() # An unbound form
    
    j = '{"markers": [{"name": "Rosaleen Mc Carthy", "long": 9.1066, "lat": 51.627, "data1": "1", "id": "2", "data2": "1"}, {"name": "Brian + Louise  Elphick", "long": 8.9751, "lat": 51.6123, "data1": "1", "id": "3", "data2": "2"}, {"name": "Graham and Sally Crowley", "long": 3.15, "lat": 51.548, "data1": "1", "id": "6", "data2": "3"}, {"name": "Eithne O Donovan", "long": 9.0942, "lat": 51.5588, "data1": "1", "id": "9", "data2": "1"}, {"name": "Declan and Rita Carroll", "long": 3.1333, "lat": 51.5881, "data1": "1", "id": "12", "data2": "1"}]}'
    
    return render(request, 'mapping/index.html', {
        'form': form,'json':j, 'qs': 'name=C&iscustomer=yesy&data=123'
    })
    
    
def getjson(request):
    print request.GET
    j = '{"markers": [{"name": "Rosaleen Mc Carthy", "long": 9.1066, "lat": 51.627, "data1": "1", "id": "2", "data2": "1"}, {"name": "Brian + Louise  Elphick", "long": 8.9751, "lat": 51.6123, "data1": "1", "id": "3", "data2": "2"}, {"name": "Graham and Sally Crowley", "long": 3.15, "lat": 51.548, "data1": "1", "id": "6", "data2": "3"}, {"name": "Eithne O Donovan", "long": 9.0942, "lat": 51.5588, "data1": "1", "id": "9", "data2": "1"}, {"name": "Declan and Rita Carroll", "long": 3.1333, "lat": 51.5881, "data1": "1", "id": "12", "data2": "1"}]}'
    
    return render(request, 'mapping/json.html', {
        "json":j
    })