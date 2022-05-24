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

from P0000Common.models import BUILDING                ### 001: 建物区分
from P0000Common.models import KEN                     ### 002: 都道府県
from P0000Common.models import CITY                    ### 003: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 004: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 005: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 006: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 007: 河川（河川・海岸）
from P0000Common.models import KASEN_TYPE              ### 008: 河川種別（河川・海岸種別）
from P0000Common.models import CAUSE                   ### 009: 水害原因
from P0000Common.models import UNDERGROUND             ### 010: 地上地下区分
from P0000Common.models import USAGE                   ### 011: 地下空間の利用形態
from P0000Common.models import FLOOD_SEDIMENT          ### 012: 浸水土砂区分
from P0000Common.models import GRADIENT                ### 013: 地盤勾配区分
from P0000Common.models import INDUSTRY                ### 014: 産業分類
from P0000Common.models import RESTORATION             ### 015: 復旧事業工種
from P0000Common.models import HOUSE_ASSET             ### 100: 県別家屋評価額
from P0000Common.models import HOUSE_DAMAGE            ### 101: 家屋被害率
from P0000Common.models import HOUSEHOLD_DAMAGE        ### 102: 家庭用品自動車以外被害率
from P0000Common.models import CAR_DAMAGE              ### 103: 家庭用品自動車被害率
from P0000Common.models import HOUSE_COST              ### 104: 家庭応急対策費
from P0000Common.models import OFFICE_ASSET            ### 105: 産業分類別資産額
from P0000Common.models import OFFICE_DAMAGE           ### 106: 事業所被害率
from P0000Common.models import OFFICE_COST             ### 107: 事業所営業停止損失
from P0000Common.models import FARMER_FISHER_DAMAGE    ### 108: 農漁家被害率
from P0000Common.models import SUIGAI                  ### 200: 水害
from P0000Common.models import WEATHER                 ### 201: 異常気象（ほぼ、水害）
from P0000Common.models import AREA                    ### 202: 区域
from P0000Common.models import IPPAN                   ### 203: 一般資産調査票
### from P0000Common.models import IPPAN_CITY          ### 204: 
### from P0000Common.models import IPPAN_KEN           ### 205: 
from P0000Common.models import KOKYO                   ### 206: 公共土木調査票
from P0000Common.models import KOEKI                   ### 207: 公益事業調査票
from P0000Common.models import TRANSACT                ###  

from P0000Common.common import print_log

