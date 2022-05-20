from django.urls import path
from . import views

app_name = 'P0200ExcelDownload'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    
    path('building/', views.building_view, name='building_view'),
    path('ken/', views.ken_view, name='ken_view'),
    path('city/', views.city_view, name='city_view'),
    path('kasen_kaigan/', views.kasen_kaigan_view, name='kasen_kaigan_view'),
    path('suikei/', views.suikei_view, name='suikei_view'),
    path('suikei_type/', views.suikei_type_view, name='suikei_type_view'),
    path('kasen/', views.kasen_view, name='kasen_view'),
    path('kasen_type/', views.kasen_type_view, name='kasen_type_view'),
    path('cause/', views.cause_view, name='cause_view'),
    path('underground/', views.underground_view, name='underground_view'),
    path('usage/', views.usage_view, name='usage_view'),
    path('flood_sediment/', views.flood_sediment_view, name='flood_sediment_view'),
    path('gradient/', views.gradient_view, name='gradient_view'),
    path('industry/', views.industry_view, name='industry_view'),
    path('house_asset/', views.house_asset_view, name='house_asset_view'),
    path('house_damage/', views.house_damage_view, name='house_damage_view'),
    path('household_damage/', views.household_damage_view, name='household_damage_view'),
    path('car_damage/', views.car_damage_view, name='car_damage_view'),
    path('house_cost/', views.house_cost_view, name='house_cost_view'),
    path('office_asset/', views.office_asset_view, name='office_asset_view'),
    path('office_damage/', views.office_damage_view, name='office_damage_view'),
    path('office_cost/', views.office_cost_view, name='office_cost_view'),
    path('farmer_fisher_damage/', views.farmer_fisher_damage_view, name='farmer_fisher_damage_view'),
    path('suigai/', views.suigai_view, name='suigai_view'),
    path('weather/', views.weather_view, name='weather_view'),
    path('area/', views.area_view, name='area_view'),
    
    path('ippan_chosa/', views.ippan_chosa_view, name='ippan_chosa_view'),
    path('ippan_city/', views.ippan_city_view, name='ippan_city_view'),
    path('ippan_ken/', views.ippan_ken_view, name='ippan_ken_view'),
    
    path('restoration/', views.restoration_view, name='restoration_view'),
    path('kokyo/', views.kokyo_view, name='kokyo_view'),
    path('koeki/', views.koeki_view, name='koeki_view'),

]
