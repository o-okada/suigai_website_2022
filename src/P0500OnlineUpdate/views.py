#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0500OnlineUpdate/views.py
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
        print_log('[INFO] P0500OnlineUpdate.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.index_view()関数 request = {}'.format(request.method), 'INFO')
        
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
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_list': ken_list,
        }
        print_log('[INFO] P0500OnlineUpdate.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def ken(request, ken_code):
def ken_view(request, ken_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        
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
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_code': ken_code,
            'ken_list': ken_list,
            'city_list': city_list,
        }
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：city_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def city(request, ken_code, city_code):    
def city_view(request, ken_code, city_code):    
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 city_code = {}'.format(city_code), 'INFO')
        
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
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_code': ken_code,
            'city_code': city_code,
            'ken_list': ken_list,
            'city_list': city_list,
        }
        print_log('[INFO] P0500OnlineUpdate.city_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：category_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def category(request, ken_code, city_code, category_code):
def category_view(request, category_code, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 category_code = {}'.format(category_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 city_code = {}'.format(city_code), 'INFO')
        
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
        suigai_list = []                                                       ### 200: 
        weather_list = []                                                      ### 201: 
        area_list = []                                                         ### 202: 
        ippan_list = []                                                        ### 203: 
        ### ippan_city_list                                                    ### 204: 
        ### ippan_ken_list                                                     ### 205: 
        ### kokyo_list = []                                                    ### 206: 
        ### koeki_list = []                                                    ### 207: 
        
        if category_code == "0":
            pass
        
        elif category_code == "200":
            suigai_list = SUIGAI.objects.raw("""
                SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)
                """, [])
        
        elif category_code == "201":
            weather_list = WEATHER.objects.raw("""
                SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)
                """, [])

        elif category_code == "202":
            area_list = AREA.objects.raw("""
                SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)
                """, [])

        elif category_code == "203":
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
                        """, [ken_code ])        
                else:
                    ippan_list = IPPAN.objects.raw(""" 
                        SELECT * FROM IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                        """, [ken_code, city_code, ])    
                
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'category_code': category_code,
            'ken_code': ken_code,
            'city_code': city_code,
            'ken_list': ken_list,
            'city_list': city_list,
            'suigai_list': suigai_list,
            'weather_list': weather_list,
            'area_list': area_list,
            'ippan_list': ippan_list,
        }
        print_log('[INFO] P0500OnlineUpdate.category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
