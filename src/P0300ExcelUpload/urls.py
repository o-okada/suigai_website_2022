from django.urls import path
from . import views

app_name = 'P0300ExcelUpload'
urlpatterns = [
    path('', views.index, name='index'),
    path('download_ippan_chosa_result/<int:excel_id>/', views.download_ippan_chosa_result, name='download_ippan_chosa_result'),    
]
