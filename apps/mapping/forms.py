from django import forms

class CustomerForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    show_online = forms.BooleanField(required=False)
    show_ex_customers = forms.BooleanField(required=False)
    
