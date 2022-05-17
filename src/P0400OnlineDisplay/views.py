#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0400OnlineDisplay/views.py
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import sys
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

from P0000Common.models import BUILDING                ### 01: 建物区分
from P0000Common.models import KEN                     ### 02: 都道府県
from P0000Common.models import CITY                    ### 03: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 04: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 05: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 06: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 07: 河川（河川・海岸）
from P0000Common.models import KASEN_TYPE              ### 08: 河川種別（河川・海岸種別）
from P0000Common.models import CAUSE                   ### 09: 水害原因
from P0000Common.models import UNDERGROUND             ### 10: 地上地下区分
from P0000Common.models import USAGE                   ### 11: 地下空間の利用形態
from P0000Common.models import FLOOD_SEDIMENT          ### 12: 浸水土砂区分
from P0000Common.models import GRADIENT                ### 13: 地盤勾配区分
from P0000Common.models import INDUSTRY                ### 14: 産業分類
from P0000Common.models import HOUSE_ASSET             ### 15: 県別家屋評価額
from P0000Common.models import HOUSE_DAMAGE            ### 16: 家屋被害率
from P0000Common.models import HOUSEHOLD_DAMAGE        ### 17: 家庭用品自動車以外被害率
from P0000Common.models import CAR_DAMAGE              ### 18: 家庭用品自動車被害率
from P0000Common.models import HOUSE_COST              ### 19: 家庭応急対策費
from P0000Common.models import OFFICE_ASSET            ### 20: 産業分類別資産額
from P0000Common.models import OFFICE_DAMAGE           ### 21: 事業所被害率
from P0000Common.models import OFFICE_COST             ### 22: 事業所営業停止損失
from P0000Common.models import FARMER_FISHER_DAMAGE    ### 23: 農漁家被害率
from P0000Common.models import WEATHER                 ### 24: 異常気象（ほぼ、水害）
from P0000Common.models import AREA                    ### 25: 区域
from P0000Common.models import IPPAN                   ### 26: 一般資産調査票
from P0000Common.models import RESTORATION             ### 27: 復旧事業工種
from P0000Common.models import KOKYO                   ### 28: 公共土木調査票
from P0000Common.models import KOEKI                   ### 29: 公益事業調査票
from P0000Common.models import TRANSACT                ### 40: 

from P0000Common.common_function import print_log

