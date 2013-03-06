from django import forms

class CustomerForm(forms.Form):
    customer_name = forms.CharField(max_length=100, required=False)
    show_online = forms.BooleanField(required=False)
    billing_active = forms.BooleanField(required=False)
    
