from django.urls import path
from . import views

app_name = 'P0300AreaWeatherUpdate'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    path('ken/<slug:ken_code>/city/<slug:city_code>/', views.ken_city_view, name='ken_city_view'), 
]
