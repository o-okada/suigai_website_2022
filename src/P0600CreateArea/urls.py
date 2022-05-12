from django.urls import path
from . import views

app_name = 'P0600CreateArea'
urlpatterns = [
    path('', views.index, name='index'),
]
