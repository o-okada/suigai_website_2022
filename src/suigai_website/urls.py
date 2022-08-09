from django.contrib import admin
from django.urls import include, path
from P0100File import views

urlpatterns = [
    ### Common Applications
    path('', include('P0000Dummy.urls')),
    ### path('', include('P0100File.urls')),
    path('P0100Login/', include('P0100Login.urls')),

    ### File Applications
    path('P0100File/', include('P0100File.urls')),

    ### Excel Applications
    path('P0200ExcelDownload/', include('P0200ExcelDownload.urls')),
    path('P0300ExcelUpload/', include('P0300ExcelUpload.urls')),
    path('P0300AreaUpload/', include('P0300AreaUpload.urls')),
    path('P0300AreaWeather/', include('P0300AreaWeather.urls')),
    ### path('P0300AreaEdit/', include('P0300AreaEdit.urls')),

    ### Online Applications
    path('P0400OnlineDisplay/', include('P0400OnlineDisplay.urls')),
    ### path('P0500OnlineUpdate/', include('P0500OnlineUpdate.urls')),

    ### Reverse Applications
    path('P0800Reverse/', include('P0800Reverse.urls')),
    
    ### Action Applications
    path('P0900Action/', include('P0900Action.urls')),
    
    ### See Python Django開発入門, P227
    path('admin/', admin.site.urls),

]
