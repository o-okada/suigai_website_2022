from django.urls import path
from . import views

app_name = 'P9300AdminLock'
urlpatterns = [
    path('', views.index, name='index'),
]
