from django.urls import path
from . import views

app_name = 'P9100AdminCheck'
urlpatterns = [
    path('', views.index, name='index'),
]
