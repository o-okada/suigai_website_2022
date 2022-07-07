from django.urls import path
from . import views

app_name = 'P0800Reverse'
urlpatterns = [
    path('input/', views.input_view, name='input_view'), 
    ### path('input/category/<slug:category_code>/', views.input_category_view, name='input_category_view'), 
    path('input/ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.input_ken_city_category_view, name='input_ken_city_category_view'), 
    
    path('summary/', views.summary_view, name='summary_view'), 
    ### path('summary/category/<slug:category_code>/', views.summary_category_view, name='summary_category_view'), 
    path('summary/ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.summary_ken_city_category_view, name='summary_ken_city_category_view'), 
]
