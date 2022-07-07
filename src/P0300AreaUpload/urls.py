from django.urls import path
from . import views

app_name = 'P0300AreaUpload'
urlpatterns = [
    path('', views.index_view, name='index_view'), 
]
