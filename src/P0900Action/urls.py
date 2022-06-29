from django.urls import path
from . import views

app_name = 'P0900Action'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    path('ken/<slug:ken_code>/city/<slug:city_code>/repository/<slug:repository_id>/', views.ken_city_repository_view, name='ken_city_repository_view'), 
    path('trigger/<slug:trigger_id>/', views.trigger_view, name='trigger_view'), 
    path('download_file/<slug:repository_id>/', views.download_file_view, name='download_file_view'),
]