###############################################################################
### 関数名：index_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view1()関数 category_code1 = {}'.format(category_code1), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ### ken_list = KEN.objects.order_by('ken_code')[:]
        ### city_list = CITY.objects.filter(ken_code=ken_code).order_by('city_code')[:]
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        
        #######################################################################
        ### レスポンスセット処理(0020)
        ### (1)コンテキストを設定して、レスポンスをブラウザに戻す。
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
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.ken_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### レスポンスセット処理(0020)
        ### (1)コンテキストを設定して、レスポンスをブラウザに戻す。
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
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.city_view()関数 city_code = {}'.format(city_code), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### レスポンスセット処理(0020)
        ### (1)コンテキストを設定して、レスポンスをブラウザに戻す。
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
def category_view2(request, category_code1, category_code2, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 category_code1 = {}'.format(category_code1), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 category_code2 = {}'.format(category_code2), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数 city_code = {}'.format(city_code), 'INFO')

        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = []
        city_list = []
        
        print_log('[INFO] SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)', 'INFO')
        ken_list = KEN.objects.raw(""" 
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
        
        print_log('[INFO] SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)', 'INFO')
        if ken_code == "0":
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [])
        else:
            city_list = CITY.objects.raw(""" 
                SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
        
        #######################################################################
        ### DBアクセス処理(0020)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        building_list = []                                                     ### 001: 
        ### ken_list                                                           ### 002: 
        ### city_list                                                          ### 003: 
        kasen_kaigan_list = []                                                 ### 004: 
        suikei_list = []                                                       ### 005: 
        suikei_type_list = []                                                  ### 006: 
        kasen_list = []                                                        ### 007: 
        kasen_type_list = []                                                   ### 008: 
        cause_list = []                                                        ### 009: 
        underground_list = []                                                  ### 010: 
        usage_list = []                                                        ### 011: 
        flood_sediment_list = []                                               ### 012: 
        gradient_list = []                                                     ### 013: 
        industry_list = []                                                     ### 014: 
        restoration_list = []                                                  ### 015: 
        house_asset_list = []                                                  ### 100: 
        house_damage_list = []                                                 ### 101: 
        household_damage_list = []                                             ### 102: 
        car_damage_list = []                                                   ### 103: 
        house_cost_list = []                                                   ### 104: 
        office_asset_list = []                                                 ### 105: 
        office_damage_list = []                                                ### 106: 
        office_cost_list = []                                                  ### 107: 
        farmer_fisher_damage_list = []                                         ### 108: 
        
        suigai_list = []                                                       ### 200: 
        weather_list = []                                                      ### 201: 
        area_list = []                                                         ### 202: 
        ippan_list = []                                                        ### 203: 
        ### ippan_city_list                                                    ### 204: 
        ### ippan_ken_list                                                     ### 205: 
        kokyo_list = []                                                        ### 206: 
        koeki_list = []                                                        ### 207: 
        
        if category_code2 == "0":
            pass
        
        elif category_code2 == "1":
            print_log('[INFO] SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)', 'INFO')
            building_list = BUILDING.objects.raw(""" 
                SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "2":
            pass
        
        elif category_code2 == "3":
            pass
        
        elif category_code2 == "4":
            print_log('[INFO] SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)', 'INFO')
            kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""
                SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "5":
            print_log('[INFO] SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)', 'INFO')
            suikei_list = SUIKEI.objects.raw(""" 
                SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "6":
            print_log('[INFO] SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)', 'INFO')
            suikei_type_list = SUIKEI_TYPE.objects.raw("""
                SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "7":
            print_log('[INFO] SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)', 'INFO')
            kasen_list = KASEN.objects.raw("""
                SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "8":
            print_log('[INFO] SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)', 'INFO')
            kasen_type_list = KASEN_TYPE.objects.raw("""
                SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "9":
            print_log('[INFO] SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)', 'INFO')
            cause_list = CAUSE.objects.raw("""
                SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "10":
            print_log('[INFO] SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)', 'INFO')
            underground_list = UNDERGROUND.objects.raw("""
                SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "11":
            print_log('[INFO] SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)', 'INFO')
            usage_list = USAGE.objects.raw("""
                SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "12":
            print_log('[INFO] SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)', 'INFO')
            flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""
                SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "13":
            print_log('[INFO] SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)', 'INFO')
            gradient_list = GRADIENT.objects.raw("""
                SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "14":
            print_log('[INFO] SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)', 'INFO')
            industry_list = INDUSTRY.objects.raw("""
                SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)
                """, [])

        elif category_code2 == "15":
            print_log('[INFO] SELECT * FROM RESTORATION ORDER BY CAST(RESTORATION_CODE AS INTEGER)', 'INFO')
            restoration_list = RESTORATION.objects.raw("""
                SELECT * FROM RESTORATION ORDER BY CAST(RESTORATION_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "100":
            print_log('[INFO] SELECT * FROM HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)', 'INFO')
            house_asset_list = HOUSE_ASSET.objects.raw("""
                SELECT * FROM HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "101":
            print_log('[INFO] SELECT * FROM HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)', 'INFO')
            house_damage_list = HOUSE_DAMAGE.objects.raw("""
                SELECT * FROM HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "102":
            print_log('[INFO] SELECT * FROM HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)', 'INFO')
            household_damage_list = HOUSEHOLD_DAMAGE.objects.raw("""
                SELECT * FROM HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "103":
            print_log('[INFO] SELECT * FROM CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)', 'INFO')
            car_damage_list = CAR_DAMAGE.objects.raw("""
                SELECT * FROM CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "104":
            print_log('[INFO] SELECT * FROM HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)', 'INFO')
            house_cost_list = HOUSE_COST.objects.raw("""
                SELECT * FROM HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "105":
            print_log('[INFO] SELECT * FROM OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)', 'INFO')
            office_asset_list = OFFICE_ASSET.objects.raw("""
                SELECT * FROM OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "106":
            print_log('[INFO] SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)', 'INFO')
            office_damage_list = OFFICE_DAMAGE.objects.raw("""
                SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "107":
            print_log('[INFO] SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)', 'INFO')
            office_cost_list = OFFICE_COST.objects.raw("""
                SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)
                """, [])
            
        elif category_code2 == "108":
            print_log('[INFO] SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)', 'INFO')
            farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.raw("""
                SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)
                """, [])

        elif category_code2 == "200":
            print_log('[INFO] SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)', 'INFO')
            suigai_list = SUIGAI.objects.raw("""
                SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)
                """, [])
            
        elif category_code2 == "201":
            print_log('[INFO] SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)', 'INFO')
            weather_list = WEATHER.objects.raw("""
                SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)
                """, [])
            
        elif category_code2 == "202":
            print_log('[INFO] SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)', 'INFO')
            area_list = AREA.objects.raw("""
                SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)
                """, [])

        elif category_code2 == "203":
            print_log('[INFO] SELECT * FROM IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)', 'INFO')
            if ken_code == "0":
                if city_code == "0":
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM IPPAN ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [])
                else:
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM IPPAN WHERE CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [city_code, ])
            else:
                if city_code == "0":
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM IPPAN WHERE KEN_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, ])
                else:
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, city_code, ])

        elif category_code2 == "204":
            pass

        elif category_code2 == "205":
            pass

        elif category_code2 == "206":
            pass

        elif category_code2 == "207":
            pass
            
        else:
            pass
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
            'category_code1': category_code1,
            'category_code2': category_code2,
            'ken_code': ken_code,
            'city_code': city_code,
            
            'building_list': building_list,                                    ### 001: 
            'ken_list': ken_list,                                              ### 002: 
            'city_list': city_list,                                            ### 003: 
            'kasen_kaigan_list': kasen_kaigan_list,                            ### 004: 
            'suikei_list': suikei_list,                                        ### 005: 
            'suikei_type_list': suikei_type_list,                              ### 006: 
            'kasen_list': kasen_list,                                          ### 007: 
            'kasen_type_list': kasen_type_list,                                ### 008: 
            'cause_list': cause_list,                                          ### 009: 
            'underground_list': underground_list,                              ### 010: 
            'usage_list': usage_list,                                          ### 011: 
            'flood_sediment_list': flood_sediment_list,                        ### 012: 
            'gradient_list': gradient_list,                                    ### 013: 
            'industry_list': industry_list,                                    ### 014: 
            'restoration_list': restoration_list,                              ### 015: 
            'house_asset_list': house_asset_list,                              ### 100: 
            'house_damage_list': house_damage_list,                            ### 101: 
            'household_damage_list': household_damage_list,                    ### 102: 
            'car_damage_list': car_damage_list,                                ### 103: 
            'house_cost_list': house_cost_list,                                ### 104: 
            'office_asset_list': office_asset_list,                            ### 105: 
            'office_damage_list': office_damage_list,                          ### 106: 
            'office_cost_list': office_cost_list,                              ### 107: 
            'farmer_fisher_damage_list': farmer_fisher_damage_list,            ### 108: 
            'suigai_list': suigai_list,                                        ### 200: 
            'weather_list': weather_list,                                      ### 201: 
            'area_list': area_list,                                            ### 202: 
            'ippan_list': ippan_list,                                          ### 203: 
        }
        print_log('[INFO] P0400OnlineDisplay.category_view2()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view2()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.category_view2()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
