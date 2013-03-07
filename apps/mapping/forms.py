from django import forms


ONLINE_CHOICES = (
    ('all', 'All'),
    ('on', 'Online'),
    ('off', 'Offline'),
)

BILLING_CHOICES = (
    ('all', 'All'),
    ('on', 'Billing'),
    ('off', 'Not Billing'),
)
   

class CustomerForm(forms.Form):
    customer_name = forms.CharField(max_length=100, required=False)
    #show_online = forms.BooleanField(required=False)
    show_online = forms.ChoiceField(choices=ONLINE_CHOICES, required = False)
    billing_active = forms.ChoiceField(choices=BILLING_CHOICES, required = False)
    customer_id = forms.CharField(max_length=5, required=False)
    
