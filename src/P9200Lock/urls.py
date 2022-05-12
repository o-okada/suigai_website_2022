from django.urls import path
from . import views

app_name = 'P9200Lock'
urlpatterns = [
    ### path('', views.index, name='index'),
    path('', views.index_view, name='index_view'),
]
