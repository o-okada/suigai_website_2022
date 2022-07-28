#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0300AreaWeather/views.py
### 水害区域図、異常気象
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import sys
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db import transaction
from django.db.models import Max
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic.base import TemplateView

import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

from P0000Common.models import BUILDING                ### 1000: 建物区分
from P0000Common.models import KEN                     ### 1010: 都道府県
from P0000Common.models import CITY                    ### 1020: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 1030: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 1040: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 1050: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 1060: 河川（河川・海岸）
from P0000Common.models import KASEN_TYPE              ### 1070: 河川種別（河川・海岸種別）
from P0000Common.models import CAUSE                   ### 1080: 水害原因
from P0000Common.models import UNDERGROUND             ### 1090: 地上地下区分
from P0000Common.models import USAGE                   ### 1100: 地下空間の利用形態
from P0000Common.models import FLOOD_SEDIMENT          ### 1110: 浸水土砂区分
from P0000Common.models import GRADIENT                ### 1120: 地盤勾配区分
from P0000Common.models import INDUSTRY                ### 1130: 産業分類

from P0000Common.models import HOUSE_ASSET             ### 2000: 家屋評価額
from P0000Common.models import HOUSE_RATE              ### 2010: 家屋被害率
from P0000Common.models import HOUSE_ALT               ### 2020: 家庭応急対策費_代替活動費
from P0000Common.models import HOUSE_CLEAN             ### 2030: 家庭応急対策費_清掃日数

from P0000Common.models import HOUSEHOLD_ASSET         ### 3000: 家庭用品自動車以外所有額
from P0000Common.models import HOUSEHOLD_RATE          ### 3010: 家庭用品自動車以外被害率

from P0000Common.models import CAR_ASSET               ### 4000: 家庭用品自動車所有額
from P0000Common.models import CAR_RATE                ### 4010: 家庭用品自動車被害率

from P0000Common.models import OFFICE_ASSET            ### 5000: 事業所資産額
from P0000Common.models import OFFICE_RATE             ### 5010: 事業所被害率
from P0000Common.models import OFFICE_SUSPEND          ### 5020: 事業所営業停止日数
from P0000Common.models import OFFICE_STAGNATE         ### 5030: 事業所営業停滞日数
from P0000Common.models import OFFICE_ALT              ### 5040: 事業所応急対策費_代替活動費

from P0000Common.models import FARMER_FISHER_ASSET     ### 6000: 農漁家資産額
from P0000Common.models import FARMER_FISHER_RATE      ### 6010: 農漁家被害率

from P0000Common.models import AREA                    ### 7000: 一般資産入力データ_水害区域
from P0000Common.models import WEATHER                 ### 7010: 一般資産入力データ_異常気象
from P0000Common.models import SUIGAI                  ### 7020: 一般資産入力データ_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7030: 一般資産入力データ_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7040: 一般資産ビューデータ_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 一般資産集計データ

from P0000Common.models import ACTION                  ### 10000: アクション
from P0000Common.models import STATUS                  ### 10010: 状態
from P0000Common.models import TRIGGER                 ### 10020: トリガーメッセージ
from P0000Common.models import APPROVAL                ### 10030: 承認メッセージ
from P0000Common.models import FEEDBACK                ### 10040: フィードバックメッセージ

from P0000Common.common import get_debug_log
from P0000Common.common import get_error_log
from P0000Common.common import get_info_log
from P0000Common.common import get_warn_log
from P0000Common.common import print_log
from P0000Common.common import reset_log

