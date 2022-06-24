from django.urls import path
from . import views

app_name = 'P0900CI'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    path('ken/<slug:ken_code>/city/<slug:city_code>/status/<slug:status_code>/', views.ken_city_status_view, name='ken_city_status_view'), 
    ### path('repository/<slug:repository_id>/', views.repository_view, name='repository_view'), 
    path('trigger/<slug:trigger_id>/', views.trigger_view, name='trigger_view'), 
    path('download_file/<slug:repository_id>/', views.download_file_view, name='download_file_view'),
]
