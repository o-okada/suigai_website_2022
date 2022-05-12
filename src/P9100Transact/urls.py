from django.urls import path
from . import views

app_name = 'P9100Transact'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('ken/<slug:ken_code>/', views.ken_view, name='ken_view'),
    path('ken/<slug:ken_code>/city/<slug:city_code>/', views.city_view, name='city_view'),
]