###############################################################################
### 関数名：index_view
### urlpattern：path('', views.index_view, name='index_view')
### template：P0300AreaWeather/index.html
### データベースに登録するボタンクリック時のPOSTに対応する処理
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0300AreaWeather.index_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request.ken_code_hidden = {}'.format(request.POST.get('ken_code_hidden')), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request.city_code_hidden = {}'.format(request.POST.get('city_code_hidden')), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request.suigai_id_hidden = {}'.format(request.POST.get('suigai_id_hidden')), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request.area_id_hidden = {}'.format(request.POST.get('area_id_hidden')), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 request.weather_id_hidden = {}'.format(request.POST.get('weather_id_hidden')), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 1/6.', 'DEBUG')

        #######################################################################
        ### 条件分岐処理(0010)
        ### (1)GETの場合、水害区域図、異常気象コード編集画面を表示して関数を抜ける。
        ### (2)POSTの場合、水害区域番号、異常気象コードをDBの水害テーブルに更新で登録する。
        ### ※関数の内部のネスト数を浅くするため。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 2/6.', 'DEBUG')
        if request.method == 'GET':
            ### ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
            template = loader.get_template('P0300AreaWeather/index.html')
            context = {
                ### 'ken_list': ken_list, 
            }
            print_log('[INFO] P0300AreaWeather.index_view()関数が正常終了しました。', 'INFO')
            return HttpResponse(template.render(context, request))
        
        elif request.method == 'POST':
            pass

        #######################################################################
        ### フォーム検証処理(0020)
        ### ※関数の内部のネスト数を浅くするため。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 3/6.', 'DEBUG')
        if request.POST.get('suigai_id_hidden') is None:
            print_log('[ERROR] P0300AreaWeather.index_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        if request.POST.get('suigai_id_hidden') is None:
            suigai_id = 0
        else:
            suigai_id = request.POST.get('suigai_id_hidden')

        if request.POST.get('ken_code_hidden') is None:
            ken_code = '0'
        else:
            ken_code = request.POST.get('ken_code_hidden')
            
        if request.POST.get('city_code_hidden') is None:
            city_code = '0'
        else:
            city_code = request.POST.get('city_code_hidden')
        
        if request.POST.get('area_id_hidden') is None:
            area_id = 0
        else:
            area_id = request.POST.get('area_id_hidden')
            
        if request.POST.get('weather_id_hidden') is None:
            weather_id = 0
        else:
            weather_id = request.POST.get('weather_id_hidden')
        
        #######################################################################
        ### DBアクセス処理(0030)
        ### DBにアクセスして、データを登録する。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 4/6.', 'DEBUG')
        connection_cursor = connection.cursor()
        try:
            connection_cursor.execute("""BEGIN""", [])
            
            if request.POST.get('area_id_hidden') is None and request.POST.get('weather_id_hidden') is None:
                print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 4_1/6.', 'DEBUG')
                connection_cursor.execute("""
                    UPDATE SUIGAI SET 
                        area_id=NULL, 
                        weather_id=NULL 
                    WHERE suigai_id=%s""", [suigai_id, ])
                
            elif request.POST.get('area_id_hidden') is None and request.POST.get('weather_id_hidden') is not None:
                print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 4_2/6.', 'DEBUG')
                connection_cursor.execute("""
                    UPDATE SUIGAI SET 
                        area_id=NULL, 
                        weather_id=%s 
                    WHERE suigai_id=%s""", [weather_id, suigai_id, ])
                
            elif request.POST.get('area_id_hidden') is not None and request.POST.get('weather_id_hidden') is None:
                print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 4_3/6.', 'DEBUG')
                connection_cursor.execute("""
                    UPDATE SUIGAI SET 
                        area_id=%s, 
                        weather_id=NULL 
                    WHERE suigai_id=%s""", [area_id, suigai_id, ])
                
            elif request.POST.get('area_id_hidden') is not None and request.POST.get('weather_id_hidden') is not None:
                print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 4_4/6.', 'DEBUG')
                connection_cursor.execute("""
                    UPDATE SUIGAI SET 
                        area_id=%s, 
                        weather_id=%s 
                    WHERE suigai_id=%s""", [area_id, weather_id, suigai_id, ])

            ### トリガーテーブルにWF10水害区域図貼付けトリガーを実行済、成功として登録する。
            connection_cursor.execute("""
                INSERT INTO TRIGGER (
                    trigger_id, suigai_id, action_code, status_code, success_count, failure_count, 
                    published_at, consumed_at, deleted_at, integrity_ok, integrity_ng, ken_code, 
                    city_code, download_file_path, download_file_name, upload_file_path, upload_file_name 
                ) VALUES (
                    (SELECT CASE WHEN (MAX(trigger_id+1)) IS NULL THEN CAST(0 AS INTEGER) ELSE CAST(MAX(trigger_id+1) AS INTEGER) END AS trigger_id FROM TRIGGER), -- trigger_id 
                    %s, -- suigai_id 
                    %s, -- action_code 
                    %s, -- status_code 
                    %s, -- success_count 
                    %s, -- failure_count 
                    CURRENT_TIMESTAMP, -- published_at 
                    CURRENT_TIMESTAMP, -- consumed_at 
                    %s, -- deleted_at 
                    %s, -- integrity_ok 
                    %s, -- integrity_ng 
                    %s, -- ken_code 
                    %s, -- city_code 
                    %s, -- download_file_path 
                    %s, -- download_file_name 
                    %s, -- upload_file_path 
                    %s  -- upload_file_name 
                )""", [
                    suigai_id, ### suigai_id 
                    'B02', ### action_code 
                    'SUCCESS', ### status_code 
                    1, ### success_count
                    0, ### failure_count
                    None, ### deleted_at 
                    '\n'.join(get_info_log()), ### integrity_ok 
                    '\n'.join(get_warn_log()), ### integrity_ng 
                    ken_code, ### ken_code 
                    ciy_code, ### city_code 
                    None, ### download_file_path 
                    None, ### download_file_name 
                    None, ### upload_file_path 
                    None, ### upload_file_name 
                ])
            ### トリガーテーブルにWF11集計処理トリガーを未実行＝次回実行対象として登録する。
            connection_cursor.execute("""
                INSERT INTO TRIGGER (
                    trigger_id, suigai_id, action_code, status_code, success_count, failure_count, 
                    published_at, consumed_at, deleted_at, integrity_ok, integrity_ng, ken_code, 
                    city_code, download_file_path, download_file_name, upload_file_path, upload_file_name 
                ) VALUES (
                    (SELECT CASE WHEN (MAX(trigger_id+1)) IS NULL THEN CAST(0 AS INTEGER) ELSE CAST(MAX(trigger_id+1) AS INTEGER) END AS trigger_id FROM TRIGGER), -- trigger_id 
                    %s, -- suigai_id 
                    %s, -- action_code 
                    %s, -- status_code 
                    %s, -- success_count 
                    %s, -- failure_count 
                    CURRENT_TIMESTAMP, -- published_at 
                    %s, -- consumed_at 
                    %s, -- deleted_at 
                    %s, -- integrity_ok 
                    %s, -- integrity_ng 
                    %s, -- ken_code 
                    %s, -- city_code 
                    %s, -- download_file_path 
                    %s, -- download_file_name 
                    %s, -- upload_file_path 
                    %s  -- upload_file_name 
                )""", [
                    suigai_id, ### suigai_id 
                    'B03', ### action_code 
                    None, ### status_code 
                    None, ### success_count
                    None, ### failure_count
                    None, ### consumed_at
                    None, ### deleted_at 
                    None, ### integrity_ok 
                    None, ### integrity_ng 
                    ken_code, ### ken_code 
                    city_code, ### city_code 
                    None, ### download_file_path 
                    None, ### download_file_name 
                    None, ### upload_file_path 
                    None, ### upload_file_name 
                ])
            ### transaction.commit()
            connection_cursor.execute("""COMMIT""", [])                    
        except:
            print_log('[ERROR] P0300AreaWeather.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            ### connection_cursor.rollback()
            connection_cursor.execute("""ROLLBACK""", [])
        finally:
            connection_cursor.close()

        #######################################################################
        ### DBアクセス処理(0040)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 5/6.', 'DEBUG')
        if suigai_id == "0":
            suigai_list = []
        else:
            suigai_list = SUIGAI.objects.raw("""
                SELECT 
                    CAST(SG1.suigai_id AS text) AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TO_CHAR(timezone('JST', SG1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                    TO_CHAR(timezone('JST', SG1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
                    SG1.cause_1_code AS cause_1_code, 
                    CA1.cause_name AS cause_1_name, 
                    SG1.cause_2_code AS cause_2_code, 
                    CA2.cause_name AS cause_2_name, 
                    SG1.cause_3_code AS cause_3_code, 
                    CA3.cause_name AS cause_3_name, 
                    SG1.area_id AS area_id, 
                    AR1.area_name AS area_name, 
                    SG1.suikei_code AS suikei_code, 
                    SK1.suikei_name AS suikei_name, 
                    SG1.kasen_code AS kasen_code, 
                    KA1.kasen_name AS kasen_name, 
                    SG1.gradient_code AS gradient_code, 
                    GR1.gradient_name AS gradient_name, 
                    SG1.residential_area AS residential_area, 
                    SG1.agricultural_area AS agricultural_area, 
                    SG1.underground_area AS underground_area, 
                    SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                    KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                    SG1.crop_damage AS crop_damage, 
                    SG1.weather_id AS weather_id, 
                    WE1.weather_name AS weather_name, 
                    TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    SG1.file_path AS file_path, 
                    SG1.file_name AS file_name, 
                    SG1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    SG1.status_code AS status_code, 
                    ST1.status_name AS status_name 
                FROM SUIGAI SG1 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN CAUSE CA1 ON SG1.cause_1_code=CA1.cause_code 
                LEFT JOIN CAUSE CA2 ON SG1.cause_2_code=CA2.cause_code 
                LEFT JOIN CAUSE CA3 ON SG1.cause_3_code=CA3.cause_code 
                LEFT JOIN AREA AR1 ON SG1.area_id=AR1.area_id 
                LEFT JOIN SUIKEI SK1 ON SG1.suikei_code=SK1.suikei_code 
                LEFT JOIN KASEN KA1 ON SG1.kasen_code=KA1.kasen_code 
                LEFT JOIN GRADIENT GR1 ON SG1.gradient_code=GR1.gradient_code 
                LEFT JOIN KASEN_KAIGAN KK1 ON SG1.kasen_kaigan_code=KK1.kasen_kaigan_code 
                LEFT JOIN WEATHER WE1 ON SG1.weather_id=WE1.weather_id 
                LEFT JOIN ACTION AC1 ON SG1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON SG1.status_code=ST1.status_code 
                WHERE SG1.suigai_id=%s AND SG1.deleted_at is NULL 
                ORDER BY CAST(SG1.suigai_id AS INTEGER) DESC""", [suigai_id, ])

        if ken_code == "0":
            area_list = []
        else:
            area_list = AREA.objects.raw("""
                SELECT 
                    AR1.area_id AS area_id, 
                    AR1.area_name AS area_name, 
                    AR1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    TO_CHAR(timezone('JST', AR1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', AR1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    AR1.file_path AS file_path, 
                    AR1.file_name AS file_name, 
                    AR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    AR1.status_code AS status_code, 
                    ST1.status_name AS status_name 
                FROM AREA AR1 
                LEFT JOIN KEN KE1 ON AR1.ken_code=KE1.ken_code 
                LEFT JOIN ACTION AC1 ON AR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON AR1.status_code=ST1.status_code 
                WHERE AR1.ken_code=%s 
                ORDER BY CAST(AR1.area_id AS INTEGER)""", [ken_code, ])

        if ken_code == "0":
            weahter_list = []
        else:
            weather_list = WEATHER.objects.raw("""
                SELECT 
                    WE1.weather_id AS weather_id, 
                    WE1.weather_name AS weather_name, 
                    WE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name 
                FROM WEATHER WE1 
                LEFT JOIN KEN KE1 ON WE1.ken_code=KE1.ken_code 
                WHERE WE1.ken_code=%s 
                ORDER BY CAST(WE1.weather_id AS INTEGER)""", [ken_code, ])
        
        #######################################################################
        ### レスポンスセット処理(0050)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.index_view()関数 STEP 6/6.', 'DEBUG')
        template = loader.get_template('P0300AreaWeather/index.html')
        context = {
            'type_code': 'ippan', 
            'ken_code': ken_code, 
            'suigai_id': suigai_id, 
            'suigai_list': suigai_list, 
            'area_list': area_list, 
            'weather_list': weather_list, 
        }
        print_log('[INFO] P0300AreaWeather.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    except:
        print_log('[ERROR] P0300AreaWeather.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0300AreaWeather.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0300AreaWeather.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：type_ken_suigai_view
### urlpattern：path('type/<slug:type_code>/ken/<slug:ken_code>/suigai/<slug:suigai_id>/', views.type_ken_suigai_view, name='type_ken_suigai_view')
### template：P0300AreaWeather/index.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def type_ken_suigai_view(request, type_code, ken_code, suigai_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        ### reset_log()
        print_log('[INFO] P0300AreaWeather.type_ken_suigai_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 suigai_id = {}'.format(suigai_id), 'DEBUG')
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 STEP 1/3.', 'DEBUG')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 STEP 2/3.', 'DEBUG')
        if suigai_id == "0":
            suigai_list = []
        else:
            suigai_list = SUIGAI.objects.raw("""
                SELECT 
                    CAST(SG1.suigai_id AS text) AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TO_CHAR(timezone('JST', SG1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                    TO_CHAR(timezone('JST', SG1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
                    SG1.cause_1_code AS cause_1_code, 
                    CA1.cause_name AS cause_1_name, 
                    SG1.cause_2_code AS cause_2_code, 
                    CA2.cause_name AS cause_2_name, 
                    SG1.cause_3_code AS cause_3_code, 
                    CA3.cause_name AS cause_3_name, 
                    SG1.area_id AS area_id, 
                    AR1.area_name AS area_name, 
                    SG1.suikei_code AS suikei_code, 
                    SK1.suikei_name AS suikei_name, 
                    SG1.kasen_code AS kasen_code, 
                    KA1.kasen_name AS kasen_name, 
                    SG1.gradient_code AS gradient_code, 
                    GR1.gradient_name AS gradient_name, 
                    SG1.residential_area AS residential_area, 
                    SG1.agricultural_area AS agricultural_area, 
                    SG1.underground_area AS underground_area, 
                    SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                    KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                    SG1.crop_damage AS crop_damage, 
                    SG1.weather_id AS weather_id, 
                    WE1.weather_name AS weather_name, 
                    TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    SG1.file_path AS file_path, 
                    SG1.file_name AS file_name, 
                    SG1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    SG1.status_code AS status_code, 
                    ST1.status_name AS status_name 
                FROM SUIGAI SG1 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN CAUSE CA1 ON SG1.cause_1_code=CA1.cause_code 
                LEFT JOIN CAUSE CA2 ON SG1.cause_2_code=CA2.cause_code 
                LEFT JOIN CAUSE CA3 ON SG1.cause_3_code=CA3.cause_code 
                LEFT JOIN AREA AR1 ON SG1.area_id=AR1.area_id 
                LEFT JOIN SUIKEI SK1 ON SG1.suikei_code=SK1.suikei_code 
                LEFT JOIN KASEN KA1 ON SG1.kasen_code=KA1.kasen_code 
                LEFT JOIN GRADIENT GR1 ON SG1.gradient_code=GR1.gradient_code 
                LEFT JOIN KASEN_KAIGAN KK1 ON SG1.kasen_kaigan_code=KK1.kasen_kaigan_code 
                LEFT JOIN WEATHER WE1 ON SG1.weather_id=WE1.weather_id 
                LEFT JOIN ACTION AC1 ON SG1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON SG1.status_code=ST1.status_code 
                WHERE SG1.suigai_id=%s AND SG1.deleted_at is NULL 
                ORDER BY CAST(SG1.suigai_id AS INTEGER) DESC""", [suigai_id, ])

        if ken_code == "0":
            area_list = []
        else:
            area_list = AREA.objects.raw("""
                SELECT 
                    AR1.area_id AS area_id, 
                    AR1.area_name AS area_name, 
                    AR1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    TO_CHAR(timezone('JST', AR1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', AR1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    AR1.file_path AS file_path, 
                    AR1.file_name AS file_name, 
                    AR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    AR1.status_code AS status_code, 
                    ST1.status_name AS status_name 
                FROM AREA AR1 
                LEFT JOIN KEN KE1 ON AR1.ken_code=KE1.ken_code 
                LEFT JOIN ACTION AC1 ON AR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON AR1.status_code=ST1.status_code 
                WHERE AR1.ken_code=%s 
                ORDER BY CAST(AR1.area_id AS INTEGER)""", [ken_code, ])

        if ken_code == "0":
            weahter_list = []
        else:
            weather_list = WEATHER.objects.raw("""
                SELECT 
                    WE1.weather_id AS weather_id, 
                    WE1.weather_name AS weather_name, 
                    WE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name 
                FROM WEATHER WE1 
                LEFT JOIN KEN KE1 ON WE1.ken_code=KE1.ken_code 
                WHERE WE1.ken_code=%s 
                ORDER BY CAST(WE1.weather_id AS INTEGER)""", [ken_code, ])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0300AreaWeather.type_ken_suigai_view()関数 STEP 3/3.', 'DEBUG')
        template = loader.get_template('P0300AreaWeather/index.html')
        context = {
            'type_code': type_code, 
            'ken_code': ken_code, 
            'suigai_id': suigai_id, 
            'suigai_list': suigai_list, 
            'area_list': area_list, 
            'weather_list': weather_list, 
        }
        print_log('[INFO] P0300AreaWeather.type_ken_suigai_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0300AreaWeather.type_ken_suigai_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0300AreaWeather.type_ken_suigai_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0300AreaWeather.type_ken_suigai_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
