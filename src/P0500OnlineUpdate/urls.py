from django.urls import path
from . import views

app_name = 'P0500OnlineUpdate'
urlpatterns = [
    path('', views.index, name='index'),
]
