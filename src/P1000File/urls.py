from django.urls import path
from . import views

app_name = 'P1000File'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/status/<slug:status_code>/', views.ken_city_status_view, name='ken_city_status_view'), 
    path('R4/', views.R4_view, name='R4_view'), 
    path('R4/ken/<slug:ken_code>/', views.R4_ken_view, name='R4_ken_view'), 
]
