from django.contrib import admin
from django.urls import include, path
import file_upload.views as file_upload ### 2022/04/22 Add

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
    path('P0600AreaCreate/', include('P0600AreaCreate.urls')),
    ### Admin Applications
    path('P9100AdminCheck/', include('P9100AdminCheck.urls')),
    path('P9200AdminHistory/', include('P9200AdminHistory.urls')),
    path('P9300AdminLock/', include('P9300AdminLock.urls')),
    
    path('admin/', admin.site.urls),
    path('success/url/', file_upload.success), ### 2022/04/22 Add
    path('file_upload/', include('file_upload.urls')), ### 2022/04/22 Add
]
