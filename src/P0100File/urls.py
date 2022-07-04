from django.urls import path
from . import views

app_name = 'P0100File'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
    path('R4/', views.R4_view, name='R4_view'), 
    path('R4/ken/<slug:ken_code>/', views.R4_ken_view, name='R4_ken_view'), 
]
