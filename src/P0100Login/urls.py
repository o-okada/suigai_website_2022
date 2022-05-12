from django.urls import path
from . import views

app_name = 'P0100Login'
urlpatterns = [
    path('', views.index_view, name='index_view'),
]
