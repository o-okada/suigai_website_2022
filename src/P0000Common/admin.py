from django.contrib import admin

### See django.pdf P442 Using a custom user model when starting a project
### from django.contrib.auth.admin import UserAdmin
### from .models import USER
### admin.site.register(USER, UserAdmin)

from .models import BUILDING                                                   ### 001: 
from .models import KEN                                                        ### 002: 
from .models import CITY                                                       ### 003: 
from .models import KASEN_KAIGAN                                               ### 004: 
from .models import SUIKEI                                                     ### 005:
from .models import SUIKEI_TYPE                                                ### 006: 
from .models import KASEN                                                      ### 007: 
from .models import KASEN_TYPE                                                 ### 008: 
from .models import CAUSE                                                      ### 009: 
from .models import UNDERGROUND                                                ### 010: 
from .models import USAGE                                                      ### 011: 
from .models import FLOOD_SEDIMENT                                             ### 012: 
from .models import GRADIENT                                                   ### 013: 
from .models import INDUSTRY                                                   ### 014: 
from .models import RESTORATION                                                ### 015: 

from .models import HOUSE_ASSET                                                ### 100: 
from .models import HOUSE_DAMAGE                                               ### 101: 
from .models import HOUSEHOLD_DAMAGE                                           ### 102: 
from .models import CAR_DAMAGE                                                 ### 103: 
from .models import HOUSE_COST                                                 ### 104: 
from .models import OFFICE_ASSET                                               ### 105: 
from .models import OFFICE_DAMAGE                                              ### 106: 
from .models import OFFICE_COST                                                ### 107: 
from .models import FARMER_FISHER_DAMAGE                                       ### 108: 

from .models import SUIGAI                                                     ### 200: 
from .models import WEATHER                                                    ### 201: 
from .models import AREA                                                       ### 202: 
from .models import IPPAN                                                      ### 203: 
from .models import KOKYO                                                      ### 204:
from .models import KOEKI                                                      ### 205: 

from .models import IPPAN_REPORT
from .models import KOKYO_REPORT
from .models import KOEKI_REPORT
from .models import APPROVE_HISTORY
from .models import REPORT_HISTORY
from .models import DISTRIBUTE_HISTORY
from .models import TRANSACT
from .models import IPPAN_KOKYO_KOEKI

admin.site.register(BUILDING)
admin.site.register(KEN)
admin.site.register(CITY)
admin.site.register(KASEN_KAIGAN)
admin.site.register(SUIKEI)
admin.site.register(SUIKEI_TYPE)
admin.site.register(KASEN)
admin.site.register(KASEN_TYPE)
admin.site.register(CAUSE)
admin.site.register(UNDERGROUND)
admin.site.register(USAGE)
admin.site.register(FLOOD_SEDIMENT)
admin.site.register(GRADIENT)
admin.site.register(INDUSTRY)
admin.site.register(RESTORATION)

admin.site.register(HOUSE_ASSET)
admin.site.register(HOUSE_DAMAGE)
admin.site.register(HOUSEHOLD_DAMAGE)
admin.site.register(CAR_DAMAGE)
admin.site.register(HOUSE_COST)
admin.site.register(OFFICE_ASSET)
admin.site.register(OFFICE_DAMAGE)
admin.site.register(OFFICE_COST)
admin.site.register(FARMER_FISHER_DAMAGE)

admin.site.register(SUIGAI)
admin.site.register(WEATHER)
admin.site.register(AREA)
admin.site.register(IPPAN)
admin.site.register(KOKYO)
admin.site.register(KOEKI)
admin.site.register(IPPAN_REPORT)
admin.site.register(KOKYO_REPORT)
admin.site.register(KOEKI_REPORT)
admin.site.register(APPROVE_HISTORY)
admin.site.register(REPORT_HISTORY)
admin.site.register(DISTRIBUTE_HISTORY)
admin.site.register(TRANSACT)
admin.site.register(IPPAN_KOKYO_KOEKI)