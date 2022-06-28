from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    ### Common Applications
    path('', include('P0000Dummy.urls')),
    path('P0100Login/', include('P0100Login.urls')),

    ### Excel Applications
    path('P0200ExcelDownload/', include('P0200ExcelDownload.urls')),
    path('P0300ExcelUpload/', include('P0300ExcelUpload.urls')),

    ### Online Applications
    path('P0400OnlineDisplay/', include('P0400OnlineDisplay.urls')),
    path('P0500OnlineUpdate/', include('P0500OnlineUpdate.urls')),

    ### Area Applications
    path('P0600CreateArea/', include('P0600CreateArea.urls')),

    ### Report Applications
    ### path('P0700Report/', include('P0700Report.urls')),

    ### Reverse Verification Applications
    path('P0800Reverse/', include('P0800Reverse.urls')),
    
    ### Action Applications
    path('P0900Action/', include('P0900Action.urls')),

    ### File Applications
    path('P1000File/', include('P1000File.urls')),

    ### Admin Applications
    ### path('P9100Transact/', include('P9100Transact.urls')),
    ### path('P9200Lock/', include('P9200Lock.urls')),
    
    ### See Python Django開発入門, P227
    path('admin/', admin.site.urls),

]
