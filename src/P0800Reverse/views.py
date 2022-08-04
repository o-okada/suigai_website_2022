#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0800Reverse/views.py
### データ整合性検証
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import sys
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic import FormView
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

from P0000Common.models import AREA                    ### 7000: 入力データ_水害区域
from P0000Common.models import WEATHER                 ### 7010: 入力データ_異常気象
from P0000Common.models import SUIGAI                  ### 7020: 入力データ_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7030: 入力データ_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7040: ビューデータ_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 集計データ

from P0000Common.common import get_debug_log
from P0000Common.common import get_error_log
from P0000Common.common import get_info_log
from P0000Common.common import get_warn_log
from P0000Common.common import print_log
from P0000Common.common import reset_log

###############################################################################
### 関数名：input_view
### urlpattern：path('input/', views.input_view, name='input_view')
### template：P0800Reverse/input.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def input_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0800Reverse.input_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0800Reverse.input_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.input_view()関数 STEP 1/2.', 'DEBUG')

        #######################################################################
        ### レスポンスセット処理(0010)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.input_view()関数 STEP 2/2.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        template = loader.get_template('P0800Reverse/input.html')
        context = {
            'ken_list': ken_list, 
        }
        print_log('[INFO] P0800Reverse.input_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0800Reverse.input_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0800Reverse.input_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Reverse.input_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：summary_view
### urlpattern：path('summary/', views.summary_view, name='summary_view')
### template：P0800Reverse/summary.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def summary_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0800Reverse.summary_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0800Reverse.summary_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.summary_view()関数 STEP 1/2.', 'DEBUG')

        #######################################################################
        ### レスポンスセット処理(0010)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.summary_view()関数 STEP 2/2.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        template = loader.get_template('P0800Reverse/summary.html')
        context = {
            'ken_list': ken_list, 
        }
        print_log('[INFO] P0800Reverse.summary_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0800Reverse.summary_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0800Reverse.summary_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Reverse.summary_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：input_ken_city_category_view
### urlpattern：path('input/ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.input_ken_city_category_view, name='input_ken_city_category_view')
### template：P0800Reverse/input.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def input_ken_city_category_view(request, ken_code, city_code, category_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0800Reverse.input_ken_city_category_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 city_code = {}'.format(city_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 category_code = {}'.format(category_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 STEP 1/5.', 'DEBUG')

        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、下記の計算式に用いるデータを取得する。
        ### (1)家屋被害額 = 延床面積 x 家屋評価額 x 浸水または土砂ごとの勾配差による被害率
        ### (2)家庭用品自動車以外被害額 = 世帯数 x 浸水または土砂ごとの家庭用品被害率 x 家庭用品自動車以外所有額
        ### (3)家庭用品自動車被害額 = 世帯数 x 自動車被害率 x 家庭用品自動車所有額
        ### (4)家庭応急対策費 = (世帯数 x 活動費) + (世帯数 x 清掃日数 x 清掃労働単価)
        ### (5)事業所被害額 = 従業者数 x 産業分類ごとの償却資産 x 浸水または土砂ごとの被害率 + 
        ### 　　　　　　　　　従業者数 x 産業分類ごとの在庫資産 x 浸水または土砂ごとの被害率
        ### (6)事業所営業損失額 = 従業者数 x (営業停止日数 + 停滞日数/2) x 付加価値額
        ### (7)農漁家被害額 = 農漁家戸数 x 農漁家の償却資産 x 浸水または土砂ごとの被害率 + 
        ###                   農漁家戸数 x 農漁家の在庫資産 x 浸水または土砂ごとの被害率
        ### (8)事業所応急対策費 = 事業所数 x 代替活動費
        #######################################################################
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 STEP 2/5.', 'DEBUG')

        #######################################################################
        ### DBアクセス処理(0020)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 STEP 3/5.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        if ken_code == '0':
            city_list = []
        else:
            city_list = CITY.objects.raw("""
                SELECT * FROM CITY WHERE ken_code=%s ORDER BY CAST(city_code AS INTEGER)""", [ken_code, ])
 
        ####################################################################### 
        ### DBアクセス処理(0030)
        ### DBにアクセスして、データを取得する。
        ### 延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
        ####################################################################### 
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 STEP 4/5.', 'DEBUG')
        ippan_reverse_list = None
        if ken_code == "0" and city_code == "0":
            pass
        elif ken_code == "0" and city_code != "0":
            pass
        elif ken_code != "0" and city_code == "0":
            pass
        elif ken_code != "0" and city_code != "0":
            ippan_reverse_list = IPPAN_VIEW.objects.raw("""
                SELECT 
                    IV1.ippan_id AS ippan_id, 
                    IV1.ippan_name AS ippan_name, 
                    IV1.suigai_id AS suigai_id, 
                    IV1.suigai_name AS suigai_name, 
                    IV1.ken_code AS ken_code, 
                    IV1.ken_name AS ken_name, 
                    IV1.city_code AS city_code, 
                    IV1.city_name AS city_name, 
                    TO_CHAR(timezone('JST', IV1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                    TO_CHAR(timezone('JST', IV1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
                    IV1.cause_1_code AS cause_1_code, 
                    IV1.cause_1_name AS cause_1_name, 
                    IV1.cause_2_code AS cause_2_code, 
                    IV1.cause_2_name AS cause_2_name, 
                    IV1.cause_3_code AS cause_3_code, 
                    IV1.cause_3_name AS cause_3_name, 
                    IV1.area_id AS area_id, 
                    IV1.area_name AS area_name, 
                    
                    IV1.suikei_code AS suikei_code, 
                    IV1.suikei_name AS suikei_name, 
                    IV1.kasen_code AS kasen_code, 
                    IV1.kasen_name AS kasen_name, 
                    IV1.gradient_code AS gradient_code, 
                    IV1.gradient_name AS gradient_name, 
    
                    CASE WHEN (IV1.residential_area) IS NULL THEN 0.0 ELSE CAST(IV1.residential_area AS NUMERIC(20,10)) END AS residential_area, 
                    CASE WHEN (IV1.agricultural_area) IS NULL THEN 0.0 ELSE CAST(IV1.agricultural_area AS NUMERIC(20,10)) END AS agricultural_area, 
                    CASE WHEN (IV1.underground_area) IS NULL THEN 0.0 ELSE CAST(IV1.underground_area AS NUMERIC(20,10)) END AS underground_area, 
                    IV1.kasen_kaigan_code AS kasen_kaigan_code, 
                    IV1.kasen_kaigan_name AS kasen_kaigan_name, 
                    CASE WHEN (IV1.crop_damage) IS NULL THEN 0.0 ELSE CAST(IV1.crop_damage AS NUMERIC(20,10)) END AS crop_damage, 
                    IV1.weather_id AS weather_id, 
                    IV1.weather_name AS weather_name, 
                    IV1.upload_file_path AS upload_file_path, 
                    IV1.upload_file_name AS upload_file_name, 
                    IV1.summary_file_path AS summary_file_path, 
                    IV1.summary_file_name AS summary_file_name, 
                    
                    IV1.building_code AS building_code, 
                    IV1.building_name AS building_name, 
                    IV1.underground_code AS underground_code, 
                    IV1.underground_name AS underground_name, 
                    IV1.flood_sediment_code AS flood_sediment_code, 
                    IV1.flood_sediment_name AS flood_sediment_name, 
                    
                    CASE WHEN (IV1.building_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv00 AS NUMERIC(20,10)) END AS building_lv00, 
                    CASE WHEN (IV1.building_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv01_49 AS NUMERIC(20,10)) END AS building_lv01_49, 
                    CASE WHEN (IV1.building_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv50_99 AS NUMERIC(20,10)) END AS building_lv50_99, 
                    CASE WHEN (IV1.building_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv100 AS NUMERIC(20,10)) END AS building_lv100, 
                    CASE WHEN (IV1.building_half) IS NULL THEN 0.0 ELSE CAST(IV1.building_half AS NUMERIC(20,10)) END AS building_half, 
                    CASE WHEN (IV1.building_full) IS NULL THEN 0.0 ELSE CAST(IV1.building_full AS NUMERIC(20,10)) END AS building_full, 
                    CASE WHEN (IV1.building_total) IS NULL THEN 0.0 ELSE CAST(IV1.building_total AS NUMERIC(20,10)) END AS building_total, 
     
                    CASE WHEN (IV1.floor_area) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area AS NUMERIC(20,10)) END AS floor_area, 
                    CASE WHEN (IV1.family) IS NULL THEN 0.0 ELSE CAST(IV1.family AS NUMERIC(20,10)) END AS family, 
                    CASE WHEN (IV1.office) IS NULL THEN 0.0 ELSE CAST(IV1.office AS NUMERIC(20,10)) END AS office, 
    
                    CASE WHEN (IV1.floor_area_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv00 AS NUMERIC(20,10)) END AS floor_area_lv00, 
                    CASE WHEN (IV1.floor_area_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv01_49 AS NUMERIC(20,10)) END AS floor_area_lv01_49, 
                    CASE WHEN (IV1.floor_area_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv50_99 AS NUMERIC(20,10)) END AS floor_area_lv50_99, 
                    CASE WHEN (IV1.floor_area_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv100 AS NUMERIC(20,10)) END AS floor_area_lv100, 
                    CASE WHEN (IV1.floor_area_half) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_half AS NUMERIC(20,10)) END AS floor_area_half, 
                    CASE WHEN (IV1.floor_area_full) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_full AS NUMERIC(20,10)) END AS floor_area_full, 
                    CASE WHEN (IV1.floor_area_total) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_total AS NUMERIC(20,10)) END AS floor_area_total, 
                    
                    CASE WHEN (IV1.family_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv00 AS NUMERIC(20,10)) END AS family_lv00, 
                    CASE WHEN (IV1.family_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv01_49 AS NUMERIC(20,10)) END AS family_lv01_49, 
                    CASE WHEN (IV1.family_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv50_99 AS NUMERIC(20,10)) END AS family_lv50_99, 
                    CASE WHEN (IV1.family_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv100 AS NUMERIC(20,10)) END AS family_lv100, 
                    CASE WHEN (IV1.family_half) IS NULL THEN 0.0 ELSE CAST(IV1.family_half AS NUMERIC(20,10)) END AS family_half, 
                    CASE WHEN (IV1.family_full) IS NULL THEN 0.0 ELSE CAST(IV1.family_full AS NUMERIC(20,10)) END AS family_full, 
                    CASE WHEN (IV1.family_total) IS NULL THEN 0.0 ELSE CAST(IV1.family_total AS NUMERIC(20,10)) END AS family_total, 
                   
                    CASE WHEN (IV1.office_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv00 AS NUMERIC(20,10)) END AS office_lv00, 
                    CASE WHEN (IV1.office_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv01_49 AS NUMERIC(20,10)) END AS office_lv01_49, 
                    CASE WHEN (IV1.office_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv50_99 AS NUMERIC(20,10)) END AS office_lv50_99, 
                    CASE WHEN (IV1.office_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv100 AS NUMERIC(20,10)) END AS office_lv100, 
                    CASE WHEN (IV1.office_half) IS NULL THEN 0.0 ELSE CAST(IV1.office_half AS NUMERIC(20,10)) END AS office_half, 
                    CASE WHEN (IV1.office_full) IS NULL THEN 0.0 ELSE CAST(IV1.office_full AS NUMERIC(20,10)) END AS office_full, 
                    CASE WHEN (IV1.office_total) IS NULL THEN 0.0 ELSE CAST(IV1.office_total AS NUMERIC(20,10)) END AS office_total, 
    
                    CASE WHEN (IV1.farmer_fisher_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_lv00, 
                    CASE WHEN (IV1.farmer_fisher_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49, 
                    CASE WHEN (IV1.farmer_fisher_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99, 
                    CASE WHEN (IV1.farmer_fisher_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_lv100, 
                    -- CASE WHEN (IV1.farmer_fisher_half) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_half AS NUMERIC(20,10)) END AS farmer_fisher_half, 
                    CASE WHEN (IV1.farmer_fisher_full) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_full AS NUMERIC(20,10)) END AS farmer_fisher_full, 
                    CASE WHEN (IV1.farmer_fisher_total) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_total AS NUMERIC(20,10)) END AS farmer_fisher_total, 
    
                    CASE WHEN (IV1.employee_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv00 AS NUMERIC(20,10)) END AS employee_lv00, 
                    CASE WHEN (IV1.employee_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv01_49 AS NUMERIC(20,10)) END AS employee_lv01_49, 
                    CASE WHEN (IV1.employee_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv50_99 AS NUMERIC(20,10)) END AS employee_lv50_99, 
                    CASE WHEN (IV1.employee_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv100 AS NUMERIC(20,10)) END AS employee_lv100, 
                    -- CASE WHEN (IV1.employee_half) IS NULL THEN 0.0 ELSE CAST(IV1.employee_half AS NUMERIC(20,10)) END AS employee_half, 
                    CASE WHEN (IV1.employee_full) IS NULL THEN 0.0 ELSE CAST(IV1.employee_full AS NUMERIC(20,10)) END AS employee_full,
                    CASE WHEN (IV1.employee_total) IS NULL THEN 0.0 ELSE CAST(IV1.employee_total AS NUMERIC(20,10)) END AS employee_total, 
    
                    IV1.industry_code AS industry_code, 
                    IV1.industry_name AS industry_name, 
                    IV1.usage_code AS usage_code,
                    IV1.usage_name AS usage_name, 

                    TO_CHAR(timezone('JST', IV1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', IV1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
    
                    -- 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_lv00 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv00_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_lv01_49 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_lv50_99 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_lv100 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv100_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_half / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_half_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.floor_area_full / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_full_reverse_floor_area, 
    
                    -- 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_lv00 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv00_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_lv01_49 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_lv50_99 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_lv100 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv100_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_half / IV1.family_total AS NUMERIC(20,10)) END AS building_half_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.family_full / IV1.family_total AS NUMERIC(20,10)) END AS building_full_reverse_family, 
    
                    -- 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_lv00 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv00_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_lv01_49 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_lv50_99 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_lv100 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv100_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_half / IV1.office_total AS NUMERIC(20,10)) END AS building_half_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0.0 ELSE CAST(IV1.building_total * IV1.office_full / IV1.office_total AS NUMERIC(20,10)) END AS building_full_reverse_office 
                    
                FROM IPPAN_VIEW IV1 
                WHERE 
                    IV1.ken_code=%s AND 
                    IV1.city_code=%s AND 
                    IV1.deleted_at is NULL 
                ORDER BY CAST(IV1.ippan_id AS INTEGER)""", [ken_code, city_code, ])
        else:
            pass

        #######################################################################
        ### レスポンスセット処理(0040)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.input_ken_city_category_view()関数 STEP 5/5.', 'DEBUG')
        template = loader.get_template('P0800Reverse/input.html')
        context = {
            'ken_code': ken_code, 
            'city_code': city_code, 
            'category_code': category_code, 
            
            'ken_list': ken_list, 
            'city_list': city_list, 
            'ippan_reverse_list': ippan_reverse_list, 
        }
        print_log('[INFO] P0800Reverse.input_ken_city_category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0800Reverse.input_ken_city_category_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0800Reverse.input_ken_city_category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Reverse.input_ken_city_category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：summary_ken_city_category_view
### urlpattern：path('summary/ken/<slug:ken_code>/city/<slug:city_code>/category/<slug:category_code>/', views.summary_ken_city_category_view, name='summary_ken_city_category_view')
### template：P0800Reverse/summary.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def summary_ken_city_category_view(request, ken_code, city_code, category_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0800Reverse.summary_ken_city_category_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 city_code = {}'.format(city_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 category_code = {}'.format(category_code), 'DEBUG')
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 STEP 1/5.', 'DEBUG')

        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、下記の計算式に用いるデータを取得する。
        ### (1)家屋被害額 = 延床面積 x 家屋評価額 x 浸水または土砂ごとの勾配差による被害率
        ### (2)家庭用品自動車以外被害額 = 世帯数 x 浸水または土砂ごとの家庭用品被害率 x 家庭用品自動車以外所有額
        ### (3)家庭用品自動車被害額 = 世帯数 x 自動車被害率 x 家庭用品自動車所有額
        ### (4)家庭応急対策費 = (世帯数 x 活動費) + (世帯数 x 清掃日数 x 清掃労働単価)
        ### (5)事業所被害額 = 従業者数 x 産業分類ごとの償却資産 x 浸水または土砂ごとの被害率 + 
        ### 　　　　　　　　　従業者数 x 産業分類ごとの在庫資産 x 浸水または土砂ごとの被害率
        ### (6)事業所営業損失額 = 従業者数 x (営業停止日数 + 停滞日数/2) x 付加価値額
        ### (7)農漁家被害額 = 農漁家戸数 x 農漁家の償却資産 x 浸水または土砂ごとの被害率 + 
        ###                   農漁家戸数 x 農漁家の在庫資産 x 浸水または土砂ごとの被害率
        ### (8)事業所応急対策費 = 事業所数 x 代替活動費
        #######################################################################
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 STEP 2/5.', 'DEBUG')

        #######################################################################
        ### DBアクセス処理(0020)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 STEP 3/5.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        if ken_code == '0':
            city_list = []
        else:
            city_list = CITY.objects.raw("""
                SELECT * FROM CITY WHERE ken_code=%s ORDER BY CAST(city_code AS INTEGER)""", [ken_code, ])
 
        ####################################################################### 
        ### DBアクセス処理(0030)
        ### DBにアクセスして、データを取得する。
        ### 延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
        ####################################################################### 
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 STEP 4/5.', 'DEBUG')
        ippan_reverse_list = None
        if ken_code == "0" and city_code == "0":
            pass
        elif ken_code == "0" and city_code != "0":
            pass
        elif ken_code != "0" and city_code == "0":
            pass
        elif ken_code != "0" and city_code != "0":
            ippan_reverse_list = IPPAN_VIEW.objects.raw("""
                SELECT 
                    IV1.ippan_id AS ippan_id, 
                    IV1.ippan_name AS ippan_name, 
                    IV1.suigai_id AS suigai_id, 
                    IV1.suigai_name AS suigai_name, 
                    IV1.ken_code AS ken_code, 
                    IV1.ken_name AS ken_name, 
                    IV1.city_code AS city_code, 
                    IV1.city_name AS city_name, 
                    IV1.cause_1_code AS cause_1_code, 
                    IV1.cause_1_name AS cause_1_name, 
                    IV1.cause_2_code AS cause_2_code, 
                    IV1.cause_2_name AS cause_2_name, 
                    IV1.cause_3_code AS cause_3_code, 
                    IV1.cause_3_name AS cause_3_name, 
                    IV1.area_id AS area_id, 
                    IV1.area_name AS area_name, 
                    
                    IV1.suikei_code AS suikei_code, 
                    IV1.suikei_name AS suikei_name, 
                    IV1.kasen_code AS kasen_code, 
                    IV1.kasen_name AS kasen_name, 
                    IV1.gradient_code AS gradient_code, 
                    IV1.gradient_name AS gradient_name, 
    
                    CASE WHEN (IV1.residential_area) IS NULL THEN 0.0 ELSE CAST(IV1.residential_area AS NUMERIC(20,10)) END AS residential_area, 
                    CASE WHEN (IV1.agricultural_area) IS NULL THEN 0.0 ELSE CAST(IV1.agricultural_area AS NUMERIC(20,10)) END AS agricultural_area, 
                    CASE WHEN (IV1.underground_area) IS NULL THEN 0.0 ELSE CAST(IV1.underground_area AS NUMERIC(20,10)) END AS underground_area, 
                    IV1.kasen_kaigan_code AS kasen_kaigan_code, 
                    IV1.kasen_kaigan_name AS kasen_kaigan_name, 
                    CASE WHEN (IV1.crop_damage) IS NULL THEN 0.0 ELSE CAST(IV1.crop_damage AS NUMERIC(20,10)) END AS crop_damage, 
                    IV1.weather_id AS weather_id, 
                    IV1.weather_name AS weather_name, 
                    
                    IV1.upload_file_path AS upload_file_path, 
                    IV1.upload_file_name AS upload_file_name, 
                    IV1.summary_file_path AS summary_file_path, 
                    IV1.summary_file_name AS summary_file_name, 
                    
                    IV1.building_code AS building_code, 
                    IV1.building_name AS building_name, 
                    IV1.underground_code AS underground_code, 
                    IV1.underground_name AS underground_name, 
                    IV1.flood_sediment_code AS flood_sediment_code, 
                    IV1.flood_sediment_name AS flood_sediment_name, 
                    
                    CASE WHEN (IV1.building_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv00 AS NUMERIC(20,10)) END AS building_lv00, 
                    CASE WHEN (IV1.building_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv01_49 AS NUMERIC(20,10)) END AS building_lv01_49, 
                    CASE WHEN (IV1.building_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv50_99 AS NUMERIC(20,10)) END AS building_lv50_99, 
                    CASE WHEN (IV1.building_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.building_lv100 AS NUMERIC(20,10)) END AS building_lv100, 
                    CASE WHEN (IV1.building_half) IS NULL THEN 0.0 ELSE CAST(IV1.building_half AS NUMERIC(20,10)) END AS building_half, 
                    CASE WHEN (IV1.building_full) IS NULL THEN 0.0 ELSE CAST(IV1.building_full AS NUMERIC(20,10)) END AS building_full, 
                    CASE WHEN (IV1.building_total) IS NULL THEN 0.0 ELSE CAST(IV1.building_total AS NUMERIC(20,10)) END AS building_total, 
     
                    CASE WHEN (IV1.floor_area) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area AS NUMERIC(20,10)) END AS floor_area, 
                    CASE WHEN (IV1.family) IS NULL THEN 0.0 ELSE CAST(IV1.family AS NUMERIC(20,10)) END AS family, 
                    CASE WHEN (IV1.office) IS NULL THEN 0.0 ELSE CAST(IV1.office AS NUMERIC(20,10)) END AS office, 
    
                    CASE WHEN (IV1.floor_area_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv00 AS NUMERIC(20,10)) END AS floor_area_lv00, 
                    CASE WHEN (IV1.floor_area_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv01_49 AS NUMERIC(20,10)) END AS floor_area_lv01_49, 
                    CASE WHEN (IV1.floor_area_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv50_99 AS NUMERIC(20,10)) END AS floor_area_lv50_99, 
                    CASE WHEN (IV1.floor_area_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_lv100 AS NUMERIC(20,10)) END AS floor_area_lv100, 
                    CASE WHEN (IV1.floor_area_half) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_half AS NUMERIC(20,10)) END AS floor_area_half, 
                    CASE WHEN (IV1.floor_area_full) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_full AS NUMERIC(20,10)) END AS floor_area_full, 
                    CASE WHEN (IV1.floor_area_total) IS NULL THEN 0.0 ELSE CAST(IV1.floor_area_total AS NUMERIC(20,10)) END AS floor_area_total, 
                    
                    CASE WHEN (IV1.family_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv00 AS NUMERIC(20,10)) END AS family_lv00, 
                    CASE WHEN (IV1.family_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv01_49 AS NUMERIC(20,10)) END AS family_lv01_49, 
                    CASE WHEN (IV1.family_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv50_99 AS NUMERIC(20,10)) END AS family_lv50_99, 
                    CASE WHEN (IV1.family_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.family_lv100 AS NUMERIC(20,10)) END AS family_lv100, 
                    CASE WHEN (IV1.family_half) IS NULL THEN 0.0 ELSE CAST(IV1.family_half AS NUMERIC(20,10)) END AS family_half, 
                    CASE WHEN (IV1.family_full) IS NULL THEN 0.0 ELSE CAST(IV1.family_full AS NUMERIC(20,10)) END AS family_full, 
                    CASE WHEN (IV1.family_total) IS NULL THEN 0.0 ELSE CAST(IV1.family_total AS NUMERIC(20,10)) END AS family_total, 
                   
                    CASE WHEN (IV1.office_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv00 AS NUMERIC(20,10)) END AS office_lv00, 
                    CASE WHEN (IV1.office_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv01_49 AS NUMERIC(20,10)) END AS office_lv01_49, 
                    CASE WHEN (IV1.office_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv50_99 AS NUMERIC(20,10)) END AS office_lv50_99, 
                    CASE WHEN (IV1.office_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.office_lv100 AS NUMERIC(20,10)) END AS office_lv100, 
                    CASE WHEN (IV1.office_half) IS NULL THEN 0.0 ELSE CAST(IV1.office_half AS NUMERIC(20,10)) END AS office_half, 
                    CASE WHEN (IV1.office_full) IS NULL THEN 0.0 ELSE CAST(IV1.office_full AS NUMERIC(20,10)) END AS office_full, 
                    CASE WHEN (IV1.office_total) IS NULL THEN 0.0 ELSE CAST(IV1.office_total AS NUMERIC(20,10)) END AS office_total, 
    
                    CASE WHEN (IV1.farmer_fisher_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_lv00, 
                    CASE WHEN (IV1.farmer_fisher_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49, 
                    CASE WHEN (IV1.farmer_fisher_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99, 
                    CASE WHEN (IV1.farmer_fisher_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_lv100, 
                    -- CASE WHEN (IV1.farmer_fisher_half) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_half AS NUMERIC(20,10)) END AS farmer_fisher_half, 
                    CASE WHEN (IV1.farmer_fisher_full) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_full AS NUMERIC(20,10)) END AS farmer_fisher_full, 
                    CASE WHEN (IV1.farmer_fisher_total) IS NULL THEN 0.0 ELSE CAST(IV1.farmer_fisher_total AS NUMERIC(20,10)) END AS farmer_fisher_total, 
    
                    CASE WHEN (IV1.employee_lv00) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv00 AS NUMERIC(20,10)) END AS employee_lv00, 
                    CASE WHEN (IV1.employee_lv01_49) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv01_49 AS NUMERIC(20,10)) END AS employee_lv01_49, 
                    CASE WHEN (IV1.employee_lv50_99) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv50_99 AS NUMERIC(20,10)) END AS employee_lv50_99, 
                    CASE WHEN (IV1.employee_lv100) IS NULL THEN 0.0 ELSE CAST(IV1.employee_lv100 AS NUMERIC(20,10)) END AS employee_lv100, 
                    -- CASE WHEN (IV1.employee_half) IS NULL THEN 0.0 ELSE CAST(IV1.employee_half AS NUMERIC(20,10)) END AS employee_half, 
                    CASE WHEN (IV1.employee_full) IS NULL THEN 0.0 ELSE CAST(IV1.employee_full AS NUMERIC(20,10)) END AS employee_full,
                    CASE WHEN (IV1.employee_total) IS NULL THEN 0.0 ELSE CAST(IV1.employee_total AS NUMERIC(20,10)) END AS employee_total, 
    
                    IV1.industry_code AS industry_code, 
                    IV1.industry_name AS industry_name, 
                    IV1.usage_code AS usage_code,
                    IV1.usage_name AS usage_name, 
                    
                    -- 県別家屋評価額(マスタDB) 
                    CASE WHEN (HA1.house_asset) IS NULL THEN 0.0 ELSE CAST(HA1.house_asset AS NUMERIC(20,10)) END AS house_asset, 
                    
                    -- 家屋被害率(マスタDB) 
                    CASE WHEN (HR1.house_rate_lv00) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv00 AS NUMERIC(20,10)) END AS house_rate_lv00, 
                    CASE WHEN (HR1.house_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv00_50 AS NUMERIC(20,10)) END AS house_rate_lv00_50, 
                    CASE WHEN (HR1.house_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv50_100 AS NUMERIC(20,10)) END AS house_rate_lv50_100, 
                    CASE WHEN (HR1.house_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv100_200 AS NUMERIC(20,10)) END AS house_rate_lv100_200, 
                    CASE WHEN (HR1.house_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv200_300 AS NUMERIC(20,10)) END AS house_rate_lv200_300, 
                    CASE WHEN (HR1.house_rate_lv300) IS NULL THEN 0.0 ELSE CAST(HR1.house_rate_lv300 AS NUMERIC(20,10)) END AS house_rate_lv300, 
                    
                    -- 家庭用品自動車以外所有額(マスタDB) 
                    CASE WHEN (HHA1.household_asset) IS NULL THEN 0.0 ELSE CAST(HHA1.household_asset AS NUMERIC(20,10)) END AS household_asset, 
                    
                    -- 家庭用品自動車以外被害率(マスタDB) 
                    CASE WHEN (HHR1.household_rate_lv00) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv00 AS NUMERIC(20,10)) END AS household_rate_lv00, 
                    CASE WHEN (HHR1.household_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv00_50 AS NUMERIC(20,10)) END AS household_rate_lv00_50, 
                    CASE WHEN (HHR1.household_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv50_100 AS NUMERIC(20,10)) END AS household_rate_lv50_100, 
                    CASE WHEN (HHR1.household_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv100_200 AS NUMERIC(20,10)) END AS household_rate_lv100_200, 
                    CASE WHEN (HHR1.household_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv200_300 AS NUMERIC(20,10)) END AS household_rate_lv200_300, 
                    CASE WHEN (HHR1.household_rate_lv300) IS NULL THEN 0.0 ELSE CAST(HHR1.household_rate_lv300 AS NUMERIC(20,10)) END AS household_rate_lv300, 
                    
                    -- 家庭用品自動車所有額(マスタDB) 
                    CASE WHEN (CA1.car_asset) IS NULL THEN 0.0 ELSE CAST(CA1.car_asset AS NUMERIC(20,10)) END AS car_asset, 
    
                    -- 家庭用品自動車被害率(マスタDB) 
                    CASE WHEN (CR1.car_rate_lv00) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv00 AS NUMERIC(20,10)) END AS car_rate_lv00, 
                    CASE WHEN (CR1.car_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv00_50 AS NUMERIC(20,10)) END AS car_rate_lv00_50, 
                    CASE WHEN (CR1.car_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv50_100 AS NUMERIC(20,10)) END AS car_rate_lv50_100, 
                    CASE WHEN (CR1.car_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv100_200 AS NUMERIC(20,10)) END AS car_rate_lv100_200, 
                    CASE WHEN (CR1.car_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv200_300 AS NUMERIC(20,10)) END AS car_rate_lv200_300, 
                    CASE WHEN (CR1.car_rate_lv300) IS NULL THEN 0.0 ELSE CAST(CR1.car_rate_lv300 AS NUMERIC(20,10)) END AS car_rate_lv300, 
                    
                    -- 家庭応急対策費_代替活動費(マスタDB)
                    CASE WHEN (HALT1.house_alt_lv00) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv00 AS NUMERIC(20,10)) END AS house_alt_lv00, 
                    CASE WHEN (HALT1.house_alt_lv00_50) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv00_50 AS NUMERIC(20,10)) END AS house_alt_lv00_50, 
                    CASE WHEN (HALT1.house_alt_lv50_100) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv50_100 AS NUMERIC(20,10)) END AS house_alt_lv50_100, 
                    CASE WHEN (HALT1.house_alt_lv100_200) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv100_200 AS NUMERIC(20,10)) END AS house_alt_lv100_200, 
                    CASE WHEN (HALT1.house_alt_lv200_300) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv200_300 AS NUMERIC(20,10)) END AS house_alt_lv200_300, 
                    CASE WHEN (HALT1.house_alt_lv300) IS NULL THEN 0.0 ELSE CAST(HALT1.house_alt_lv300 AS NUMERIC(20,10)) END AS house_alt_lv300, 
    
                    -- 家庭応急対策費_清掃労働単価(マスタDB) 
                    CASE WHEN (HCL1.house_clean_unit_cost) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_unit_cost AS NUMERIC(20,10)) END AS house_clean_unit_cost, 
    
                    -- 家庭応急対策費_清掃日数(マスタDB) 
                    CASE WHEN (HCL1.house_clean_days_lv00) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv00 AS NUMERIC(20,10)) END AS house_clean_days_lv00, 
                    CASE WHEN (HCL1.house_clean_days_lv00_50) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv00_50 AS NUMERIC(20,10)) END AS house_clean_days_lv00_50, 
                    CASE WHEN (HCL1.house_clean_days_lv50_100) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv50_100 AS NUMERIC(20,10)) END AS house_clean_days_lv50_100, 
                    CASE WHEN (HCL1.house_clean_days_lv100_200) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv100_200 AS NUMERIC(20,10)) END AS house_clean_days_lv100_200, 
                    CASE WHEN (HCL1.house_clean_days_lv200_300) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv200_300 AS NUMERIC(20,10)) END AS house_clean_days_lv200_300, 
                    CASE WHEN (HCL1.house_clean_days_lv300) IS NULL THEN 0.0 ELSE CAST(HCL1.house_clean_days_lv300 AS NUMERIC(20,10)) END AS house_clean_days_lv300, 
                    
                    -- 事業所資産額_償却資産額(マスタDB) 
                    CASE WHEN (OA1.office_dep_asset) IS NULL THEN 0.0 ELSE CAST(OA1.office_dep_asset AS NUMERIC(20,10)) END AS office_dep_asset, 
                    
                    -- 事業所被害率_償却資産被害率(マスタDB) 
                    CASE WHEN (OR1.office_dep_rate_lv00) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv00 AS NUMERIC(20,10)) END AS office_dep_rate_lv00, 
                    CASE WHEN (OR1.office_dep_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv00_50 AS NUMERIC(20,10)) END AS office_dep_rate_lv00_50, 
                    CASE WHEN (OR1.office_dep_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv50_100 AS NUMERIC(20,10)) END AS office_dep_rate_lv50_100, 
                    CASE WHEN (OR1.office_dep_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv100_200 AS NUMERIC(20,10)) END AS office_dep_rate_lv100_200, 
                    -- CASE WHEN (OR1.office_dep_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv200_300 AS NUMERIC(20,10)) END AS office_dep_rate_lv200_300, 
                    CASE WHEN (OR1.office_dep_rate_lv300) IS NULL THEN 0.0 ELSE CAST(OR1.office_dep_rate_lv300 AS NUMERIC(20,10)) END AS office_dep_rate_lv300, 
    
                    -- 事業所資産額_在庫資産額(マスタDB) 
                    CASE WHEN (OA1.office_inv_asset) IS NULL THEN 0.0 ELSE CAST(OA1.office_inv_asset AS NUMERIC(20,10)) END AS office_inv_asset, 
    
                    -- 事業所被害率_在庫資産被害率(マスタDB) 
                    CASE WHEN (OR1.office_inv_rate_lv00) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv00 AS NUMERIC(20,10)) END AS office_inv_rate_lv00, 
                    CASE WHEN (OR1.office_inv_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv00_50 AS NUMERIC(20,10)) END AS office_inv_rate_lv00_50, 
                    CASE WHEN (OR1.office_inv_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv50_100 AS NUMERIC(20,10)) END AS office_inv_rate_lv50_100, 
                    CASE WHEN (OR1.office_inv_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv100_200 AS NUMERIC(20,10)) END AS office_inv_rate_lv100_200, 
                    -- CASE WHEN (OR1.office_inv_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv200_300 AS NUMERIC(20,10)) END AS office_inv_rate_lv200_300, 
                    CASE WHEN (OR1.office_inv_rate_lv300) IS NULL THEN 0.0 ELSE CAST(OR1.office_inv_rate_lv300 AS NUMERIC(20,10)) END AS office_inv_rate_lv300, 
    
                    -- 事業所資産額_付加価値額(マスタDB) 
                    CASE WHEN (OA1.office_va_asset) IS NULL THEN 0.0 ELSE CAST(OA1.office_va_asset AS NUMERIC(20,10)) END AS office_va_asset, 
    
                    -- 事業所被害額_営業停止に伴う被害額(マスタDB) 
                    CASE WHEN (OSUS1.office_sus_days_lv00) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv00 AS NUMERIC(20,10)) END AS office_sus_days_lv00, 
                    CASE WHEN (OSUS1.office_sus_days_lv00_50) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv00_50 AS NUMERIC(20,10)) END AS office_sus_days_lv00_50, 
                    CASE WHEN (OSUS1.office_sus_days_lv50_100) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv50_100 AS NUMERIC(20,10)) END AS office_sus_days_lv50_100, 
                    CASE WHEN (OSUS1.office_sus_days_lv100_200) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv100_200 AS NUMERIC(20,10)) END AS office_sus_days_lv100_200, 
                    -- CASE WHEN (OSUS1.office_sus_days_lv200_300) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv200_300 AS NUMERIC(20,10)) END AS office_sus_days_lv200_300, 
                    CASE WHEN (OSUS1.office_sus_days_lv300) IS NULL THEN 0.0 ELSE CAST(OSUS1.office_sus_days_lv300 AS NUMERIC(20,10)) END AS office_sus_days_lv300, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(マスタDB) 
                    CASE WHEN (OSTG1.office_stg_days_lv00) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv00 AS NUMERIC(20,10)) END AS office_stg_days_lv00, 
                    CASE WHEN (OSTG1.office_stg_days_lv00_50) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv00_50 AS NUMERIC(20,10)) END AS office_stg_days_lv00_50, 
                    CASE WHEN (OSTG1.office_stg_days_lv50_100) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv50_100 AS NUMERIC(20,10)) END AS office_stg_days_lv50_100, 
                    CASE WHEN (OSTG1.office_stg_days_lv100_200) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv100_200 AS NUMERIC(20,10)) END AS office_stg_days_lv100_200, 
                    -- CASE WHEN (OSTG1.office_stg_days_lv200_300) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv200_300 AS NUMERIC(20,10)) END AS office_stg_days_lv200_300, 
                    CASE WHEN (OSTG1.office_stg_days_lv300) IS NULL THEN 0.0 ELSE CAST(OSTG1.office_stg_days_lv300 AS NUMERIC(20,10)) END AS office_stg_days_lv300, 
                    
                    -- 農漁家資産額_償却資産額(マスタDB) 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset) IS NULL THEN 0.0 ELSE CAST(FFA1.farmer_fisher_dep_asset AS NUMERIC(20,10)) END AS farmer_fisher_dep_asset, 
                    
                    -- 農漁家被害率_償却資産被害率(マスタDB) 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv00) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv00, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv00_50 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv00_50, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv50_100 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv50_100, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv100_200 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv100_200, 
                    -- CASE WHEN (FFR1.farmer_fisher_dep_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv200_300 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv200_300, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv300) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv300 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv300, 
    
                    -- 農漁家資産額_在庫資産額(マスタDB) 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset) IS NULL THEN 0.0 ELSE CAST(FFA1.farmer_fisher_inv_asset AS NUMERIC(20,10)) END AS farmer_fisher_inv_asset, 
                    
                    -- 農漁家被害率_在庫資産被害率(マスタDB) 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv00) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv00, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv00_50) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv00_50 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv00_50, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv50_100) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv50_100 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv50_100, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv100_200) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv100_200 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv100_200, 
                    -- CASE WHEN (FFR1.farmer_fisher_inv_rate_lv200_300) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv200_300 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv200_300, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv300) IS NULL THEN 0.0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv300 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv300, 
                    
                    -- 事業所応急対策費_代替活動費(マスタDB) 
                    CASE WHEN (OALT1.office_alt_lv00) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv00 AS NUMERIC(20,10)) END AS office_alt_lv00, 
                    CASE WHEN (OALT1.office_alt_lv00_50) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv00_50 AS NUMERIC(20,10)) END AS office_alt_lv00_50, 
                    CASE WHEN (OALT1.office_alt_lv50_100) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv50_100 AS NUMERIC(20,10)) END AS office_alt_lv50_100, 
                    CASE WHEN (OALT1.office_alt_lv100_200) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv100_200 AS NUMERIC(20,10)) END AS office_alt_lv100_200, 
                    CASE WHEN (OALT1.office_alt_lv200_300) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv200_300 AS NUMERIC(20,10)) END AS office_alt_lv200_300, 
                    CASE WHEN (OALT1.office_alt_lv300) IS NULL THEN 0.0 ELSE CAST(OALT1.office_alt_lv300 AS NUMERIC(20,10)) END AS office_alt_lv300, 
                    
                    -- 家屋被害額(集計DB) 
                    CASE WHEN (IS1.house_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_lv00 AS NUMERIC(20,10)) END AS house_summary_lv00, 
                    CASE WHEN (IS1.house_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_lv01_49 AS NUMERIC(20,10)) END AS house_summary_lv01_49, 
                    CASE WHEN (IS1.house_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_lv50_99 AS NUMERIC(20,10)) END AS house_summary_lv50_99, 
                    CASE WHEN (IS1.house_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_lv100 AS NUMERIC(20,10)) END AS house_summary_lv100, 
                    CASE WHEN (IS1.house_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_half AS NUMERIC(20,10)) END AS house_summary_half, 
                    CASE WHEN (IS1.house_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.house_summary_full AS NUMERIC(20,10)) END AS house_summary_full, 
                    
                    -- 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv00 / (HA1.house_asset * HR1.house_rate_lv00) AS NUMERIC(20,10)) END AS floor_area_lv00_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv01_49 / (HA1.house_asset * HR1.house_rate_lv00_50) AS NUMERIC(20,10)) END AS floor_area_lv01_49_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv50_99 / (HA1.house_asset * HR1.house_rate_lv50_100) AS NUMERIC(20,10)) END AS floor_area_lv50_99_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv100 / (HA1.house_asset * HR1.house_rate_lv100_200) AS NUMERIC(20,10)) END AS floor_area_lv100_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_half / (HA1.house_asset * HR1.house_rate_lv200_300) AS NUMERIC(20,10)) END AS floor_area_half_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_full / (HA1.house_asset * HR1.house_rate_lv300) AS NUMERIC(20,10)) END AS floor_area_full_reverse_house_summary, 
                    
                    -- 家庭用品自動車以外被害額(集計DB) 
                    CASE WHEN (IS1.household_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_lv00 AS NUMERIC(20,10)) END AS household_summary_lv00,
                    CASE WHEN (IS1.household_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_lv01_49 AS NUMERIC(20,10)) END AS household_summary_lv01_49, 
                    CASE WHEN (IS1.household_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_lv50_99 AS NUMERIC(20,10)) END AS household_summary_lv50_99, 
                    CASE WHEN (IS1.household_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_lv100 AS NUMERIC(20,10)) END AS household_summary_lv100, 
                    CASE WHEN (IS1.household_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_half AS NUMERIC(20,10)) END AS household_summary_half, 
                    CASE WHEN (IS1.household_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.household_summary_full AS NUMERIC(20,10)) END AS household_summary_full, 
    
                    -- 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv00 / (HHA1.household_asset * HHR1.household_rate_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv01_49 / (HHA1.household_asset * HHR1.household_rate_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv50_99 / (HHA1.household_asset * HHR1.household_rate_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv100 / (HHA1.household_asset * HHR1.household_rate_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_half / (HHA1.household_asset * HHR1.household_rate_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_full / (HHA1.household_asset * HHR1.household_rate_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_household_summary, 
                    
                    -- 家庭用品自動車被害額(集計DB) 
                    CASE WHEN (IS1.car_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_lv00 AS NUMERIC(20,10)) END AS car_summary_lv00, 
                    CASE WHEN (IS1.car_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_lv01_49 AS NUMERIC(20,10)) END AS car_summary_lv01_49, 
                    CASE WHEN (IS1.car_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_lv50_99 AS NUMERIC(20,10)) END AS car_summary_lv50_99, 
                    CASE WHEN (IS1.car_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_lv100 AS NUMERIC(20,10)) END AS car_summary_lv100, 
                    CASE WHEN (IS1.car_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_half AS NUMERIC(20,10)) END AS car_summary_half, 
                    CASE WHEN (IS1.car_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.car_summary_full AS NUMERIC(20,10)) END AS car_summary_full, 
    
                    -- 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv00 / (CA1.car_asset * CR1.car_rate_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv01_49 / (CA1.car_asset * CR1.car_rate_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv50_99 / (CA1.car_asset * CR1.car_rate_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv100 / (CA1.car_asset * CR1.car_rate_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_half / (CA1.car_asset * CR1.car_rate_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_full / (CA1.car_asset * CR1.car_rate_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_car_summary, 
    
                    -- 家庭応急対策費_代替活動費(集計DB) 
                    CASE WHEN (IS1.house_alt_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_lv00 AS NUMERIC(20,10)) END AS house_alt_summary_lv00, 
                    CASE WHEN (IS1.house_alt_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_lv01_49 AS NUMERIC(20,10)) END AS house_alt_summary_lv01_49, 
                    CASE WHEN (IS1.house_alt_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_lv50_99 AS NUMERIC(20,10)) END AS house_alt_summary_lv50_99, 
                    CASE WHEN (IS1.house_alt_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_lv100 AS NUMERIC(20,10)) END AS house_alt_summary_lv100, 
                    CASE WHEN (IS1.house_alt_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_half AS NUMERIC(20,10)) END AS house_alt_summary_half, 
                    CASE WHEN (IS1.house_alt_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.house_alt_summary_full AS NUMERIC(20,10)) END AS house_alt_summary_full, 
    
                    -- 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HALT1.house_alt_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv00 / HALT1.house_alt_lv00 AS NUMERIC(20,10)) END AS family_lv00_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv01_49 / HALT1.house_alt_lv00_50 AS NUMERIC(20,10)) END AS family_lv01_49_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv50_99 / HALT1.house_alt_lv50_100 AS NUMERIC(20,10)) END AS family_lv50_99_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv100 / HALT1.house_alt_lv100_200 AS NUMERIC(20,10)) END AS family_lv100_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_half / HALT1.house_alt_lv200_300 AS NUMERIC(20,10)) END AS family_half_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_full / HALT1.house_alt_lv300 AS NUMERIC(20,10)) END AS family_full_reverse_house_alt_summary, 
    
                    -- 家庭応急対策費_清掃費(集計DB) 
                    CASE WHEN (IS1.house_clean_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_lv00 AS NUMERIC(20,10)) END AS house_clean_summary_lv00, 
                    CASE WHEN (IS1.house_clean_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_lv01_49 AS NUMERIC(20,10)) END AS house_clean_summary_lv01_49, 
                    CASE WHEN (IS1.house_clean_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_lv50_99 AS NUMERIC(20,10)) END AS house_clean_summary_lv50_99, 
                    CASE WHEN (IS1.house_clean_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_lv100 AS NUMERIC(20,10)) END AS house_clean_summary_lv100, 
                    CASE WHEN (IS1.house_clean_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_half AS NUMERIC(20,10)) END AS house_clean_summary_half, 
                    CASE WHEN (IS1.house_clean_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.house_clean_summary_full AS NUMERIC(20,10)) END AS house_clean_summary_full, 
    
                    -- 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv00 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv01_49 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv50_99 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv100 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_half / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_full / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_house_clean_summary, 
    
                    -- 事業所被害額_償却資産被害額(集計DB) 
                    CASE WHEN (IS1.office_dep_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_lv00 AS NUMERIC(20,10)) END AS office_dep_summary_lv00, 
                    CASE WHEN (IS1.office_dep_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_lv01_49 AS NUMERIC(20,10)) END AS office_dep_summary_lv01_49, 
                    CASE WHEN (IS1.office_dep_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_lv50_99 AS NUMERIC(20,10)) END AS office_dep_summary_lv50_99, 
                    CASE WHEN (IS1.office_dep_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_lv100 AS NUMERIC(20,10)) END AS office_dep_summary_lv100, 
                    -- CASE WHEN (IS1.office_dep_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_half AS NUMERIC(20,10)) END AS office_dep_summary_half, 
                    CASE WHEN (IS1.office_dep_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.office_dep_summary_full AS NUMERIC(20,10)) END AS office_dep_summary_full, 
                    
                    -- 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv00 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv01_49 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00_50) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv50_99 / (OA1.office_dep_asset * OR1.office_dep_rate_lv50_100) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv100 / (OA1.office_dep_asset * OR1.office_dep_rate_lv100_200) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_dep_summary, 
                    -- CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_half / (OA1.office_dep_asset * OR1.office_dep_rate_lv200_300) AS NUMERIC(20,10)) END AS employee_half_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_full / (OA1.office_dep_asset * OR1.office_dep_rate_lv300) AS NUMERIC(20,10)) END AS employee_full_reverse_office_dep_summary, 
    
                    -- 事業所被害額_在庫資産被害額(集計DB) 
                    CASE WHEN (IS1.office_inv_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_lv00 AS NUMERIC(20,10)) END AS office_inv_summary_lv00, 
                    CASE WHEN (IS1.office_inv_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_lv01_49 AS NUMERIC(20,10)) END AS office_inv_summary_lv01_49, 
                    CASE WHEN (IS1.office_inv_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_lv50_99 AS NUMERIC(20,10)) END AS office_inv_summary_lv50_99, 
                    CASE WHEN (IS1.office_inv_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_lv100 AS NUMERIC(20,10)) END AS office_inv_summary_lv100, 
                    -- CASE WHEN (IS1.office_inv_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_half AS NUMERIC(20,10)) END AS office_inv_summary_half, 
                    CASE WHEN (IS1.office_inv_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.office_inv_summary_full AS NUMERIC(20,10)) END AS office_inv_summary_full, 
                    
                    -- 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv00 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv01_49 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00_50) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv50_99 / (OA1.office_inv_asset * OR1.office_inv_rate_lv50_100) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv100 / (OA1.office_inv_asset * OR1.office_inv_rate_lv100_200) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_inv_summary, 
                    -- CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_half / (OA1.office_inv_asset * OR1.office_inv_rate_lv200_300) AS NUMERIC(20,10)) END AS employee_half_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_full / (OA1.office_inv_asset * OR1.office_inv_rate_lv300) AS NUMERIC(20,10)) END AS employee_full_reverse_office_inv_summary, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB) 
                    CASE WHEN (IS1.office_sus_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_lv00 AS NUMERIC(20,10)) END AS office_sus_summary_lv00, 
                    CASE WHEN (IS1.office_sus_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_lv01_49 AS NUMERIC(20,10)) END AS office_sus_summary_lv01_49, 
                    CASE WHEN (IS1.office_sus_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_lv50_99 AS NUMERIC(20,10)) END AS office_sus_summary_lv50_99, 
                    CASE WHEN (IS1.office_sus_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_lv100 AS NUMERIC(20,10)) END AS office_sus_summary_lv100, 
                    -- CASE WHEN (IS1.office_sus_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_half AS NUMERIC(20,10)) END AS office_sus_summary_half, 
                    CASE WHEN (IS1.office_sus_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.office_sus_summary_full AS NUMERIC(20,10)) END AS office_sus_summary_full, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv00 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv00 / (OSUS1.office_sus_days_lv00 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv01_49 / (OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv50_99 / (OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv100 / (OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_sus_summary, 
                    -- CASE WHEN ABS(OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_half / (OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_half_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv300 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_full / (OSUS1.office_sus_days_lv300 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_full_reverse_office_sus_summary, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB) 
                    CASE WHEN (IS1.office_stg_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_lv00 AS NUMERIC(20,10)) END AS office_stg_summary_lv00, 
                    CASE WHEN (IS1.office_stg_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_lv01_49 AS NUMERIC(20,10)) END AS office_stg_summary_lv01_49, 
                    CASE WHEN (IS1.office_stg_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_lv50_99 AS NUMERIC(20,10)) END AS office_stg_summary_lv50_99, 
                    CASE WHEN (IS1.office_stg_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_lv100 AS NUMERIC(20,10)) END AS office_stg_summary_lv100, 
                    -- CASE WHEN (IS1.office_stg_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_half AS NUMERIC(20,10)) END AS office_stg_summary_half, 
                    CASE WHEN (IS1.office_stg_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.office_stg_summary_full AS NUMERIC(20,10)) END AS office_stg_summary_full, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv00 / (OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv01_49 / (OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv50_99 / (OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv100 / (OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_stg_summary, 
                    -- CASE WHEN ABS(OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_half / (OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_half_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_full / (OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_full_reverse_office_stg_summary, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB) 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv00, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv01_49, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv50_99, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv100, 
                    -- CASE WHEN (IS1.farmer_fisher_dep_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_half AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_half, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_dep_summary_full AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_full, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv00 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00) AS NUMERIC(20,10)) END AS farmer_fisher_lv00_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv01_49 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50) AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv50_99 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100) AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv100 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200) AS NUMERIC(20,10)) END AS farmer_fisher_lv100_reverse_farmer_fisher_dep_summary, 
                    -- CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_half / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300) AS NUMERIC(20,10)) END AS farmer_fisher_half_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_full / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300) AS NUMERIC(20,10)) END AS farmer_fisher_full_reverse_farmer_fisher_dep_summary, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB) 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv00, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv01_49, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv50_99, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv100, 
                    -- CASE WHEN (IS1.farmer_fisher_inv_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_half AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_half, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.farmer_fisher_inv_summary_full AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_full, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv00 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00) AS NUMERIC(20,10)) END AS farmer_fisher_lv00_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv01_49 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50) AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv50_99 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100) AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv100 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200) AS NUMERIC(20,10)) END AS farmer_fisher_lv100_reverse_farmer_fisher_inv_summary, 
                    -- CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_half / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300) AS NUMERIC(20,10)) END AS farmer_fisher_half_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_full / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300) AS NUMERIC(20,10)) END AS farmer_fisher_full_reverse_farmer_fisher_inv_summary, 
    
                    -- 事業所応急対策費_代替活動費(集計DB) 
                    CASE WHEN (IS1.office_alt_summary_lv00) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_lv00 AS NUMERIC(20,10)) END AS office_alt_summary_lv00, 
                    CASE WHEN (IS1.office_alt_summary_lv01_49) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_lv01_49 AS NUMERIC(20,10)) END AS office_alt_summary_lv01_49, 
                    CASE WHEN (IS1.office_alt_summary_lv50_99) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_lv50_99 AS NUMERIC(20,10)) END AS office_alt_summary_lv50_99, 
                    CASE WHEN (IS1.office_alt_summary_lv100) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_lv100 AS NUMERIC(20,10)) END AS office_alt_summary_lv100, 
                    CASE WHEN (IS1.office_alt_summary_half) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_half AS NUMERIC(20,10)) END AS office_alt_summary_half, 
                    CASE WHEN (IS1.office_alt_summary_full) IS NULL THEN 0.0 ELSE CAST(IS1.office_alt_summary_full AS NUMERIC(20,10)) END AS office_alt_summary_full, 
    
                    -- 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 
                    CASE WHEN ABS(OALT1.office_alt_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv00 / OALT1.office_alt_lv00 AS NUMERIC(20,10)) END AS office_lv00_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv01_49 / OALT1.office_alt_lv00_50 AS NUMERIC(20,10)) END AS office_lv01_49_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv50_99 / OALT1.office_alt_lv50_100 AS NUMERIC(20,10)) END AS office_lv50_99_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv100 / OALT1.office_alt_lv100_200 AS NUMERIC(20,10)) END AS office_lv100_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_half / OALT1.office_alt_lv200_300 AS NUMERIC(20,10)) END AS office_half_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_full / OALT1.office_alt_lv300 AS NUMERIC(20,10)) END AS office_full_reverse_office_alt_summary 
                    
                FROM IPPAN_VIEW IV1 
                LEFT JOIN IPPAN_SUMMARY IS1 ON IV1.ippan_id = IS1.ippan_id 
                LEFT JOIN HOUSE_ASSET HA1 ON IV1.ken_code = HA1.ken_code 
                LEFT JOIN HOUSE_RATE HR1 ON IV1.flood_sediment_code = HR1.flood_sediment_code AND IV1.gradient_code = HR1.gradient_code 
                LEFT JOIN HOUSEHOLD_RATE HHR1 ON IV1.flood_sediment_code = HHR1.flood_sediment_code 
                LEFT JOIN OFFICE_ASSET OA1 ON IV1.industry_code = OA1.industry_code 
                LEFT JOIN OFFICE_RATE OR1 ON IV1.flood_sediment_code = OR1.flood_sediment_code 
                LEFT JOIN FARMER_FISHER_RATE FFR1 ON IV1.flood_sediment_code = FFR1.flood_sediment_code, -- why left join ? see below comment
                HOUSEHOLD_ASSET HHA1, 
                CAR_ASSET CA1, 
                CAR_RATE CR1, 
                HOUSE_ALT HALT1, 
                HOUSE_CLEAN HCL1, 
                OFFICE_SUSPEND OSUS1, 
                OFFICE_STAGNATE OSTG1, 
                FARMER_FISHER_ASSET FFA1, 
                OFFICE_ALT OALT1 
                WHERE 
                    IV1.ken_code=%s AND 
                    IV1.city_code=%s AND 
                    IV1.deleted_at is NULL 
                ORDER BY CAST(IV1.IPPAN_ID AS INTEGER)""", [ken_code, city_code, ])

            ### 複数レコードあるテーブルは単純に結合しないこと。
            ### 複数レコードあるテーブルはLEFT JOINにすること。
            ### 理由は、検索結果の件数がメインのテーブルの件数ではなく、結合したテーブルの複数レコード分となるため。
            
        else:
            pass
            
        #######################################################################
        ### レスポンスセット処理(0040)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0800Reverse.summary_ken_city_category_view()関数 STEP 5/5.', 'DEBUG')
        template = loader.get_template('P0800Reverse/summary.html')
        context = {
            'ken_code': ken_code, 
            'city_code': city_code, 
            'category_code': category_code, 
            
            'ken_list': ken_list, 
            'city_list': city_list, 
            'ippan_reverse_list': ippan_reverse_list, 
        }
        print_log('[INFO] P0800Reverse.summary_ken_city_category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0800Reverse.summary_ken_city_category_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0800Reverse.summary_ken_city_category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Reverse.summary_ken_city_category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
