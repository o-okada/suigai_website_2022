from django.urls import path
from . import views

app_name = 'P0900Action'
urlpatterns = [
    path('', views.index_view, name='index_view'), ### 自動実行進捗状況一覧表示画面
    path('suigai/<slug:suigai_id>/', views.suigai_view, name='suigai_view'), ### 自動実行進捗状況一覧表示画面
    path('trigger/<slug:trigger_id>/', views.trigger_view, name='trigger_view'), ### 自動実行進捗状況詳細表示画面
    path('download_file/<slug:repository_id>/', views.download_file_view, name='download_file_view'), ### ファイルダウンロード

    ### path('graph/', views.graph_view, name='graph_view'), ### 自動実行進捗状況グラフ表示画面
    ### path('ken/<slug:ken_code>/city/<slug:city_code>/repository/<slug:repository_id>/', views.ken_city_repository_view, name='ken_city_repository_view'), ### 自動実行進捗状況グラフ表示画面
]
