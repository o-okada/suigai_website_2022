from django.urls import path
from . import views

app_name = 'P0200ExcelDownload'
urlpatterns = [
    ### path('', views.IndexView.as_view(), name="index"),
    ### path('diary-update/<int:pk>/', views.DiaryUpdateView.as_view(), name="diary_update"),
    ### path('<int:question_id>/', views.detail, name='detail'),
    ### path('<int:question_id>/results/', views.results, name='results'),
    ### path('<int:question_id>/vote/', views.vote, name='vote'),
    ### path('download_file/', views.download_file, name='download_file'),
    ### path('download_p0200prefecture/', views.download_p0200prefecture, name='download_p0200prefecture'),
    ### path('download_p0200city/', views.download_p0200city, name='download_p0200city'),

    path('', views.index, name='index'),
    
    path('download_building/', views.download_building, name='download_building'),
    path('download_ken/', views.download_ken, name='download_ken'),
    path('download_city/', views.download_city, name='download_city'),
    path('download_kasen_kaigan/', views.download_kasen_kaigan, name='download_kasen_kaigan'),
    path('download_suikei/', views.download_suikei, name='download_suikei'),
    path('download_suikei_type/', views.download_suikei_type, name='download_suikei_type'),
    path('download_kasen/', views.download_kasen, name='download_kasen'),
    path('download_kasen_type/', views.download_kasen_type, name='download_kasen_type'),
    path('download_cause/', views.download_cause, name='download_cause'),
    path('download_underground/', views.download_underground, name='download_underground'),
    path('download_usage/', views.download_usage, name='download_usage'),
    path('download_flood_sediment/', views.download_flood_sediment, name='download_flood_sediment'),
    path('download_gradient/', views.download_gradient, name='download_gradient'),
    path('download_industry/', views.download_industry, name='download_industry'),
    path('download_house_asset/', views.download_house_asset, name='download_house_asset'),
    path('download_house_damage/', views.download_house_damage, name='download_house_damage'),
    path('download_household_damage/', views.download_household_damage, name='download_household_damage'),
    path('download_car_damage/', views.download_car_damage, name='download_car_damage'),
    path('download_house_cost/', views.download_house_cost, name='download_house_cost'),
    path('download_office_asset/', views.download_office_asset, name='download_office_asset'),
    path('download_office_damage/', views.download_office_damage, name='download_office_damage'),
    path('download_office_cost/', views.download_office_cost, name='download_office_cost'),
    path('download_farmer_fisher_damage/', views.download_farmer_fisher_damage, name='download_farmer_fisher_damage'),
    path('download_weather/', views.download_weather, name='download_weather'),
    path('download_area/', views.download_area, name='download_area'),
    
    path('download_ippan_chosa/', views.download_ippan_chosa, name='download_ippan_chosa'),
    path('download_ippan_city/', views.download_ippan_city, name='download_ippan_city'),
    path('download_ippan_ken/', views.download_ippan_ken, name='download_ippan_ken'),
    
    path('download_restoration/', views.download_restoration, name='download_restoration'),
    path('download_kokyo/', views.download_kokyo, name='download_kokyo'),
    path('download_koeki/', views.download_koeki, name='download_koeki'),

]
