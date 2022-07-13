from django.urls import path
from . import views

app_name = 'P0400OnlineDisplay'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('category1/<slug:category_code1>/category2/<slug:category_code2>/ken/<slug:ken_code>/city/<slug:city_code>/', views.category1_category2_ken_city_view, name='category1_category2_ken_city_view'),
]
