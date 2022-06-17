from django.urls import path
from . import views

app_name = 'P0800Reverse'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('category/<slug:category_code>/', views.category_view, name='category_view'),
]
