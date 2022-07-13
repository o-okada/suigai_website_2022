from django.urls import path
from . import views

app_name = 'P0100File'
urlpatterns = [
    path('type/<slug:type_code>/', views.type_view, name='type_view'), 
    path('type/<slug:type_code>/ken/<slug:ken_code>/', views.type_ken_view, name='type_ken_view'), 
]
