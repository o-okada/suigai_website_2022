from django.urls import path
from . import views

app_name = 'P0000Dummy'
urlpatterns = [
    path('', views.index_view, name='index_view'),
]
