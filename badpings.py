#!/usr/bin/python
import sys
import MySQLdb

import os
import sys

sys.path.append("/home/ids/Development/rbb_website")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rbb_website.settings")

from django.core.management import setup_environ
import settings

setup_environ(settings)
from django.db import models
from mapping.models import Customer, Detail, Sector

estonia_host = "91.142.225.201"
estonia_user = "rapidBBuser"
estonia_pass = "clonakilty&*Y*&784"
estonia_db = "monitoringServer"
estonia_port = 4498

mapping_host = "91.142.236.186"
mapping_user = "datauser"
mapping_pass = "V259BaGu"
mapping_db = "django_db"
mapping_port = 3386

try:
    estonia_db = MySQLdb.connect(host=estonia_host, user=estonia_user, passwd=estonia_pass, db=estonia_db, port=estonia_port)
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)


 
estonia_cursor = estonia_db.cursor()
sql = "select * from SIMPLEtodaysWorstPings"
sql = "select `customerQueue`.`customerID` AS `CustomerID`,`slowPingResults`.`ipAddress` AS `IPAddress`,`customerQueue`.`queueName` AS `CustomerName`,`accessPoint`.`id` AS `AP_ID`, `accessPoint`.`hostname` AS `AccessPoint`,min(`slowPingResults`.`minBadPing`) AS `MinimumBadPing (ms)`,max(`slowPingResults`.`maxBadPing`) AS `MaximumBadPing (ms)`,sum(`slowPingResults`.`numBadPings`) AS `NumberofBadPings`,((sum(`slowPingResults`.`numBadPings`) / sum(`slowPingResults`.`numTotPings`)) * 100) AS `BadPings %` from ((`slowPingResults` left join `customerQueue` on((`slowPingResults`.`ipAddress` = `customerQueue`.`targetAddresses`))) left join `accessPoint` on((`customerQueue`.`accessPointID` = `accessPoint`.`id`))) where ((`slowPingResults`.`date` = cast(now() as date)) and (`slowPingResults`.`numBadPings` > 1)) group by `slowPingResults`.`ipAddress` order by ((sum(`slowPingResults`.`numBadPings`) / sum(`slowPingResults`.`numTotPings`)) * 100) desc"
estonia_cursor.execute(sql)    
results = estonia_cursor.fetchall()
for row in results:
    c = Customer.objects.get(row[0])
    print c
    column1 = row[0]
    column2 = row[3]
    column3 = row[4]
    column4 = row[5]
    column5 = row[6]
    column6 = row[7]
    column7 = row[8]
    print " %s, %s, %s, %s, %s, %s, %s"%(column1,column2, column3, column4, column5, column6, column7)

estonia_db.close()

##
##try:
##    mapping_db = MySQLdb.connect(host=mapping_host, user=mapping_user, passwd=mapping_pass, db=mapping_db, port=mapping_port)
##except MySQLdb.Error, e:
##     print "Error %d: %s" % (e.args[0], e.args[1])
##     sys.exit (1)
##   
##mapping_cursor = mapping_db.cursor()
##sql = "select * from mapping_customer"
##mapping_cursor.execute(sql)    
##results = mapping_cursor.fetchall()
##for row in results:
##    column1 = row[0]
##    column2 = row[1]
##    print "column1: %s, column2: %s"%(column1,column2)
##

