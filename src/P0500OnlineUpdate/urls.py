from django.urls import path
from . import views

app_name = 'P0500OnlineUpdate'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:ken_code>/ken/', views.ken, name='ken'),
    path('<slug:ken_code>/<slug:city_code>/city/', views.city, name='city'),
    path('<slug:ken_code>/<slug:city_code>/<slug:category_code>/category/', views.category, name='category'),
]
