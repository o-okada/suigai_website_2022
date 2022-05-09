from django.urls import path
from . import views

app_name = 'P9100AdminCheck'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:ken_code>/ken/', views.ken, name='ken'),
    path('<slug:ken_code>/<slug:city_code>/city/', views.city, name='city'),
]
