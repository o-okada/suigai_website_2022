#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0500OnlineUpdate/views.py
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
        print_log('[INFO] P0500OnlineUpdate.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.index_view()関数 request = {}'.format(request.method), 'INFO')
        
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
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.ken_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        
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
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_list': ken_list,
            'city_list': city_list,
            'ken_code': ken_code,
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
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.city_view()関数 city_code = {}'.format(city_code), 'INFO')
        
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
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_list': ken_list,
            'city_list': city_list,
            'ken_code': ken_code,
            'city_code': city_code,
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
def category_view(request, ken_code, city_code, category_code):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 city_code = {}'.format(city_code), 'INFO')
        print_log('[INFO] P0500OnlineUpdate.category_view()関数 category_code = {}'.format(category_code), 'INFO')
        
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
                    """, [ken_code ])        
            else:
                ippan_list = IPPAN.objects.raw(""" 
                    SELECT * FROM P0000COMMON_IPPAN WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(IPPAN_ID AS INTEGER)
                    """, [ken_code, city_code, ])    
                
        #######################################################################
        ### レスポンスセット処理
        ### （１）コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0500OnlineUpdate/index.html')
        context = {
            'ken_list': ken_list,
            'city_list': city_list,
            'ippan_list': ippan_list,
            'ken_code': ken_code,
            'city_code': city_code,
            'category_code': category_code,
        }
        print_log('[INFO] P0500OnlineUpdate.category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0500OnlineUpdate.category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
