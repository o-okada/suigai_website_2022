#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0400OnlineDisplay/views.py
### オンライン表示
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
from P0000Common.models import KOEKI_INDUSTRY          ### 1140: 公益事業分類

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

from P0000Common.common import get_debug_log
from P0000Common.common import get_error_log
from P0000Common.common import get_info_log
from P0000Common.common import get_warn_log
from P0000Common.common import print_log
from P0000Common.common import reset_log

###############################################################################
### 関数名：index_view
### urlpattern：path('', views.index_view, name='index_view')
### template：P0400OnlineDisplay/index.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        ### reset_log()
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0400OnlineDisplay.index_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.index_view()関数 STEP 1/3.', 'DEBUG')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.index_view()関数 STEP 2/3.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.index_view()関数 STEP 3/3.', 'DEBUG')
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_list': ken_list, 
        }
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：category1_category2_ken_city_view
### urlpattern：path('category1/<slug:category_code1>/category2/<slug:category_code2>/ken/<slug:ken_code>/city/<slug:city_code>/', views.category1_category2_ken_city_view, name='category1_category2_ken_city_view'),
### template：P0400OnlineDisplay/index.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def category1_category2_ken_city_view(request, category_code1, category_code2, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        ### reset_log()
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 category_code1 = {}'.format(category_code1), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 category_code2 = {}'.format(category_code2), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 city_code = {}'.format(city_code), 'DEBUG')
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 1/5.', 'DEBUG')

        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 2/5.', 'DEBUG')
        ken_list = []
        city_list = []
        
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(ken_code AS INTEGER)""", [])
        
        if ken_code == "0":
            city_list = CITY.objects.raw("""
                SELECT 
                    CT1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    CT1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    CASE WHEN (CT1.city_population) IS NULL THEN 0.00 ELSE CAST(CT1.city_population AS NUMERIC(20,10)) END AS city_population, 
                    CASE WHEN (CT1.city_area) IS NULL THEN 0.00 ELSE CAST(CT1.city_area AS NUMERIC(20,10)) END AS city_area 
                FROM CITY CT1 
                LEFT JOIN KEN KE1 ON CT1.ken_code=KE1.ken_code 
                ORDER BY CAST(CT1.CITY_CODE AS INTEGER)""", [])
        else:
            city_list = CITY.objects.raw("""
                SELECT 
                    CT1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    CT1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    CASE WHEN (CT1.city_population) IS NULL THEN 0.0 ELSE CAST(CT1.city_population AS NUMERIC(20,10)) END AS city_population, 
                    CASE WHEN (CT1.city_area) IS NULL THEN 0.0 ELSE CAST(CT1.city_area AS NUMERIC(20,10)) END AS city_area 
                FROM CITY CT1 
                LEFT JOIN KEN KE1 ON CT1.ken_code=KE1.ken_code 
                WHERE CT1.KEN_CODE=%s 
                ORDER BY CAST(CT1.CITY_CODE AS INTEGER)""", [ken_code, ])
        
        #######################################################################
        ### DBアクセス処理(0020)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 3/5.', 'DEBUG')
        building_list = []                             ### 1000: 建物区分（マスタDB）
        ### ken_list                                   ### 1010: 都道府県（マスタDB）
        ### city_list                                  ### 1020: 市区町村（マスタDB）
        kasen_kaigan_list = []                         ### 1030: 水害発生地点工種（河川海岸区分）（マスタDB）
        suikei_list = []                               ### 1040: 水系（水系・沿岸）（マスタDB）
        suikei_type_list = []                          ### 1050: 水系種別（水系・沿岸種別）（マスタDB）
        kasen_list = []                                ### 1060: 河川（河川・海岸）（マスタDB）
        kasen_type_list = []                           ### 1070: 河川種別（河川・海岸種別）
        cause_list = []                                ### 1080: 水害原因
        underground_list = []                          ### 1090: 地上地下区分
        usage_list = []                                ### 1100: 地下空間の利用形態
        flood_sediment_list = []                       ### 1110: 浸水土砂区分
        gradient_list = []                             ### 1120: 地盤勾配区分
        industry_list = []                             ### 1130: 産業分類
        house_asset_list = []                          ### 2000: 家屋評価額
        house_rate_list = []                           ### 2010: 家屋被害率
        house_alt_list = []                            ### 2020: 家庭応急対策費_代替活動費
        house_clean_list = []                          ### 2030: 家庭応急対策費_清掃日数
        household_asset_list = []                      ### 3000: 家庭用品自動車以外所有額
        household_rate_list = []                       ### 3010: 家庭用品自動車以外被害率
        car_asset_list = []                            ### 4000: 家庭用品自動車所有額
        car_rate_list = []                             ### 4010: 家庭用品自動車被害率
        office_asset_list = []                         ### 5000: 事業所資産額
        office_rate_list = []                          ### 5010: 事業所被害率
        office_suspend_list = []                       ### 5020: 事業所営業停止日数
        office_stagnate_list = []                      ### 5030: 事業所営業停滞日数
        office_alt_list = []                           ### 5040: 事業所応急対策費_代替活動費
        farmer_fisher_asset_list = []                  ### 6000: 農漁家資産額
        farmer_fisher_rate_list = []                   ### 6010: 農漁家被害率
        area_list = []                                 ### 7000: 一般資産入力データ_水害区域
        weather_list = []                              ### 7010: 一般資産入力データ_異常気象
        suigai_list = []                               ### 7020: 一般資産入力データ_ヘッダ部分
        ippan_list = []                                ### 7030: 一般資産入力データ_一覧表部分
        ippan_view_list = []                           ### 7040: 一般資産ビューデータ_一覧表部分
        ippan_summary_list = []                        ### 8000: 一般資産集計データ
        ippan_group_by_ken_list = []                   ### 8010: 
        ippan_group_by_suikei_list = []                ### 8020: 
        action_list = []                               ### 10000: アクション
        status_list = []                               ### 10010: 状態
        trigger_list = []                              ### 10020: トリガーメッセージ
        
        #######################################################################
        ### DBアクセス処理(0030)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 4/5.', 'DEBUG')
        ### 参照するデータの種別を選択してください。
        if category_code2 == "0":
            pass
        
        ### 建物区分: BUILDING
        elif category_code2 == "1" or category_code2 == "1000":
            building_list = BUILDING.objects.raw("""
                SELECT 
                    building_code, 
                    building_name 
                FROM BUILDING 
                ORDER BY CAST(building_code AS INTEGER)""", [])
            
        ### 都道府県: KEN
        elif category_code2 == "2" or category_code2 == "1010":
            pass
        
        ### 市区町村: CITY
        elif category_code2 == "3" or category_code2 == "1020":
            pass
        
        ### 水害発生地点工種（河川海岸区分）: KASEN_KAIGAN
        elif category_code2 == "4" or category_code2 == "1030":
            kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""
                SELECT 
                    kasen_kaigan_code, 
                    kasen_kaigan_name 
                FROM KASEN_KAIGAN 
                ORDER BY CAST(kasen_kaigan_code AS INTEGER)""", [])
            
        ### 水系: SUIKEI
        elif category_code2 == "5" or category_code2 == "1040":
            suikei_list = SUIKEI.objects.raw("""
                SELECT 
                    SK1.suikei_code AS suikei_code, 
                    SK1.suikei_name AS suikei_name, 
                    SK1.suikei_type_code AS suikei_type_code, 
                    ST1.suikei_type_name AS suikei_type_name 
                FROM SUIKEI SK1 
                LEFT JOIN SUIKEI_TYPE ST1 ON SK1.suikei_type_code=ST1.suikei_type_code 
                ORDER BY CAST(SK1.suikei_code AS INTEGER)""", [])
            
        ### 水系種別: SUIKEI_TYPE
        elif category_code2 == "6" or category_code2 == "1050":
            suikei_type_list = SUIKEI_TYPE.objects.raw("""
                SELECT 
                    suikei_type_code, 
                    suikei_type_name 
                FROM SUIKEI_TYPE 
                ORDER BY CAST(suikei_type_code AS INTEGER)""", [])
            
        ### 河川（河川・海岸）: KASEN
        elif category_code2 == "7" or category_code2 == "1060":
            kasen_list = KASEN.objects.raw("""
                SELECT 
                    KA1.kasen_code AS kasen_code, 
                    KA1.kasen_name AS kasen_name, 
                    KA1.kasen_type_code AS kasen_type_code, 
                    KT1.kasen_type_name AS kasen_type_name, 
                    SK1.suikei_code AS suikei_code, 
                    SK1.suikei_name AS suikei_name 
                FROM KASEN KA1 
                LEFT JOIN KASEN_TYPE KT1 ON KA1.kasen_type_code=KT1.kasen_type_code 
                LEFT JOIN SUIKEI SK1 ON KA1.suikei_code=SK1.suikei_code 
                ORDER BY CAST(KA1.kasen_code AS INTEGER)""", [])
            
        ### 河川種別（河川・海岸種別）: KASEN_TYPE
        elif category_code2 == "8" or category_code2 == "1070":
            kasen_type_list = KASEN_TYPE.objects.raw("""
                SELECT 
                    kasen_type_code, 
                    kasen_type_name 
                FROM KASEN_TYPE 
                ORDER BY CAST(kasen_type_code AS INTEGER)""", [])
            
        ### 水害原因: CAUSE
        elif category_code2 == "9" or category_code2 == "1080":
            cause_list = CAUSE.objects.raw("""
                SELECT 
                    cause_code, 
                    cause_name 
                FROM CAUSE 
                ORDER BY CAST(cause_code AS INTEGER)""", [])
            
        ### 地上地下区分: UNDERGROUND
        elif category_code2 == "10" or category_code2 == "1090":
            underground_list = UNDERGROUND.objects.raw("""
                SELECT 
                    underground_code, 
                    underground_name 
                FROM UNDERGROUND 
                ORDER BY CAST(underground_code AS INTEGER)""", [])
            
        ### 地下空間の利用形態: USAGE
        elif category_code2 == "11" or category_code2 == "1100":
            usage_list = USAGE.objects.raw("""
                SELECT 
                    usage_code, 
                    usage_name 
                FROM USAGE 
                ORDER BY CAST(usage_code AS INTEGER)""", [])
            
        ### 浸水土砂区分: FLOOD_SEDIMENT
        elif category_code2 == "12" or category_code2 == "1110":
            flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""
                SELECT 
                    flood_sediment_code, 
                    flood_sediment_name 
                FROM FLOOD_SEDIMENT 
                ORDER BY CAST(flood_sediment_code AS INTEGER)""", [])
            
        ### 地盤勾配区分: GRADIENT
        elif category_code2 == "13" or category_code2 == "1120":
            gradient_list = GRADIENT.objects.raw("""
                SELECT 
                    gradient_code, 
                    gradient_name 
                FROM GRADIENT 
                ORDER BY CAST(gradient_code AS INTEGER)""", [])
            
        ### 産業分類: INDUSTRY
        elif category_code2 == "14" or category_code2 == "1130":
            industry_list = INDUSTRY.objects.raw("""
                SELECT 
                    industry_code, 
                    industry_name 
                FROM INDUSTRY 
                ORDER BY CAST(industry_code AS INTEGER)""", [])
            
        ### 家屋評価額: HOUSE_ASSET
        elif category_code2 == "100" or category_code2 == "2000":
            house_asset_list = HOUSE_ASSET.objects.raw("""
                SELECT 
                    HA1.house_asset_code AS house_asset_code, 
                    HA1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    CAST(HA1.house_asset AS NUMERIC(20,10)) AS house_asset 
                FROM HOUSE_ASSET HA1 
                LEFT JOIN KEN KE1 ON HA1.ken_code=KE1.ken_code 
                ORDER BY CAST(HA1.house_asset_code AS INTEGER)""", [])
            
        ### 家屋被害率: HOUSE_RATE
        elif category_code2 == "101" or category_code2 == "2010":
            house_rate_list = HOUSE_RATE.objects.raw("""
                SELECT 
                    HR1.house_rate_code AS house_rate_code, 
                    HR1.flood_sediment_code AS flood_sediment_code, 
                    FS1.flood_sediment_name AS flood_sediment_name, 
                    HR1.gradient_code AS gradient_code, 
                    GR1.gradient_name AS gradient_name, 
                    CAST(HR1.house_rate_lv00 AS NUMERIC(20,10)) AS house_rate_lv00, 
                    CAST(HR1.house_rate_lv00_50 AS NUMERIC(20,10)) AS house_rate_lv00_50, 
                    CAST(HR1.house_rate_lv50_100 AS NUMERIC(20,10)) AS house_rate_lv50_100, 
                    CAST(HR1.house_rate_lv100_200 AS NUMERIC(20,10)) AS house_rate_lv100_200, 
                    CAST(HR1.house_rate_lv200_300 AS NUMERIC(20,10)) AS house_rate_lv200_300, 
                    CAST(HR1.house_rate_lv300 AS NUMERIC(20,10)) AS house_rate_lv300 
                FROM HOUSE_RATE HR1 
                LEFT JOIN FLOOD_SEDIMENT FS1 ON HR1.flood_sediment_code=FS1.flood_sediment_code 
                LEFT JOIN GRADIENT GR1 ON HR1.gradient_code=GR1.gradient_code 
                ORDER BY CAST(HR1.house_rate_code AS INTEGER)""", [])
            
        ### 家庭応急対策費_代替活動費: HOUSE_ALT
        elif category_code2 == "102" or category_code2 == "2020":
            house_alt_list = HOUSE_ALT.objects.raw("""
                SELECT 
                    house_alt_code, 
                    CAST(house_alt_lv00 AS NUMERIC(20,10)) AS house_alt_lv00, 
                    CAST(house_alt_lv00_50 AS NUMERIC(20,10)) AS house_alt_lv00_50, 
                    CAST(house_alt_lv50_100 AS NUMERIC(20,10)) AS house_alt_lv50_100, 
                    CAST(house_alt_lv100_200 AS NUMERIC(20,10)) AS house_alt_lv100_200, 
                    CAST(house_alt_lv200_300 AS NUMERIC(20,10)) AS house_alt_lv200_300, 
                    CAST(house_alt_lv300 AS NUMERIC(20,10)) AS house_alt_lv300 
                FROM HOUSE_ALT 
                ORDER BY CAST(house_alt_code AS INTEGER)""", [])
            
        ### 家庭応急対策費_清掃日数_清掃労働単価: HOUSE_CLEAN
        elif category_code2 == "103" or category_code2 == "2030":
            house_clean_list = HOUSE_CLEAN.objects.raw("""
                SELECT 
                    house_clean_code, 
                    CAST(house_clean_days_lv00 AS NUMERIC(20,10)) AS house_clean_days_lv00, 
                    CAST(house_clean_days_lv00_50 AS NUMERIC(20,10)) AS house_clean_days_lv00_50, 
                    CAST(house_clean_days_lv50_100 AS NUMERIC(20,10)) AS house_clean_days_lv50_100, 
                    CAST(house_clean_days_lv100_200 AS NUMERIC(20,10)) AS house_clean_days_lv100_200, 
                    CAST(house_clean_days_lv200_300 AS NUMERIC(20,10)) AS house_clean_days_lv200_300, 
                    CAST(house_clean_days_lv300 AS NUMERIC(20,10)) AS house_clean_days_lv300, 
                    CAST(house_clean_unit_cost  AS NUMERIC(20,10)) AS house_clean_unit_cost
                FROM HOUSE_CLEAN 
                ORDER BY CAST(house_clean_code AS INTEGER)""", [])
            
        ### 家庭用品自動車以外所有額: HOUSEHOLD_ASSET
        elif category_code2 == "104" or category_code2 == "3000":
            household_asset_list = HOUSEHOLD_ASSET.objects.raw("""
                SELECT 
                    household_asset_code, 
                    CAST(household_asset AS NUMERIC(20,10)) AS household_asset  
                FROM HOUSEHOLD_ASSET 
                ORDER BY CAST(household_asset_code AS INTEGER)""", [])
            
        ### 家庭用品自動車以外被害率: HOUSEHOLD_RATE
        elif category_code2 == "105" or category_code2 == "3010":
            household_rate_list = HOUSEHOLD_RATE.objects.raw("""
                SELECT 
                    HR1.household_rate_code AS household_rate_code, 
                    HR1.flood_sediment_code AS flood_sediment_code, 
                    FS1.flood_sediment_name AS flood_sediment_name, 
                    CAST(HR1.household_rate_lv00 AS NUMERIC(20,10)) AS household_rate_lv00, 
                    CAST(HR1.household_rate_lv00_50 AS NUMERIC(20,10)) AS household_rate_lv00_50, 
                    CAST(HR1.household_rate_lv50_100 AS NUMERIC(20,10)) AS household_rate_lv50_100, 
                    CAST(HR1.household_rate_lv100_200 AS NUMERIC(20,10)) AS household_rate_lv100_200, 
                    CAST(HR1.household_rate_lv200_300 AS NUMERIC(20,10)) AS household_rate_lv200_300, 
                    CAST(HR1.household_rate_lv300 AS NUMERIC(20,10)) AS household_rate_lv300 
                FROM HOUSEHOLD_RATE HR1 
                LEFT JOIN FLOOD_SEDIMENT FS1 ON HR1.flood_sediment_code=FS1.flood_sediment_code 
                ORDER BY CAST(HR1.household_rate_code AS INTEGER)""", [])
            
        ### 家庭用品自動車所有額: CAR_ASSET
        elif category_code2 == "106" or category_code2 == "4000":
            car_asset_list = CAR_ASSET.objects.raw("""
                SELECT 
                    car_asset_code, 
                    CAST(car_asset AS NUMERIC(20,10)) AS car_asset 
                FROM CAR_ASSET 
                ORDER BY CAST(car_asset_code AS INTEGER)""", [])
            
        ### 家庭用品自動車被害率: CAR_RATE
        elif category_code2 == "107" or category_code2 == "4010":
            car_rate_list = CAR_RATE.objects.raw("""
                SELECT 
                    car_rate_code, 
                    CAST(car_rate_lv00 AS NUMERIC(20,10)) AS car_rate_lv00, 
                    CAST(car_rate_lv00_50 AS NUMERIC(20,10)) AS car_rate_lv00_50, 
                    CAST(car_rate_lv50_100 AS NUMERIC(20,10)) AS car_rate_lv50_100, 
                    CAST(car_rate_lv100_200 AS NUMERIC(20,10)) AS car_rate_lv100_200, 
                    CAST(car_rate_lv200_300 AS NUMERIC(20,10)) AS car_rate_lv200_300, 
                    CAST(car_rate_lv300 AS NUMERIC(20,10)) AS car_rate_lv300 
                FROM CAR_RATE 
                ORDER BY CAST(car_rate_code AS INTEGER)""", [])
            
        ### 事業所資産額: OFFICE_ASSET
        elif category_code2 == "108" or category_code2 == "5000":
            office_asset_list = OFFICE_ASSET.objects.raw("""
                SELECT 
                    OA1.office_asset_code AS office_asset_code, 
                    OA1.industry_code AS industry_code, 
                    ID1.industry_name AS industry_name, 
                    CAST(OA1.office_dep_asset AS NUMERIC(20,10)) AS office_dep_asset, 
                    CAST(OA1.office_inv_asset AS NUMERIC(20,10)) AS office_inv_asset, 
                    CAST(OA1.office_va_asset AS NUMERIC(20,10)) AS office_va_asset 
                FROM OFFICE_ASSET OA1 
                LEFT JOIN INDUSTRY ID1 ON OA1.industry_code=ID1.industry_code 
                ORDER BY CAST(OA1.office_asset_code AS INTEGER)""", [])

        ### 事業所被害率: OFFICE_RATE
        elif category_code2 == "109" or category_code2 == "5010":
            office_rate_list = OFFICE_RATE.objects.raw("""
                SELECT 
                    OR1.office_rate_code AS office_rate_code, 
                    OR1.flood_sediment_code AS flood_sediment_code, 
                    FS1.flood_sediment_name AS flood_sediment_name, 
                    CAST(OR1.office_dep_rate_lv00 AS NUMERIC(20,10)) AS office_dep_rate_lv00, 
                    CAST(OR1.office_dep_rate_lv00_50 AS NUMERIC(20,10)) AS office_dep_rate_lv00_50, 
                    CAST(OR1.office_dep_rate_lv50_100 AS NUMERIC(20,10)) AS office_dep_rate_lv50_100, 
                    CAST(OR1.office_dep_rate_lv100_200 AS NUMERIC(20,10)) AS office_dep_rate_lv100_200, 
                    CAST(OR1.office_dep_rate_lv200_300 AS NUMERIC(20,10)) AS office_dep_rate_lv200_300, 
                    CAST(OR1.office_dep_rate_lv300 AS NUMERIC(20,10)) AS office_dep_rate_lv300, 
                    CAST(OR1.office_inv_rate_lv00 AS NUMERIC(20,10)) AS office_inv_rate_lv00, 
                    CAST(OR1.office_inv_rate_lv00_50 AS NUMERIC(20,10)) AS office_inv_rate_lv00_50, 
                    CAST(OR1.office_inv_rate_lv50_100 AS NUMERIC(20,10)) AS office_inv_rate_lv50_100, 
                    CAST(OR1.office_inv_rate_lv100_200 AS NUMERIC(20,10)) AS office_inv_rate_lv100_200, 
                    CAST(OR1.office_inv_rate_lv200_300 AS NUMERIC(20,10)) AS office_inv_rate_lv200_300, 
                    CAST(OR1.office_inv_rate_lv300 AS NUMERIC(20,10)) AS office_inv_rate_lv300 
                FROM OFFICE_RATE OR1 
                LEFT JOIN FLOOD_SEDIMENT FS1 ON OR1.flood_sediment_code=FS1.flood_sediment_code 
                ORDER BY CAST(OR1.office_rate_code AS INTEGER)""", [])

        ### 事業所営業停止日数: OFFICE_SUSPEND
        elif category_code2 == "110" or category_code2 == "5020":
            office_suspend_list = OFFICE_SUSPEND.objects.raw("""
                SELECT 
                    office_sus_code, 
                    CAST(office_sus_days_lv00 AS NUMERIC(20,10)) AS office_sus_days_lv00, 
                    CAST(office_sus_days_lv00_50 AS NUMERIC(20,10)) AS office_sus_days_lv00_50, 
                    CAST(office_sus_days_lv50_100 AS NUMERIC(20,10)) AS office_sus_days_lv50_100, 
                    CAST(office_sus_days_lv100_200 AS NUMERIC(20,10)) AS office_sus_days_lv100_200, 
                    CAST(office_sus_days_lv200_300 AS NUMERIC(20,10)) AS office_sus_days_lv200_300, 
                    CAST(office_sus_days_lv300 AS NUMERIC(20,10)) AS office_sus_days_lv300 
                FROM OFFICE_SUSPEND 
                ORDER BY CAST(office_sus_code AS INTEGER)""", [])
            
        ### 事業所営業停滞日数: OFFICE_STAGNATE
        elif category_code2 == "111" or category_code2 == "5030":
            office_stagnate_list = OFFICE_STAGNATE.objects.raw("""
                SELECT 
                    office_stg_code, 
                    CAST(office_stg_days_lv00 AS NUMERIC(20,10)) AS office_stg_days_lv00, 
                    CAST(office_stg_days_lv00_50 AS NUMERIC(20,10)) AS office_stg_days_lv00_50, 
                    CAST(office_stg_days_lv50_100 AS NUMERIC(20,10)) AS office_stg_days_lv50_100, 
                    CAST(office_stg_days_lv100_200 AS NUMERIC(20,10)) AS office_stg_days_lv100_200, 
                    CAST(office_stg_days_lv200_300 AS NUMERIC(20,10)) AS office_stg_days_lv200_300, 
                    CAST(office_stg_days_lv300 AS NUMERIC(20,10)) AS office_stg_days_lv300 
                FROM OFFICE_STAGNATE 
                ORDER BY CAST(office_stg_code AS INTEGER)""", [])

        ### 事業所応急対策費_代替活動費: OFFICE_ALT
        elif category_code2 == "112" or category_code2 == "5040":
            office_alt_list = OFFICE_ALT.objects.raw("""
                SELECT 
                    office_alt_code, 
                    CAST(office_alt_lv00 AS NUMERIC(20,10)) AS office_alt_lv00, 
                    CAST(office_alt_lv00_50 AS NUMERIC(20,10)) AS office_alt_lv00_50, 
                    CAST(office_alt_lv50_100 AS NUMERIC(20,10)) AS office_alt_lv50_100, 
                    CAST(office_alt_lv100_200 AS NUMERIC(20,10)) AS office_alt_lv100_200, 
                    CAST(office_alt_lv200_300 AS NUMERIC(20,10)) AS office_alt_lv200_300, 
                    CAST(office_alt_lv300 AS NUMERIC(20,10)) AS office_alt_lv300 
                FROM OFFICE_ALT 
                ORDER BY CAST(office_alt_code AS INTEGER)""", [])
            
        ### 農漁家資産額: FARMER_FISHER_ASSET
        elif category_code2 == "113" or category_code2 == "6000":
            farmer_fisher_asset_list = FARMER_FISHER_ASSET.objects.raw("""
                SELECT 
                    farmer_fisher_asset_code, 
                    CAST(farmer_fisher_dep_asset AS NUMERIC(20,10)) AS farmer_fisher_dep_asset, 
                    CAST(farmer_fisher_inv_asset AS NUMERIC(20,10)) AS farmer_fisher_inv_asset 
                FROM FARMER_FISHER_ASSET 
                ORDER BY CAST(farmer_fisher_asset_code AS INTEGER)""", [])

        ### 農漁家被害率: FARMER_FISHER_RATE
        elif category_code2 == "114" or category_code2 == "6010":
            farmer_fisher_rate_list = FARMER_FISHER_RATE.objects.raw("""
                SELECT 
                    FFR1.farmer_fisher_rate_code AS farmer_fisher_rate_code, 
                    FFR1.flood_sediment_code AS flood_sediment_code, 
                    FS1.flood_sediment_name AS flood_sediment_name, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv00 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv00, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv00_50 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv00_50, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv50_100 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv50_100, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv100_200 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv100_200, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv200_300 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv200_300, 
                    CAST(FFR1.farmer_fisher_dep_rate_lv300 AS NUMERIC(20,10)) AS farmer_fisher_dep_rate_lv300, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv00 AS NUMERIC(20,10)) AS farmer_fisher_inv_rate_lv00, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv00_50 AS NUMERIC(20,10)) AS farmer_fisher_inv_rate_lv00_50, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv50_100 AS NUMERIC(20,10)) AS farmer_fisher_inv_rate_lv50_100, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv100_200 AS NUMERIC(20,10)) AS farmer_fisher_inv_rate_lv100_200, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv200_300 AS NUMERIC(20,10)) ASfarmer_fisher_inv_rate_lv200_300, 
                    CAST(FFR1.farmer_fisher_inv_rate_lv300 AS NUMERIC(20,10)) AS farmer_fisher_inv_rate_lv300 
                FROM FARMER_FISHER_RATE FFR1 
                LEFT JOIN FLOOD_SEDIMENT FS1 ON FFR1.flood_sediment_code=FS1.flood_sediment_code 
                ORDER BY CAST(FFR1.farmer_fisher_rate_code AS INTEGER)""", [])

        ### 水害区域: AREA
        elif category_code2 == "200" or category_code2 == "7000":
            area_list = AREA.objects.raw("""
                SELECT 
                    AR1.area_id AS area_id, 
                    AR1.area_name AS area_name, 
                    AR1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    TO_CHAR(timezone('JST', AR1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', AR1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    AR1.upload_file_path AS upload_file_path, 
                    AR1.upload_file_name AS upload_file_name, 
                    AR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    AR1.status_code AS status_code, 
                    ST1.status_name AS status_name 
                FROM AREA AR1 
                LEFT JOIN KEN KE1 ON AR1.ken_code=KE1.ken_code 
                LEFT JOIN ACTION AC1 ON AR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON AR1.status_code=ST1.status_code 
                WHERE deleted_at IS NULL 
                ORDER BY CAST(AR1.area_id AS INTEGER)""", [])
            
        ### 異常気象: WEATHER
        elif category_code2 == "201" or category_code2 == "7010":
            weather_list = WEATHER.objects.raw("""
                SELECT 
                    WE1.weather_id AS weather_id, 
                    WE1.weather_name AS weather_name, 
                    TO_CHAR(timezone('JST', WE1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                    TO_CHAR(timezone('JST', WE1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
                    WE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name 
                FROM WEATHER WE1 
                LEFT JOIN KEN KE1 ON WE1.ken_code=KE1.ken_code 
                ORDER BY CAST(WE1.weather_id AS INTEGER)""", [])
            
        ### ヘッダ部分: SUIGAI
        elif category_code2 == "202" or category_code2 == "7020":
            if ken_code == "0" and city_code == "0": 
                suigai_list = SUIGAI.objects.raw("""
                    SELECT 
                        SG1.suigai_id AS suigai_id, 
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
                        CAST(SG1.residential_area AS NUMERIC(20,10)) AS residential_area, 
                        CAST(SG1.agricultural_area AS NUMERIC(20,10)) AS agricultural_area, 
                        CAST(SG1.underground_area AS NUMERIC(20,10)) AS underground_area, 
                        SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                        KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                        CAST(SG1.crop_damage AS NUMERIC(20,10)) AS crop_damage, 
                        SG1.weather_id AS weather_id, 
                        WE1.weather_name AS weather_name, 
                        TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                        TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                        SG1.upload_file_path AS upload_file_path, 
                        SG1.upload_file_name AS upload_file_name, 
                        SG1.summary_file_path AS summary_file_path, 
                        SG1.summary_file_name AS summary_file_name, 
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
                    WHERE SG1.deleted_at IS NULL 
                    ORDER BY CAST(SG1.suigai_id AS INTEGER)""", [])
                
            elif ken_code == "0" and city_code != "0":
                suigai_list = SUIGAI.objects.raw("""
                    SELECT 
                        SG1.suigai_id AS suigai_id, 
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
                        CAST(SG1.residential_area AS NUMERIC(20,10)) AS residential_area, 
                        CAST(SG1.agricultural_area AS NUMERIC(20,10)) AS agricultural_area, 
                        CAST(SG1.underground_area AS NUMERIC(20,10)) AS underground_area, 
                        SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                        KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                        CAST(SG1.crop_damage AS NUMERIC(20,10)) AS crop_damage, 
                        SG1.weather_id AS weather_id, 
                        WE1.weather_name AS weather_name, 
                        TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                        TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                        SG1.upload_file_path AS upload_file_path, 
                        SG1.upload_file_name AS upload_file_name, 
                        SG1.summary_file_path AS summary_file_path, 
                        SG1.summary_file_name AS summary_file_name, 
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
                    WHERE SG1.city_code=%s AND SG1.deleted_at IS NULL 
                    ORDER BY CAST(SG1.suigai_id AS INTEGER)""", [city_code, ])
            
            elif ken_code != "0" and city_code == "0":
                suigai_list = SUIGAI.objects.raw("""
                    SELECT 
                        SG1.suigai_id AS suigai_id, 
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
                        CAST(SG1.residential_area AS NUMERIC(20,10)) AS residential_area, 
                        CAST(SG1.agricultural_area AS NUMERIC(20,10)) AS agricultural_area, 
                        CAST(SG1.underground_area AS NUMERIC(20,10)) AS underground_area, 
                        SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                        KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                        CAST(SG1.crop_damage AS NUMERIC(20,10)) AS crop_damage, 
                        SG1.weather_id AS weather_id, 
                        WE1.weather_name AS weather_name, 
                        TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                        TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                        SG1.upload_file_path AS upload_file_path, 
                        SG1.upload_file_name AS upload_file_name, 
                        SG1.summary_file_path AS summary_file_path, 
                        SG1.summary_file_name AS summary_file_name, 
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
                    WHERE SG1.ken_code=%s AND SG1.deleted_at IS NULL 
                    ORDER BY CAST(SG1.suigai_id AS INTEGER)""", [ken_code, ])
            
            elif ken_code != "0" and city_code != "0":
                suigai_list = SUIGAI.objects.raw("""
                    SELECT 
                        SG1.suigai_id AS suigai_id, 
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
                        CAST(SG1.residential_area AS NUMERIC(20,10)) AS residential_area, 
                        CAST(SG1.agricultural_area AS NUMERIC(20,10)) AS agricultural_area, 
                        CAST(SG1.underground_area AS NUMERIC(20,10)) AS underground_area, 
                        SG1.kasen_kaigan_code AS kasen_kaigan_code, 
                        KK1.kasen_kaigan_name AS kasen_kaigan_name, 
                        CAST(SG1.crop_damage AS NUMERIC(20,10)) AS crop_damage, 
                        SG1.weather_id AS weather_id, 
                        WE1.weather_name AS weather_name, 
                        TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                        TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                        SG1.upload_file_path AS upload_file_path, 
                        SG1.upload_file_name AS upload_file_name, 
                        SG1.summary_file_path AS summary_file_path, 
                        SG1.summary_file_name AS summary_file_name, 
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
                    WHERE SG1.ken_code=%s AND SG1.city_code=%s AND SG1.deleted_at is NULL 
                    ORDER BY CAST(SG1.suigai_id AS INTEGER)""", [ken_code, city_code, ])
            else:
                pass
            
        ### 一覧表部分: IPPAN
        elif category_code2 == "203" or category_code2 == "7030":
            ippan_list = IPPAN.objects.raw("""
                SELECT 
                    IP1.ippan_id AS ippan_id, 
                    IP1.ippan_name AS ippan_name, 
                    IP1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    IP1.building_code AS building_code, 
                    BD1.building_name AS building_name, 
                    IP1.underground_code AS underground_code, 
                    UD1.underground_name AS underground_name, 
                    IP1.flood_sediment_code AS flood_sediment_code, 
                    FS1.flood_sediment_name AS flood_sediment_name, 
                    CAST(IP1.building_lv00 AS NUMERIC(20,10)) AS building_lv00, 
                    CAST(IP1.building_lv01_49 AS NUMERIC(20,10)) AS building_lv01_49, 
                    CAST(IP1.building_lv50_99 AS NUMERIC(20,10)) AS building_lv50_99, 
                    CAST(IP1.building_lv100 AS NUMERIC(20,10)) AS building_lv100, 
                    CAST(IP1.building_half AS NUMERIC(20,10)) AS building_half, 
                    CAST(IP1.building_full AS NUMERIC(20,10)) AS building_full, 
                    CAST(IP1.floor_area AS NUMERIC(20,10)) AS floor_area, 
                    CAST(IP1.family AS NUMERIC(20,10)) AS family, 
                    CAST(IP1.office AS NUMERIC(20,10)) AS office, 
                    CAST(IP1.farmer_fisher_lv00 AS NUMERIC(20,10)) AS farmer_fisher_lv00, 
                    CAST(IP1.farmer_fisher_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_lv01_49, 
                    CAST(IP1.farmer_fisher_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_lv50_99, 
                    CAST(IP1.farmer_fisher_lv100 AS NUMERIC(20,10)) AS farmer_fisher_lv100, 
                    CAST(IP1.farmer_fisher_full AS NUMERIC(20,10)) AS farmer_fisher_full, 
                    CAST(IP1.employee_lv00 AS NUMERIC(20,10)) AS employee_lv00, 
                    CAST(IP1.employee_lv01_49 AS NUMERIC(20,10)) AS employee_lv01_49, 
                    CAST(IP1.employee_lv50_99 AS NUMERIC(20,10)) AS employee_lv50_99, 
                    CAST(IP1.employee_lv100 AS NUMERIC(20,10)) AS employee_lv100, 
                    CAST(IP1.employee_full AS NUMERIC(20,10)) AS employee_full, 
                    IP1.industry_code AS industry_code, 
                    ID1.industry_name AS industry_name, 
                    IP1.usage_code AS usage_code, 
                    US1.usage_name AS usage_name, 
                    IP1.comment AS comment, 
                    TO_CHAR(timezone('JST', IP1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', IP1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM IPPAN IP1 
                LEFT JOIN SUIGAI SG1 ON IP1.suigai_id=SG1.suigai_id 
                LEFT JOIN BUILDING BD1 ON IP1.building_code=BD1.building_code 
                LEFT JOIN UNDERGROUND UD1 ON IP1.underground_code=UD1.underground_code 
                LEFT JOIN FLOOD_SEDIMENT FS1 ON IP1.flood_sediment_code=FS1.flood_sediment_code 
                LEFT JOIN INDUSTRY ID1 ON IP1.industry_code=ID1.industry_code 
                LEFT JOIN USAGE US1 ON IP1.usage_code=US1.usage_code 
                WHERE IP1.deleted_at IS NULL 
                ORDER BY CAST(IP1.ippan_id AS INTEGER)""", [])

        ### 一覧表部分_按分データ: IPPAN_VIEW
        elif category_code2 == "204" or category_code2 == "7040":
            ippan_view_list = IPPAN_VIEW.objects.raw(""" 
                SELECT 
                    ippan_id AS ippan_id, 
                    ippan_name AS ippan_name, 
                    suigai_id AS suigai_id, 
                    suigai_name AS suigai_name, 
                    building_code AS building_code, 
                    building_name AS building_name, 
                    underground_code AS underground_code, 
                    underground_name AS underground_name, 
                    flood_sediment_code AS flood_sediment_code, 
                    flood_sediment_name AS flood_sediment_name, 
                    CAST(building_lv00 AS NUMERIC(20,10)) AS building_lv00, 
                    CAST(building_lv01_49 AS NUMERIC(20,10)) AS building_lv01_49, 
                    CAST(building_lv50_99 AS NUMERIC(20,10)) AS building_lv50_99, 
                    CAST(building_lv100 AS NUMERIC(20,10)) AS building_lv100, 
                    CAST(building_half AS NUMERIC(20,10)) AS building_half, 
                    CAST(building_full AS NUMERIC(20,10)) AS building_full, 
                    CAST(building_total AS NUMERIC(20,10)) AS building_total, 
                    CAST(floor_area AS NUMERIC(20,10)) AS floor_area, 
                    CAST(family AS NUMERIC(20,10)) AS family, 
                    CAST(office AS NUMERIC(20,10)) AS office, 
                    CAST(floor_area_lv00 AS NUMERIC(20,10)) AS floor_area_lv00, 
                    CAST(floor_area_lv01_49 AS NUMERIC(20,10)) AS floor_area_lv01_49, 
                    CAST(floor_area_lv50_99 AS NUMERIC(20,10)) AS floor_area_lv50_99, 
                    CAST(floor_area_lv100 AS NUMERIC(20,10)) AS floor_area_lv100, 
                    CAST(floor_area_half AS NUMERIC(20,10)) AS floor_area_half, 
                    CAST(floor_area_full AS NUMERIC(20,10)) AS floor_area_full, 
                    CAST(floor_area_total AS NUMERIC(20,10)) AS floor_area_total, 
                    CAST(family_lv00 AS NUMERIC(20,10)) AS family_lv00, 
                    CAST(family_lv01_49 AS NUMERIC(20,10)) AS family_lv01_49, 
                    CAST(family_lv50_99 AS NUMERIC(20,10)) AS family_lv50_99, 
                    CAST(family_lv100 AS NUMERIC(20,10)) AS family_lv100, 
                    CAST(family_half AS NUMERIC(20,10)) AS family_half, 
                    CAST(family_full AS NUMERIC(20,10)) AS family_full, 
                    CAST(family_total AS NUMERIC(20,10)) AS family_total, 
                    CAST(office_lv00 AS NUMERIC(20,10)) AS office_lv00, 
                    CAST(office_lv01_49 AS NUMERIC(20,10)) AS office_lv01_49, 
                    CAST(office_lv50_99 AS NUMERIC(20,10)) AS office_lv50_99, 
                    CAST(office_lv100 AS NUMERIC(20,10)) AS office_lv100, 
                    CAST(office_half AS NUMERIC(20,10)) AS office_half, 
                    CAST(office_full AS NUMERIC(20,10)) AS office_full, 
                    CAST(office_total AS NUMERIC(20,10)) AS office_total, 
                    CAST(farmer_fisher_lv00 AS NUMERIC(20,10)) AS farmer_fisher_lv00, 
                    CAST(farmer_fisher_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_lv01_49, 
                    CAST(farmer_fisher_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_lv50_99, 
                    CAST(farmer_fisher_lv100 AS NUMERIC(20,10)) AS farmer_fisher_lv100, 
                    CAST(farmer_fisher_full AS NUMERIC(20,10)) AS farmer_fisher_full, 
                    CAST(farmer_fisher_total AS NUMERIC(20,10)) AS farmer_fisher_total, 
                    CAST(employee_lv00 AS NUMERIC(20,10)) AS employee_lv00, 
                    CAST(employee_lv01_49 AS NUMERIC(20,10)) AS employee_lv01_49, 
                    CAST(employee_lv50_99 AS NUMERIC(20,10)) AS employee_lv50_99, 
                    CAST(employee_lv100 AS NUMERIC(20,10)) AS employee_lv100, 
                    CAST(employee_full AS NUMERIC(20,10)) AS employee_full, 
                    CAST(employee_total AS NUMERIC(20,10)) AS employee_total, 
                    industry_code AS industry_code, 
                    industry_name AS industry_name, 
                    usage_code AS usage_code, 
                    usage_name AS usage_name, 
                    comment, 
                    TO_CHAR(timezone('JST', committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS commited_at, 
                    TO_CHAR(timezone('JST', deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at  
                FROM IPPAN_VIEW 
                WHERE deleted_at IS NULL 
                ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])

        ### 集計データ: IPPAN_SUMMARY
        elif category_code2 == "300" or category_code2 == "8000":
            ippan_summary_list = IPPAN_SUMMARY.objects.raw("""
                SELECT 
                    IS1.id AS id, 
                    IS1.ippan_id AS ippan_id, 
                    IP1.ippan_name AS ippan_name, 
                    IS1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    
                    CAST(IS1.house_summary_lv00 AS NUMERIC(20,10)) AS house_summary_lv00, 
                    CAST(IS1.house_summary_lv01_49 AS NUMERIC(20,10)) AS house_summary_lv01_49, 
                    CAST(IS1.house_summary_lv50_99 AS NUMERIC(20,10)) AS house_summary_lv50_99, 
                    CAST(IS1.house_summary_lv100 AS NUMERIC(20,10)) AS house_summary_lv100, 
                    CAST(IS1.house_summary_half AS NUMERIC(20,10)) AS house_summary_half, 
                    CAST(IS1.house_summary_full AS NUMERIC(20,10)) AS house_summary_full, 
                    
                    CAST(IS1.household_summary_lv00 AS NUMERIC(20,10)) AS household_summary_lv00, 
                    CAST(IS1.household_summary_lv01_49 AS NUMERIC(20,10)) AS household_summary_lv01_49, 
                    CAST(IS1.household_summary_lv50_99 AS NUMERIC(20,10)) AS household_summary_lv50_99, 
                    CAST(IS1.household_summary_lv100 AS NUMERIC(20,10)) AS household_summary_lv100, 
                    CAST(IS1.household_summary_half AS NUMERIC(20,10)) AS household_summary_half, 
                    CAST(IS1.household_summary_full AS NUMERIC(20,10)) AS household_summary_full, 
                    
                    CAST(IS1.car_summary_lv00 AS NUMERIC(20,10)) AS car_summary_lv00, 
                    CAST(IS1.car_summary_lv01_49 AS NUMERIC(20,10)) AS car_summary_lv01_49, 
                    CAST(IS1.car_summary_lv50_99 AS NUMERIC(20,10)) AS car_summary_lv50_99, 
                    CAST(IS1.car_summary_lv100 AS NUMERIC(20,10)) AS car_summary_lv100, 
                    CAST(IS1.car_summary_half AS NUMERIC(20,10)) AS car_summary_half, 
                    CAST(IS1.car_summary_full AS NUMERIC(20,10)) AS car_summary_full, 
                    
                    CAST(IS1.house_alt_summary_lv00 AS NUMERIC(20,10)) AS house_alt_summary_lv00, 
                    CAST(IS1.house_alt_summary_lv01_49 AS NUMERIC(20,10)) AS house_alt_summary_lv01_49, 
                    CAST(IS1.house_alt_summary_lv50_99 AS NUMERIC(20,10)) AS house_alt_summary_lv50_99, 
                    CAST(IS1.house_alt_summary_lv100 AS NUMERIC(20,10)) AS house_alt_summary_lv100, 
                    CAST(IS1.house_alt_summary_half AS NUMERIC(20,10)) AS house_alt_summary_half, 
                    CAST(IS1.house_alt_summary_full AS NUMERIC(20,10)) AS house_alt_summary_full, 
                    
                    CAST(IS1.house_clean_summary_lv00 AS NUMERIC(20,10)) AS house_clean_summary_lv00, 
                    CAST(IS1.house_clean_summary_lv01_49 AS NUMERIC(20,10)) AS house_clean_summary_lv01_49, 
                    CAST(IS1.house_clean_summary_lv50_99 AS NUMERIC(20,10)) AS house_clean_summary_lv50_99, 
                    CAST(IS1.house_clean_summary_lv100 AS NUMERIC(20,10)) AS house_clean_summary_lv100, 
                    CAST(IS1.house_clean_summary_half AS NUMERIC(20,10)) AS house_clean_summary_half, 
                    CAST(IS1.house_clean_summary_full AS NUMERIC(20,10)) AS house_clean_summary_full, 
                    
                    CAST(IS1.office_dep_summary_lv00 AS NUMERIC(20,10)) AS office_dep_summary_lv00, 
                    CAST(IS1.office_dep_summary_lv01_49 AS NUMERIC(20,10)) AS office_dep_summary_lv01_49, 
                    CAST(IS1.office_dep_summary_lv50_99 AS NUMERIC(20,10)) AS office_dep_summary_lv50_99, 
                    CAST(IS1.office_dep_summary_lv100 AS NUMERIC(20,10)) AS office_dep_summary_lv100, 
                    CAST(IS1.office_dep_summary_full AS NUMERIC(20,10)) AS office_dep_summary_full, 
                    
                    CAST(IS1.office_inv_summary_lv00 AS NUMERIC(20,10)) AS office_inv_summary_lv00, 
                    CAST(IS1.office_inv_summary_lv01_49 AS NUMERIC(20,10)) AS office_inv_summary_lv01_49, 
                    CAST(IS1.office_inv_summary_lv50_99 AS NUMERIC(20,10)) AS office_inv_summary_lv50_99, 
                    CAST(IS1.office_inv_summary_lv100 AS NUMERIC(20,10)) AS office_inv_summary_lv100, 
                    CAST(IS1.office_inv_summary_full AS NUMERIC(20,10)) AS office_inv_summary_full, 
                    
                    CAST(IS1.office_sus_summary_lv00 AS NUMERIC(20,10)) AS office_sus_summary_lv00, 
                    CAST(IS1.office_sus_summary_lv01_49 AS NUMERIC(20,10)) AS office_sus_summary_lv01_49, 
                    CAST(IS1.office_sus_summary_lv50_99 AS NUMERIC(20,10)) AS office_sus_summary_lv50_99, 
                    CAST(IS1.office_sus_summary_lv100 AS NUMERIC(20,10)) AS office_sus_summary_lv100, 
                    CAST(IS1.office_sus_summary_full AS NUMERIC(20,10)) AS office_sus_summary_full, 
                    
                    CAST(IS1.office_stg_summary_lv00 AS NUMERIC(20,10)) AS office_stg_summary_lv00, 
                    CAST(IS1.office_stg_summary_lv01_49 AS NUMERIC(20,10)) AS office_stg_summary_lv01_49, 
                    CAST(IS1.office_stg_summary_lv50_99 AS NUMERIC(20,10)) AS office_stg_summary_lv50_99, 
                    CAST(IS1.office_stg_summary_lv100 AS NUMERIC(20,10)) AS office_stg_summary_lv100, 
                    CAST(IS1.office_stg_summary_full AS NUMERIC(20,10)) AS office_stg_summary_full, 
                    
                    CAST(IS1.farmer_fisher_dep_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv00, 
                    CAST(IS1.farmer_fisher_dep_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv01_49, 
                    CAST(IS1.farmer_fisher_dep_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv50_99, 
                    CAST(IS1.farmer_fisher_dep_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv100, 
                    CAST(IS1.farmer_fisher_dep_summary_full AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_full, 
                    
                    CAST(IS1.farmer_fisher_inv_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv00, 
                    CAST(IS1.farmer_fisher_inv_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv01_49, 
                    CAST(IS1.farmer_fisher_inv_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv50_99, 
                    CAST(IS1.farmer_fisher_inv_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv100, 
                    CAST(IS1.farmer_fisher_inv_summary_full AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_full, 
                    
                    CAST(IS1.office_alt_summary_lv00 AS NUMERIC(20,10)) AS office_alt_summary_lv00, 
                    CAST(IS1.office_alt_summary_lv01_49 AS NUMERIC(20,10)) AS office_alt_summary_lv01_49, 
                    CAST(IS1.office_alt_summary_lv50_99 AS NUMERIC(20,10)) AS office_alt_summary_lv50_99, 
                    CAST(IS1.office_alt_summary_lv100 AS NUMERIC(20,10)) AS office_alt_summary_lv100, 
                    CAST(IS1.office_alt_summary_half AS NUMERIC(20,10)) AS office_alt_summary_half, 
                    CAST(IS1.office_alt_summary_full AS NUMERIC(20,10)) AS office_alt_summary_full 
                    
                FROM IPPAN_SUMMARY IS1 
                LEFT JOIN IPPAN IP1 ON IS1.ippan_id=IP1.ippan_id 
                LEFT JOIN SUIGAI SG1 ON IS1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                WHERE IS1.deleted_at IS NULL 
                ORDER BY CAST(IS1.IPPAN_ID AS INTEGER)""", [])

        ### 集計データ_都道府県別: IPPAN_GROUP_BY_KEN
        elif category_code2 == "301" or category_code2 == "8010":
            ### print_log('[INFO] SELECT * FROM IPPAN_SUMMARY GROUP BY () ORDER BY CAST(AS INTEGER)', 'INFO')
            ### ippan_group_by_ken_list = IPPAN_SUMMARY.objects.raw("""
            ###     SELECT 
            ###         1 AS id, 
            ###         SUM(floor_area) AS floor_area 
            ###     FROM IPPAN 
            ###     GROUP BY ippan_id 
            ### """, [])

            ### GROUP BY に使用する都道府県コードをIPPAN_SUMMARYモデルのidに使用する。
            ### IPPAN_SUMMARYモデルのidを指定しないと、<class 'django.core.exceptions.FieldDoesNotExist'>のエラーとなるため。
            ### SQLは実行できるが、IPPAN_SUMMARYモデルに正しくセットできないため。
            ### 都道府県コードをPKとする別のモデルを定義しても良さそうだが、未検証。
            ippan_group_by_ken_list = IPPAN_SUMMARY.objects.raw("""
                SELECT 
                    SUB1.id AS id, 
                    SUB1.id AS ken_code, 
                    KE1.ken_name AS ken_name, 

                    CAST(SUB1.house_summary_lv00 AS NUMERIC(20,10)) AS house_summary_lv00, 
                    CAST(SUB1.house_summary_lv01_49 AS NUMERIC(20,10)) AS house_summary_lv01_49, 
                    CAST(SUB1.house_summary_lv50_99 AS NUMERIC(20,10)) AS house_summary_lv50_99, 
                    CAST(SUB1.house_summary_lv100 AS NUMERIC(20,10)) AS house_summary_lv100, 
                    CAST(SUB1.house_summary_half AS NUMERIC(20,10)) AS house_summary_half, 
                    CAST(SUB1.house_summary_full AS NUMERIC(20,10)) AS house_summary_full, 

                    CAST(SUB1.household_summary_lv00 AS NUMERIC(20,10)) AS household_summary_lv00, 
                    CAST(SUB1.household_summary_lv01_49 AS NUMERIC(20,10)) AS household_summary_lv01_49, 
                    CAST(SUB1.household_summary_lv50_99 AS NUMERIC(20,10)) AS household_summary_lv50_99, 
                    CAST(SUB1.household_summary_lv100 AS NUMERIC(20,10)) AS household_summary_lv100, 
                    CAST(SUB1.household_summary_half AS NUMERIC(20,10)) AS household_summary_half, 
                    CAST(SUB1.household_summary_full AS NUMERIC(20,10)) AS household_summary_full, 

                    CAST(SUB1.car_summary_lv00 AS NUMERIC(20,10)) AS car_summary_lv00, 
                    CAST(SUB1.car_summary_lv01_49 AS NUMERIC(20,10)) AS car_summary_lv01_49, 
                    CAST(SUB1.car_summary_lv50_99 AS NUMERIC(20,10)) AS car_summary_lv50_99, 
                    CAST(SUB1.car_summary_lv100 AS NUMERIC(20,10)) AS car_summary_lv100, 
                    CAST(SUB1.car_summary_half AS NUMERIC(20,10)) AS car_summary_half, 
                    CAST(SUB1.car_summary_full AS NUMERIC(20,10)) AS car_summary_full, 

                    CAST(SUB1.house_alt_summary_lv00 AS NUMERIC(20,10)) AS house_alt_summary_lv00, 
                    CAST(SUB1.house_alt_summary_lv01_49 AS NUMERIC(20,10)) AS house_alt_summary_lv01_49, 
                    CAST(SUB1.house_alt_summary_lv50_99 AS NUMERIC(20,10)) AS house_alt_summary_lv50_99, 
                    CAST(SUB1.house_alt_summary_lv100 AS NUMERIC(20,10)) AS house_alt_summary_lv100, 
                    CAST(SUB1.house_alt_summary_half AS NUMERIC(20,10)) AS house_alt_summary_half, 
                    CAST(SUB1.house_alt_summary_full AS NUMERIC(20,10)) AS house_alt_summary_full, 

                    CAST(SUB1.house_clean_summary_lv00 AS NUMERIC(20,10)) AS house_clean_summary_lv00, 
                    CAST(SUB1.house_clean_summary_lv01_49 AS NUMERIC(20,10)) AS house_clean_summary_lv01_49, 
                    CAST(SUB1.house_clean_summary_lv50_99 AS NUMERIC(20,10)) AS house_clean_summary_lv50_99, 
                    CAST(SUB1.house_clean_summary_lv100 AS NUMERIC(20,10)) AS house_clean_summary_lv100, 
                    CAST(SUB1.house_clean_summary_half AS NUMERIC(20,10)) AS house_clean_summary_half, 
                    CAST(SUB1.house_clean_summary_full AS NUMERIC(20,10)) AS house_clean_summary_full, 

                    CAST(SUB1.office_dep_summary_lv00 AS NUMERIC(20,10)) AS office_dep_summary_lv00, 
                    CAST(SUB1.office_dep_summary_lv01_49 AS NUMERIC(20,10)) AS office_dep_summary_lv01_49, 
                    CAST(SUB1.office_dep_summary_lv50_99 AS NUMERIC(20,10)) AS office_dep_summary_lv50_99, 
                    CAST(SUB1.office_dep_summary_lv100 AS NUMERIC(20,10)) AS office_dep_summary_lv100, 
                    CAST(SUB1.office_dep_summary_full AS NUMERIC(20,10)) AS office_dep_summary_full, 

                    CAST(SUB1.office_inv_summary_lv00 AS NUMERIC(20,10)) AS office_inv_summary_lv00, 
                    CAST(SUB1.office_inv_summary_lv01_49 AS NUMERIC(20,10)) AS office_inv_summary_lv01_49, 
                    CAST(SUB1.office_inv_summary_lv50_99 AS NUMERIC(20,10)) AS office_inv_summary_lv50_99, 
                    CAST(SUB1.office_inv_summary_lv100 AS NUMERIC(20,10)) AS office_inv_summary_lv100, 
                    CAST(SUB1.office_inv_summary_full AS NUMERIC(20,10)) AS office_inv_summary_full, 

                    CAST(SUB1.office_sus_summary_lv00 AS NUMERIC(20,10)) AS office_sus_summary_lv00, 
                    CAST(SUB1.office_sus_summary_lv01_49 AS NUMERIC(20,10)) AS office_sus_summary_lv01_49,  
                    CAST(SUB1.office_sus_summary_lv50_99 AS NUMERIC(20,10)) AS office_sus_summary_lv50_99, 
                    CAST(SUB1.office_sus_summary_lv100 AS NUMERIC(20,10)) AS office_sus_summary_lv100, 
                    CAST(SUB1.office_sus_summary_full AS NUMERIC(20,10)) AS office_sus_summary_full, 

                    CAST(SUB1.office_stg_summary_lv00 AS NUMERIC(20,10)) AS office_stg_summary_lv00, 
                    CAST(SUB1.office_stg_summary_lv01_49 AS NUMERIC(20,10)) AS office_stg_summary_lv01_49, 
                    CAST(SUB1.office_stg_summary_lv50_99 AS NUMERIC(20,10)) AS office_stg_summary_lv50_99, 
                    CAST(SUB1.office_stg_summary_lv100 AS NUMERIC(20,10)) AS office_stg_summary_lv100, 
                    CAST(SUB1.office_stg_summary_full AS NUMERIC(20,10)) AS office_stg_summary_full, 

                    CAST(SUB1.farmer_fisher_dep_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv00, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv01_49, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv50_99, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv100, 
                    CAST(SUB1.farmer_fisher_dep_summary_full AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_full, 

                    CAST(SUB1.farmer_fisher_inv_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv00, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv01_49, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv50_99, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv100, 
                    CAST(SUB1.farmer_fisher_inv_summary_full AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_full, 

                    CAST(SUB1.office_alt_summary_lv00 AS NUMERIC(20,10)) AS office_alt_summary_lv00, 
                    CAST(SUB1.office_alt_summary_lv01_49 AS NUMERIC(20,10)) AS office_alt_summary_lv01_49, 
                    CAST(SUB1.office_alt_summary_lv50_99 AS NUMERIC(20,10)) AS office_alt_summary_lv50_99, 
                    CAST(SUB1.office_alt_summary_lv100 AS NUMERIC(20,10)) AS office_alt_summary_lv100, 
                    CAST(SUB1.office_alt_summary_half AS NUMERIC(20,10)) AS office_alt_summary_half, 
                    CAST(SUB1.office_alt_summary_full AS NUMERIC(20,10)) AS office_alt_summary_full 
                FROM (
                SELECT 
                    SG1.ken_code AS id, 
                    SUM(IS1.house_summary_lv00) AS house_summary_lv00, 
                    SUM(IS1.house_summary_lv01_49) AS house_summary_lv01_49, 
                    SUM(IS1.house_summary_lv50_99) AS house_summary_lv50_99, 
                    SUM(IS1.house_summary_lv100) AS house_summary_lv100, 
                    SUM(IS1.house_summary_half) AS house_summary_half, 
                    SUM(IS1.house_summary_full) AS house_summary_full, 

                    SUM(IS1.household_summary_lv00) AS household_summary_lv00, 
                    SUM(IS1.household_summary_lv01_49) AS household_summary_lv01_49, 
                    SUM(IS1.household_summary_lv50_99) AS household_summary_lv50_99, 
                    SUM(IS1.household_summary_lv100) AS household_summary_lv100, 
                    SUM(IS1.household_summary_half) AS household_summary_half, 
                    SUM(IS1.household_summary_full) AS household_summary_full, 

                    SUM(IS1.car_summary_lv00) AS car_summary_lv00, 
                    SUM(IS1.car_summary_lv01_49) AS car_summary_lv01_49, 
                    SUM(IS1.car_summary_lv50_99) AS car_summary_lv50_99, 
                    SUM(IS1.car_summary_lv100) AS car_summary_lv100, 
                    SUM(IS1.car_summary_half) AS car_summary_half, 
                    SUM(IS1.car_summary_full) AS car_summary_full, 

                    SUM(IS1.house_alt_summary_lv00) AS house_alt_summary_lv00, 
                    SUM(IS1.house_alt_summary_lv01_49) AS house_alt_summary_lv01_49, 
                    SUM(IS1.house_alt_summary_lv50_99) AS house_alt_summary_lv50_99, 
                    SUM(IS1.house_alt_summary_lv100) AS house_alt_summary_lv100, 
                    SUM(IS1.house_alt_summary_half) AS house_alt_summary_half, 
                    SUM(IS1.house_alt_summary_full) AS house_alt_summary_full, 

                    SUM(IS1.house_clean_summary_lv00) AS house_clean_summary_lv00, 
                    SUM(IS1.house_clean_summary_lv01_49) AS house_clean_summary_lv01_49, 
                    SUM(IS1.house_clean_summary_lv50_99) AS house_clean_summary_lv50_99, 
                    SUM(IS1.house_clean_summary_lv100) AS house_clean_summary_lv100, 
                    SUM(IS1.house_clean_summary_half) AS house_clean_summary_half, 
                    SUM(IS1.house_clean_summary_full) AS house_clean_summary_full, 

                    SUM(IS1.office_dep_summary_lv00) AS office_dep_summary_lv00, 
                    SUM(IS1.office_dep_summary_lv01_49) AS office_dep_summary_lv01_49, 
                    SUM(IS1.office_dep_summary_lv50_99) AS office_dep_summary_lv50_99, 
                    SUM(IS1.office_dep_summary_lv100) AS office_dep_summary_lv100, 
                    -- SUM(IS1.office_dep_summary_half) AS office_dep_summary_half, 
                    SUM(IS1.office_dep_summary_full) AS office_dep_summary_full, 

                    SUM(IS1.office_inv_summary_lv00) AS office_inv_summary_lv00, 
                    SUM(IS1.office_inv_summary_lv01_49) AS office_inv_summary_lv01_49, 
                    SUM(IS1.office_inv_summary_lv50_99) AS office_inv_summary_lv50_99, 
                    SUM(IS1.office_inv_summary_lv100) AS office_inv_summary_lv100, 
                    -- SUM(IS1.office_inv_summary_half) AS office_inv_summary_half, 
                    SUM(IS1.office_inv_summary_full) AS office_inv_summary_full, 

                    SUM(IS1.office_sus_summary_lv00) AS office_sus_summary_lv00, 
                    SUM(IS1.office_sus_summary_lv01_49) AS office_sus_summary_lv01_49, 
                    SUM(IS1.office_sus_summary_lv50_99) AS office_sus_summary_lv50_99, 
                    SUM(IS1.office_sus_summary_lv100) AS office_sus_summary_lv100, 
                    -- SUM(IS1.office_sus_summary_half) AS office_sus_summary_half, 
                    SUM(IS1.office_sus_summary_full) AS office_sus_summary_full, 

                    SUM(IS1.office_stg_summary_lv00) AS office_stg_summary_lv00, 
                    SUM(IS1.office_stg_summary_lv01_49) AS office_stg_summary_lv01_49, 
                    SUM(IS1.office_stg_summary_lv50_99) AS office_stg_summary_lv50_99, 
                    SUM(IS1.office_stg_summary_lv100) AS office_stg_summary_lv100, 
                    -- SUM(IS1.office_stg_summary_half) AS office_stg_summary_half, 
                    SUM(IS1.office_stg_summary_full) AS office_stg_summary_full, 

                    SUM(IS1.farmer_fisher_dep_summary_lv00) AS farmer_fisher_dep_summary_lv00, 
                    SUM(IS1.farmer_fisher_dep_summary_lv01_49) AS farmer_fisher_dep_summary_lv01_49, 
                    SUM(IS1.farmer_fisher_dep_summary_lv50_99) AS farmer_fisher_dep_summary_lv50_99, 
                    SUM(IS1.farmer_fisher_dep_summary_lv100) AS farmer_fisher_dep_summary_lv100, 
                    -- SUM(IS1.farmer_fisher_dep_summary_half) AS farmer_fisher_dep_summary_half, 
                    SUM(IS1.farmer_fisher_dep_summary_full) AS farmer_fisher_dep_summary_full, 

                    SUM(IS1.farmer_fisher_inv_summary_lv00) AS farmer_fisher_inv_summary_lv00, 
                    SUM(IS1.farmer_fisher_inv_summary_lv01_49) AS farmer_fisher_inv_summary_lv01_49, 
                    SUM(IS1.farmer_fisher_inv_summary_lv50_99) AS farmer_fisher_inv_summary_lv50_99, 
                    SUM(IS1.farmer_fisher_inv_summary_lv100) AS farmer_fisher_inv_summary_lv100, 
                    -- SUM(IS1.farmer_fisher_inv_summary_half) AS farmer_fisher_inv_summary_half, 
                    SUM(IS1.farmer_fisher_inv_summary_full) AS farmer_fisher_inv_summary_full, 

                    SUM(IS1.office_alt_summary_lv00) AS office_alt_summary_lv00, 
                    SUM(IS1.office_alt_summary_lv01_49) AS office_alt_summary_lv01_49, 
                    SUM(IS1.office_alt_summary_lv50_99) AS office_alt_summary_lv50_99, 
                    SUM(IS1.office_alt_summary_lv100) AS office_alt_summary_lv100, 
                    SUM(IS1.office_alt_summary_half) AS office_alt_summary_half, 
                    SUM(IS1.office_alt_summary_full) AS office_alt_summary_full 
                    
                FROM IPPAN_SUMMARY IS1 
                LEFT JOIN SUIGAI SG1 ON IS1.suigai_id = SG1.suigai_id 
                WHERE IS1.deleted_at IS NULL 
                GROUP BY SG1.ken_code 
                ORDER BY CAST(SG1.KEN_CODE AS INTEGER)
                ) SUB1 
                LEFT JOIN KEN KE1 ON SUB1.id=KE1.ken_code 
            """, [])

        ### 集計データ_水系別: IPPAN_GROUP_BY_SUIKEI
        elif category_code2 == "302" or category_code2 == "8020":
            ### print_log('[INFO] SELECT * FROM IPPAN_SUMMARY GROUP BY () ORDER BY CAST(AS INTEGER)', 'INFO')
            ### GROUP BY に使用する水系コードをIPPAN_SUMMARYモデルのidに使用する。
            ### IPPAN_SUMMARYモデルのidを指定しないと、<class 'django.core.exceptions.FieldDoesNotExist'>のエラーとなるため。
            ### SQLは実行できるが、IPPAN_SUMMARYモデルに正しくセットできないため。
            ### 水系コードをPKとする別のモデルを定義しても良さそうだが、未検証。
            ippan_group_by_suikei_list = IPPAN_SUMMARY.objects.raw("""
                SELECT 
                    SUB1.id AS id, 
                    SUB1.id AS suikei_code, 
                    SK1.suikei_name AS suikei_name, 

                    CAST(SUB1.house_summary_lv00 AS NUMERIC(20,10)) AS house_summary_lv00, 
                    CAST(SUB1.house_summary_lv01_49 AS NUMERIC(20,10)) AS house_summary_lv01_49, 
                    CAST(SUB1.house_summary_lv50_99 AS NUMERIC(20,10)) AS house_summary_lv50_99, 
                    CAST(SUB1.house_summary_lv100 AS NUMERIC(20,10)) AS house_summary_lv100, 
                    CAST(SUB1.house_summary_half AS NUMERIC(20,10)) AS house_summary_half, 
                    CAST(SUB1.house_summary_full AS NUMERIC(20,10)) AS house_summary_full, 

                    CAST(SUB1.household_summary_lv00 AS NUMERIC(20,10)) AS household_summary_lv00, 
                    CAST(SUB1.household_summary_lv01_49 AS NUMERIC(20,10)) AS household_summary_lv01_49, 
                    CAST(SUB1.household_summary_lv50_99 AS NUMERIC(20,10)) AS household_summary_lv50_99, 
                    CAST(SUB1.household_summary_lv100 AS NUMERIC(20,10)) AS household_summary_lv100, 
                    CAST(SUB1.household_summary_half AS NUMERIC(20,10)) AS household_summary_half, 
                    CAST(SUB1.household_summary_full AS NUMERIC(20,10)) AS household_summary_full, 

                    CAST(SUB1.car_summary_lv00 AS NUMERIC(20,10)) AS car_summary_lv00, 
                    CAST(SUB1.car_summary_lv01_49 AS NUMERIC(20,10)) AS car_summary_lv01_49, 
                    CAST(SUB1.car_summary_lv50_99 AS NUMERIC(20,10)) AS car_summary_lv50_99, 
                    CAST(SUB1.car_summary_lv100 AS NUMERIC(20,10)) AS car_summary_lv100, 
                    CAST(SUB1.car_summary_half AS NUMERIC(20,10)) AS car_summary_half, 
                    CAST(SUB1.car_summary_full AS NUMERIC(20,10)) AS car_summary_full, 

                    CAST(SUB1.house_alt_summary_lv00 AS NUMERIC(20,10)) AS house_alt_summary_lv00, 
                    CAST(SUB1.house_alt_summary_lv01_49 AS NUMERIC(20,10)) AS house_alt_summary_lv01_49, 
                    CAST(SUB1.house_alt_summary_lv50_99 AS NUMERIC(20,10)) AS house_alt_summary_lv50_99, 
                    CAST(SUB1.house_alt_summary_lv100 AS NUMERIC(20,10)) AS house_alt_summary_lv100, 
                    CAST(SUB1.house_alt_summary_half AS NUMERIC(20,10)) AS house_alt_summary_half, 
                    CAST(SUB1.house_alt_summary_full AS NUMERIC(20,10)) AS house_alt_summary_full, 

                    CAST(SUB1.house_clean_summary_lv00 AS NUMERIC(20,10)) AS house_clean_summary_lv00, 
                    CAST(SUB1.house_clean_summary_lv01_49 AS NUMERIC(20,10)) AS house_clean_summary_lv01_49, 
                    CAST(SUB1.house_clean_summary_lv50_99 AS NUMERIC(20,10)) AS house_clean_summary_lv50_99, 
                    CAST(SUB1.house_clean_summary_lv100 AS NUMERIC(20,10)) AS house_clean_summary_lv100, 
                    CAST(SUB1.house_clean_summary_half AS NUMERIC(20,10)) AS house_clean_summary_half, 
                    CAST(SUB1.house_clean_summary_full AS NUMERIC(20,10)) AS house_clean_summary_full, 

                    CAST(SUB1.office_dep_summary_lv00 AS NUMERIC(20,10)) AS office_dep_summary_lv00, 
                    CAST(SUB1.office_dep_summary_lv01_49 AS NUMERIC(20,10)) AS office_dep_summary_lv01_49, 
                    CAST(SUB1.office_dep_summary_lv50_99 AS NUMERIC(20,10)) AS office_dep_summary_lv50_99, 
                    CAST(SUB1.office_dep_summary_lv100 AS NUMERIC(20,10)) AS office_dep_summary_lv100, 
                    CAST(SUB1.office_dep_summary_full AS NUMERIC(20,10)) AS office_dep_summary_full, 

                    CAST(SUB1.office_inv_summary_lv00 AS NUMERIC(20,10)) AS office_inv_summary_lv00, 
                    CAST(SUB1.office_inv_summary_lv01_49 AS NUMERIC(20,10)) AS office_inv_summary_lv01_49, 
                    CAST(SUB1.office_inv_summary_lv50_99 AS NUMERIC(20,10)) AS office_inv_summary_lv50_99, 
                    CAST(SUB1.office_inv_summary_lv100 AS NUMERIC(20,10)) AS office_inv_summary_lv100, 
                    CAST(SUB1.office_inv_summary_full AS NUMERIC(20,10)) AS office_inv_summary_full, 

                    CAST(SUB1.office_sus_summary_lv00 AS NUMERIC(20,10)) AS office_sus_summary_lv00, 
                    CAST(SUB1.office_sus_summary_lv01_49 AS NUMERIC(20,10)) AS office_sus_summary_lv01_49,  
                    CAST(SUB1.office_sus_summary_lv50_99 AS NUMERIC(20,10)) AS office_sus_summary_lv50_99, 
                    CAST(SUB1.office_sus_summary_lv100 AS NUMERIC(20,10)) AS office_sus_summary_lv100, 
                    CAST(SUB1.office_sus_summary_full AS NUMERIC(20,10)) AS office_sus_summary_full, 

                    CAST(SUB1.office_stg_summary_lv00 AS NUMERIC(20,10)) AS office_stg_summary_lv00, 
                    CAST(SUB1.office_stg_summary_lv01_49 AS NUMERIC(20,10)) AS office_stg_summary_lv01_49, 
                    CAST(SUB1.office_stg_summary_lv50_99 AS NUMERIC(20,10)) AS office_stg_summary_lv50_99, 
                    CAST(SUB1.office_stg_summary_lv100 AS NUMERIC(20,10)) AS office_stg_summary_lv100, 
                    CAST(SUB1.office_stg_summary_full AS NUMERIC(20,10)) AS office_stg_summary_full, 

                    CAST(SUB1.farmer_fisher_dep_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv00, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv01_49, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv50_99, 
                    CAST(SUB1.farmer_fisher_dep_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_lv100, 
                    CAST(SUB1.farmer_fisher_dep_summary_full AS NUMERIC(20,10)) AS farmer_fisher_dep_summary_full, 

                    CAST(SUB1.farmer_fisher_inv_summary_lv00 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv00, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv01_49 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv01_49, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv50_99 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv50_99, 
                    CAST(SUB1.farmer_fisher_inv_summary_lv100 AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_lv100, 
                    CAST(SUB1.farmer_fisher_inv_summary_full AS NUMERIC(20,10)) AS farmer_fisher_inv_summary_full, 

                    CAST(SUB1.office_alt_summary_lv00 AS NUMERIC(20,10)) AS office_alt_summary_lv00, 
                    CAST(SUB1.office_alt_summary_lv01_49 AS NUMERIC(20,10)) AS office_alt_summary_lv01_49, 
                    CAST(SUB1.office_alt_summary_lv50_99 AS NUMERIC(20,10)) AS office_alt_summary_lv50_99, 
                    CAST(SUB1.office_alt_summary_lv100 AS NUMERIC(20,10)) AS office_alt_summary_lv100, 
                    CAST(SUB1.office_alt_summary_half AS NUMERIC(20,10)) AS office_alt_summary_half, 
                    CAST(SUB1.office_alt_summary_full AS NUMERIC(20,10)) AS office_alt_summary_full 
                FROM (    
                SELECT 
                    SG1.suikei_code AS id, 
                    SUM(IS1.house_summary_lv00) AS house_summary_lv00, 
                    SUM(IS1.house_summary_lv01_49) AS house_summary_lv01_49, 
                    SUM(IS1.house_summary_lv50_99) AS house_summary_lv50_99, 
                    SUM(IS1.house_summary_lv100) AS house_summary_lv100, 
                    SUM(IS1.house_summary_half) AS house_summary_half, 
                    SUM(IS1.house_summary_full) AS house_summary_full, 

                    SUM(IS1.household_summary_lv00) AS household_summary_lv00, 
                    SUM(IS1.household_summary_lv01_49) AS household_summary_lv01_49, 
                    SUM(IS1.household_summary_lv50_99) AS household_summary_lv50_99, 
                    SUM(IS1.household_summary_lv100) AS household_summary_lv100, 
                    SUM(IS1.household_summary_half) AS household_summary_half, 
                    SUM(IS1.household_summary_full) AS household_summary_full, 

                    SUM(IS1.car_summary_lv00) AS car_summary_lv00, 
                    SUM(IS1.car_summary_lv01_49) AS car_summary_lv01_49, 
                    SUM(IS1.car_summary_lv50_99) AS car_summary_lv50_99, 
                    SUM(IS1.car_summary_lv100) AS car_summary_lv100, 
                    SUM(IS1.car_summary_half) AS car_summary_half, 
                    SUM(IS1.car_summary_full) AS car_summary_full, 

                    SUM(IS1.house_alt_summary_lv00) AS house_alt_summary_lv00, 
                    SUM(IS1.house_alt_summary_lv01_49) AS house_alt_summary_lv01_49, 
                    SUM(IS1.house_alt_summary_lv50_99) AS house_alt_summary_lv50_99, 
                    SUM(IS1.house_alt_summary_lv100) AS house_alt_summary_lv100, 
                    SUM(IS1.house_alt_summary_half) AS house_alt_summary_half, 
                    SUM(IS1.house_alt_summary_full) AS house_alt_summary_full, 

                    SUM(IS1.house_clean_summary_lv00) AS house_clean_summary_lv00, 
                    SUM(IS1.house_clean_summary_lv01_49) AS house_clean_summary_lv01_49, 
                    SUM(IS1.house_clean_summary_lv50_99) AS house_clean_summary_lv50_99, 
                    SUM(IS1.house_clean_summary_lv100) AS house_clean_summary_lv100, 
                    SUM(IS1.house_clean_summary_half) AS house_clean_summary_half, 
                    SUM(IS1.house_clean_summary_full) AS house_clean_summary_full, 

                    SUM(IS1.office_dep_summary_lv00) AS office_dep_summary_lv00, 
                    SUM(IS1.office_dep_summary_lv01_49) AS office_dep_summary_lv01_49, 
                    SUM(IS1.office_dep_summary_lv50_99) AS office_dep_summary_lv50_99, 
                    SUM(IS1.office_dep_summary_lv100) AS office_dep_summary_lv100, 
                    -- SUM(IS1.office_dep_summary_half) AS office_dep_summary_half, 
                    SUM(IS1.office_dep_summary_full) AS office_dep_summary_full, 

                    SUM(IS1.office_inv_summary_lv00) AS office_inv_summary_lv00, 
                    SUM(IS1.office_inv_summary_lv01_49) AS office_inv_summary_lv01_49, 
                    SUM(IS1.office_inv_summary_lv50_99) AS office_inv_summary_lv50_99, 
                    SUM(IS1.office_inv_summary_lv100) AS office_inv_summary_lv100, 
                    -- SUM(IS1.office_inv_summary_half) AS office_inv_summary_half, 
                    SUM(IS1.office_inv_summary_full) AS office_inv_summary_full, 

                    SUM(IS1.office_sus_summary_lv00) AS office_sus_summary_lv00, 
                    SUM(IS1.office_sus_summary_lv01_49) AS office_sus_summary_lv01_49, 
                    SUM(IS1.office_sus_summary_lv50_99) AS office_sus_summary_lv50_99, 
                    SUM(IS1.office_sus_summary_lv100) AS office_sus_summary_lv100, 
                    -- SUM(IS1.office_sus_summary_half) AS office_sus_summary_half, 
                    SUM(IS1.office_sus_summary_full) AS office_sus_summary_full, 

                    SUM(IS1.office_stg_summary_lv00) AS office_stg_summary_lv00, 
                    SUM(IS1.office_stg_summary_lv01_49) AS office_stg_summary_lv01_49, 
                    SUM(IS1.office_stg_summary_lv50_99) AS office_stg_summary_lv50_99, 
                    SUM(IS1.office_stg_summary_lv100) AS office_stg_summary_lv100, 
                    -- SUM(IS1.office_stg_summary_half) AS office_stg_summary_half, 
                    SUM(IS1.office_stg_summary_full) AS office_stg_summary_full, 

                    SUM(IS1.farmer_fisher_dep_summary_lv00) AS farmer_fisher_dep_summary_lv00, 
                    SUM(IS1.farmer_fisher_dep_summary_lv01_49) AS farmer_fisher_dep_summary_lv01_49, 
                    SUM(IS1.farmer_fisher_dep_summary_lv50_99) AS farmer_fisher_dep_summary_lv50_99, 
                    SUM(IS1.farmer_fisher_dep_summary_lv100) AS farmer_fisher_dep_summary_lv100, 
                    -- SUM(IS1.farmer_fisher_dep_summary_half) AS farmer_fisher_dep_summary_half, 
                    SUM(IS1.farmer_fisher_dep_summary_full) AS farmer_fisher_dep_summary_full, 

                    SUM(IS1.farmer_fisher_inv_summary_lv00) AS farmer_fisher_inv_summary_lv00, 
                    SUM(IS1.farmer_fisher_inv_summary_lv01_49) AS farmer_fisher_inv_summary_lv01_49, 
                    SUM(IS1.farmer_fisher_inv_summary_lv50_99) AS farmer_fisher_inv_summary_lv50_99, 
                    SUM(IS1.farmer_fisher_inv_summary_lv100) AS farmer_fisher_inv_summary_lv100, 
                    -- SUM(IS1.farmer_fisher_inv_summary_half) AS farmer_fisher_inv_summary_half, 
                    SUM(IS1.farmer_fisher_inv_summary_full) AS farmer_fisher_inv_summary_full, 

                    SUM(IS1.office_alt_summary_lv00) AS office_alt_summary_lv00, 
                    SUM(IS1.office_alt_summary_lv01_49) AS office_alt_summary_lv01_49, 
                    SUM(IS1.office_alt_summary_lv50_99) AS office_alt_summary_lv50_99, 
                    SUM(IS1.office_alt_summary_lv100) AS office_alt_summary_lv100, 
                    SUM(IS1.office_alt_summary_half) AS office_alt_summary_half, 
                    SUM(IS1.office_alt_summary_full) AS office_alt_summary_full 
                    
                FROM IPPAN_SUMMARY IS1 
                LEFT JOIN SUIGAI SG1 ON IS1.suigai_id = SG1.suigai_id 
                WHERE IS1.deleted_at IS NULL 
                GROUP BY SG1.suikei_code 
                ORDER BY CAST(SG1.suikei_code AS INTEGER)
                ) SUB1 
                LEFT JOIN SUIKEI SK1 ON SUB1.id=SK1.suikei_code 
            """, [])

        ### アクション: ACTION
        elif category_code2 == "10000":
            action_list = ACTION.objects.raw("""
                SELECT 
                    action_code, 
                    action_name 
                FROM ACTION 
                -- ORDER BY CAST(ACTION_CODE AS INTEGER)
                ORDER BY ACTION_CODE 
                """, [])

        ### 状態: STATUS
        elif category_code2 == "10010":
            status_list = STATUS.objects.raw("""
                SELECT 
                    status_code, 
                    status_name 
                FROM STATUS 
                -- ORDER BY CAST(STATUS_CODE AS INTEGER)
                ORDER BY STATUS_CODE
                """, [])

        ### トリガーメッセージ: TRIGGER
        elif category_code2 == "10020":
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    TO_CHAR(timezone('JST', TR1.published_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS published_at, 
                    TO_CHAR(timezone('JST', TR1.consumed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS consumed_at, 
                    TO_CHAR(timezone('JST', TR1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 
                    TR1.integrity_ok AS integrity_ok, 
                    TR1.integrity_ng AS integrity_ng 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                WHERE TR1.deleted_at IS NULL 
                ORDER BY CAST(TRIGGER_ID AS INTEGER)""", [])

        ### 
        elif category_code2 == "10030":
            approve_list = APPROVE.objects.raw("""
                SELECT 
                    * 
                FROM APPROVE 
                ORDER BY CAST(APPROVE_ID AS INTEGER)""", [])

        ### 
        elif category_code2 == "10040":
            feedback_list = FEEDBACK.objects.raw("""
                SELECT 
                    * 
                FROM FEEDBACK 
                ORDER BY CAST(FEEDBACK_ID AS INTEGER)""", [])

        else:
            pass
        
        #######################################################################
        ### レスポンスセット処理(0040)
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 5/5.', 'DEBUG')
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'category_code1': category_code1,
            'category_code2': category_code2,
            'ken_code': ken_code,
            'city_code': city_code,
            'building_list': building_list,                                    ### 1000: 建物区分 
            'ken_list': ken_list,                                              ### 1010: 都道府県 
            'city_list': city_list,                                            ### 1020: 市区町村 
            'kasen_kaigan_list': kasen_kaigan_list,                            ### 1030: 水害発生地点工種（河川海岸区分） 
            'suikei_list': suikei_list,                                        ### 1040: 水系（水系・沿岸） 
            'suikei_type_list': suikei_type_list,                              ### 1050: 水系種別（水系・沿岸種別） 
            'kasen_list': kasen_list,                                          ### 1060: 河川（河川・海岸） 
            'kasen_type_list': kasen_type_list,                                ### 1070: 河川種別（河川・海岸種別） 
            'cause_list': cause_list,                                          ### 1080: 水害原因 
            'underground_list': underground_list,                              ### 1090: 地上地下区分 
            'usage_list': usage_list,                                          ### 1100: 地下空間の利用形態 
            'flood_sediment_list': flood_sediment_list,                        ### 1110: 浸水土砂区分 
            'gradient_list': gradient_list,                                    ### 1120: 地盤勾配区分 
            'industry_list': industry_list,                                    ### 1130: 産業分類 
            'house_asset_list': house_asset_list,                              ### 2000: 家屋評価額 
            'house_rate_list': house_rate_list,                                ### 2010: 家屋被害率 
            'house_alt_list': house_alt_list,                                  ### 2020: 家庭応急対策費_代替活動費 
            'house_clean_list': house_clean_list,                              ### 2030: 家庭応急対策費_清掃日数
            'household_asset_list': household_asset_list,                      ### 3000: 家庭用品自動車以外所有額 
            'household_rate_list': household_rate_list,                        ### 3010: 家庭用品自動車以外被害率
            'car_asset_list': car_asset_list,                                  ### 4000: 家庭用品自動車所有額 
            'car_rate_list': car_rate_list,                                    ### 4010: 家庭用品自動車被害率
            'office_asset_list': office_asset_list,                            ### 5000: 事業所資産額 
            'office_rate_list': office_rate_list,                              ### 5010: 事業所被害率 
            'office_suspend_list': office_suspend_list,                        ### 5020: 事業所営業停止日数 
            'office_stagnate_list': office_stagnate_list,                      ### 5030: 事業所営業停滞日数 
            'office_alt_list': office_alt_list,                                ### 5040: 事業所応急対策費_代替活動費
            'farmer_fisher_asset_list': farmer_fisher_asset_list,              ### 6000: 農漁家資産額 
            'farmer_fisher_rate_list': farmer_fisher_rate_list,                ### 6010: 農漁家被害率 
            'area_list': area_list,                                            ### 7000: 一般資産入力データ_水害区域 
            'weather_list': weather_list,                                      ### 7010: 一般資産入力データ_異常気象 
            'suigai_list': suigai_list,                                        ### 7020: 一般資産入力データ_ヘッダ部分 
            'ippan_list': ippan_list,                                          ### 7030: 一般資産入力データ_一覧表部分 
            'ippan_view_list': ippan_view_list,                                ### 7040: 一般資産ビューデータ_一覧表部分 
            'ippan_summary_list': ippan_summary_list,                          ### 8000: 一般資産集計データ 
            'ippan_group_by_ken_list': ippan_group_by_ken_list,                ### 8010: 
            'ippan_group_by_suikei_list': ippan_group_by_suikei_list,          ### 8020: 
            'action_list': action_list,                                        ### 10000: アクション 
            'status_list': status_list,                                        ### 10010: 状態 
            'trigger_list': trigger_list,                                      ### 10020: トリガーメッセージ 
        }
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0400OnlineDisplay.category1_category2_ken_city_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category1_category2_ken_city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category1_category2_ken_city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
