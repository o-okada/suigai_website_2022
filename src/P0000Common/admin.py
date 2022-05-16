from django.contrib import admin

### See django.pdf P442 Using a custom user model when starting a project
### from django.contrib.auth.admin import UserAdmin
### from .models import USER
### admin.site.register(USER, UserAdmin)

from .models import BUILDING
from .models import KEN
from .models import CITY
from .models import KASEN_KAIGAN
from .models import SUIKEI
from .models import SUIKEI_TYPE
from .models import KASEN
from .models import KASEN_TYPE
from .models import CAUSE
from .models import UNDERGROUND
from .models import USAGE
from .models import FLOOD_SEDIMENT
from .models import GRADIENT
from .models import INDUSTRY
from .models import HOUSE_ASSET
from .models import HOUSE_DAMAGE
from .models import HOUSEHOLD_DAMAGE
from .models import CAR_DAMAGE
from .models import HOUSE_COST
from .models import OFFICE_ASSET
from .models import OFFICE_DAMAGE
from .models import OFFICE_COST
from .models import FARMER_FISHER_DAMAGE
from .models import WEATHER
from .models import AREA
from .models import IPPAN
from .models import RESTORATION
from .models import KOKYO
from .models import KOEKI
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
admin.site.register(HOUSE_ASSET)
admin.site.register(HOUSE_DAMAGE)
admin.site.register(HOUSEHOLD_DAMAGE)
admin.site.register(CAR_DAMAGE)
admin.site.register(HOUSE_COST)
admin.site.register(OFFICE_ASSET)
admin.site.register(OFFICE_DAMAGE)
admin.site.register(OFFICE_COST)
admin.site.register(FARMER_FISHER_DAMAGE)
admin.site.register(WEATHER)
admin.site.register(AREA)
admin.site.register(IPPAN)
admin.site.register(RESTORATION)
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