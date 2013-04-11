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

HASPHONE_CHOICES= (
    ('all', 'All'),
    ('on', 'Has Phone Number'),
    ('off', 'No Phone Number'),
) 

  
PHONE_CHOICES = (
    ('off', 'Off'),
    ('1', '1 Hour'),
    ('2', '2 Hour'),
    ('6', '6 Hours'),
    ('12', '12 Hours'),
    ('24', '1 Day'),
    ('48', '2 Days'),
    ('96', '4 Days'),
    ('168', '1 Week'),
)

PHONE_RANGE_CHOICES = (
    ('off', 'Off'),
    ('1', '1 Hour'),
    ('2', '2 Hour'),
    ('6', '6 Hours'),
    ('12', '12 Hours'),
    ('24', '1 Day'),
    ('48', '2 Days'),
    ('96', '4 Days'),
    ('168', '1 Week'),
)
SECTOR_ID_CHOICES = (
    ('all', 'All'),
    ('None','None'),
    ('2.4 AP','2.4 AP'),
    ('2.4-BLD','2.4-BLD'),
    ('2.4timol','2.4timol'),
    ('AP-Skibb','AP-Skibb'),
    ('ARDFIELD-AP','ARDFIELD-AP'),
    ('Ardfield3','Ardfield3'),
    ('Ardfield3.1','Ardfield3.1'),
    ('Barna sct','Barna sct'),
    ('Butlerstown-Butlrs','Butlerstown-Butlrs'),
    ('Butlerstown-Courtmac','Butlerstown-Courtmac'),
    ('Butlerstown-Courtmac-2','Butlerstown-Courtmac-2'),
    ('CastleFrekeRBB','CastleFrekeRBB'),
    ('Crossbarry-3','Crossbarry-3'),
    ('JP 5GHz','JP 5GHz'),
    ('PTPCrossbarry','PTPCrossbarry'),
    ('RBB-rosscarbery1','RBB-rosscarbery1'),
    ('RBB-rosscarbery2','RBB-rosscarbery2'),
    ('RapibBB_Derrycool','RapibBB_Derrycool'),
    ('Rapid Broadband','Rapid Broadband'),
    ('Rapid Broadband 2','Rapid Broadband 2'),
    ('Rapid.Broadband.Kilmeen','Rapid.Broadband.Kilmeen'),
    ('RapidBB_Ballinglanna','RapidBB_Ballinglanna'),
    ('RapidBroadBandPN','RapidBroadBandPN'),
    ('RapidBroadband68','RapidBroadband68'),
    ('RapidBroadbandCahergal','RapidBroadbandCahergal'),
    ('RapidBroadbandClonlea','RapidBroadbandClonlea'),
    ('RapidBroadbandClonlea5','RapidBroadbandClonlea5'),
    ('RapidBroadbandDonoure','RapidBroadbandDonoure'),
    ('RapidBroadbandRineen','RapidBroadbandRineen'),
    ('Rapidbroadband478','Rapidbroadband478'),
    ('UHlink54','UHlink54'),
    ('ardfield-scly-1','ardfield-scly-1'),
    ('ardfield-scly-2','ardfield-scly-2'),
    ('ardfield-tc','ardfield-tc'),
    ('ban-ban-h-sct','ban-ban-h-sct'),
    ('ban-ban-h-sct1','ban-ban-h-sct1'),
    ('ban-sector-bal','ban-sector-bal'),
    ('ban-sector-bal-1','ban-sector-bal-1'),
    ('ban-sector-bal-2','ban-sector-bal-2'),
    ('ban-sector-bal-3','ban-sector-bal-3'),
    ('ban-sector-bal-4','ban-sector-bal-4'),
    ('ban-sector-clon','ban-sector-clon'),
    ('barna bandon','barna bandon'),
    ('barna innishannon','barna innishannon'),
    ('barryroe','barryroe'),
    ('bealad-south-sct','bealad-south-sct'),
    ('bealad-west-sct','bealad-west-sct'),
    ('bealadsector','bealadsector'),
    ('bealadsector-2','bealadsector-2'),
    ('bld-chr-ptmp','bld-chr-ptmp'),
    ('bld-chrgh','bld-chrgh'),
    ('bld-gldr-ptmp','bld-gldr-ptmp'),
    ('bluid2','bluid2'),
    ('bluid3','bluid3'),
    ('btlrstwn-cln-1','btlrstwn-cln-1'),
    ('btlrstwn-cln-2','btlrstwn-cln-2'),
    ('caherbeg-ross','caherbeg-ross'),
    ('caherbeg-windm','caherbeg-windm'),
    ('caherbegMikroTik60','caherbegMikroTik60'),
    ('caherbegp2p','caherbegp2p'),
    ('caherbegsector','caherbegsector'),
    ('castle2','castle2'),
    ('castle3','castle3'),
    ('chrbg-bealad-3,frequency = 5','chrbg-bealad-3,frequency = 5'),
    ('clgby-crtmcshrry','clgby-crtmcshrry'),
    ('cool sector','cool sector'),
    ('cool-ban','cool-ban'),
    ('cool-clon','cool-clon'),
    ('coolig-pink-ptp(h)','coolig-pink-ptp(h)'),
    ('coppeen-sct1','coppeen-sct1'),
    ('coppeen-sct2','coppeen-sct2'),
    ('derryduff-sct','derryduff-sct'),
    ('derryduff-sct1','derryduff-sct1'),
    ('derryduff-sct2','derryduff-sct2'),
    ('derryduff-sct3','derryduff-sct3'),
    ('dfBandon','dfBandon'),
    ('dfKilbritain','dfKilbritain'),
    ('drmlg-se-sct','drmlg-se-sct'),
    ('drmlg-sw-sct','drmlg-sw-sct'),
    ('dunm-ptp','dunm-ptp'),
    ('dunmanwaysector','dunmanwaysector'),
    ('glandoresct','glandoresct'),
    ('grtr-sct1','grtr-sct1'),
    ('grtr-sct2','grtr-sct2'),
    ('grtr-sct3','grtr-sct3'),
    ('heg-ban','heg-ban'),
    ('heg-drin','heg-drin'),
    ('heg-dun','heg-dun'),
    ('hh-bndn-sct','hh-bndn-sct'),
    ('hh-dndrw-sct','hh-dndrw-sct'),
    ('hh-inshn-sct','hh-inshn-sct'),
    ('horsehill','horsehill'),
    ('jp','jp'),
    ('klgbn-sct1','klgbn-sct1'),
    ('klgbn-sct2','klgbn-sct2'),
    ('klgbn-sct3','klgbn-sct3'),
    ('leap-chrgh-sct','leap-chrgh-sct'),
    ('leap-nrth-sct','leap-nrth-sct'),
    ('lepsec','lepsec'),
    ('lepskib','lepskib'),
    ('mikrotik3.5','mikrotik3.5'),
    ('rapidbroadband2','rapidbroadband2'),
    ('rossmoresector','rossmoresector'),
    ('sector','sector'),
    ('shrkn-rbb','shrkn-rbb'),
    ('test1','test1'),
    ('timol-left','timol-left'),
    ('timol-right','timol-right'),
    ('wcbs-sct1','wcbs-sct1'),
    ('wcbs-sct2','wcbs-sct2'),
    ('wcbs-sct2.1','wcbs-sct2.1')
)


class CustomerForm(forms.Form):
    customer_name = forms.CharField(max_length=100, required=False)
    has_phone = forms.ChoiceField(choices=HASPHONE_CHOICES, required = False)
    show_online = forms.ChoiceField(choices=ONLINE_CHOICES, required = False)
    billing_active = forms.ChoiceField(choices=BILLING_CHOICES, required = False)
    customer_id = forms.CharField(max_length=5, required=False)
    sector_id = forms.ChoiceField(choices=SECTOR_ID_CHOICES, required = False)
    will_come_back = forms.BooleanField(required=False)
    no_gps = forms.BooleanField(required=False)
    phone_active = forms.ChoiceField(choices=PHONE_CHOICES, required = False)
    phone_out = forms.ChoiceField(choices=PHONE_CHOICES, required = False)
    phone_out_range = forms.ChoiceField(choices=PHONE_RANGE_CHOICES, required = False)
    
