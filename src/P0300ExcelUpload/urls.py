from django.urls import path
from . import views

app_name = 'P0300ExcelUpload'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('ippan_chosa_result/<int:excel_id>/', views.ippan_chosa_result_view, name='ippan_chosa_result_view'),
]