###############################################################################
### 関数名：index_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def index(request):
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw("""
            SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])

        #######################################################################
        ### レスポンスセット処理
        ### （１）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
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
### 関数名：category_view1
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def category_view1(request, category_code1):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数 category_code1 = {}'.format(category_code1), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        ### ken_list = KEN.objects.order_by('ken_code')[:]
        ### city_list = CITY.objects.filter(ken_code=ken_code).order_by('city_code')[:]
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_list': ken_list,
            'category_code1': category_code1,
        }
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view1()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view1()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def ken(request, ken_code):
### def ken_view(request, ken_code):
def ken_view(request, category_code1, ken_code):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_list': ken_list,
            'city_list': city_list,
            'ken_code': ken_code,
            'category_code1': category_code1,
        }
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：city_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def city(request, ken_code, city_code):
### def city_view(request, ken_code, city_code):
def city_view(request, category_code1, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 city_code = {}'.format(city_code), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_list': ken_list,
            'city_list': city_list,
            'ken_code': ken_code,
            'city_code': city_code,
            'category_code1': category_code1,
        }
        print_log('[INFO] P0400OnlineDisplay.city_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：category_view2
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def category(request, ken_code, city_code, category_code):
### def category_view(request, ken_code, city_code, category_code):
def category_view2(request, category_code1, ken_code, city_code, category_code2):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 city_code = {}'.format(city_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 category_code2 = {}'.format(category_code2), 'INFO')

        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = []
        city_list = []
        
        print_log('[INFO] SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)', 'INFO')
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        
        print_log('[INFO] SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)', 'INFO')
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### DBアクセス処理
        ### （１）DBにアクセスして、データを取得する。
        #######################################################################
        building_list = []
        kasen_kaigan_list = []
        suikei_list = []
        suikei_type_list = []
        kasen_list = []
        kasen_type_list = []
        cause_list = []
        underground_list = []
        usage_list = []
        flood_sediment_list = []
        gradient_list = []
        industry_list = []
        house_asset_list = []
        house_damage_list = []
        household_damage_list = []
        car_damage_list = []
        house_cost_list = []
        office_asset_list = []
        office_damage_list = []
        farmer_fisher_damage_list = []
        weather_list = []
        area_list = []
        ippan_list = []
        
        if category_code2 == "1":
            pass
        
        elif category_code2 == "2":
            print_log('[INFO] SELECT * FROM P0000COMMON_IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)', 'INFO')
            if ken_code == "0":
                if city_code == "0":
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM P0000COMMON_IPPAN ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [])
                else:
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM P0000COMMON_IPPAN WHERE CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [city_code, ])
            else:
                if city_code == "0":
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM P0000COMMON_IPPAN WHERE KEN_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, ])
                else:
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM P0000COMMON_IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, city_code, ])
            
        elif category_code2 == "3":
            pass
        
        elif category_code2 == "4":
            pass
        
        elif category_code2 == "5":
            pass
        
        elif category_code2 == "6":
            pass
        
        elif category_code2 == "7":
            pass
        
        elif category_code2 == "8":
            pass
        
        elif category_code2 == "9":
            pass
        
        elif category_code2 == "10":
            print_log('[INFO] SELECT * FROM P0000COMMON_BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)', 'INFO')
            building_list = BUILDING.objects.raw(""" 
                SELECT * FROM P0000COMMON_BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "11":
            pass
        
        elif category_code2 == "12":
            pass
        
        elif category_code2 == "13":
            print_log('[INFO] SELECT * FROM P0000COMMON_KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)', 'INFO')
            kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""
                SELECT * FROM P0000COMMON_KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "14":
            print_log('[INFO] SELECT * FROM P0000COMMON_SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)', 'INFO')
            suikei_list = SUIKEI.objects.raw(""" 
                SELECT * FROM P0000COMMON_SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "15":
            print_log('[INFO] SELECT * FROM P0000COMMON_SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)', 'INFO')
            suikei_type_list = SUIKEI_TYPE.objects.raw("""
                SELECT * FROM P0000COMMON_SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "16":
            print_log('[INFO] SELECT * FROM P0000COMMON_KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)', 'INFO')
            kasen_list = KASEN.objects.raw("""
                SELECT * FROM P0000COMMON_KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "17":
            print_log('[INFO] SELECT * FROM P0000COMMON_KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)', 'INFO')
            kasen_type_list = KASEN_TYPE.objects.raw("""
                SELECT * FROM P0000COMMON_KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "18":
            print_log('[INFO] SELECT * FROM P0000COMMON_CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)', 'INFO')
            cause_list = CAUSE.objects.raw("""
                SELECT * FROM P0000COMMON_CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "19":
            print_log('[INFO] SELECT * FROM P0000COMMON_UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)', 'INFO')
            underground_list = UNDERGROUND.objects.raw("""
                SELECT * FROM P0000COMMON_UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "20":
            print_log('[INFO] SELECT * FROM P0000COMMON_USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)', 'INFO')
            usage_list = USAGE.objects.raw("""
                SELECT * FROM P0000COMMON_USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "21":
            print_log('[INFO] SELECT * FROM P0000COMMON_FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)', 'INFO')
            flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""
                SELECT * FROM P0000COMMON_FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "22":
            print_log('[INFO] SELECT * FROM P0000COMMON_GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)', 'INFO')
            gradient_list = GRADIENT.objects.raw("""
                SELECT * FROM P0000COMMON_GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "23":
            print_log('[INFO] SELECT * FROM P0000COMMON_INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)', 'INFO')
            industry_list = INDUSTRY.objects.raw("""
                SELECT * FROM P0000COMMON_INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "24":
            print_log('[INFO] SELECT * FROM P0000COMMON_HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)', 'INFO')
            house_asset_list = HOUSE_ASSET.objects.raw("""
                SELECT * FROM P0000COMMON_HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "25":
            print_log('[INFO] SELECT * FROM P0000COMMON_HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)', 'INFO')
            house_damage_list = HOUSE_DAMAGE.objects.raw("""
                SELECT * FROM P0000COMMON_HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "26":
            print_log('[INFO] SELECT * FROM P0000COMMON_HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)', 'INFO')
            household_damage_list = HOUSEHOLD_DAMAGE.objects.raw("""
                SELECT * FROM P0000COMMON_HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "27":
            print_log('[INFO] SELECT * FROM P0000COMMON_CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)', 'INFO')
            car_damage_list = CAR_DAMAGE.objects.raw("""
                SELECT * FROM P0000COMMON_CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "28":
            print_log('[INFO] SELECT * FROM P0000COMMON_HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)', 'INFO')
            house_cost_list = HOUSE_COST.objects.raw("""
                SELECT * FROM P0000COMMON_HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "29":
            print_log('[INFO] SELECT * FROM P0000COMMON_OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)', 'INFO')
            office_asset_list = OFFICE_ASSET.objects.raw("""
                SELECT * FROM P0000COMMON_OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "30":
            print_log('[INFO] SELECT * FROM P0000COMMON_OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)', 'INFO')
            office_damage_list = OFFICE_DAMAGE.objects.raw("""
                SELECT * FROM P0000COMMON_OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "31":
            print_log('[INFO] SELECT * FROM P0000COMMON_OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)', 'INFO')
            office_cost_list = OFFICE_COST.objects.raw("""
                SELECT * FROM P0000COMMON_OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "32":
            print_log('[INFO] SELECT * FROM P0000COMMON_FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)', 'INFO')
            farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.raw("""
                SELECT * FROM P0000COMMON_FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "33":
            print_log('[INFO] SELECT * FROM P0000COMMON_WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)', 'INFO')
            weather_list = WEATHER.objects.raw("""
                SELECT * FROM P0000COMMON_WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)
                """, [])
            
        elif category_code2 == "34":
            print_log('[INFO] SELECT * FROM P0000COMMON_AREA ORDER BY CAST(AREA_ID AS INTEGER)', 'INFO')
            area_list = AREA.objects.raw("""
                SELECT * FROM P0000COMMON_AREA ORDER BY CAST(AREA_ID AS INTEGER)
                """, [])
            
        else:
            pass
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'ken_code': ken_code,
            'city_code': city_code,
            'category_code1': category_code1,
            'category_code2': category_code2,
            'building_list': building_list,
            'ken_list': ken_list,
            'city_list': city_list,
            'kasen_kaigan_list': kasen_kaigan_list,
            'suikei_list': suikei_list,
            'suikei_type_list': suikei_type_list,
            'kasen_list': kasen_list,
            'kasen_type_list': kasen_type_list,
            'cause_list': cause_list,
            'underground_list': underground_list,
            'usage_list': usage_list,
            'flood_sediment_list': flood_sediment_list,
            'gradient_list': gradient_list,
            'industry_list': industry_list,
            'house_asset_list': house_asset_list,
            'house_damage_list': house_damage_list,
            'household_damage_list': household_damage_list,
            'car_damage_list': car_damage_list,
            'house_cost_list': house_cost_list,
            'office_asset_list': office_asset_list,
            'office_damage_list': office_damage_list,
            'farmer_fisher_damage_list': farmer_fisher_damage_list,
            'weather_list': weather_list,
            'area_list': area_list,
            'ippan_list': ippan_list,
        }
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view2()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view2()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
