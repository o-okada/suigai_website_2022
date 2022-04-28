from django.urls import path
from . import views

app_name = 'P9200AdminHistory'
urlpatterns = [
    path('', views.index, name='index'),
]
