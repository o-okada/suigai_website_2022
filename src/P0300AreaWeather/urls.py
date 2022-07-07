from django.urls import path
from . import views

app_name = 'P0300AreaWeather'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/', views.ken_city_view, name='ken_city_view'), 
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/suigai/<slug:suigai_id>/', views.ken_city_suigai_view, name='ken_city_suigai_view'), 
    path('type/<slug:type_code>/ken/<slug:ken_code>/city/<slug:city_code>/suigai/<slug:suigai_id>/', views.type_ken_city_suigai_view, name='type_ken_city_suigai_view'), 
]
