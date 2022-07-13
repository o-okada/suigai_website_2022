from django.urls import path
from . import views

app_name = 'P0300AreaWeather'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    path('type/<slug:type_code>/ken/<slug:ken_code>/suigai/<slug:suigai_id>/', views.type_ken_suigai_view, name='type_ken_suigai_view'), 
]
