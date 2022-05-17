from django.urls import path
from . import views

app_name = 'P0400OnlineDisplay'
urlpatterns = [
    ### path('', views.index_view, name='index_view'),
    ### path('ken/<slug:ken_code>/', views.ken_view, name='ken_view'),
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/', views.city_view, name='city_view'),
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.category_view, name='category_view'),
    path('', views.index_view, name='index_view'),
    path('category1/<slug:category_code1>/', views.category_view1, name='category_view1'),
    path('category1/<slug:category_code1>/ken/<slug:ken_code>/', views.ken_view, name='ken_view'),
    path('category1/<slug:category_code1>/ken/<slug:ken_code>/city/<slug:city_code>/', views.city_view, name='city_view'),
    path('category1/<slug:category_code1>/ken/<slug:ken_code>/city/<slug:city_code>/category2/<slug:category_code2>/', views.category_view2, name='category_view2'),

]
