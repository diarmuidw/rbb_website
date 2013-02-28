from django.db import models
from django.contrib import admin

class Customer(models.Model):
    customer_id         = models.IntegerField(null=False, unique=True, db_index=True)
    first_name          = models.CharField(max_length=30, null=False)
    last_name           = models.CharField(max_length=30, null=False)
    gps_latitude        = models.CharField(max_length=50, null=True)
    gps_longitude       = models.CharField(max_length=50, null=True)
    voip_number         = models.CharField(max_length=20, null=True, default='')
    ip                  = models.IPAddressField(unique=True, null=True, default='')
    billing_active      = models.NullBooleanField(null=True, default=0)
    def __unicode__(self):
        return (self.first_name + " " + self.last_name)


class Detail(models.Model):
    customer            = models.ForeignKey(Customer, db_index=True)
    time_stamp		= models.DateTimeField(auto_now_add=True)
    last_ping           = models.FloatField(null=True)
    avg_ping            = models.FloatField(null=True)
    sip_reg             = models.FloatField(null=True)
    on_call		= models.BooleanField(null=False, default=0)
    reg_ip              = models.IPAddressField(unique=False, null=True, default='')

