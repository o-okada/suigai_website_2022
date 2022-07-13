from django.contrib import admin

### See django.pdf P442 Using a custom user model when starting a project
### from django.contrib.auth.admin import UserAdmin
### from .models import USER
### admin.site.register(USER, UserAdmin)

from .models import BUILDING

admin.site.register(BUILDING)
