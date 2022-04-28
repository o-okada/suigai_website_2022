from django.urls import path
from . import views

app_name = 'P0400OnlineDisplay'
urlpatterns = [
    path('', views.index, name='index'),
]
