#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0400OnlineDisplay/views.py
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
from P0000Common.models import REPOSITORY              ### 10050: EXCELファイルレポジトリ
### from P0000Common.models import EXECUTE             ### 10060: 実行管理

from P0000Common.common import print_log

###############################################################################
### 関数名： index_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 2/3.', 'INFO')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_list': ken_list, 
        }
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：category1_category2_ken_city_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def category_view2(request, category_code1, category_code2, ken_code, city_code):
def category1_category2_ken_city_view(request, category_code1, category_code2, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 category_code2 = {}'.format(category_code2), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 city_code = {}'.format(city_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 1/4.', 'INFO')

        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 2/4.', 'INFO')
        ken_list = []
        city_list = []
        
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        
        if ken_code == "0":
            city_list = CITY.objects.raw("""SELECT * FROM CITY ORDER BY CAST(CITY_CODE AS INTEGER)""", [])
        else:
            city_list = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken_code,])
        
        #######################################################################
        ### DBアクセス処理(0020)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 3/4.', 'INFO')
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
        approval_list = []                             ### 10030: 承認メッセージ
        feedback_list = []                             ### 10040: フィードバックメッセージ
        repository_list = []                           ### 10050: EXCELファイルレポジトリ
        ### execute_list = []                          ### 10060: 実行管理
        
        if category_code2 == "0":
            pass
        
        elif category_code2 == "1" or category_code2 == "10000":
            building_list = BUILDING.objects.raw("""
                SELECT 
                    BUILDING_CODE, 
                    BUILDING_NAME 
                FROM BUILDING 
                ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
            
        elif category_code2 == "2" or category_code2 == "1010":
            pass
        
        elif category_code2 == "3" or category_code2 == "1020":
            pass
        
        elif category_code2 == "4" or category_code2 == "1030":
            kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""
                SELECT 
                    KASEN_KAIGAN_CODE, 
                    KASEN_KAIGAN_NAME 
                FROM KASEN_KAIGAN 
                ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
            
        elif category_code2 == "5" or category_code2 == "1040":
            suikei_list = SUIKEI.objects.raw("""
                SELECT 
                    SK1.SUIKEI_CODE, 
                    SK1.SUIKEI_NAME, 
                    SK1.SUIKEI_TYPE_CODE, 
                    ST1.SUIKEI_TYPE_NAME 
                FROM SUIKEI SK1 
                LEFT JOIN SUIKEI_TYPE ST1 ON SK1.SUIKEI_TYPE_CODE=ST1.SUIKEI_TYPE_CODE 
                ORDER BY CAST(SK1.SUIKEI_CODE AS INTEGER)""", [])
            
        elif category_code2 == "6" or category_code2 == "1050":
            suikei_type_list = SUIKEI_TYPE.objects.raw("""
                SELECT 
                    SUIKEI_TYPE_CODE, 
                    SUIKEI_TYPE_NAME 
                FROM SUIKEI_TYPE 
                ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
            
        elif category_code2 == "7" or category_code2 == "1060":
            kasen_list = KASEN.objects.raw("""
                SELECT 
                    KA1.KASEN_CODE, 
                    KA1.KASEN_NAME, 
                    KA1.KASEN_TYPE_CODE, 
                    KT1.KASEN_TYPE_NAME, 
                    SK1.SUIKEI_CODE, 
                    ST1.SUIKEI_NAME 
                FROM KASEN KA1 
                LEFT JOIN KASEN_TYPE KT1 ON KA1.KASEN_TYPE_CODE=KT1.KASEN_TYPE_CODE 
                LEFT JOIN SUIKEI SK1 ON KA1.SUIKEI_CODE=SK1.SUIKEI_CODE 
                ORDER BY CAST(KA1.KASEN_CODE AS INTEGER)""", [])
            
        elif category_code2 == "8" or category_code2 == "1070":
            kasen_type_list = KASEN_TYPE.objects.raw("""
                SELECT 
                    * 
                FROM KASEN_TYPE 
                ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
            
        elif category_code2 == "9" or category_code2 == "1080":
            cause_list = CAUSE.objects.raw("""
                SELECT 
                    * 
                FROM CAUSE 
                ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
            
        elif category_code2 == "10" or category_code2 == "1090":
            underground_list = UNDERGROUND.objects.raw("""
                SELECT 
                    * 
                FROM UNDERGROUND 
                ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
            
        elif category_code2 == "11" or category_code2 == "1100":
            usage_list = USAGE.objects.raw("""
                SELECT 
                    * 
                FROM USAGE 
                ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
            
        elif category_code2 == "12" or category_code2 == "1110":
            flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""
                SELECT 
                    * 
                FROM FLOOD_SEDIMENT 
                ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
            
        elif category_code2 == "13" or category_code2 == "1120":
            gradient_list = GRADIENT.objects.raw("""
                SELECT 
                    * 
                FROM GRADIENT 
                ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
            
        elif category_code2 == "14" or category_code2 == "1130":
            industry_list = INDUSTRY.objects.raw("""
                SELECT 
                    * 
                FROM INDUSTRY 
                ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])


            
        elif category_code2 == "100" or category_code2 == "2000":
            house_asset_list = HOUSE_ASSET.objects.raw("""
                SELECT 
                    * 
                FROM HOUSE_ASSET 
                ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)""", [])
            
        elif category_code2 == "101" or category_code2 == "2010":
            house_rate_list = HOUSE_RATE.objects.raw("""
                SELECT 
                    * 
                FROM HOUSE_RATE 
                ORDER BY CAST(HOUSE_RATE_CODE AS INTEGER)""", [])
            
        elif category_code2 == "102" or category_code2 == "2020":
            house_alt_list = HOUSE_ALT.objects.raw("""
                SELECT 
                    * 
                FROM HOUSE_ALT 
                ORDER BY CAST(HOUSE_ALT_CODE AS INTEGER)""", [])
            
        elif category_code2 == "103" or category_code2 == "2030":
            house_clean_list = HOUSE_CLEAN.objects.raw("""
                SELECT 
                    * 
                FROM HOUSE_CLEAN 
                ORDER BY CAST(HOUSE_CLEAN_CODE AS INTEGER)""", [])


            
        elif category_code2 == "104" or category_code2 == "3000":
            household_asset_list = HOUSEHOLD_ASSET.objects.raw("""
                SELECT 
                    * 
                FROM HOUSEHOLD_ASSET 
                ORDER BY CAST(HOUSEHOLD_ASSET_CODE AS INTEGER)""", [])
            
        elif category_code2 == "105" or category_code2 == "3010":
            household_rate_list = HOUSEHOLD_RATE.objects.raw("""
                SELECT 
                    * 
                FROM HOUSEHOLD_RATE 
                ORDER BY CAST(HOUSEHOLD_RATE_CODE AS INTEGER)""", [])


            
        elif category_code2 == "106" or category_code2 == "4000":
            car_asset_list = CAR_ASSET.objects.raw("""
                SELECT 
                    * 
                FROM CAR_ASSET 
                ORDER BY CAST(CAR_ASSET_CODE AS INTEGER)""", [])
            
        elif category_code2 == "107" or category_code2 == "4010":
            car_rate_list = CAR_RATE.objects.raw("""
                SELECT 
                    * 
                FROM CAR_RATE 
                ORDER BY CAST(CAR_RATE_CODE AS INTEGER)""", [])

            
            
        elif category_code2 == "108" or category_code2 == "5000":
            office_asset_list = OFFICE_ASSET.objects.raw("""
                SELECT 
                    * 
                FROM OFFICE_ASSET 
                ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)""", [])

        elif category_code2 == "109" or category_code2 == "5010":
            office_rate_list = OFFICE_RATE.objects.raw("""
                SELECT 
                    * 
                FROM OFFICE_RATE 
                ORDER BY CAST(OFFICE_RATE_CODE AS INTEGER)""", [])

        elif category_code2 == "110" or category_code2 == "5020":
            office_suspend_list = OFFICE_SUSPEND.objects.raw("""
                SELECT 
                    * 
                FROM OFFICE_SUSPEND 
                ORDER BY CAST(OFFICE_SUS_CODE AS INTEGER)""", [])

        elif category_code2 == "111" or category_code2 == "5030":
            office_stagnate_list = OFFICE_STAGNATE.objects.raw("""
                SELECT 
                    * 
                FROM OFFICE_STAGNATE 
                ORDER BY CAST(OFFICE_STG_CODE AS INTEGER)""", [])

        elif category_code2 == "112" or category_code2 == "5040":
            office_alt_list = OFFICE_ALT.objects.raw("""
                SELECT 
                    * 
                FROM OFFICE_ALT 
                ORDER BY CAST(OFFICE_ALT_CODE AS INTEGER)""", [])



        elif category_code2 == "113" or category_code2 == "6000":
            farmer_fisher_asset_list = FARMER_FISHER_ASSET.objects.raw("""
                SELECT 
                    * 
                FROM FARMER_FISHER_ASSET 
                ORDER BY CAST(FARMER_FISHER_ASSET_CODE AS INTEGER)""", [])

        elif category_code2 == "114" or category_code2 == "6010":
            farmer_fisher_rate_list = FARMER_FISHER_RATE.objects.raw("""
                SELECT 
                    * 
                FROM FARMER_FISHER_RATE 
                ORDER BY CAST(FARMER_FISHER_RATE_CODE AS INTEGER)""", [])



        elif category_code2 == "200" or category_code2 == "7000":
            area_list = AREA.objects.raw("""
                SELECT 
                    * 
                FROM AREA 
                ORDER BY CAST(AREA_ID AS INTEGER)""", [])
            
        elif category_code2 == "201" or category_code2 == "7010":
            weather_list = WEATHER.objects.raw("""
                SELECT 
                    * 
                FROM WEATHER 
                ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
            
        elif category_code2 == "202" or category_code2 == "7020":
            suigai_list = SUIGAI.objects.raw("""
                SELECT 
                    * 
                FROM SUIGAI 
                ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])

        elif category_code2 == "203" or category_code2 == "7030":
            ippan_list = IPPAN.objects.raw("""
                SELECT 
                    * 
                FROM IPPAN 
                ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])

        elif category_code2 == "204" or category_code2 == "7040":
            if ken_code == "0":
                if city_code == "0":
                    ippan_view_list = IPPAN_VIEW.objects.raw(""" 
                        SELECT * FROM IPPAN_VIEW ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [])
                else:
                    ippan_view_list = IPPAN_VIEW.objects.raw(""" 
                        SELECT * FROM IPPAN_VIEW WHERE CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [city_code, ])
            else:
                if city_code == "0":
                    ippan_view_list = IPPAN_VIEW.objects.raw(""" 
                        SELECT * FROM IPPAN_VIEW WHERE KEN_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, ])
                else:
                    ippan_view_list = IPPAN_VIEW.objects.raw(""" 
                        SELECT * FROM IPPAN_VIEW WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, city_code, ])

        elif category_code2 == "300" or category_code2 == "8000":
            ippan_summary_list = IPPAN_SUMMARY.objects.raw("""SELECT * FROM IPPAN_SUMMARY ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])

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
                GROUP BY SG1.ken_code 
                ORDER BY CAST(SG1.KEN_CODE AS INTEGER)
            """, [])

        elif category_code2 == "302" or category_code2 == "8020":
            ### print_log('[INFO] SELECT * FROM IPPAN_SUMMARY GROUP BY () ORDER BY CAST(AS INTEGER)', 'INFO')
            ### GROUP BY に使用する水系コードをIPPAN_SUMMARYモデルのidに使用する。
            ### IPPAN_SUMMARYモデルのidを指定しないと、<class 'django.core.exceptions.FieldDoesNotExist'>のエラーとなるため。
            ### SQLは実行できるが、IPPAN_SUMMARYモデルに正しくセットできないため。
            ### 水系コードをPKとする別のモデルを定義しても良さそうだが、未検証。
            ippan_group_by_suikei_list = IPPAN_SUMMARY.objects.raw("""
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
                GROUP BY SG1.suikei_code 
                ORDER BY CAST(SG1.suikei_code AS INTEGER)
            """, [])

        elif category_code2 == "10000":
            action_list = ACTION.objects.raw("""
                SELECT 
                    * 
                FROM ACTION 
                ORDER BY CAST(ACTION_CODE AS INTEGER)""", [])

        elif category_code2 == "10010":
            status_list = STATUS.objects.raw("""
                SELECT 
                    * 
                FROM STATUS 
                ORDER BY CAST(STATUS_CODE AS INTEGER)""", [])

        elif category_code2 == "10020":
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                ORDER BY CAST(TRIGGER_ID AS INTEGER)""", [])

        elif category_code2 == "10030":
            approve_list = APPROVE.objects.raw("""
                SELECT 
                    * 
                FROM APPROVE 
                ORDER BY CAST(APPROVE_ID AS INTEGER)""", [])

        elif category_code2 == "10040":
            feedback_list = FEEDBACK.objects.raw("""
                SELECT 
                    * 
                FROM FEEDBACK 
                ORDER BY CAST(FEEDBACK_ID AS INTEGER)""", [])

        elif category_code2 == "10050":
            repository_list = REPOSITORY.objects.raw("""
                SELECT 
                    * 
                FROM REPOSITORY 
                ORDER BY CAST(REPOSITORY_ID AS INTEGER)""", [])

        ### elif category_code2 == "10060":
        ###     pass

        else:
            pass
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数 STEP 4/4.', 'INFO')
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
            'approval_list': approval_list,                                    ### 10030: 承認メッセージ 
            'feedback_list': feedback_list,                                    ### 10040: フィードバックメッセージ 
            'repository_list': repository_list,                                ### 10050: EXCELファイルレポジトリ
            ### 'execute_list': execute_list,                                  ### 10060: 実行管理
            
        }
        print_log('[INFO] P0400OnlineDisplay.category1_category2_ken_city_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category1_category2_ken_city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category1_category2_ken_city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
