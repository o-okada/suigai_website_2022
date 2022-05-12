from django.urls import path
from . import views

app_name = 'P0500OnlineUpdate'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('ken/<slug:ken_code>/', views.ken_view, name='ken_view'),
    path('ken/<slug:ken_code>/city/<slug:city_code>/', views.city_view, name='city_view'),
    path('ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.category_view, name='category_view'),
]
