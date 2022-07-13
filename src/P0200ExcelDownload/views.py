#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0200ExcelDownload/views.py
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
### from P0000Common.models import CITY_VIEW           ### 1025: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 1030: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 1040: 水系（水系・沿岸）
### from P0000Common.models import SUIKEI_VIEW         ### 1045: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 1050: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 1060: 河川（河川・海岸）
### from P0000Common.models import KASEN_VIEW          ### 1065: 河川（河川・海岸）
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
from P0000Common.models import HOUSE_CLEAN             ### 2030: 家庭応急対策費_清掃日数、清掃労働単価

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

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 集計データ_集計結果

from P0000Common.common import print_log

###############################################################################
### 関数名：index_view(request)
### urlpattern：path('', views.index_view, name='index_view')
### template：P0200ExcelDownload/index.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.index_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、都道府県データを取得する。
        ### (2)DBにアクセスして、市区町村データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.index_view()関数 STEP 2/4.', 'INFO')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        city_list01 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['01', ])
        city_list02 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['02', ])
        city_list03 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['03', ])
        city_list04 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['04', ])
        city_list05 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['05', ])
        city_list06 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['06', ])
        city_list07 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['07', ])
        city_list08 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['08', ])
        city_list09 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['09', ])
        city_list10 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['10', ])
        city_list11 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['11', ])
        city_list12 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['12', ])
        city_list13 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['13', ])
        city_list14 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['14', ])
        city_list15 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['15', ])
        city_list16 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['16', ])
        city_list17 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['17', ])
        city_list18 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['18', ])
        city_list19 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['19', ])
        city_list20 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['20', ])
        city_list21 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['21', ])
        city_list22 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['22', ])
        city_list23 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['23', ])
        city_list24 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['24', ])
        city_list25 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['25', ])
        city_list26 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['26', ])
        city_list27 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['27', ])
        city_list28 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['28', ])
        city_list29 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['29', ])
        city_list30 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['30', ])
        city_list31 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['31', ])
        city_list32 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['32', ])
        city_list33 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['33', ])
        city_list34 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['34', ])
        city_list35 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['35', ])
        city_list36 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['36', ])
        city_list37 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['37', ])
        city_list38 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['38', ])
        city_list39 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['39', ])
        city_list40 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['40', ])
        city_list41 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['41', ])
        city_list42 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['42', ])
        city_list43 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['43', ])
        city_list44 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['44', ])
        city_list45 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['45', ])
        city_list46 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['46', ])
        city_list47 = CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", ['47', ])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.index_view()関数 STEP 3/4.', 'INFO')
        template = loader.get_template('P0200ExcelDownload/index.html')
        context = {
            'ken_list': ken_list,
            'city_list01': city_list01,
            'city_list02': city_list02,
            'city_list03': city_list03,
            'city_list04': city_list04,
            'city_list05': city_list05,
            'city_list06': city_list06,
            'city_list07': city_list07,
            'city_list08': city_list08,
            'city_list09': city_list09,
            'city_list10': city_list10,
            'city_list11': city_list11,
            'city_list12': city_list12,
            'city_list13': city_list13,
            'city_list14': city_list14,
            'city_list15': city_list15,
            'city_list16': city_list16,
            'city_list17': city_list17,
            'city_list18': city_list18,
            'city_list19': city_list19,
            'city_list20': city_list20,
            'city_list21': city_list21,
            'city_list22': city_list22,
            'city_list23': city_list23,
            'city_list24': city_list24,
            'city_list25': city_list25,
            'city_list26': city_list26,
            'city_list27': city_list27,
            'city_list28': city_list28,
            'city_list29': city_list29,
            'city_list30': city_list30,
            'city_list31': city_list31,
            'city_list32': city_list32,
            'city_list33': city_list33,
            'city_list34': city_list34,
            'city_list35': city_list35,
            'city_list36': city_list36,
            'city_list37': city_list37,
            'city_list38': city_list38,
            'city_list39': city_list39,
            'city_list40': city_list40,
            'city_list41': city_list41,
            'city_list42': city_list42,
            'city_list43': city_list43,
            'city_list44': city_list44,
            'city_list45': city_list45,
            'city_list46': city_list46,
            'city_list47': city_list47,
        }
        print_log('[INFO] P0200ExcelDownload.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：building_view(request, lock)
### 1000：建物区分
### urlpattern：path('building/', views.building_view, name='building_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def building_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、建物区分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.building_view()関数 STEP 2/4.', 'INFO')
        building_list = BUILDING.objects.raw("""SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
        
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.building_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_building.xlsx'
        download_file_path = 'static/download_building.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '建物区分'
        ws.cell(row=1, column=1).value = '建物区分コード'
        ws.cell(row=1, column=2).value = '建物区分名'
        
        if building_list:
            for i, building in enumerate(building_list):
                ws.cell(row=i+2, column=1).value = building.building_code
                ws.cell(row=i+2, column=2).value = building.building_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.building_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="building.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.building_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.building_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_view(request, lock)
### 1010：都道府県
### urlpattern：path('ken/', views.ken_view, name='ken_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ken_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、都道府県データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 STEP 2/4.', 'INFO')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ken.xlsx'
        download_file_path = 'static/download_ken.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '都道府県'
        ws.cell(row=1, column=1).value = '都道府県コード'
        ws.cell(row=1, column=2).value = '都道府県名'
        
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws.cell(row=i+2, column=1).value = ken.ken_code
                ws.cell(row=i+2, column=2).value = ken.ken_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ken.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：city_view(request, lock)
### 1020：市区町村
### urlpattern：path('city/', views.city_view, name='city_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def city_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、市区町村データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 2/4.', 'INFO')
        city_list = CITY.objects.raw("""
            SELECT 
                CT1.city_code AS city_code, 
                CT1.city_name AS city_name, 
                CT1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                CT1.city_population AS city_population, 
                CT1.city_area AS city_area 
            FROM CITY CT1 
            LEFT JOIN KEN KE1 ON CT1.ken_code=KE1.ken_code 
            ORDER BY CAST(CT1.city_code AS INTEGER)""", [])
        
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_city.xlsx'
        download_file_path = 'static/download_city.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '市区町村'
        ws.cell(row=1, column=1).value = '市区町村コード'
        ws.cell(row=1, column=2).value = '市区町村名'
        ws.cell(row=1, column=3).value = '都道府県コード'
        ws.cell(row=1, column=4).value = '都道府県名'
        ws.cell(row=1, column=5).value = '市区町村人口'
        ws.cell(row=1, column=6).value = '市区町村面積'
        
        if city_list:
            for i, city in enumerate(city_list):
                ws.cell(row=i+2, column=1).value = city.city_code
                ws.cell(row=i+2, column=2).value = city.city_name
                ws.cell(row=i+2, column=3).value = city.ken_code
                ws.cell(row=i+2, column=4).value = city.ken_name
                ws.cell(row=i+2, column=5).value = city.city_population
                ws.cell(row=i+2, column=6).value = city.city_area
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="city.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：kasen_kaigan_view(request, lock)
### 1030：水害発生地点工種（河川海岸区分）
### urlpattern：path('kasen_kaigan/', views.kasen_kaigan_view, name='kasen_kaigan_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_kaigan_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、水害発生地点工種（河川海岸区分）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 STEP 2/4.', 'INFO')
        kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_kasen_kaigan.xlsx'
        download_file_path = 'static/download_kasen_kaigan.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '河川海岸区分'
        ws.cell(row=1, column=1).value = '河川海岸区分コード'
        ws.cell(row=1, column=2).value = '河川海岸区分名'
        
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws.cell(row=i+2, column=1).value = kasen_kaigan.kasen_kaigan_code
                ws.cell(row=i+2, column=2).value = kasen_kaigan.kasen_kaigan_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_kaigan.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_kaigan_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_kaigan_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：suikei_view(request, lock)
### 1040：水系（水系・沿岸）
### urlpattern：path('suikei/', views.suikei_view, name='suikei_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suikei_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、水系（水系・沿岸）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 2/4.', 'INFO')
        suikei_list = SUIKEI.objects.raw("""
            SELECT 
                SK1.suikei_code AS suikei_code, 
                SK1.suikei_name AS suikei_name, 
                SK1.suikei_type_code AS suikei_type_code, 
                ST1.suikei_type_name AS suikei_type_name 
            FROM SUIKEI SK1 
            LEFT JOIN SUIKEI_TYPE ST1 ON SK1.suikei_type_code=ST1.suikei_type_code 
            ORDER BY CAST(SK1.suikei_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_suikei.xlsx'
        download_file_path = 'static/download_suikei.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '水系'
        ws.cell(row=1, column=1).value = '水系コード'
        ws.cell(row=1, column=2).value = '水系名'
        ws.cell(row=1, column=3).value = '水系種別コード'
        ws.cell(row=1, column=4).value = '水系種別名'
        
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws.cell(row=i+2, column=1).value = suikei.suikei_code
                ws.cell(row=i+2, column=2).value = suikei.suikei_name
                ws.cell(row=i+2, column=3).value = suikei.suikei_type_code
                ws.cell(row=i+2, column=4).value = suikei.suikei_type_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suikei_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suikei_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：suikei_type_view(request, lock)
### 1050：水系種別（水系・沿岸種別）
### urlpattern：path('suikei_type/', views.suikei_type_view, name='suikei_type_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suikei_type_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、水系種別（水系・沿岸種別）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 STEP 2/4.', 'INFO')
        suikei_type_list = SUIKEI_TYPE.objects.raw("""SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_suikei_type.xlsx'
        download_file_path = 'static/download_suikei_type.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '水系種別'
        ws.cell(row=1, column=1).value = '水系種別コード'
        ws.cell(row=1, column=2).value = '水系種別名'
        
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws.cell(row=i+2, column=1).value = suikei_type.suikei_type_code
                ws.cell(row=i+2, column=2).value = suikei_type.suikei_type_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei_type.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suikei_type_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suikei_type_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：kasen_view(request, lock)
### 1060：河川（河川・海岸）
### urlpattern：path('kasen/', views.kasen_view, name='kasen_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、河川（河川・海岸）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 2/4.', 'INFO')
        kasen_list = KASEN.objects.raw("""
            SELECT 
                KA1.kasen_code AS kasen_code, 
                KA1.kasen_name AS kasen_name, 
                KA1.kasen_type_code AS kasen_type_code, 
                KT1.kasen_type_name AS kasen_type_name, 
                KA1.suikei_code AS suikei_code, 
                SK1.suikei_name AS suikei_name 
            FROM KASEN KA1 
            LEFT JOIN KASEN_TYPE KT1 ON KA1.kasen_type_code=KT1.kasen_type_code 
            LEFT JOIN SUIKEI SK1 ON KA1.suikei_code=SK1.suikei_code 
            ORDER BY CAST(KA1.kasen_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_kasen.xlsx'
        download_file_path = 'static/download_kasen.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '河川'
        ws.cell(row=1, column=1).value = '河川コード'
        ws.cell(row=1, column=2).value = '河川名'
        ws.cell(row=1, column=3).value = '河川種別コード'
        ws.cell(row=1, column=4).value = '河川種別名'
        ws.cell(row=1, column=5).value = '水系コード'
        ws.cell(row=1, column=6).value = '水系名'
        
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws.cell(row=i+2, column=1).value = kasen.kasen_code
                ws.cell(row=i+2, column=2).value = kasen.kasen_name
                ws.cell(row=i+2, column=3).value = kasen.kasen_type_code
                ws.cell(row=i+2, column=4).value = kasen.kasen_type_name
                ws.cell(row=i+2, column=5).value = kasen.suikei_code
                ws.cell(row=i+2, column=6).value = kasen.suikei_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：kasen_type_view(request, lock)
### 1070：河川種別（河川・海岸種別）
### urlpattern：path('kasen_type/', views.kasen_type_view, name='kasen_type_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_type_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、河川種別（河川・海岸種別）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 STEP 2/4.', 'INFO')
        kasen_type_list = KASEN_TYPE.objects.raw("""SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_kasen_type.xlsx'
        download_file_path = 'static/download_kasen_type.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '河川種別'
        ws.cell(row=1, column=1).value = '河川種別コード'
        ws.cell(row=1, column=2).value = '河川種別名'
        
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws.cell(row=i+2, column=1).value = kasen_type.kasen_type_code
                ws.cell(row=i+2, column=2).value = kasen_type.kasen_type_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_type.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_type_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kasen_type_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：cause_view(request, lock)
### 1080：水害原因
### urlpattern：path('cause/', views.cause_view, name='cause_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def cause_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、水害原因データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 STEP 2/4.', 'INFO')
        cause_list = CAUSE.objects.raw("""SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_cause.xlsx'
        download_file_path = 'static/download_cause.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '水害原因'
        ws.cell(row=1, column=1).value = '水害原因コード'
        ws.cell(row=1, column=2).value = '水害原因名'
        
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws.cell(row=i+2, column=1).value = cause.cause_code
                ws.cell(row=i+2, column=2).value = cause.cause_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cause.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.cause_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.cause_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：underground_view(request, lock)
### 1090：地上地下区分
### urlpattern：path('underground/', views.underground_view, name='underground_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def underground_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、地上地下区分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 STEP 2/4.', 'INFO')
        underground_list = UNDERGROUND.objects.raw("""SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_underground.xlsx'
        download_file_path = 'static/download_underground.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '地上地下区分'
        ws.cell(row=1, column=1).value = '地上地下区分コード'
        ws.cell(row=1, column=2).value = '地上地下区分名'
        
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws.cell(row=i+2, column=1).value = underground.underground_code
                ws.cell(row=i+2, column=2).value = underground.underground_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="underground.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.underground_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.underground_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：usage_view(request, lock)
### 1100：地下空間の利用形態
### urlpattern：path('usage/', views.usage_view, name='usage_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def usage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、地下空間の利用形態データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 STEP 2/4.', 'INFO')
        usage_list = USAGE.objects.raw("""SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_usage.xlsx'
        download_file_path = 'static/download_usage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '地下空間の利用形態'
        ws.cell(row=1, column=1).value = '地下空間の利用形態コード'
        ws.cell(row=1, column=2).value = '地下空間の利用形態名'
        
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws.cell(row=i+2, column=1).value = usage.usage_code
                ws.cell(row=i+2, column=2).value = usage.usage_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="usage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.usage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.usage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：flood_sediment_view(request, lock)
### 1110：浸水土砂区分
### urlpattern：path('flood_sediment/', views.flood_sediment_view, name='flood_sediment_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def flood_sediment_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、浸水土砂区分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 STEP 2/4.', 'INFO')
        flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_flood_sediment.xlsx'
        download_file_path = 'static/download_flood_sediment.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '浸水土砂区分'
        ws.cell(row=1, column=1).value = '浸水土砂区分コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分名'
        
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws.cell(row=i+2, column=1).value = flood_sediment.flood_sediment_code
                ws.cell(row=i+2, column=2).value = flood_sediment.flood_sediment_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="flood_sediment.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.flood_sediment_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.flood_sediment_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：gradient_view(request, lock)
### 1120：地盤勾配区分
### urlpattern：path('gradient/', views.gradient_view, name='gradient_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def gradient_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、地盤勾配区分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 STEP 2/4.', 'INFO')
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_gradient.xlsx'
        download_file_path = 'static/download_gradient.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '地盤勾配区分'
        ws.cell(row=1, column=1).value = '地盤勾配区分コード'
        ws.cell(row=1, column=2).value = '地盤勾配区分名'
        
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws.cell(row=i+2, column=1).value = gradient.gradient_code
                ws.cell(row=i+2, column=2).value = gradient.gradient_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="gradient.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.gradient_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.gradient_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：industry_view(request, lock)
### 1130：産業分類
### urlpattern：path('industry/', views.industry_view, name='industry_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def industry_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、産業分類データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 STEP 2/4.', 'INFO')
        industry_list = INDUSTRY.objects.raw("""SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_industry.xlsx'
        download_file_path = 'static/download_industry.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '産業分類'
        ws.cell(row=1, column=1).value = '産業分類コード'
        ws.cell(row=1, column=2).value = '産業分類名'
        
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws.cell(row=i+2, column=1).value = industry.industry_code
                ws.cell(row=i+2, column=2).value = industry.industry_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="industry.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.industry_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.industry_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_asset_view(request, lock)
### 2000：家屋評価額
### urlpattern：path('house_asset/', views.house_asset_view, name='house_asset_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、県別家屋評価額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 2/4.', 'INFO')
        house_asset_list = HOUSE_ASSET.objects.raw("""
            SELECT 
                HA1.house_asset_code AS house_asset_code, 
                HA1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                HA1.house_asset AS house_asset 
            FROM HOUSE_ASSET HA1 
            LEFT JOIN KEN KE1 ON HA1.ken_code=KE1.ken_code 
            ORDER BY CAST(HA1.house_asset_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_asset.xlsx'
        download_file_path = 'static/download_house_asset.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家屋被害'
        ws.cell(row=1, column=1).value = '家屋被害コード'
        ws.cell(row=1, column=2).value = '都道府県コード'
        ws.cell(row=1, column=3).value = '都道府県名'
        ws.cell(row=1, column=4).value = '家屋評価額'
        
        if house_asset_list:
            for i, house_asset in enumerate(house_asset_list):
                ws.cell(row=i+2, column=1).value = house_asset.house_asset_code
                ws.cell(row=i+2, column=2).value = house_asset.ken_code
                ws.cell(row=i+2, column=3).value = house_asset.ken_name
                ws.cell(row=i+2, column=4).value = house_asset.house_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_asset.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_asset_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_asset_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_rate_view(request, lock)
### 2010：家屋被害率
### urlpattern：path('house_rate/', views.house_rate_view, name='house_rate_view'
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_rate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家屋被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 STEP 2/4.', 'INFO')
        house_rate_list = HOUSE_RATE.objects.raw("""
            SELECT 
                HR1.house_rate_code AS house_rate_code, 
                HR1.flood_sediment_code AS flood_sediment_code, 
                flood_sediment_name AS flood_sediment_name, 
                HR1.gradient_code AS gradient_code, 
                gradient_name AS gradient_name, 
                HR1.house_rate_lv00 AS house_rate_lv00, 
                HR1.house_rate_lv00_50 AS house_rate_lv00_50, 
                HR1.house_rate_lv50_100 AS house_rate_lv50_100, 
                HR1.house_rate_lv100_200 AS house_rate_lv100_200, 
                HR1.house_rate_lv200_300 AS house_rate_lv200_300 
            FROM HOUSE_RATE HR1 
            LEFT JOIN FLOOD_SEDIMENT FS1 ON HR1.flood_sediment_code=FS1.flood_sediment_code 
            LEFT JOIN GRADIENT GR1 ON HR1.gradient_code=GR1.gradient_code 
            ORDER BY CAST(HR1.house_rate_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_rate.xlsx'
        download_file_path = 'static/download_house_rate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家屋被害率'
        ws.cell(row=1, column=1).value = '家屋被害率コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分コード'
        ws.cell(row=1, column=3).value = '浸水土砂区分名'
        ws.cell(row=1, column=4).value = '地盤勾配区分コード'
        ws.cell(row=1, column=5).value = '地盤勾配区分名'
        ws.cell(row=1, column=6).value = '家屋被害率_床下'
        ws.cell(row=1, column=7).value = '家屋被害率_0から50cm未満'
        ws.cell(row=1, column=8).value = '家屋被害率_50から100cm未満'
        ws.cell(row=1, column=9).value = '家屋被害率_100から200cm未満'
        ws.cell(row=1, column=10).value = '家屋被害率_200から300cm未満'
        ws.cell(row=1, column=11).value = '家屋被害率_300cm以上'
        
        if house_rate_list:
            for i, house_rate in enumerate(house_rate_list):
                ws.cell(row=i+2, column=1).value = house_rate.house_rate_code
                ws.cell(row=i+2, column=2).value = house_rate.flood_sediment_code
                ws.cell(row=i+2, column=3).value = house_rate.flood_sediment_name
                ws.cell(row=i+2, column=4).value = house_rate.gradient_code
                ws.cell(row=i+2, column=5).value = house_rate.gradient_name
                ws.cell(row=i+2, column=6).value = house_rate.house_rate_lv00
                ws.cell(row=i+2, column=7).value = house_rate.house_rate_lv00_50
                ws.cell(row=i+2, column=8).value = house_rate.house_rate_lv50_100
                ws.cell(row=i+2, column=9).value = house_rate.house_rate_lv100_200
                ws.cell(row=i+2, column=10).value = house_rate.house_rate_lv200_300
                ws.cell(row=i+2, column=11).value = house_rate.house_rate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_rate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_rate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_rate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_rate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_alt_view(request, lock)
### 2020：家庭応急対策費_代替活動費
### urlpattern：path('house_alt/', views.house_alt_view, name='house_alt_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_alt_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家庭応急対策費データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 STEP 2/4.', 'INFO')
        house_alt_list = HOUSE_ALT.objects.raw("""SELECT * FROM HOUSE_ALT ORDER BY CAST(HOUSE_ALT_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_alt.xlsx'
        download_file_path = 'static/download_house_alt.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭応急対策費_代替活動費'
        ws.cell(row=1, column=1).value = '家庭応急対策費_代替活動費コード'
        ws.cell(row=1, column=2).value = '家庭応急対策費_代替活動費_床下'
        ws.cell(row=1, column=3).value = '家庭応急対策費_代替活動費_0から50cm未満'
        ws.cell(row=1, column=4).value = '家庭応急対策費_代替活動費_50から100cm未満'
        ws.cell(row=1, column=5).value = '家庭応急対策費_代替活動費_100から200cm未満'
        ws.cell(row=1, column=6).value = '家庭応急対策費_代替活動費_200から300cm未満'
        ws.cell(row=1, column=7).value = '家庭応急対策費_代替活動費_300cm以上'
        
        if house_alt_list:
            for i, house_alt in enumerate(house_alt_list):
                ws.cell(row=i+2, column=1).value = house_alt.house_alt_code
                ws.cell(row=i+2, column=2).value = house_alt.house_alt_lv00
                ws.cell(row=i+2, column=3).value = house_alt.house_alt_lv00_50
                ws.cell(row=i+2, column=4).value = house_alt.house_alt_lv50_100
                ws.cell(row=i+2, column=5).value = house_alt.house_alt_lv100_200
                ws.cell(row=i+2, column=6).value = house_alt.house_alt_lv200_300
                ws.cell(row=i+2, column=7).value = house_alt.house_alt_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_alt_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_alt.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_alt_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_alt_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_clean_view(request, lock)
### 2030：家庭応急対策費_清掃日数、清掃労働単価
### urlpattern：path('house_clean/', views.house_clean_view, name='house_clean_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_clean_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家庭応急対策費_清掃日数、清掃労働単価データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 STEP 2/4.', 'INFO')
        house_clean_list = HOUSE_CLEAN.objects.raw("""SELECT * FROM HOUSE_CLEAN ORDER BY CAST(HOUSE_CLEAN_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_clean.xlsx'
        download_file_path = 'static/download_house_clean.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭応急対策費_清掃日数'
        ws.cell(row=1, column=1).value = '家庭応急対策費_清掃日数コード'
        ws.cell(row=1, column=2).value = '家庭応急対策費_清掃日数_床下'
        ws.cell(row=1, column=3).value = '家庭応急対策費_清掃日数_0から50cm未満'
        ws.cell(row=1, column=4).value = '家庭応急対策費_清掃日数_50から100cm未満'
        ws.cell(row=1, column=5).value = '家庭応急対策費_清掃日数_100から200cm未満'
        ws.cell(row=1, column=6).value = '家庭応急対策費_清掃日数_200から300cm未満'
        ws.cell(row=1, column=7).value = '家庭応急対策費_清掃日数_300cm以上'
        ws.cell(row=1, column=8).value = '家庭応急対策費_清掃労働単価'
        
        if house_clean_list:
            for i, house_clean in enumerate(house_clean_list):
                ws.cell(row=i+2, column=1).value = house_clean.house_clean_code
                ws.cell(row=i+2, column=2).value = house_clean.house_clean_days_lv00
                ws.cell(row=i+2, column=3).value = house_clean.house_clean_days_lv00_50
                ws.cell(row=i+2, column=4).value = house_clean.house_clean_days_lv50_100
                ws.cell(row=i+2, column=5).value = house_clean.house_clean_days_lv100_200
                ws.cell(row=i+2, column=6).value = house_clean.house_clean_days_lv200_300
                ws.cell(row=i+2, column=7).value = house_clean.house_clean_days_lv300
                ws.cell(row=i+2, column=8).value = house_clean.house_clean_unit_cost
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_clean_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_clean.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_clean_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_clean_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：household_asset_view(request, lock)
### 3000：家庭用品自動車以外所有額
### urlpattern：path('household_asset/', views.household_asset_view, name='household_asset_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def household_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家庭用品自動車以外所有額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 STEP 2/4.', 'INFO')
        household_asset_list = HOUSEHOLD_ASSET.objects.raw("""SELECT * FROM HOUSEHOLD_ASSET ORDER BY CAST(HOUSEHOLD_ASSET_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_household_asset.xlsx'
        download_file_path = 'static/download_household_asset.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭用品自動車以外所有額'
        ws.cell(row=1, column=1).value = '家庭用品自動車以外所有額コード'
        ws.cell(row=1, column=2).value = '家庭用品自動車以外所有額'
        
        if household_asset_list:
            for i, household_asset in enumerate(household_asset_list):
                ws.cell(row=i+2, column=1).value = household_asset.household_asset_code
                ws.cell(row=i+2, column=2).value = household_asset.household_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_asset_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_asset.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_asset_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_asset_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：household_rate_view(request, lock)
### 3010：家庭用品自動車以外被害率
### urlpattern：path('household_rate/', views.household_rate_view, name='household_rate_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def household_rate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家庭用品自動車以外被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 STEP 2/4.', 'INFO')
        household_rate_list = HOUSEHOLD_RATE.objects.raw("""
            SELECT 
                HR1.househole_rate_code AS household_rate_code, 
                HR1.flood_sediment_code AS flood_sediment_code, 
                FS1.flood_sediment_name AS flood_sediment_name, 
                HR1.household_rate_lv00 AS household_rate_lv00, 
                HR1.household_rate_lv00_50 AS household_rate_lv00_50, 
                HR1.household_rate_lv50_100 AS household_rate_lv50_100, 
                HR1.household_rate_lv100_200 AS household_rate_lv100_200, 
                HR1.household_rate_lv200_300 AS household_rate_lv200_300, 
                HR1.household_rate_lv300 AS household_rate_lv300 
            FROM HOUSEHOLD_RATE HR1 
            LEFT JOIN FLOOD_SEDIMENT FS1 ON HR1.flood_sediment_code=FS1.flood_sediment_code 
            ORDER BY CAST(HR1.household_rate_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_household_rate.xlsx'
        download_file_path = 'static/download_household_rate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭用品自動車以外被害率'
        ws.cell(row=1, column=1).value = '家庭用品自動車以外被害率コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分コード'
        ws.cell(row=1, column=3).value = '浸水土砂区分名'
        ws.cell(row=1, column=4).value = '家庭用品自動車以外被害率_床下'
        ws.cell(row=1, column=5).value = '家庭用品自動車以外被害率_0から50cm未満'
        ws.cell(row=1, column=6).value = '家庭用品自動車以外被害率_50から100cm未満'
        ws.cell(row=1, column=7).value = '家庭用品自動車以外被害率_100から200cm未満'
        ws.cell(row=1, column=8).value = '家庭用品自動車以外被害率_200から300cm未満'
        ws.cell(row=1, column=9).value = '家庭用品自動車以外被害率_300cm以上'
        
        if household_rate_list:
            for i, household_rate in enumerate(household_rate_list):
                ws.cell(row=i+2, column=1).value = household_rate.household_rate_code
                ws.cell(row=i+2, column=2).value = household_rate.flood_sediment_code
                ws.cell(row=i+2, column=3).value = household_rate.flood_sediment_name
                ws.cell(row=i+2, column=4).value = household_rate.household_rate_lv00
                ws.cell(row=i+2, column=5).value = household_rate.household_rate_lv00_50
                ws.cell(row=i+2, column=6).value = household_rate.household_rate_lv50_100
                ws.cell(row=i+2, column=7).value = household_rate.household_rate_lv100_200
                ws.cell(row=i+2, column=8).value = household_rate.household_rate_lv200_300
                ws.cell(row=i+2, column=9).value = household_rate.household_rate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_rate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_rate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_rate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_rate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：car_asset_view(request, lock)
### 4000：家庭用品自動車所有額
### urlpattern：path('car_asset/', views.car_asset_view, name='car_asset_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def car_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、家庭用品自動車所有額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 STEP 2/4.', 'INFO')
        car_asset_list = CAR_ASSET.objects.raw("""SELECT * FROM CAR_ASSET ORDER BY CAST(CAR_ASSET_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_car_asset.xlsx'
        download_file_path = 'static/download_car_asset.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭用品自動車所有額'
        ws.cell(row=1, column=1).value = '家庭用品自動車所有額コード'
        ws.cell(row=1, column=2).value = '家庭用品自動車所有額'
        
        if car_asset_list:
            for i, car_asset in enumerate(car_asset_list):
                ws.cell(row=i+2, column=1).value = car_asset.car_asset_code
                ws.cell(row=i+2, column=2).value = car_asset.car_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0000)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_asset_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car_asset.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_asset_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_asset_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：car_rate_view(request, lock)
### 4010：家庭用品自動車被害率
### urlpattern：path('car_rate/', views.car_rate_view, name='car_rate_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def car_rate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所営業停止損失データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 STEP 2/4.', 'INFO')
        car_rate_list = CAR_RATE.objects.raw("""SELECT * FROM CAR_RATE ORDER BY CAST(CAR_RATE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_car_rate.xlsx'
        download_file_path = 'static/download_car_rate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭用品自動車被害率'
        ws.cell(row=1, column=1).value = '家庭用品自動車被害率コード'
        ws.cell(row=1, column=2).value = '家庭用品自動車被害率_床下'
        ws.cell(row=1, column=3).value = '家庭用品自動車被害率_0から50cm未満'
        ws.cell(row=1, column=4).value = '家庭用品自動車被害率_50から100cm未満'
        ws.cell(row=1, column=5).value = '家庭用品自動車被害率_100から200cm未満'
        ws.cell(row=1, column=6).value = '家庭用品自動車被害率_200から300cm未満'
        ws.cell(row=1, column=7).value = '家庭用品自動車被害率_300cm以上'
        
        if car_rate_list:
            for i, car_rate in enumerate(car_rate_list):
                ws.cell(row=i+2, column=1).value = car_rate.car_rate_code
                ws.cell(row=i+2, column=2).value = car_rate.car_rate_lv00
                ws.cell(row=i+2, column=3).value = car_rate.car_rate_lv00_50
                ws.cell(row=i+2, column=4).value = car_rate.car_rate_lv50_100
                ws.cell(row=i+2, column=5).value = car_rate.car_rate_lv100_200
                ws.cell(row=i+2, column=6).value = car_rate.car_rate_lv200_300
                ws.cell(row=i+2, column=7).value = car_rate.car_rate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_rate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car_rate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_rate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_rate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_asset_view(request, lock)
### 5000：事業所資産額
### urlpattern：path('office_asset/', views.office_asset_view, name='office_asset_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所資産額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 2/4.', 'INFO')
        office_asset_list = OFFICE_ASSET.objects.raw("""
            SELECT 
                OA1.office_asset_code AS office_asset_code, 
                OA1.industry_code AS industry_code, 
                IN1.industry_name AS industry_name, 
                OA1.office_dep_asset AS office_dep_asset, 
                OA1.office_inv_asset AS office_inv_asset, 
                OA1.office_va_asset AS office_va_asset 
            FROM OFFICE_ASSET OA1 
            LEFT JOIN INDUSTRY IN1 ON OA1.industry_code=IN1.industry_code 
            ORDER BY CAST(OA1.office_asset_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_asset.xlsx'
        download_file_path = 'static/download_office_asset.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所資産額'
        ws.cell(row=1, column=1).value = '事業所資産額コード'
        ws.cell(row=1, column=2).value = '産業分類コード'
        ws.cell(row=1, column=3).value = '産業分類名'
        ws.cell(row=1, column=4).value = '事業所資産額_償却資産額'
        ws.cell(row=1, column=5).value = '事業所資産額_在庫資産額'
        ws.cell(row=1, column=6).value = '事業所資産額_付加価値額'
        
        if office_asset_list:
            for i, office_asset in enumerate(office_asset_list):
                ws.cell(row=i+2, column=1).value = office_asset.office_asset_code
                ws.cell(row=i+2, column=2).value = office_asset.industry_code
                ws.cell(row=i+2, column=3).value = office_asset.industry_name
                ws.cell(row=i+2, column=4).value = office_asset.office_dep_asset
                ws.cell(row=i+2, column=5).value = office_asset.office_inv_asset
                ws.cell(row=i+2, column=6).value = office_asset.office_va_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_asset.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_asset_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_asset_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_rate_view(request, lock)
### 5010：事業所被害率
### urlpattern：path('office_rate/', views.office_rate_view, name='office_rate_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_rate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 STEP 2/4.', 'INFO')
        office_rate_list = OFFICE_RATE.objects.raw("""
            SELECT 
                OR1.office_rate_code AS office_rate_code, 
                OR1.flood_sediment_code AS flood_sediment_code, 
                FS1.flood_sediment_name AS flood_sediment_name, 
                OR1.office_dep_rate_lv00 AS office_dep_rate_lv00, 
                OR1.office_dep_rate_lv00_50 AS office_dep_rate_lv00_50, 
                OR1.office_dep_rate_lv50_100 AS office_dep_rate_lv50_100, 
                OR1.office_dep_rate_lv100_200 AS office_dep_rate_lv100_200, 
                OR1.office_dep_rate_lv200_300 AS office_dep_rate_lv200_300, 
                OR1.office_dep_rate_lv300 AS office_dep_rate_lv300, 
                OR1.office_inv_rate_lv00 AS office_inv_rate_lv00, 
                OR1.office_inv_rate_lv00_50 AS office_inv_rate_lv00_50, 
                OR1.office_inv_rate_lv50_100 AS office_inv_rate_lv50_100, 
                OR1.office_inv_rate_lv100_200 AS office_inv_rate_lv100_200, 
                OR1.office_inv_rate_lv200_300 AS office_inv_rate_lv200_300, 
                OR1.office_inv_rate_lv300 AS office_inv_rate_lv300 
            FROM OFFICE_RATE OR1 
            LEFT JOIN FLOOD_SEDIMENT FS1 ON OR1.flood_sediment_code=FS1.flood_sediment_code 
            ORDER BY CAST(OR1.office_rate_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_rate.xlsx'
        download_file_path = 'static/download_office_rate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所被害率'
        ws.cell(row=1, column=1).value = '事業所被害率コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分コード'
        ws.cell(row=1, column=3).value = '浸水土砂区分名'
        ws.cell(row=1, column=4).value = '事業所被害率_償却資産被害率_床下'
        ws.cell(row=1, column=5).value = '事業所被害率_償却資産被害率_0から50cm未満'
        ws.cell(row=1, column=6).value = '事業所被害率_償却資産被害率_50から100cm未満'
        ws.cell(row=1, column=7).value = '事業所被害率_償却資産被害率_100から200cm未満'
        ws.cell(row=1, column=8).value = '事業所被害率_償却資産被害率_200から300cm未満'
        ws.cell(row=1, column=9).value = '事業所被害率_償却資産被害率数_300cm以上'
        ws.cell(row=1, column=10).value = '事業所被害率_在庫資産被害率_床下'
        ws.cell(row=1, column=11).value = '事業所被害率_在庫資産被害率_0から50cm未満'
        ws.cell(row=1, column=12).value = '事業所被害率_在庫資産被害率_50から100cm未満'
        ws.cell(row=1, column=13).value = '事業所被害率_在庫資産被害率_100から200cm未満'
        ws.cell(row=1, column=14).value = '事業所被害率_在庫資産被害率_200から300cm未満'
        ws.cell(row=1, column=15).value = '事業所被害率_在庫資産被害率数_300cm以上'
        
        if office_rate_list:
            for i, office_rate in enumerate(office_rate_list):
                ws.cell(row=i+2, column=1).value = office_rate.office_rate_code
                ws.cell(row=i+2, column=2).value = office_rate.flood_sediment_code
                ws.cell(row=i+2, column=3).value = office_rate.flood_sediment_name
                ws.cell(row=i+2, column=4).value = office_rate.office_dep_rate_lv00
                ws.cell(row=i+2, column=5).value = office_rate.office_dep_rate_lv00_50
                ws.cell(row=i+2, column=6).value = office_rate.office_dep_rate_lv50_100
                ws.cell(row=i+2, column=7).value = office_rate.office_dep_rate_lv100_200
                ws.cell(row=i+2, column=8).value = office_rate.office_dep_rate_lv200_300
                ws.cell(row=i+2, column=9).value = office_rate.office_dep_rate_lv300
                ws.cell(row=i+2, column=10).value = office_rate.office_inv_rate_lv00
                ws.cell(row=i+2, column=11).value = office_rate.office_inv_rate_lv00_50
                ws.cell(row=i+2, column=12).value = office_rate.office_inv_rate_lv50_100
                ws.cell(row=i+2, column=13).value = office_rate.office_inv_rate_lv100_200
                ws.cell(row=i+2, column=14).value = office_rate.office_inv_rate_lv200_300
                ws.cell(row=i+2, column=15).value = office_rate.office_inv_rate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_rate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_rate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_rate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_rate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_suspend_view(request, lock)
### 5020：事業所営業停止日数
### urlpattern：path('office_suspend/', views.office_suspend_view, name='office_suspend_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_suspend_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所営業停止日数データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 STEP 2/4.', 'INFO')
        office_suspend_list = OFFICE_SUSPEND.objects.raw("""SELECT * FROM OFFICE_SUSPEND ORDER BY CAST(OFFICE_SUS_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_suspend.xlsx'
        download_file_path = 'static/download_office_suspend.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所営業停止日数'
        ws.cell(row=1, column=1).value = '事業所営業停止日数コード'
        ws.cell(row=1, column=2).value = '事業所営業停止日数_床下'
        ws.cell(row=1, column=3).value = '事業所営業停止日数_0から50cm未満'
        ws.cell(row=1, column=4).value = '事業所営業停止日数_50から100cm未満'
        ws.cell(row=1, column=5).value = '事業所営業停止日数_100から200cm未満'
        ws.cell(row=1, column=6).value = '事業所営業停止日数_200から300cm未満'
        ws.cell(row=1, column=7).value = '事業所営業停止日数_300cm以上'
        
        if office_suspend_list:
            for i, office_suspend in enumerate(office_suspend_list):
                ws.cell(row=i+2, column=1).value = office_suspend.office_sus_code
                ws.cell(row=i+2, column=2).value = office_suspend.office_sus_days_lv00
                ws.cell(row=i+2, column=3).value = office_suspend.office_sus_days_lv00_50
                ws.cell(row=i+2, column=4).value = office_suspend.office_sus_days_lv50_100
                ws.cell(row=i+2, column=5).value = office_suspend.office_sus_days_lv100_200
                ws.cell(row=i+2, column=6).value = office_suspend.office_sus_days_lv200_300
                ws.cell(row=i+2, column=7).value = office_suspend.office_sus_days_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_suspend_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_suspend.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_suspend_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_suspend_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_stagnate_view(request, lock)
### 5030：事業所営業停滞日数
### urlpattern：path('office_stagnate/', views.office_stagnate_view, name='office_stagnate_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_stagnate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所営業停滞日数データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 STEP 2/4.', 'INFO')
        office_stagnate_list = OFFICE_STAGNATE.objects.raw("""SELECT * FROM OFFICE_STAGNATE ORDER BY CAST(OFFICE_STG_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_stagnate.xlsx'
        download_file_path = 'static/download_office_stagnate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所営業停滞日数'
        ws.cell(row=1, column=1).value = '事業所営業停滞日数コード'
        ws.cell(row=1, column=2).value = '事業所営業停滞日数_床下'
        ws.cell(row=1, column=3).value = '事業所営業停滞日数_0から50cm未満'
        ws.cell(row=1, column=4).value = '事業所営業停滞日数_50から100cm未満'
        ws.cell(row=1, column=5).value = '事業所営業停滞日数_100から200cm未満'
        ws.cell(row=1, column=6).value = '事業所営業停滞日数_200から300cm未満'
        ws.cell(row=1, column=7).value = '事業所営業停滞日数_300cm以上'
        
        if office_stagnate_list:
            for i, office_stagnate in enumerate(office_stagnate_list):
                ws.cell(row=i+2, column=1).value = office_stagnate.office_stg_code
                ws.cell(row=i+2, column=2).value = office_stagnate.office_stg_days_lv00
                ws.cell(row=i+2, column=3).value = office_stagnate.office_stg_days_lv00_50
                ws.cell(row=i+2, column=4).value = office_stagnate.office_stg_days_lv50_100
                ws.cell(row=i+2, column=5).value = office_stagnate.office_stg_days_lv100_200
                ws.cell(row=i+2, column=6).value = office_stagnate.office_stg_days_lv200_300
                ws.cell(row=i+2, column=7).value = office_stagnate.office_stg_days_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_stagnate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_stagnate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_stagnate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_stagnate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_alt_view(request, lock)
### 5040：事業所応急対策費_代替活動費
### urlpattern：
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_alt_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、事業所応急対策費_代替活動費データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 STEP 2/4.', 'INFO')
        office_alt_list = OFFICE_ALT.objects.raw("""SELECT * FROM OFFICE_ALT ORDER BY CAST(OFFICE_ALT_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_alt.xlsx'
        download_file_path = 'static/download_office_alt.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所応急対策費_代替活動費'
        ws.cell(row=1, column=1).value = '事業所応急対策費_代替活動費コード'
        ws.cell(row=1, column=2).value = '事業所応急対策費_代替活動費_床下'
        ws.cell(row=1, column=3).value = '事業所応急対策費_代替活動費_0から50cm未満'
        ws.cell(row=1, column=4).value = '事業所応急対策費_代替活動費_50から100cm未満'
        ws.cell(row=1, column=5).value = '事業所応急対策費_代替活動費_100から200cm未満'
        ws.cell(row=1, column=6).value = '事業所応急対策費_代替活動費_200から300cm未満'
        ws.cell(row=1, column=7).value = '事業所応急対策費_代替活動費_300cm以上'
        
        if office_alt_list:
            for i, office_alt in enumerate(office_alt_list):
                ws.cell(row=i+2, column=1).value = office_alt.office_alt_code
                ws.cell(row=i+2, column=2).value = office_alt.office_alt_lv00
                ws.cell(row=i+2, column=3).value = office_alt.office_alt_lv00_50
                ws.cell(row=i+2, column=4).value = office_alt.office_alt_lv50_100
                ws.cell(row=i+2, column=5).value = office_alt.office_alt_lv100_200
                ws.cell(row=i+2, column=6).value = office_alt.office_alt_lv200_300
                ws.cell(row=i+2, column=7).value = office_alt.office_alt_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_alt_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_alt.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_alt_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_alt_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：farmer_fisher_asset_view(request, lock)
### 6000：農漁家資産額
### urlpattern：path('farmer_fisher_asset/', views.farmer_fisher_asset_view, name='farmer_fisher_asset_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def farmer_fisher_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、農漁家資産額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 STEP 2/4.', 'INFO')
        farmer_fisher_asset_list = FARMER_FISHER_ASSET.objects.raw("""SELECT * FROM FARMER_FISHER_ASSET ORDER BY CAST(FARMER_FISHER_ASSET_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_farmer_fisher_asset.xlsx'
        download_file_path = 'static/download_farmer_fisher_asset.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '農漁家資産額'
        ws.cell(row=1, column=1).value = '農漁家資産額コード'
        ws.cell(row=1, column=2).value = '農漁家資産額_償却資産額'
        ws.cell(row=1, column=3).value = '農漁家資産額_在庫資産額'
        
        if farmer_fisher_asset_list:
            for i, farmer_fisher_asset in enumerate(farmer_fisher_asset_list):
                ws.cell(row=i+2, column=1).value = farmer_fisher_asset.farmer_fisher_asset_code
                ws.cell(row=i+2, column=2).value = farmer_fisher_asset.farmer_fisher_dep_asset
                ws.cell(row=i+2, column=3).value = farmer_fisher_asset.farmer_fisher_inv_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_asset_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="farmer_fisher_asset.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_asset_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_asset_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：farmer_fisher_rate_view(request, lock)
### 6010：農漁家被害率
### urlpattern：path('farmer_fisher_rate/', views.farmer_fisher_rate_view, name='farmer_fisher_rate_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def farmer_fisher_rate_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、農漁家被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 STEP 2/4.', 'INFO')
        farmer_fisher_rate_list = FARMER_FISHER_RATE.objects.raw("""
            SELECT 
                FF1.farmer_fisher_rate_code AS farmer_fisher_rate_code, 
                FF1.flood_sediment_code AS flood_sediment_code, 
                FS1.flood_sediment_name AS flood_sediment_name, 
                FF1.farmer_fisher_dep_rate_lv00 AS farmer_fisher_dep_lv00, 
                FF1.farmer_fisher_dep_rate_lv00_50 AS farmer_fisher_dep_lv00_50, 
                FF1.farmer_fisher_dep_rate_lv50_100 AS farmer_fisher_dep_lv50_100, 
                FF1.farmer_fisher_dep_rate_lv100_200 AS farmer_fisher_dep_lv100_200, 
                FF1.farmer_fisher_dep_rate_lv200_300 AS farmer_fisher_dep_lv200_300, 
                FF1.farmer_fisher_dep_rate_lv300 AS farmer_fisher_dep_lv300, 
                FF1.farmer_fisher_inv_rate_lv00 AS farmer_fisher_inv_lv00, 
                FF1.farmer_fisher_inv_rate_lv00_50 AS farmer_fisher_inv_lv00_50, 
                FF1.farmer_fisher_inv_rate_lv50_100 AS farmer_fisher_inv_lv50_100, 
                FF1.farmer_fisher_inv_rate_lv100_200 AS farmer_fisher_inv_lv100_200, 
                FF1.farmer_fisher_inv_rate_lv200_300 AS farmer_fisher_inv_lv200_300, 
                FF1.farmer_fisher_inv_rate_lv300 AS farmer_fisher_inv_lv300 
            FROM FARMER_FISHER_RATE FF1 
            LEFT JOIN FLOOD_SEDIMENT FS1 ON FF1.flood_sediment_code=FS1.flood_sediment_code 
            ORDER BY CAST(FF1.farmer_fisher_rate_code AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_farmer_fisher_rate.xlsx'
        download_file_path = 'static/download_farmer_fisher_rate.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '農漁家被害率'
        ws.cell(row=1, column=1).value = '農漁家被害率コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分コード'
        ws.cell(row=1, column=3).value = '浸水土砂区分名'
        ws.cell(row=1, column=4).value = '農漁家被害率_償却資産被害率_床下'
        ws.cell(row=1, column=5).value = '農漁家被害率_償却資産被害率_0から50cm未満'
        ws.cell(row=1, column=6).value = '農漁家被害率_償却資産被害率_50から100cm未満'
        ws.cell(row=1, column=7).value = '農漁家被害率_償却資産被害率_100から200cm未満'
        ws.cell(row=1, column=8).value = '農漁家被害率_償却資産被害率_200から300cm未満'
        ws.cell(row=1, column=9).value = '農漁家被害率_償却資産被害率_300cm以上'
        ws.cell(row=1, column=10).value = '農漁家被害率_在庫資産被害率_床下'
        ws.cell(row=1, column=11).value = '農漁家被害率_在庫資産被害率_0から50cm未満'
        ws.cell(row=1, column=12).value = '農漁家被害率_在庫資産被害率_50から100cm未満'
        ws.cell(row=1, column=13).value = '農漁家被害率_在庫資産被害率_100から200cm未満'
        ws.cell(row=1, column=14).value = '農漁家被害率_在庫資産被害率_200から300cm未満'
        ws.cell(row=1, column=15).value = '農漁家被害率_在庫資産被害率_300cm以上'
        
        if farmer_fisher_rate_list:
            for i, farmer_fisher_rate in enumerate(farmer_fisher_rate_list):
                ws.cell(row=i+2, column=1).value = farmer_fisher_rate.farmer_fisher_rate_code
                ws.cell(row=i+2, column=2).value = farmer_fisher_rate.flood_sediment_code
                ws.cell(row=i+2, column=3).value = farmer_fisher_rate.flood_sediment_name
                ws.cell(row=i+2, column=4).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv00
                ws.cell(row=i+2, column=5).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv00_50
                ws.cell(row=i+2, column=6).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv50_100
                ws.cell(row=i+2, column=7).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv100_200
                ws.cell(row=i+2, column=8).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv200_300
                ws.cell(row=i+2, column=9).value = farmer_fisher_rate.farmer_fisher_dep_rate_lv300
                ws.cell(row=i+2, column=10).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv00
                ws.cell(row=i+2, column=11).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv00_50
                ws.cell(row=i+2, column=12).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv50_100
                ws.cell(row=i+2, column=13).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv100_200
                ws.cell(row=i+2, column=14).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv200_300
                ws.cell(row=i+2, column=15).value = farmer_fisher_rate.farmer_fisher_inv_rate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_rate_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="farmer_fisher_rate.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_rate_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_rate_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：area_view(request, lock)
### 7000：入力データ_水害区域
### urlpattern：path('area/', views.area_view, name='area_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def area_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、一般資産入力データ_水害区域データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.area_view()関数 STEP 2/4.', 'INFO')
        area_list = AREA.objects.raw("""SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.area_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_area.xlsx'
        download_file_path = 'static/download_area.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '一般資産入力データ_水害区域'
        ws.cell(row=1, column=1).value = '区域ID'
        ws.cell(row=1, column=2).value = '区域名'
        
        if area_list:
            for i, area in enumerate(area_list):
                ws.cell(row=i+2, column=1).value = area.area_id
                ws.cell(row=i+2, column=2).value = area.area_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.area_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="area.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.area_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.area_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：weather_view(request, lock)
### 7010：入力データ_異常気象
### urlpattern：path('weather/', views.weather_view, name='weather_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def weather_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、入力データ_異常気象データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 2/4.', 'INFO')
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
            ORDER BY CAST(weather_id AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_weather.xlsx'
        download_file_path = 'static/download_weather.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '入力データ_異常気象'
        ws.cell(row=1, column=1).value = '異常気象ID'
        ws.cell(row=1, column=2).value = '異常気象名'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        ws.cell(row=1, column=5).value = '都道府県コード'
        ws.cell(row=1, column=6).value = '都道府県名'

        ws.cell(row=2, column=1).value = 'weather_id'
        ws.cell(row=2, column=2).value = 'weather_name'
        ws.cell(row=2, column=3).value = 'begin_date'
        ws.cell(row=2, column=4).value = 'end_date'
        ws.cell(row=2, column=5).value = 'ken_code'
        ws.cell(row=2, column=6).value = 'ken_name'
        
        if weather_list:
            for i, weather in enumerate(weather_list):
                ws.cell(row=i+3, column=1).value = weather.weather_id
                ws.cell(row=i+3, column=2).value = weather.weather_name
                ws.cell(row=i+3, column=3).value = weather.begin_date
                ws.cell(row=i+3, column=4).value = weather.end_date
                ws.cell(row=i+3, column=5).value = weather.ken_code
                ws.cell(row=i+3, column=6).value = weather.ken_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="weather.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.weather_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.weather_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：suigai_view(request, lock)
### 7020：入力データ_ヘッダ部分
### urlpattern：path('suigai/', views.suigai_view, name='suigai_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suigai_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、水害データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 2/4.', 'INFO')
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
            ORDER BY CAST(SG1.suigai_id AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_suigai.xlsx'
        download_file_path = 'static/download_suigai.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = 'シート'
        ws.cell(row=1, column=1).value = 'シートID'
        ws.cell(row=1, column=2).value = 'シート名'
        ws.cell(row=1, column=3).value = '都道府県コード'
        ws.cell(row=1, column=4).value = '都道府県名'
        ws.cell(row=1, column=5).value = '市区町村コード'
        ws.cell(row=1, column=6).value = '市区町村名'
        ws.cell(row=1, column=7).value = '開始日'
        ws.cell(row=1, column=8).value = '終了日'
        ws.cell(row=1, column=9).value = '水害原因_1_コード'
        ws.cell(row=1, column=10).value = '水害原因_1_名'
        ws.cell(row=1, column=11).value = '水害原因_2_コード'
        ws.cell(row=1, column=12).value = '水害原因_2_名'
        ws.cell(row=1, column=13).value = '水害原因_3_コード'
        ws.cell(row=1, column=14).value = '水害原因_3_名'
        ws.cell(row=1, column=15).value = '水害区域ID'
        ws.cell(row=1, column=16).value = '水害区域名'
        ws.cell(row=1, column=17).value = '水系コード'
        ws.cell(row=1, column=18).value = '水系名'
        ws.cell(row=1, column=19).value = '河川コード'
        ws.cell(row=1, column=20).value = '河川名'
        ws.cell(row=1, column=21).value = '地盤勾配区分コード'
        ws.cell(row=1, column=22).value = '地盤勾配区分名'
        ws.cell(row=1, column=23).value = '宅地面積（単位m2）'
        ws.cell(row=1, column=24).value = '農地面積（単位m2）'
        ws.cell(row=1, column=25).value = '地下面積（単位m2）'
        ws.cell(row=1, column=26).value = '河川海岸（工種）コード'
        ws.cell(row=1, column=27).value = '河川海岸（工種）名'
        ws.cell(row=1, column=28).value = '農作物被害額（単位千円）'
        ws.cell(row=1, column=29).value = '異常気象ID'
        ws.cell(row=1, column=30).value = '異常気象名'
        ws.cell(row=1, column=31).value = 'コミット日時'
        ws.cell(row=1, column=32).value = '削除日時'
        ws.cell(row=1, column=33).value = 'ファイルパス'
        ws.cell(row=1, column=34).value = 'ファイル名'
        ws.cell(row=1, column=35).value = 'アクションコード'
        ws.cell(row=1, column=36).value = 'アクション名'
        ws.cell(row=1, column=37).value = '状態コード'
        ws.cell(row=1, column=38).value = '状態名'

        ws.cell(row=2, column=1).value = 'suigai_id'
        ws.cell(row=2, column=2).value = 'suigai_name'
        ws.cell(row=2, column=3).value = 'ken_code'
        ws.cell(row=2, column=4).value = 'ken_name'
        ws.cell(row=2, column=5).value = 'city_code'
        ws.cell(row=2, column=6).value = 'city_name'
        ws.cell(row=2, column=7).value = 'begin_date'
        ws.cell(row=2, column=8).value = 'end_date'
        ws.cell(row=2, column=9).value = 'cause_1_code'
        ws.cell(row=2, column=10).value = 'cause_1_name'
        ws.cell(row=2, column=11).value = 'cause_2_code'
        ws.cell(row=2, column=12).value = 'cause_2_name'
        ws.cell(row=2, column=13).value = 'cause_3_code'
        ws.cell(row=2, column=14).value = 'cause_3_name'
        ws.cell(row=2, column=15).value = 'area_id'
        ws.cell(row=2, column=16).value = 'area_name'
        ws.cell(row=2, column=17).value = 'suikei_code'
        ws.cell(row=2, column=18).value = 'suikei_name'
        ws.cell(row=2, column=19).value = 'kasen_code'
        ws.cell(row=2, column=20).value = 'kasen_name'
        ws.cell(row=2, column=21).value = 'gradient_code'
        ws.cell(row=2, column=22).value = 'gradient_name'
        ws.cell(row=2, column=23).value = 'residential_area'
        ws.cell(row=2, column=24).value = 'agricultural_area'
        ws.cell(row=2, column=25).value = 'underground_area'
        ws.cell(row=2, column=26).value = 'kasen_kaigan_code'
        ws.cell(row=2, column=27).value = 'kasen_kaigan_name'
        ws.cell(row=2, column=28).value = 'crop_damage'
        ws.cell(row=2, column=29).value = 'weather_id'
        ws.cell(row=2, column=30).value = 'weather_name'
        ws.cell(row=2, column=31).value = 'committed_at'
        ws.cell(row=2, column=32).value = 'deleted_at'
        ws.cell(row=2, column=33).value = 'file_path'
        ws.cell(row=2, column=34).value = 'file_name'
        ws.cell(row=2, column=35).value = 'action_code'
        ws.cell(row=2, column=36).value = 'action_name'
        ws.cell(row=2, column=37).value = 'status_code'
        ws.cell(row=2, column=38).value = 'status_name'
        
        if suigai_list:
            for i, suigai in enumerate(suigai_list):
                ws.cell(row=i+3, column=1).value = suigai.suigai_id
                ws.cell(row=i+3, column=2).value = suigai.suigai_name
                ws.cell(row=i+3, column=3).value = suigai.ken_code
                ws.cell(row=i+3, column=4).value = suigai.ken_name
                ws.cell(row=i+3, column=5).value = suigai.city_code
                ws.cell(row=i+3, column=6).value = suigai.city_name
                ws.cell(row=i+3, column=7).value = suigai.begin_date
                ws.cell(row=i+3, column=8).value = suigai.end_date
                ws.cell(row=i+3, column=9).value = suigai.cause_1_code
                ws.cell(row=i+3, column=10).value = suigai.cause_1_name
                ws.cell(row=i+3, column=11).value = suigai.cause_2_code
                ws.cell(row=i+3, column=12).value = suigai.cause_2_name
                ws.cell(row=i+3, column=13).value = suigai.cause_3_code
                ws.cell(row=i+3, column=14).value = suigai.cause_3_name
                ws.cell(row=i+3, column=15).value = suigai.area_id
                ws.cell(row=i+3, column=16).value = suigai.area_name
                ws.cell(row=i+3, column=17).value = suigai.suikei_code
                ws.cell(row=i+3, column=18).value = suigai.suikei_name
                ws.cell(row=i+3, column=19).value = suigai.kasen_code
                ws.cell(row=i+3, column=20).value = suigai.kasen_name
                ws.cell(row=i+3, column=21).value = suigai.gradient_code
                ws.cell(row=i+3, column=22).value = suigai.gradient_name
                ws.cell(row=i+3, column=23).value = suigai.residential_area
                ws.cell(row=i+3, column=24).value = suigai.agricultural_area
                ws.cell(row=i+3, column=25).value = suigai.underground_area
                ws.cell(row=i+3, column=26).value = suigai.kasen_kaigan_code
                ws.cell(row=i+3, column=27).value = suigai.kasen_kaigan_name
                ws.cell(row=i+3, column=28).value = suigai.crop_damage
                ws.cell(row=i+3, column=29).value = suigai.weather_id
                ws.cell(row=i+3, column=30).value = suigai.weather_name
                ws.cell(row=i+3, column=31).value = suigai.committed_at
                ws.cell(row=i+3, column=32).value = suigai.deleted_at
                ws.cell(row=i+3, column=33).value = suigai.file_path
                ws.cell(row=i+3, column=34).value = suigai.file_name
                ws.cell(row=i+3, column=35).value = suigai.action_code
                ws.cell(row=i+3, column=36).value = suigai.action_name
                ws.cell(row=i+3, column=37).value = suigai.status_code
                ws.cell(row=i+3, column=38).value = suigai.status_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suigai.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suigai_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.suigai_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_view(request, lock)
### 7030：入力データ_一覧表部分
### urlpattern：path('ippan/', views.ippan_view, name='ippan_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、入力データ_一覧表部分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 STEP 2/4.', 'INFO')
        ippan_list = IPPAN.objects.raw("""SELECT * FROM IPPAN ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ippan.xlsx'
        download_file_path = 'static/download_ippan.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '入力データ_一覧表部分'
        ws.cell(row=1, column=1).value = '行ID'
        ws.cell(row=1, column=2).value = '町丁目、大字名'
        ws.cell(row=1, column=3).value = '水害ID'
        ws.cell(row=1, column=4).value = '建物区分コード'
        ws.cell(row=1, column=5).value = '地上地下区分コード'
        ws.cell(row=1, column=6).value = '浸水土砂区分コード'
        ws.cell(row=1, column=7).value = '被害建物棟数_床下'
        ws.cell(row=1, column=8).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=9).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=10).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=11).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=12).value = '被害建物棟数_全壊'
        ws.cell(row=1, column=13).value = '延床面積'
        ws.cell(row=1, column=14).value = '被災世帯数'
        ws.cell(row=1, column=15).value = '被災事業所数'
        ws.cell(row=1, column=16).value = '農漁家戸数_床下'
        ws.cell(row=1, column=17).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=18).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=19).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=20).value = '農漁家戸数_全壊'
        ws.cell(row=1, column=21).value = '被災従業者数_床下'
        ws.cell(row=1, column=22).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=23).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=24).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=25).value = '被災従業者数_全壊'
        ws.cell(row=1, column=26).value = '産業分類コード'
        ws.cell(row=1, column=27).value = '地下空間の利用形態コード'
        ws.cell(row=1, column=28).value = '備考'
        ws.cell(row=1, column=29).value = '削除日時'

        ws.cell(row=2, column=1).value = 'ippan_id'
        ws.cell(row=2, column=2).value = 'ippan_name'
        ws.cell(row=2, column=3).value = 'suigai_id'
        ws.cell(row=2, column=4).value = 'building_code'
        ws.cell(row=2, column=5).value = 'underground_code'
        ws.cell(row=2, column=6).value = 'flood_sediment_code'
        ws.cell(row=2, column=7).value = 'building_lv00'
        ws.cell(row=2, column=8).value = 'building_lv01_49'
        ws.cell(row=2, column=9).value = 'building_lv50_99'
        ws.cell(row=2, column=10).value = 'building_lv100'
        ws.cell(row=2, column=11).value = 'building_half'
        ws.cell(row=2, column=12).value = 'building_full'
        ws.cell(row=2, column=13).value = 'floor_area'
        ws.cell(row=2, column=14).value = 'family_area'
        ws.cell(row=2, column=15).value = 'office_area'
        ws.cell(row=2, column=16).value = 'farmer_fisher_lv00'
        ws.cell(row=2, column=17).value = 'farmer_fisher_lv01_49'
        ws.cell(row=2, column=18).value = 'farmer_fisher_lv50_99'
        ws.cell(row=2, column=19).value = 'farmer_fisher_lv100'
        ws.cell(row=2, column=20).value = 'farmer_fisher_full'
        ws.cell(row=2, column=21).value = 'employee_lv00'
        ws.cell(row=2, column=22).value = 'employee_lv01_49'
        ws.cell(row=2, column=23).value = 'employee_lv50_99'
        ws.cell(row=2, column=24).value = 'employee_lv100'
        ws.cell(row=2, column=25).value = 'employee_full'
        ws.cell(row=2, column=26).value = 'industry_code'
        ws.cell(row=2, column=27).value = 'usage_code'
        ws.cell(row=2, column=28).value = 'comment'
        ws.cell(row=2, column=29).value = 'deleted_at'
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws.cell(row=i+3, column=1).value = ippan.ippan_id
                ws.cell(row=i+3, column=2).value = ippan.ippan_name
                ws.cell(row=i+3, column=3).value = ippan.suigai_id
                ws.cell(row=i+3, column=4).value = ippan.building_code
                ws.cell(row=i+3, column=5).value = ippan.underground_code
                ws.cell(row=i+3, column=6).value = ippan.flood_sediment_code
                ws.cell(row=i+3, column=7).value = ippan.building_lv00
                ws.cell(row=i+3, column=8).value = ippan.building_lv01_49
                ws.cell(row=i+3, column=9).value = ippan.building_lv50_99
                ws.cell(row=i+3, column=10).value = ippan.building_lv100
                ws.cell(row=i+3, column=11).value = ippan.building_half
                ws.cell(row=i+3, column=12).value = ippan.building_full
                ws.cell(row=i+3, column=13).value = ippan.floor_area
                ws.cell(row=i+3, column=14).value = ippan.family
                ws.cell(row=i+3, column=15).value = ippan.office
                ws.cell(row=i+3, column=16).value = ippan.farmer_fisher_lv00
                ws.cell(row=i+3, column=17).value = ippan.farmer_fisher_lv01_49
                ws.cell(row=i+3, column=18).value = ippan.farmer_fisher_lv50_99
                ws.cell(row=i+3, column=19).value = ippan.farmer_fisher_lv100
                ws.cell(row=i+3, column=20).value = ippan.farmer_fisher_full
                ws.cell(row=i+3, column=21).value = ippan.employee_lv00
                ws.cell(row=i+3, column=22).value = ippan.employee_lv01_49
                ws.cell(row=i+3, column=23).value = ippan.employee_lv50_99
                ws.cell(row=i+3, column=24).value = ippan.employee_lv100
                ws.cell(row=i+3, column=25).value = ippan.employee_full
                ws.cell(row=i+3, column=26).value = ippan.industry_code
                ws.cell(row=i+3, column=27).value = ippan.usage_code
                ws.cell(row=i+3, column=28).value = ippan.comment
                ws.cell(row=i+3, column=29).value = str(ippan.deleted_at)

        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_view_view(request, lock)
### 7040：ビューデータ_一覧表部分
### urlpattern：path('ippan_view/', views.ippan_view_view, name='ippan_view_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_view_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、一般資産ビューデータ一覧表部分データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 STEP 2/4.', 'INFO')
        ippan_view_list = IPPAN_VIEW.objects.raw("""SELECT * FROM IPPAN_VIEW ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ippan_view.xlsx'
        download_file_path = 'static/download_ippan_view.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = 'ビューデータ_一覧表部分'
        ws.cell(row=1, column=1).value = '行ID'
        ws.cell(row=1, column=2).value = '町丁目、大字名'
        ws.cell(row=1, column=3).value = '水害ID'
        ws.cell(row=1, column=4).value = '水害名'
        ws.cell(row=1, column=5).value = '都道府県コード'
        ws.cell(row=1, column=6).value = '都道府県名'
        ws.cell(row=1, column=7).value = '市区町村コード'
        ws.cell(row=1, column=8).value = '市区町村名'
        ws.cell(row=1, column=9).value = '水害原因コード1'
        ws.cell(row=1, column=10).value = '水害原因名1'
        ws.cell(row=1, column=11).value = '水害原因コード2'
        ws.cell(row=1, column=12).value = '水害原因名2'
        ws.cell(row=1, column=13).value = '水害原因コード3'
        ws.cell(row=1, column=14).value = '水害原因名3'
        ws.cell(row=1, column=15).value = '水害区域ID'
        ws.cell(row=1, column=16).value = '水害区域名'
        ws.cell(row=1, column=17).value = '水系コード'
        ws.cell(row=1, column=18).value = '水系名'
        ws.cell(row=1, column=19).value = '河川コード'
        ws.cell(row=1, column=20).value = '河川名'
        ws.cell(row=1, column=21).value = '地盤勾配区分コード'
        ws.cell(row=1, column=22).value = '地盤勾配区分名'
        ws.cell(row=1, column=23).value = '宅地面積'
        ws.cell(row=1, column=24).value = '農地面積'
        ws.cell(row=1, column=25).value = '地下面積'
        ws.cell(row=1, column=26).value = '河川海岸（工種）コード'
        ws.cell(row=1, column=27).value = '河川海岸（工種）名'
        ws.cell(row=1, column=28).value = '農作物被害額'
        ws.cell(row=1, column=29).value = '異常気象ID'
        ws.cell(row=1, column=30).value = '異常気象名'
        ws.cell(row=1, column=31).value = '建物区分コード'
        ws.cell(row=1, column=32).value = '建物区分名'
        ws.cell(row=1, column=33).value = '地上地下区分コード'
        ws.cell(row=1, column=34).value = '地上地下区分名'
        ws.cell(row=1, column=35).value = '浸水土砂区分コード'
        ws.cell(row=1, column=36).value = '浸水土砂区分名'
        ws.cell(row=1, column=37).value = '被害建物棟数_床下'
        ws.cell(row=1, column=38).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=39).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=40).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=41).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=42).value = '被害建物棟数_全壊'
        ws.cell(row=1, column=43).value = '被害建物棟数_合計'
        ws.cell(row=1, column=44).value = '延床面積'
        ws.cell(row=1, column=45).value = '被災世帯数'
        ws.cell(row=1, column=46).value = '被災事業所数'
        ws.cell(row=1, column=47).value = '延床面積_床下'
        ws.cell(row=1, column=48).value = '延床面積_01から49cm'
        ws.cell(row=1, column=49).value = '延床面積_50から99cm'
        ws.cell(row=1, column=50).value = '延床面積_100cm以上'
        ws.cell(row=1, column=51).value = '延床面積_半壊'
        ws.cell(row=1, column=52).value = '延床面積_全壊'
        ws.cell(row=1, column=53).value = '延床面積_合計'
        ws.cell(row=1, column=54).value = '被災世帯数_床下'
        ws.cell(row=1, column=55).value = '被災世帯数_01から49cm'
        ws.cell(row=1, column=56).value = '被災世帯数_50から99cm'
        ws.cell(row=1, column=57).value = '被災世帯数_100cm以上'
        ws.cell(row=1, column=58).value = '被災世帯数_半壊'
        ws.cell(row=1, column=59).value = '被災世帯数_全壊'
        ws.cell(row=1, column=60).value = '被災世帯数_合計'
        ws.cell(row=1, column=61).value = '被災事業所数_床下'
        ws.cell(row=1, column=62).value = '被災事業所数_01から49cm'
        ws.cell(row=1, column=63).value = '被災事業所数_50から99cm'
        ws.cell(row=1, column=64).value = '被災事業所数_100cm以上'
        ws.cell(row=1, column=65).value = '被災事業所数_半壊'
        ws.cell(row=1, column=66).value = '被災事業所数_全壊'
        ws.cell(row=1, column=67).value = '被災事業所数_合計'
        ws.cell(row=1, column=68).value = '農漁家戸数_床下'
        ws.cell(row=1, column=69).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=70).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=71).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=72).value = '農漁家戸数_全壊'
        ws.cell(row=1, column=73).value = '農漁家戸数_合計'
        ws.cell(row=1, column=74).value = '被災従業者数_床下'
        ws.cell(row=1, column=75).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=76).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=77).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=78).value = '被災従業者数_全壊'
        ws.cell(row=1, column=79).value = '被災従業者数_合計'
        ws.cell(row=1, column=80).value = '産業分類コード'
        ws.cell(row=1, column=81).value = '産業分類名'
        ws.cell(row=1, column=82).value = '地下空間の利用形態コード'
        ws.cell(row=1, column=83).value = '地下空間の利用形態名'
        ws.cell(row=1, column=84).value = '備考'
        ws.cell(row=1, column=85).value = '削除日時'

        ws.cell(row=2, column=1).value = 'ippan_id'
        ws.cell(row=2, column=2).value = 'ippan_name'
        ws.cell(row=2, column=3).value = 'suigai_id'
        ws.cell(row=2, column=4).value = 'suigai_name'
        ws.cell(row=2, column=5).value = 'ken_code'
        ws.cell(row=2, column=6).value = 'ken_name'
        ws.cell(row=2, column=7).value = 'city_code'
        ws.cell(row=2, column=8).value = 'city_name'
        ws.cell(row=2, column=9).value = 'cause_1_code'
        ws.cell(row=2, column=10).value = 'cause_1_name'
        ws.cell(row=2, column=11).value = 'cause_2_code'
        ws.cell(row=2, column=12).value = 'cause_2_name'
        ws.cell(row=2, column=13).value = 'cause_3_code'
        ws.cell(row=2, column=14).value = 'cause_3_name'
        ws.cell(row=2, column=15).value = 'area_id'
        ws.cell(row=2, column=16).value = 'area_name'
        ws.cell(row=2, column=17).value = 'suikei_code'
        ws.cell(row=2, column=18).value = 'suikei_name'
        ws.cell(row=2, column=19).value = 'kasen_code'
        ws.cell(row=2, column=20).value = 'kasen_name'
        ws.cell(row=2, column=21).value = 'gradient_code'
        ws.cell(row=2, column=22).value = 'gradient_name'
        ws.cell(row=2, column=23).value = 'residential_area'
        ws.cell(row=2, column=24).value = 'agricultural_area'
        ws.cell(row=2, column=25).value = 'underground_area'
        ws.cell(row=2, column=26).value = 'kasen_kaigan_code'
        ws.cell(row=2, column=27).value = 'kasen_kaigan_name'
        ws.cell(row=2, column=28).value = 'crop_damage'
        ws.cell(row=2, column=29).value = 'weather_id'
        ws.cell(row=2, column=30).value = 'weather_name'
        ws.cell(row=2, column=31).value = 'building_code'
        ws.cell(row=2, column=32).value = 'building_name'
        ws.cell(row=2, column=33).value = 'underground_code'
        ws.cell(row=2, column=34).value = 'underground_name'
        ws.cell(row=2, column=35).value = 'flood_sediment_code'
        ws.cell(row=2, column=36).value = 'flood_sediment_name'
        ws.cell(row=2, column=37).value = 'building_lv00'
        ws.cell(row=2, column=38).value = 'building_lv01_49'
        ws.cell(row=2, column=39).value = 'building_lv50_99'
        ws.cell(row=2, column=40).value = 'building_lv100'
        ws.cell(row=2, column=41).value = 'building_half'
        ws.cell(row=2, column=42).value = 'building_full'
        ws.cell(row=2, column=43).value = 'building_total'
        ws.cell(row=2, column=44).value = 'floor_area'
        ws.cell(row=2, column=45).value = 'family'
        ws.cell(row=2, column=46).value = 'office'
        ws.cell(row=2, column=47).value = 'floor_area_lv00'
        ws.cell(row=2, column=48).value = 'floor_area_lv01_49'
        ws.cell(row=2, column=49).value = 'floor_area_lv50_99'
        ws.cell(row=2, column=50).value = 'floor_area_lv100'
        ws.cell(row=2, column=51).value = 'floor_area_half'
        ws.cell(row=2, column=52).value = 'floor_area_full'
        ws.cell(row=2, column=53).value = 'floor_area_total'
        ws.cell(row=2, column=54).value = 'family_lv00'
        ws.cell(row=2, column=55).value = 'family_lv01_49'
        ws.cell(row=2, column=56).value = 'family_lv50_99'
        ws.cell(row=2, column=57).value = 'family_lv100'
        ws.cell(row=2, column=58).value = 'family_half'
        ws.cell(row=2, column=59).value = 'family_full'
        ws.cell(row=2, column=60).value = 'family_total'
        ws.cell(row=2, column=61).value = 'office_lv00'
        ws.cell(row=2, column=62).value = 'office_lv01_49'
        ws.cell(row=2, column=63).value = 'office_lv50_99'
        ws.cell(row=2, column=64).value = 'office_lv100'
        ws.cell(row=2, column=65).value = 'office_half'
        ws.cell(row=2, column=66).value = 'office_full'
        ws.cell(row=2, column=67).value = 'office_total'
        ws.cell(row=2, column=68).value = 'farmer_fisher_lv00'
        ws.cell(row=2, column=69).value = 'farmer_fisher_lv01_49'
        ws.cell(row=2, column=70).value = 'farmer_fisher_lv50_99'
        ws.cell(row=2, column=71).value = 'farmer_fisher_lv100'
        ws.cell(row=2, column=72).value = 'farmer_fisher_full'
        ws.cell(row=2, column=73).value = 'farmer_fisher_total'
        ws.cell(row=2, column=74).value = 'employee_lv00'
        ws.cell(row=2, column=75).value = 'employee_lv01_49'
        ws.cell(row=2, column=76).value = 'employee_lv50_99'
        ws.cell(row=2, column=77).value = 'employee_lv100'
        ws.cell(row=2, column=78).value = 'employee_full'
        ws.cell(row=2, column=79).value = 'employee_total'
        ws.cell(row=2, column=80).value = 'industry_code'
        ws.cell(row=2, column=81).value = 'industry_name'
        ws.cell(row=2, column=82).value = 'usage_code'
        ws.cell(row=2, column=83).value = 'usage_name'
        ws.cell(row=2, column=84).value = 'comment'
        ws.cell(row=2, column=85).value = 'deleted_at'
        
        if ippan_view_list:
            for i, ippan_view in enumerate(ippan_view_list):
                ws.cell(row=i+3, column=1).value = ippan_view.ippan_id
                ws.cell(row=i+3, column=2).value = ippan_view.ippan_name
                ws.cell(row=i+3, column=3).value = ippan_view.suigai_id
                ws.cell(row=i+3, column=4).value = ippan_view.suigai_name
                ws.cell(row=i+3, column=5).value = ippan_view.ken_code
                ws.cell(row=i+3, column=6).value = ippan_view.ken_name
                ws.cell(row=i+3, column=7).value = ippan_view.city_code
                ws.cell(row=i+3, column=8).value = ippan_view.city_name
                ws.cell(row=i+3, column=9).value = ippan_view.cause_1_code
                ws.cell(row=i+3, column=10).value = ippan_view.cause_1_name
                ws.cell(row=i+3, column=11).value = ippan_view.cause_2_code
                ws.cell(row=i+3, column=12).value = ippan_view.cause_2_name
                ws.cell(row=i+3, column=13).value = ippan_view.cause_3_code
                ws.cell(row=i+3, column=14).value = ippan_view.cause_3_name
                ws.cell(row=i+3, column=15).value = ippan_view.area_id
                ws.cell(row=i+3, column=16).value = ippan_view.area_name
                ws.cell(row=i+3, column=17).value = ippan_view.suikei_code
                ws.cell(row=i+3, column=18).value = ippan_view.suikei_name
                ws.cell(row=i+3, column=19).value = ippan_view.kasen_code
                ws.cell(row=i+3, column=20).value = ippan_view.kasen_name
                ws.cell(row=i+3, column=21).value = ippan_view.gradient_code
                ws.cell(row=i+3, column=22).value = ippan_view.gradient_name
                ws.cell(row=i+3, column=23).value = ippan_view.residential_area
                ws.cell(row=i+3, column=24).value = ippan_view.agricultural_area
                ws.cell(row=i+3, column=25).value = ippan_view.underground_area
                ws.cell(row=i+3, column=26).value = ippan_view.kasen_kaigan_code
                ws.cell(row=i+3, column=27).value = ippan_view.kasen_kaigan_name
                ws.cell(row=i+3, column=28).value = ippan_view.crop_damage
                ws.cell(row=i+3, column=29).value = ippan_view.weather_id
                ws.cell(row=i+3, column=30).value = ippan_view.weather_name
                ws.cell(row=i+3, column=31).value = ippan_view.building_code
                ws.cell(row=i+3, column=32).value = ippan_view.building_name
                ws.cell(row=i+3, column=33).value = ippan_view.underground_code
                ws.cell(row=i+3, column=34).value = ippan_view.underground_name
                ws.cell(row=i+3, column=35).value = ippan_view.flood_sediment_code
                ws.cell(row=i+3, column=36).value = ippan_view.flood_sediment_name
                ws.cell(row=i+3, column=37).value = ippan_view.building_lv00
                ws.cell(row=i+3, column=38).value = ippan_view.building_lv01_49
                ws.cell(row=i+3, column=39).value = ippan_view.building_lv50_99
                ws.cell(row=i+3, column=40).value = ippan_view.building_lv100
                ws.cell(row=i+3, column=41).value = ippan_view.building_half
                ws.cell(row=i+3, column=42).value = ippan_view.building_full
                ws.cell(row=i+3, column=43).value = ippan_view.building_total
                ws.cell(row=i+3, column=44).value = ippan_view.floor_area
                ws.cell(row=i+3, column=45).value = ippan_view.family
                ws.cell(row=i+3, column=46).value = ippan_view.office
                ws.cell(row=i+3, column=47).value = ippan_view.floor_area_lv00
                ws.cell(row=i+3, column=48).value = ippan_view.floor_area_lv01_49
                ws.cell(row=i+3, column=49).value = ippan_view.floor_area_lv50_99

                ws.cell(row=i+3, column=50).value = ippan_view.floor_area_lv100
                ws.cell(row=i+3, column=51).value = ippan_view.floor_area_half
                ws.cell(row=i+3, column=52).value = ippan_view.floor_area_full
                ws.cell(row=i+3, column=53).value = ippan_view.floor_area_total
                ws.cell(row=i+3, column=54).value = ippan_view.family_lv00
                ws.cell(row=i+3, column=55).value = ippan_view.family_lv01_49
                ws.cell(row=i+3, column=56).value = ippan_view.family_lv50_99
                ws.cell(row=i+3, column=57).value = ippan_view.family_lv100
                ws.cell(row=i+3, column=58).value = ippan_view.family_half
                ws.cell(row=i+3, column=59).value = ippan_view.family_full

                ws.cell(row=i+3, column=60).value = ippan_view.family_total
                ws.cell(row=i+3, column=61).value = ippan_view.office_lv00
                ws.cell(row=i+3, column=62).value = ippan_view.office_lv01_49
                ws.cell(row=i+3, column=63).value = ippan_view.office_lv50_99
                ws.cell(row=i+3, column=64).value = ippan_view.office_lv100
                ws.cell(row=i+3, column=65).value = ippan_view.office_half
                ws.cell(row=i+3, column=66).value = ippan_view.office_full
                ws.cell(row=i+3, column=67).value = ippan_view.office_total
                ws.cell(row=i+3, column=68).value = ippan_view.farmer_fisher_lv00
                ws.cell(row=i+3, column=69).value = ippan_view.farmer_fisher_lv01_49

                ws.cell(row=i+3, column=70).value = ippan_view.farmer_fisher_lv50_99
                ws.cell(row=i+3, column=71).value = ippan_view.farmer_fisher_lv100
                ws.cell(row=i+3, column=72).value = ippan_view.farmer_fisher_full
                ws.cell(row=i+3, column=73).value = ippan_view.farmer_fisher_total
                ws.cell(row=i+3, column=74).value = ippan_view.employee_lv00
                ws.cell(row=i+3, column=75).value = ippan_view.employee_lv01_49
                ws.cell(row=i+3, column=76).value = ippan_view.employee_lv50_99
                ws.cell(row=i+3, column=77).value = ippan_view.employee_lv100
                ws.cell(row=i+3, column=78).value = ippan_view.employee_full
                ws.cell(row=i+3, column=79).value = ippan_view.employee_total

                ws.cell(row=i+3, column=80).value = ippan_view.industry_code
                ws.cell(row=i+3, column=81).value = ippan_view.industry_name
                ws.cell(row=i+3, column=82).value = ippan_view.usage_code
                ws.cell(row=i+3, column=83).value = ippan_view.usage_name
                ws.cell(row=i+3, column=84).value = ippan_view.comment
                ws.cell(row=i+3, column=85).value = str(ippan_view.deleted_at)

        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_view_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_view.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_view_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_view_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_summary_view(request, lock)
### 8000：集計データ_集計結果
### urlpattern：path('ippan_summary/', views.ippan_summary_view, name='ippan_summary_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_summary_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、集計データ_集計結果データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 STEP 2/4.', 'INFO')
        ippan_summary_list = IPPAN_SUMMARY.objects.raw("""SELECT * FROM IPPAN_SUMMARY ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ippan_summary.xlsx'
        download_file_path = 'static/download_ippan_summary.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '集計データ_集計結果'
        ws.cell(row=1, column=1).value = '行ID'
        ws.cell(row=1, column=2).value = '水害ID'
        ws.cell(row=1, column=3).value = '家屋被害額_床下'
        ws.cell(row=1, column=4).value = '家屋被害額_01から49cm'
        ws.cell(row=1, column=5).value = '家屋被害額_50から99cm'
        ws.cell(row=1, column=6).value = '家屋被害額_100cm以上'
        ws.cell(row=1, column=7).value = '家屋被害額_半壊'
        ws.cell(row=1, column=8).value = '家屋被害額_全壊'
        ws.cell(row=1, column=9).value = '家庭用品自動車以外被害額_床下'
        ws.cell(row=1, column=10).value = '家庭用品自動車以外被害額_01から49cm'
        ws.cell(row=1, column=11).value = '家庭用品自動車以外被害額_50から99cm'
        ws.cell(row=1, column=12).value = '家庭用品自動車以外被害額_100cm以上'
        ws.cell(row=1, column=13).value = '家庭用品自動車以外被害額_半壊'
        ws.cell(row=1, column=14).value = '家庭用品自動車以外被害額_全壊'
        ws.cell(row=1, column=15).value = '家庭用品自動車被害額_床下'
        ws.cell(row=1, column=16).value = '家庭用品自動車被害額_01から49cm'
        ws.cell(row=1, column=17).value = '家庭用品自動車被害額_50から99cm'
        ws.cell(row=1, column=18).value = '家庭用品自動車被害額_100cm以上'
        ws.cell(row=1, column=19).value = '家庭用品自動車被害額_半壊'
        ws.cell(row=1, column=20).value = '家庭用品自動車被害額_全壊'
        ws.cell(row=1, column=21).value = '家庭応急対策費_代替活動費_床下'
        ws.cell(row=1, column=22).value = '家庭応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=23).value = '家庭応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=24).value = '家庭応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=25).value = '家庭応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=26).value = '家庭応急対策費_代替活動費_全壊'
        ws.cell(row=1, column=27).value = '家庭応急対策費_清掃費_床下'
        ws.cell(row=1, column=28).value = '家庭応急対策費_清掃費_01から49cm'
        ws.cell(row=1, column=29).value = '家庭応急対策費_清掃費_50から99cm'
        ws.cell(row=1, column=30).value = '家庭応急対策費_清掃費_100cm以上'
        ws.cell(row=1, column=31).value = '家庭応急対策費_清掃費_半壊'
        ws.cell(row=1, column=32).value = '家庭応急対策費_清掃費_全壊'
        ws.cell(row=1, column=33).value = '事業所被害額_償却資産被害額_床下'
        ws.cell(row=1, column=34).value = '事業所被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=35).value = '事業所被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=36).value = '事業所被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=37).value = '事業所被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=38).value = '事業所被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=39).value = '事業所被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=40).value = '事業所被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=41).value = '事業所被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=42).value = '事業所被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=43).value = '事業所被害額_営業停止に伴う被害額_床下'
        ws.cell(row=1, column=44).value = '事業所被害額_営業停止に伴う被害額_01から49cm'
        ws.cell(row=1, column=45).value = '事業所被害額_営業停止に伴う被害額_50から99cm'
        ws.cell(row=1, column=46).value = '事業所被害額_営業停止に伴う被害額_100cm以上'
        ws.cell(row=1, column=47).value = '事業所被害額_営業停止に伴う被害額_全壊'
        ws.cell(row=1, column=48).value = '事業所被害額_営業停滞に伴う被害額_床下'
        ws.cell(row=1, column=49).value = '事業所被害額_営業停滞に伴う被害額_01から49cm'
        ws.cell(row=1, column=50).value = '事業所被害額_営業停滞に伴う被害額_50から99cm'
        ws.cell(row=1, column=51).value = '事業所被害額_営業停滞に伴う被害額_100cm以上'
        ws.cell(row=1, column=52).value = '事業所被害額_営業停滞に伴う被害額_全壊'
        ws.cell(row=1, column=53).value = '農漁家被害額_償却資産被害額_床下'
        ws.cell(row=1, column=54).value = '農漁家被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=55).value = '農漁家被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=56).value = '農漁家被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=57).value = '農漁家被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=58).value = '農漁家被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=59).value = '農漁家被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=60).value = '農漁家被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=61).value = '農漁家被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=62).value = '農漁家被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=63).value = '事業所応急対策費_代替活動費_床下'
        ws.cell(row=1, column=64).value = '事業所応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=65).value = '事業所応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=66).value = '事業所応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=67).value = '事業所応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=68).value = '事業所応急対策費_代替活動費_全壊'
        ws.cell(row=1, column=69).value = '削除日時'

        ws.cell(row=2, column=1).value = 'ippan_id'
        ws.cell(row=2, column=2).value = 'suigai_id'
        ws.cell(row=2, column=3).value = 'house_summary_lv00'
        ws.cell(row=2, column=4).value = 'house_summary_lv01_49'
        ws.cell(row=2, column=5).value = 'house_summary_lv50_99'
        ws.cell(row=2, column=6).value = 'house_summary_lv100'
        ws.cell(row=2, column=7).value = 'house_summary_half'
        ws.cell(row=2, column=8).value = 'house_summary_full'
        ws.cell(row=2, column=9).value = 'household_summary_lv00'
        ws.cell(row=2, column=10).value = 'household_summary_lv01_49'
        ws.cell(row=2, column=11).value = 'household_summary_lv50_99'
        ws.cell(row=2, column=12).value = 'household_summary_lv100'
        ws.cell(row=2, column=13).value = 'household_summary_half'
        ws.cell(row=2, column=14).value = 'household_summary_full'
        ws.cell(row=2, column=15).value = 'car_summary_lv00'
        ws.cell(row=2, column=16).value = 'car_summary_lv01_49'
        ws.cell(row=2, column=17).value = 'car_summary_lv50_99'
        ws.cell(row=2, column=18).value = 'car_summary_lv100'
        ws.cell(row=2, column=19).value = 'car_summary_half'
        ws.cell(row=2, column=20).value = 'car_summary_full'
        ws.cell(row=2, column=21).value = 'house_alt_lv00'
        ws.cell(row=2, column=22).value = 'house_alt_lv01_49'
        ws.cell(row=2, column=23).value = 'house_alt_lv50_99'
        ws.cell(row=2, column=24).value = 'house_alt_lv100'
        ws.cell(row=2, column=25).value = 'house_alt_half'
        ws.cell(row=2, column=26).value = 'house_alt_full'
        ws.cell(row=2, column=27).value = 'house_clean_lv00'
        ws.cell(row=2, column=28).value = 'house_clean_lv01_49'
        ws.cell(row=2, column=29).value = 'house_clean_lv50_99'
        ws.cell(row=2, column=30).value = 'house_clean_lv100'
        ws.cell(row=2, column=31).value = 'house_clean_half'
        ws.cell(row=2, column=32).value = 'house_clean_full'
        ws.cell(row=2, column=33).value = 'office_dep_summary_lv00'
        ws.cell(row=2, column=34).value = 'office_dep_summary_lv01_49'
        ws.cell(row=2, column=35).value = 'office_dep_summary_lv50_99'
        ws.cell(row=2, column=36).value = 'office_dep_summary_lv100'
        ws.cell(row=2, column=37).value = 'office_dep_summary_full'
        ws.cell(row=2, column=38).value = 'office_inv_summary_lv00'
        ws.cell(row=2, column=39).value = 'office_inv_summary_lv01_49'
        ws.cell(row=2, column=40).value = 'office_inv_summary_lv50_99'
        ws.cell(row=2, column=41).value = 'office_inv_summary_lv100'
        ws.cell(row=2, column=42).value = 'office_inv_summary_full'
        ws.cell(row=2, column=43).value = 'office_sus_summary_lv00'
        ws.cell(row=2, column=44).value = 'office_sus_summary_lv01_49'
        ws.cell(row=2, column=45).value = 'office_sus_summary_lv50_99'
        ws.cell(row=2, column=46).value = 'office_sus_summary_lv100'
        ws.cell(row=2, column=47).value = 'office_sus_summary_full'
        ws.cell(row=2, column=48).value = 'office_stg_summary_lv00'
        ws.cell(row=2, column=49).value = 'office_stg_summary_lv01_49'
        ws.cell(row=2, column=50).value = 'office_stg_summary_lv50_99'
        ws.cell(row=2, column=51).value = 'office_stg_summary_lv100'
        ws.cell(row=2, column=52).value = 'office_stg_summary_full'
        ws.cell(row=2, column=53).value = 'farmer_fisher_dep_summary_lv00'
        ws.cell(row=2, column=54).value = 'farmer_fisher_dep_summary_lv01_49'
        ws.cell(row=2, column=55).value = 'farmer_fisher_dep_summary_lv50_99'
        ws.cell(row=2, column=56).value = 'farmer_fisher_dep_summary_lv100'
        ws.cell(row=2, column=57).value = 'farmer_fisher_dep_summary_full'
        ws.cell(row=2, column=58).value = 'farmer_fisher_inv_summary_lv00'
        ws.cell(row=2, column=59).value = 'farmer_fisher_inv_summary_lv01_49'
        ws.cell(row=2, column=60).value = 'farmer_fisher_inv_summary_lv50_99'
        ws.cell(row=2, column=61).value = 'farmer_fisher_inv_summary_lv100'
        ws.cell(row=2, column=62).value = 'farmer_fisher_inv_summary_full'
        ws.cell(row=2, column=63).value = 'office_alt_summary_lv00'
        ws.cell(row=2, column=64).value = 'office_alt_summary_lv01_49'
        ws.cell(row=2, column=65).value = 'office_alt_summary_lv50_99'
        ws.cell(row=2, column=66).value = 'office_alt_summary_lv100'
        ws.cell(row=2, column=67).value = 'office_alt_summary_half'
        ws.cell(row=2, column=68).value = 'office_alt_summary_full'
        ws.cell(row=2, column=69).value = 'deleted_at'
        
        if ippan_summary_list:
            for i, ippan_summary in enumerate(ippan_summary_list):
                ws.cell(row=i+3, column=1).value = ippan_summary.ippan_id
                ws.cell(row=i+3, column=2).value = ippan_summary.suigai_id
                ws.cell(row=i+3, column=3).value = ippan_summary.house_summary_lv00
                ws.cell(row=i+3, column=4).value = ippan_summary.house_summary_lv01_49
                ws.cell(row=i+3, column=5).value = ippan_summary.house_summary_lv50_99
                ws.cell(row=i+3, column=6).value = ippan_summary.house_summary_lv100
                ws.cell(row=i+3, column=7).value = ippan_summary.house_summary_half
                ws.cell(row=i+3, column=8).value = ippan_summary.house_summary_full
                ws.cell(row=i+3, column=9).value = ippan_summary.household_summary_lv00
                ws.cell(row=i+3, column=10).value = ippan_summary.household_summary_lv01_49
                ws.cell(row=i+3, column=11).value = ippan_summary.household_summary_lv50_99
                ws.cell(row=i+3, column=12).value = ippan_summary.household_summary_lv100
                ws.cell(row=i+3, column=13).value = ippan_summary.household_summary_half
                ws.cell(row=i+3, column=14).value = ippan_summary.household_summary_full
                ws.cell(row=i+3, column=15).value = ippan_summary.car_summary_lv00
                ws.cell(row=i+3, column=16).value = ippan_summary.car_summary_lv01_49
                ws.cell(row=i+3, column=17).value = ippan_summary.car_summary_lv50_99
                ws.cell(row=i+3, column=18).value = ippan_summary.car_summary_lv100
                ws.cell(row=i+3, column=19).value = ippan_summary.car_summary_half
                ws.cell(row=i+3, column=20).value = ippan_summary.car_summary_full
                ws.cell(row=i+3, column=21).value = ippan_summary.house_alt_summary_lv00
                ws.cell(row=i+3, column=22).value = ippan_summary.house_alt_summary_lv01_49
                ws.cell(row=i+3, column=23).value = ippan_summary.house_alt_summary_lv50_99
                ws.cell(row=i+3, column=24).value = ippan_summary.house_alt_summary_lv100
                ws.cell(row=i+3, column=25).value = ippan_summary.house_alt_summary_half
                ws.cell(row=i+3, column=26).value = ippan_summary.house_alt_summary_full
                ws.cell(row=i+3, column=27).value = ippan_summary.house_clean_summary_lv00
                ws.cell(row=i+3, column=28).value = ippan_summary.house_clean_summary_lv01_49
                ws.cell(row=i+3, column=29).value = ippan_summary.house_clean_summary_lv50_99
                ws.cell(row=i+3, column=30).value = ippan_summary.house_clean_summary_lv100
                ws.cell(row=i+3, column=31).value = ippan_summary.house_clean_summary_half
                ws.cell(row=i+3, column=32).value = ippan_summary.house_clean_summary_full
                ws.cell(row=i+3, column=33).value = ippan_summary.office_dep_summary_lv00
                ws.cell(row=i+3, column=34).value = ippan_summary.office_dep_summary_lv01_49
                ws.cell(row=i+3, column=35).value = ippan_summary.office_dep_summary_lv50_99
                ws.cell(row=i+3, column=36).value = ippan_summary.office_dep_summary_lv100
                ws.cell(row=i+3, column=37).value = ippan_summary.office_dep_summary_full
                ws.cell(row=i+3, column=38).value = ippan_summary.office_inv_summary_lv00
                ws.cell(row=i+3, column=39).value = ippan_summary.office_inv_summary_lv01_49
                ws.cell(row=i+3, column=40).value = ippan_summary.office_inv_summary_lv50_99
                ws.cell(row=i+3, column=41).value = ippan_summary.office_inv_summary_lv100
                ws.cell(row=i+3, column=42).value = ippan_summary.office_inv_summary_full
                ws.cell(row=i+3, column=43).value = ippan_summary.office_sus_summary_lv00
                ws.cell(row=i+3, column=44).value = ippan_summary.office_sus_summary_lv01_49
                ws.cell(row=i+3, column=45).value = ippan_summary.office_sus_summary_lv50_99
                ws.cell(row=i+3, column=46).value = ippan_summary.office_sus_summary_lv100
                ws.cell(row=i+3, column=47).value = ippan_summary.office_sus_summary_full
                ws.cell(row=i+3, column=48).value = ippan_summary.office_stg_summary_lv00
                ws.cell(row=i+3, column=49).value = ippan_summary.office_stg_summary_lv01_49
                ws.cell(row=i+3, column=50).value = ippan_summary.office_stg_summary_lv50_99
                ws.cell(row=i+3, column=51).value = ippan_summary.office_stg_summary_lv100
                ws.cell(row=i+3, column=52).value = ippan_summary.office_stg_summary_full
                ws.cell(row=i+3, column=53).value = ippan_summary.farmer_fisher_dep_summary_lv00
                ws.cell(row=i+3, column=54).value = ippan_summary.farmer_fisher_dep_summary_lv01_49
                ws.cell(row=i+3, column=55).value = ippan_summary.farmer_fisher_dep_summary_lv50_99
                ws.cell(row=i+3, column=56).value = ippan_summary.farmer_fisher_dep_summary_lv100
                ws.cell(row=i+3, column=57).value = ippan_summary.farmer_fisher_dep_summary_full
                ws.cell(row=i+3, column=58).value = ippan_summary.farmer_fisher_inv_summary_lv00
                ws.cell(row=i+3, column=59).value = ippan_summary.farmer_fisher_inv_summary_lv01_49
                ws.cell(row=i+3, column=60).value = ippan_summary.farmer_fisher_inv_summary_lv50_99
                ws.cell(row=i+3, column=61).value = ippan_summary.farmer_fisher_inv_summary_lv100
                ws.cell(row=i+3, column=62).value = ippan_summary.farmer_fisher_inv_summary_full
                ws.cell(row=i+3, column=63).value = ippan_summary.office_alt_summary_lv00
                ws.cell(row=i+3, column=64).value = ippan_summary.office_alt_summary_lv01_49
                ws.cell(row=i+3, column=65).value = ippan_summary.office_alt_summary_lv50_99
                ws.cell(row=i+3, column=66).value = ippan_summary.office_alt_summary_lv100
                ws.cell(row=i+3, column=67).value = ippan_summary.office_alt_summary_half
                ws.cell(row=i+3, column=68).value = ippan_summary.office_alt_summary_full
                ws.cell(row=i+3, column=69).value = str(ippan_summary.deleted_at)
            
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_summary_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_summary.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_summary_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_summary_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_group_by_ken_view(request, lock)
### 8010：集計データ_集計結果_都道府県別
### urlpattern：path('ippan_group_by_ken/', views.ippan_group_by_ken_view, name='ippan_group_by_ken_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_group_by_ken_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、集計データ_集計結果_都道府県別データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 STEP 2/4.', 'INFO')
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
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ippan_group_by_ken.xlsx'
        download_file_path = 'static/download_ippan_group_by_ken.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '一般資産集計データ_集計結果_都道府県別'
        ws.cell(row=1, column=1).value = '都道府県コード'
        ### ws.cell(row=1, column=2).value = '一般資産調査票ID'
        ### ws.cell(row=1, column=3).value = '水害ID'
        ws.cell(row=1, column=2).value = '家屋被害額_床下'
        ws.cell(row=1, column=3).value = '家屋被害額_01から49cm'
        ws.cell(row=1, column=4).value = '家屋被害額_50から99cm'
        ws.cell(row=1, column=5).value = '家屋被害額_100cm以上'
        ws.cell(row=1, column=6).value = '家屋被害額_半壊'
        ws.cell(row=1, column=7).value = '家屋被害額_全壊'
        ws.cell(row=1, column=8).value = '家庭用品自動車以外被害額_床下'
        ws.cell(row=1, column=9).value = '家庭用品自動車以外被害額_01から49cm'
        ws.cell(row=1, column=10).value = '家庭用品自動車以外被害額_50から99cm'
        ws.cell(row=1, column=11).value = '家庭用品自動車以外被害額_100cm以上'
        ws.cell(row=1, column=12).value = '家庭用品自動車以外被害額_半壊'
        ws.cell(row=1, column=13).value = '家庭用品自動車以外被害額_全壊'
        ws.cell(row=1, column=14).value = '家庭用品自動車被害額_床下'
        ws.cell(row=1, column=15).value = '家庭用品自動車被害額_01から49cm'
        ws.cell(row=1, column=16).value = '家庭用品自動車被害額_50から99cm'
        ws.cell(row=1, column=17).value = '家庭用品自動車被害額_100cm以上'
        ws.cell(row=1, column=18).value = '家庭用品自動車被害額_半壊'
        ws.cell(row=1, column=19).value = '家庭用品自動車被害額_全壊'
        ws.cell(row=1, column=20).value = '家庭応急対策費_代替活動費_床下'
        ws.cell(row=1, column=21).value = '家庭応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=22).value = '家庭応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=23).value = '家庭応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=24).value = '家庭応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=25).value = '家庭応急対策費_代替活動費_全壊'
        ws.cell(row=1, column=26).value = '家庭応急対策費_清掃費_床下'
        ws.cell(row=1, column=27).value = '家庭応急対策費_清掃費_01から49cm'
        ws.cell(row=1, column=28).value = '家庭応急対策費_清掃費_50から99cm'
        ws.cell(row=1, column=29).value = '家庭応急対策費_清掃費_100cm以上'
        ws.cell(row=1, column=30).value = '家庭応急対策費_清掃費_半壊'
        ws.cell(row=1, column=31).value = '家庭応急対策費_清掃費_全壊'
        ws.cell(row=1, column=32).value = '事業所被害額_償却資産被害額_床下'
        ws.cell(row=1, column=33).value = '事業所被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=34).value = '事業所被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=35).value = '事業所被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=36).value = '事業所被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=37).value = '事業所被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=38).value = '事業所被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=39).value = '事業所被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=40).value = '事業所被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=41).value = '事業所被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=42).value = '事業所被害額_営業停止に伴う被害額_床下'
        ws.cell(row=1, column=43).value = '事業所被害額_営業停止に伴う被害額_01から49cm'
        ws.cell(row=1, column=44).value = '事業所被害額_営業停止に伴う被害額_50から99cm'
        ws.cell(row=1, column=45).value = '事業所被害額_営業停止に伴う被害額_100cm以上'
        ws.cell(row=1, column=46).value = '事業所被害額_営業停止に伴う被害額_全壊'
        ws.cell(row=1, column=47).value = '事業所被害額_営業停滞に伴う被害額_床下'
        ws.cell(row=1, column=48).value = '事業所被害額_営業停滞に伴う被害額_01から49cm'
        ws.cell(row=1, column=49).value = '事業所被害額_営業停滞に伴う被害額_50から99cm'
        ws.cell(row=1, column=50).value = '事業所被害額_営業停滞に伴う被害額_100cm以上'
        ws.cell(row=1, column=51).value = '事業所被害額_営業停滞に伴う被害額_全壊'
        ws.cell(row=1, column=52).value = '農漁家被害額_償却資産被害額_床下'
        ws.cell(row=1, column=53).value = '農漁家被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=54).value = '農漁家被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=55).value = '農漁家被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=56).value = '農漁家被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=57).value = '農漁家被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=58).value = '農漁家被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=59).value = '農漁家被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=60).value = '農漁家被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=61).value = '農漁家被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=62).value = '事業所応急対策費_代替活動費_床下'
        ws.cell(row=1, column=63).value = '事業所応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=64).value = '事業所応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=65).value = '事業所応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=66).value = '事業所応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=67).value = '事業所応急対策費_代替活動費_全壊'
        
        if ippan_group_by_ken_list:
            for i, ippan_group_by_ken in enumerate(ippan_group_by_ken_list):
                ws.cell(row=i+2, column=1).value = ippan_group_by_ken.id
                ### ws.cell(row=i+2, column=2).value = ippan_group_by_ken.ippan_id
                ### ws.cell(row=i+2, column=3).value = ippan_group_by_ken.suigai_id
                ws.cell(row=i+2, column=2).value = ippan_group_by_ken.house_summary_lv00
                ws.cell(row=i+2, column=3).value = ippan_group_by_ken.house_summary_lv01_49
                ws.cell(row=i+2, column=4).value = ippan_group_by_ken.house_summary_lv50_99
                ws.cell(row=i+2, column=5).value = ippan_group_by_ken.house_summary_lv100
                ws.cell(row=i+2, column=6).value = ippan_group_by_ken.house_summary_half
                ws.cell(row=i+2, column=7).value = ippan_group_by_ken.house_summary_full
                ws.cell(row=i+2, column=8).value = ippan_group_by_ken.household_summary_lv00
                ws.cell(row=i+2, column=9).value = ippan_group_by_ken.household_summary_lv01_49
                ws.cell(row=i+2, column=10).value = ippan_group_by_ken.household_summary_lv50_99
                ws.cell(row=i+2, column=11).value = ippan_group_by_ken.household_summary_lv100
                ws.cell(row=i+2, column=12).value = ippan_group_by_ken.household_summary_half
                ws.cell(row=i+2, column=13).value = ippan_group_by_ken.household_summary_full
                ws.cell(row=i+2, column=14).value = ippan_group_by_ken.car_summary_lv00
                ws.cell(row=i+2, column=15).value = ippan_group_by_ken.car_summary_lv01_49
                ws.cell(row=i+2, column=16).value = ippan_group_by_ken.car_summary_lv50_99
                ws.cell(row=i+2, column=17).value = ippan_group_by_ken.car_summary_lv100
                ws.cell(row=i+2, column=18).value = ippan_group_by_ken.car_summary_half
                ws.cell(row=i+2, column=19).value = ippan_group_by_ken.car_summary_full
                ws.cell(row=i+2, column=20).value = ippan_group_by_ken.house_alt_summary_lv00
                ws.cell(row=i+2, column=21).value = ippan_group_by_ken.house_alt_summary_lv01_49
                ws.cell(row=i+2, column=22).value = ippan_group_by_ken.house_alt_summary_lv50_99
                ws.cell(row=i+2, column=23).value = ippan_group_by_ken.house_alt_summary_lv100
                ws.cell(row=i+2, column=24).value = ippan_group_by_ken.house_alt_summary_half
                ws.cell(row=i+2, column=25).value = ippan_group_by_ken.house_alt_summary_full
                ws.cell(row=i+2, column=26).value = ippan_group_by_ken.house_clean_summary_lv00
                ws.cell(row=i+2, column=27).value = ippan_group_by_ken.house_clean_summary_lv01_49
                ws.cell(row=i+2, column=28).value = ippan_group_by_ken.house_clean_summary_lv50_99
                ws.cell(row=i+2, column=29).value = ippan_group_by_ken.house_clean_summary_lv100
                ws.cell(row=i+2, column=30).value = ippan_group_by_ken.house_clean_summary_half
                ws.cell(row=i+2, column=31).value = ippan_group_by_ken.house_clean_summary_full
                ws.cell(row=i+2, column=32).value = ippan_group_by_ken.office_dep_summary_lv00
                ws.cell(row=i+2, column=33).value = ippan_group_by_ken.office_dep_summary_lv01_49
                ws.cell(row=i+2, column=34).value = ippan_group_by_ken.office_dep_summary_lv50_99
                ws.cell(row=i+2, column=35).value = ippan_group_by_ken.office_dep_summary_lv100
                ws.cell(row=i+2, column=36).value = ippan_group_by_ken.office_dep_summary_full
                ws.cell(row=i+2, column=37).value = ippan_group_by_ken.office_inv_summary_lv00
                ws.cell(row=i+2, column=38).value = ippan_group_by_ken.office_inv_summary_lv01_49
                ws.cell(row=i+2, column=39).value = ippan_group_by_ken.office_inv_summary_lv50_99
                ws.cell(row=i+2, column=40).value = ippan_group_by_ken.office_inv_summary_lv100
                ws.cell(row=i+2, column=41).value = ippan_group_by_ken.office_inv_summary_full
                ws.cell(row=i+2, column=42).value = ippan_group_by_ken.office_sus_summary_lv00
                ws.cell(row=i+2, column=43).value = ippan_group_by_ken.office_sus_summary_lv01_49
                ws.cell(row=i+2, column=44).value = ippan_group_by_ken.office_sus_summary_lv50_99
                ws.cell(row=i+2, column=45).value = ippan_group_by_ken.office_sus_summary_lv100
                ws.cell(row=i+2, column=46).value = ippan_group_by_ken.office_sus_summary_full
                ws.cell(row=i+2, column=47).value = ippan_group_by_ken.office_stg_summary_lv00
                ws.cell(row=i+2, column=48).value = ippan_group_by_ken.office_stg_summary_lv01_49
                ws.cell(row=i+2, column=49).value = ippan_group_by_ken.office_stg_summary_lv50_99
                ws.cell(row=i+2, column=50).value = ippan_group_by_ken.office_stg_summary_lv100
                ws.cell(row=i+2, column=51).value = ippan_group_by_ken.office_stg_summary_full
                ws.cell(row=i+2, column=52).value = ippan_group_by_ken.farmer_fisher_dep_summary_lv00
                ws.cell(row=i+2, column=53).value = ippan_group_by_ken.farmer_fisher_dep_summary_lv01_49
                ws.cell(row=i+2, column=54).value = ippan_group_by_ken.farmer_fisher_dep_summary_lv50_99
                ws.cell(row=i+2, column=55).value = ippan_group_by_ken.farmer_fisher_dep_summary_lv100
                ws.cell(row=i+2, column=56).value = ippan_group_by_ken.farmer_fisher_dep_summary_full
                ws.cell(row=i+2, column=57).value = ippan_group_by_ken.farmer_fisher_inv_summary_lv00
                ws.cell(row=i+2, column=58).value = ippan_group_by_ken.farmer_fisher_inv_summary_lv01_49
                ws.cell(row=i+2, column=59).value = ippan_group_by_ken.farmer_fisher_inv_summary_lv50_99
                ws.cell(row=i+2, column=60).value = ippan_group_by_ken.farmer_fisher_inv_summary_lv100
                ws.cell(row=i+2, column=61).value = ippan_group_by_ken.farmer_fisher_inv_summary_full
                ws.cell(row=i+2, column=62).value = ippan_group_by_ken.office_alt_summary_lv00
                ws.cell(row=i+2, column=63).value = ippan_group_by_ken.office_alt_summary_lv01_49
                ws.cell(row=i+2, column=64).value = ippan_group_by_ken.office_alt_summary_lv50_99
                ws.cell(row=i+2, column=65).value = ippan_group_by_ken.office_alt_summary_lv100
                ws.cell(row=i+2, column=66).value = ippan_group_by_ken.office_alt_summary_half
                ws.cell(row=i+2, column=67).value = ippan_group_by_ken.office_alt_summary_full
            
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_ken_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_group_by_ken.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_group_by_ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_group_by_ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_group_by_suikei_view(request, lock)
### 8020：集計データ_集計結果_水系別
### urlpattern：path('ippan_group_by_suikei/', views.ippan_group_by_suikei_view, name='ippan_group_by_suikei')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_group_by_suikei_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、一般資産集計データ_集計結果_水系別データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 STEP 2/4.', 'INFO')
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
            ORDER BY CAST(SG1.SUIKEI_CODE AS INTEGER)
        """, [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_ippan_group_by_suikei.xlsx'
        download_file_path = 'static/download_ippan_group_by_suikei.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '一般資産集計データ_集計結果_水系別'
        ws.cell(row=1, column=1).value = '水系コード'
        ### ws.cell(row=1, column=2).value = '一般資産調査票ID'
        ### ws.cell(row=1, column=3).value = '水害ID'
        ws.cell(row=1, column=2).value = '家屋被害額_床下'
        ws.cell(row=1, column=3).value = '家屋被害額_01から49cm'
        ws.cell(row=1, column=4).value = '家屋被害額_50から99cm'
        ws.cell(row=1, column=5).value = '家屋被害額_100cm以上'
        ws.cell(row=1, column=6).value = '家屋被害額_半壊'
        ws.cell(row=1, column=7).value = '家屋被害額_全壊'
        ws.cell(row=1, column=8).value = '家庭用品自動車以外被害額_床下'
        ws.cell(row=1, column=9).value = '家庭用品自動車以外被害額_01から49cm'
        ws.cell(row=1, column=10).value = '家庭用品自動車以外被害額_50から99cm'
        ws.cell(row=1, column=11).value = '家庭用品自動車以外被害額_100cm以上'
        ws.cell(row=1, column=12).value = '家庭用品自動車以外被害額_半壊'
        ws.cell(row=1, column=13).value = '家庭用品自動車以外被害額_全壊'
        ws.cell(row=1, column=14).value = '家庭用品自動車被害額_床下'
        ws.cell(row=1, column=15).value = '家庭用品自動車被害額_01から49cm'
        ws.cell(row=1, column=16).value = '家庭用品自動車被害額_50から99cm'
        ws.cell(row=1, column=17).value = '家庭用品自動車被害額_100cm以上'
        ws.cell(row=1, column=18).value = '家庭用品自動車被害額_半壊'
        ws.cell(row=1, column=19).value = '家庭用品自動車被害額_全壊'
        ws.cell(row=1, column=20).value = '家庭応急対策費_代替活動費_床下'
        ws.cell(row=1, column=21).value = '家庭応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=22).value = '家庭応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=23).value = '家庭応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=24).value = '家庭応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=25).value = '家庭応急対策費_代替活動費_全壊'
        ws.cell(row=1, column=26).value = '家庭応急対策費_清掃費_床下'
        ws.cell(row=1, column=27).value = '家庭応急対策費_清掃費_01から49cm'
        ws.cell(row=1, column=28).value = '家庭応急対策費_清掃費_50から99cm'
        ws.cell(row=1, column=29).value = '家庭応急対策費_清掃費_100cm以上'
        ws.cell(row=1, column=30).value = '家庭応急対策費_清掃費_半壊'
        ws.cell(row=1, column=31).value = '家庭応急対策費_清掃費_全壊'
        ws.cell(row=1, column=32).value = '事業所被害額_償却資産被害額_床下'
        ws.cell(row=1, column=33).value = '事業所被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=34).value = '事業所被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=35).value = '事業所被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=36).value = '事業所被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=37).value = '事業所被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=38).value = '事業所被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=39).value = '事業所被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=40).value = '事業所被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=41).value = '事業所被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=42).value = '事業所被害額_営業停止に伴う被害額_床下'
        ws.cell(row=1, column=43).value = '事業所被害額_営業停止に伴う被害額_01から49cm'
        ws.cell(row=1, column=44).value = '事業所被害額_営業停止に伴う被害額_50から99cm'
        ws.cell(row=1, column=45).value = '事業所被害額_営業停止に伴う被害額_100cm以上'
        ws.cell(row=1, column=46).value = '事業所被害額_営業停止に伴う被害額_全壊'
        ws.cell(row=1, column=47).value = '事業所被害額_営業停滞に伴う被害額_床下'
        ws.cell(row=1, column=48).value = '事業所被害額_営業停滞に伴う被害額_01から49cm'
        ws.cell(row=1, column=49).value = '事業所被害額_営業停滞に伴う被害額_50から99cm'
        ws.cell(row=1, column=50).value = '事業所被害額_営業停滞に伴う被害額_100cm以上'
        ws.cell(row=1, column=51).value = '事業所被害額_営業停滞に伴う被害額_全壊'
        ws.cell(row=1, column=52).value = '農漁家被害額_償却資産被害額_床下'
        ws.cell(row=1, column=53).value = '農漁家被害額_償却資産被害額_01から49cm'
        ws.cell(row=1, column=54).value = '農漁家被害額_償却資産被害額_50から99cm'
        ws.cell(row=1, column=55).value = '農漁家被害額_償却資産被害額_100cm以上'
        ws.cell(row=1, column=56).value = '農漁家被害額_償却資産被害額_全壊'
        ws.cell(row=1, column=57).value = '農漁家被害額_在庫資産被害額_床下'
        ws.cell(row=1, column=58).value = '農漁家被害額_在庫資産被害額_01から49cm'
        ws.cell(row=1, column=59).value = '農漁家被害額_在庫資産被害額_50から99cm'
        ws.cell(row=1, column=60).value = '農漁家被害額_在庫資産被害額_100cm以上'
        ws.cell(row=1, column=61).value = '農漁家被害額_在庫資産被害額_全壊'
        ws.cell(row=1, column=62).value = '事業所応急対策費_代替活動費_床下'
        ws.cell(row=1, column=63).value = '事業所応急対策費_代替活動費_01から49cm'
        ws.cell(row=1, column=64).value = '事業所応急対策費_代替活動費_50から99cm'
        ws.cell(row=1, column=65).value = '事業所応急対策費_代替活動費_100cm以上'
        ws.cell(row=1, column=66).value = '事業所応急対策費_代替活動費_半壊'
        ws.cell(row=1, column=67).value = '事業所応急対策費_代替活動費_全壊'
        
        if ippan_group_by_suikei_list:
            for i, ippan_group_by_suikei in enumerate(ippan_group_by_suikei_list):
                ws.cell(row=i+2, column=1).value = ippan_group_by_suikei.id
                ### ws.cell(row=i+2, column=2).value = ippan_group_by_suikei.ippan_id
                ### ws.cell(row=i+2, column=3).value = ippan_group_by_suikei.suigai_id
                ws.cell(row=i+2, column=2).value = ippan_group_by_suikei.house_summary_lv00
                ws.cell(row=i+2, column=3).value = ippan_group_by_suikei.house_summary_lv01_49
                ws.cell(row=i+2, column=4).value = ippan_group_by_suikei.house_summary_lv50_99
                ws.cell(row=i+2, column=5).value = ippan_group_by_suikei.house_summary_lv100
                ws.cell(row=i+2, column=6).value = ippan_group_by_suikei.house_summary_half
                ws.cell(row=i+2, column=7).value = ippan_group_by_suikei.house_summary_full
                ws.cell(row=i+2, column=8).value = ippan_group_by_suikei.household_summary_lv00
                ws.cell(row=i+2, column=9).value = ippan_group_by_suikei.household_summary_lv01_49
                ws.cell(row=i+2, column=10).value = ippan_group_by_suikei.household_summary_lv50_99
                ws.cell(row=i+2, column=11).value = ippan_group_by_suikei.household_summary_lv100
                ws.cell(row=i+2, column=12).value = ippan_group_by_suikei.household_summary_half
                ws.cell(row=i+2, column=13).value = ippan_group_by_suikei.household_summary_full
                ws.cell(row=i+2, column=14).value = ippan_group_by_suikei.car_summary_lv00
                ws.cell(row=i+2, column=15).value = ippan_group_by_suikei.car_summary_lv01_49
                ws.cell(row=i+2, column=16).value = ippan_group_by_suikei.car_summary_lv50_99
                ws.cell(row=i+2, column=17).value = ippan_group_by_suikei.car_summary_lv100
                ws.cell(row=i+2, column=18).value = ippan_group_by_suikei.car_summary_half
                ws.cell(row=i+2, column=19).value = ippan_group_by_suikei.car_summary_full
                ws.cell(row=i+2, column=20).value = ippan_group_by_suikei.house_alt_summary_lv00
                ws.cell(row=i+2, column=21).value = ippan_group_by_suikei.house_alt_summary_lv01_49
                ws.cell(row=i+2, column=22).value = ippan_group_by_suikei.house_alt_summary_lv50_99
                ws.cell(row=i+2, column=23).value = ippan_group_by_suikei.house_alt_summary_lv100
                ws.cell(row=i+2, column=24).value = ippan_group_by_suikei.house_alt_summary_half
                ws.cell(row=i+2, column=25).value = ippan_group_by_suikei.house_alt_summary_full
                ws.cell(row=i+2, column=26).value = ippan_group_by_suikei.house_clean_summary_lv00
                ws.cell(row=i+2, column=27).value = ippan_group_by_suikei.house_clean_summary_lv01_49
                ws.cell(row=i+2, column=28).value = ippan_group_by_suikei.house_clean_summary_lv50_99
                ws.cell(row=i+2, column=29).value = ippan_group_by_suikei.house_clean_summary_lv100
                ws.cell(row=i+2, column=30).value = ippan_group_by_suikei.house_clean_summary_half
                ws.cell(row=i+2, column=31).value = ippan_group_by_suikei.house_clean_summary_full
                ws.cell(row=i+2, column=32).value = ippan_group_by_suikei.office_dep_summary_lv00
                ws.cell(row=i+2, column=33).value = ippan_group_by_suikei.office_dep_summary_lv01_49
                ws.cell(row=i+2, column=34).value = ippan_group_by_suikei.office_dep_summary_lv50_99
                ws.cell(row=i+2, column=35).value = ippan_group_by_suikei.office_dep_summary_lv100
                ws.cell(row=i+2, column=36).value = ippan_group_by_suikei.office_dep_summary_full
                ws.cell(row=i+2, column=37).value = ippan_group_by_suikei.office_inv_summary_lv00
                ws.cell(row=i+2, column=38).value = ippan_group_by_suikei.office_inv_summary_lv01_49
                ws.cell(row=i+2, column=39).value = ippan_group_by_suikei.office_inv_summary_lv50_99
                ws.cell(row=i+2, column=40).value = ippan_group_by_suikei.office_inv_summary_lv100
                ws.cell(row=i+2, column=41).value = ippan_group_by_suikei.office_inv_summary_full
                ws.cell(row=i+2, column=42).value = ippan_group_by_suikei.office_sus_summary_lv00
                ws.cell(row=i+2, column=43).value = ippan_group_by_suikei.office_sus_summary_lv01_49
                ws.cell(row=i+2, column=44).value = ippan_group_by_suikei.office_sus_summary_lv50_99
                ws.cell(row=i+2, column=45).value = ippan_group_by_suikei.office_sus_summary_lv100
                ws.cell(row=i+2, column=46).value = ippan_group_by_suikei.office_sus_summary_full
                ws.cell(row=i+2, column=47).value = ippan_group_by_suikei.office_stg_summary_lv00
                ws.cell(row=i+2, column=48).value = ippan_group_by_suikei.office_stg_summary_lv01_49
                ws.cell(row=i+2, column=49).value = ippan_group_by_suikei.office_stg_summary_lv50_99
                ws.cell(row=i+2, column=50).value = ippan_group_by_suikei.office_stg_summary_lv100
                ws.cell(row=i+2, column=51).value = ippan_group_by_suikei.office_stg_summary_full
                ws.cell(row=i+2, column=52).value = ippan_group_by_suikei.farmer_fisher_dep_summary_lv00
                ws.cell(row=i+2, column=53).value = ippan_group_by_suikei.farmer_fisher_dep_summary_lv01_49
                ws.cell(row=i+2, column=54).value = ippan_group_by_suikei.farmer_fisher_dep_summary_lv50_99
                ws.cell(row=i+2, column=55).value = ippan_group_by_suikei.farmer_fisher_dep_summary_lv100
                ws.cell(row=i+2, column=56).value = ippan_group_by_suikei.farmer_fisher_dep_summary_full
                ws.cell(row=i+2, column=57).value = ippan_group_by_suikei.farmer_fisher_inv_summary_lv00
                ws.cell(row=i+2, column=58).value = ippan_group_by_suikei.farmer_fisher_inv_summary_lv01_49
                ws.cell(row=i+2, column=59).value = ippan_group_by_suikei.farmer_fisher_inv_summary_lv50_99
                ws.cell(row=i+2, column=60).value = ippan_group_by_suikei.farmer_fisher_inv_summary_lv100
                ws.cell(row=i+2, column=61).value = ippan_group_by_suikei.farmer_fisher_inv_summary_full
                ws.cell(row=i+2, column=62).value = ippan_group_by_suikei.office_alt_summary_lv00
                ws.cell(row=i+2, column=63).value = ippan_group_by_suikei.office_alt_summary_lv01_49
                ws.cell(row=i+2, column=64).value = ippan_group_by_suikei.office_alt_summary_lv50_99
                ws.cell(row=i+2, column=65).value = ippan_group_by_suikei.office_alt_summary_lv100
                ws.cell(row=i+2, column=66).value = ippan_group_by_suikei.office_alt_summary_half
                ws.cell(row=i+2, column=67).value = ippan_group_by_suikei.office_alt_summary_full
            
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_group_by_suikei_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_group_by_suikei.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_group_by_suikei_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_group_by_suikei_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_chosa_view(request, lock)
### 一般資産調査票（調査員用）
### ※複数EXCELファイル、複数EXCELシート対応版
### urlpattern：path('ippan_chosa/', views.ippan_chosa_view, name='ippan_chosa_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_chosa_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        ### (2)GETメソッドの場合、関数を抜ける。
        ### (3)POSTリクエストの市区町村数が0件の場合、関数を抜ける。
        ### ※関数の内部のネスト数を浅くするため。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 city_code_hidden= {}'.format(request.POST.get('city_code_hidden')), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 1/12.', 'INFO')

        if request.method == 'GET':
            print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        if request.POST.get('city_code_hidden') is None:
            print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')
            
        city_code_request = [x.strip() for x in request.POST.get('city_code_hidden').split(',')][:-1]

        if city_code_request:
            if len(city_code_request) == 0:
                print_log('[WARN] P0200ExcelDownload.ippan_chosa_view()関数で警告が発生しました。', 'WARN')
                return render(request, 'warning.html')

        #######################################################################
        ### 局所定数セット処理(0010)
        ### VLOOKUP用の局所定数をセットする。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 2/12.', 'INFO')
        VLOOK_VALUE = [
            'B', 'G', 'L', 'Q', 'V', 'AA', 'AF', 'AK', 'AP', 'AU', 
            'AZ', 'BE', 'BJ', 'BO', 'BT', 'BY', 'CD', 'CI', 'CN', 'CS', 
            'CX', 'DC', 'DH', 'DM', 'DR', 'DW', 'EB', 'EG', 'EL', 'EQ', 
            'EV', 'FA', 'FF', 'FK', 'FP', 'FU', 'FZ', 'GE', 'GJ', 'GO', 
            'GT', 'GY', 'HD', 'HI', 'HN', 'HS', 'HX', 'IC', 'IH', 'IM', 
            'IR', 'IW', 'JB', 'JG', 'JL', 'JQ', 'JV', 'KA', 'KF', 'KK', 
            'KP', 'KU', 'KZ', 'LE', 'LJ', 'LO', 'LT', 'LY', 'MD', 'MI', 
            'MN', 'MS', 'MX', 'NC', 'NH', 'NM', 'NR', 'NW', 'OB', 'OG', 
            'OL', 'OQ', 'OV', 'PA', 'PF', 'PK', 'PP', 'PU', 'PZ', 'QE', 
            'QJ', 'QO', 'QT', 'QY', 'RD', 'RI', 'RN', 'RS', 'RX', 'SC', 
            'SH', 'SM', 'SR', 'SW', 'TB', 'TG', 'TL', 'TQ', 'TV', 'UA', 
            'UF', 'UK', 'UP', 'UU', 'UZ', 'VE', 'VJ', 'VO', 'VT', 'VY', 
            'WD', 'WI', 'WN', 'WS', 'WX', 'XC', 'XH', 'XM', 'XR', 'XW', 
            'YB', 'YG', 'YL', 'YQ', 'YV', 'ZA', 'ZF', 'ZK', 'ZP', 'ZU', 
            'ZZ', 'AAE', 'AAJ', 'AAO', 'AAT', 'AAY', 'ABD', 'ABI', 'ABN', 'ABS', 
            'ABX', 'ACC', 'ACH', 'ACM', 'ACR', 'ACW', 'ADB', 'ADG', 'ADL', 'ADQ', 
            'ADV', 'AEA', 'AEF', 'AEK', 'AEP', 'AEU', 'AEZ', 'AFE', 'AFJ', 'AFO', 
            'AFT', 'AFY', 'AGD', 'AGI', 'AGN', 'AGS', 'AGX', 'AHC', 'AHH', 'AHM', 
            'AHR', 'AHW', 'AIB', 'AIG', 'AIL', 'AIQ', 'AIV', 'AJA', 'AJF', 'AJK', 
            'AJP', 'AJU', 'AJZ', 'AKE', 'AKJ', 'AKO', 'AKT', 'AKY', 'ALD', 'ALI', 
            'ALN', 'ALS', 'ALX', 'AMC', 'AMH', 'AMM', 'AMR', 'AMW', 'ANB', 'ANG', 
            'ANL', 'ANQ', 'ANV', 'AOA', 'AOF', 'AOK', 'AOP', 'AOU', 'AOZ', 'APE', 
            'APJ', 'APO', 'APT', 'APY', 'AQD', 'AQI', 'AQN', 'AQS', 'AQX', 'ARC', 
            'ARH', 'ARM', 'ARR', 'ARW', 'ASB', 'ASG', 'ASL', 'ASQ', 'ASV', 'ATA', 
            'ATF', 'ATK', 'ATP', 'ATU', 'ATZ', 'AUE', 'AUJ', 'AUO', 'AUT', 'AUY', 
            'AVD', 'AVI', 'AVN', 'AVS', 'AVX', 'AWC', 'AWH', 'AWM', 'AWR', 'AWW', 
            'AXB', 'AXG', 'AXL', 'AXQ', 'AXV', 'AYA', 'AYF', 'AYK', 'AYP', 'AYU', 
            'AYZ', 'AZE', 'AZJ', 'AZO', 'AZT', 'AZY'
            ]

        #######################################################################
        ### DBアクセス処理(0020)
        ### DBから市区町村コード毎の一般調査票入力データのヘッダ部の件数を取得する。
        ### ※関数のメインの処理の前に、EXCELのファイル数、シート数を確定するため。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 3/12.', 'INFO')
        ### 市区町村コード毎の一般調査票入力データのヘッダ部の数、市区町村コード毎のシート数
        ### 例:[3, 2, 6, ] ※市区町村1のシート数3、市区町村2のシート数2、市区町村3のシート数6
        ### 市区町村コード毎の一般調査票入力データのヘッダ部IDのリスト、市区町村コード毎のシートID、水害IDのリスト
        ### 例:[[1,2,3], [4,5], [6,7,8,9,10,11], ] ※市区町村1のシート数3、市区町村2のシート数2、市区町村3のシート数6
        suigai_count_list = []
        suigai_id_list = []
        for city_code in city_code_request:
            suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI WHERE city_code=%s ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [city_code,])
            if suigai_list:
                suigai_count_list.append(len(suigai_list))
            else:
                suigai_count_list.append(0)

        for city_code in city_code_request:
            suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI WHERE city_code=%s ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [city_code,])
            ### if suigai_list:
            ###     _suigai_id_ = []
            ###     for suigai in suigai_list:
            ###         _suigai_id_.append(suigai.suigai_id)
            ###     
            ###     suigai_id.append(_suigai_id_)
            ### else:
            ###     suigai_id.append([])
            suigai_id_list.append([suigai.suigai_id for suigai in suigai_list])
                
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 suigai_count_list = {}'.format(suigai_count_list), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 suigai_id_list = {}'.format(suigai_id_list), 'INFO')
        
        #######################################################################
        ### EXCEL入出力処理(0030)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        ### ※市区町村毎にEXCELファイルを作成する。
        ### ※水害毎にEXCELシートを作成する。
        ### ※0件の場合、入力用にIPPANシートを10枚作成する。
        ### ※5件の場合、既存データ用にIPPANシートを5枚作成する。
        ### ※5件の場合、入力用にIPPANシートを10枚作成する。（合計15枚作成する。）
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 4/12.', 'INFO')
        download_file_path = []
        wb = []
        ws_ippan = []
        ws_building = []
        ws_ken = []
        ws_city = []
        ws_kasen_kaigan = []
        ws_suikei = []
        ws_suikei_type = []
        ws_kasen = []
        ws_kasen_type = []
        ws_cause = []
        ws_underground = []
        ws_usage = []
        ws_flood_sediment = []
        ws_gradient = []
        ws_industry = []
        ws_suigai = []
        ws_weather = []
        ws_area = []
        ws_city_vlook = []
        ws_kasen_vlook = []
        ws_suikei_type_vlook = [] ### NEW
        ws_kasen_type_vlook = []  ### NEW
        
        ### len(city_code_request)=ワークブックの数=EXCELファイルの数
        ### 一般資産テーブルを除き、EXCELファイル毎に、テーブル毎に１シートとする。
        ### 一般資産テーブルについては、EXCELファイル毎に、一般資産入力データ_ヘッダ部分、水害毎に1シートとする。
        ### 上記に加えて、新規入力用に空欄のシート10シートとする。
        for i, city_code in enumerate(city_code_request):
            template_file_path = 'static/template_ippan_chosa.xlsx'
            download_file_path.append('static/download_ippan_chosa_' + city_code + '.xlsx')
            
            wb.append(openpyxl.load_workbook(template_file_path, keep_vba=False))
            
            ws_building.append(wb[i]["BUILDING"])
            ws_ken.append(wb[i]["KEN"])
            ws_city.append(wb[i]["CITY"])
            ws_kasen_kaigan.append(wb[i]["KASEN_KAIGAN"])
            ws_suikei.append(wb[i]["SUIKEI"])
            ws_suikei_type.append(wb[i]["SUIKEI_TYPE"])
            ws_kasen.append(wb[i]["KASEN"])
            ws_kasen_type.append(wb[i]["KASEN_TYPE"])
            ws_cause.append(wb[i]["CAUSE"])
            ws_underground.append(wb[i]["UNDERGROUND"])
            ws_usage.append(wb[i]["USAGE"])
            ws_flood_sediment.append(wb[i]["FLOOD_SEDIMENT"])
            ws_gradient.append(wb[i]["GRADIENT"])
            ws_industry.append(wb[i]["INDUSTRY"])
            ws_suigai.append(wb[i]["SUIGAI"])
            ws_weather.append(wb[i]["WEATHER"])
            ws_area.append(wb[i]["AREA"])
            ws_city_vlook.append(wb[i]["CITY_VLOOK"])
            ws_kasen_vlook.append(wb[i]["KASEN_VLOOK"])
            ws_suikei_type_vlook.append(wb[i]["SUIKEI_TYPE_VLOOK"]) ### NEW
            ws_kasen_type_vlook.append(wb[i]["KASEN_TYPE_VLOOK"])   ### NEW
            
            ### 上記に加えて、新規入力用に空欄のシート10シートとする。
            ws_copy = []
            ws_copy.append(wb[i]["IPPAN"])
            for j in range(suigai_count_list[i] + 10):
                ws_copy.append(wb[i].copy_worksheet(wb[i]["IPPAN"]))
                ws_copy[j+1].title = 'IPPAN' + str(j+1)
                
            ws_ippan.append(ws_copy)

        #######################################################################
        ### DBアクセス処理(0040)
        ### EXCEL入出力処理(0040)
        ### (1)DBから建物区分等のマスタデータを取得する。
        ### (2)EXCELのマスタ用のシートのセルに、DBから取得した建物区分等のマスタデータを埋め込む。
        ### =VLOOKUP(B10,SUIKEI_TYPE_VLOOKUP!A:B,2,0)
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 5/12.', 'INFO')
        
        ### 1000: 建物区分シート
        print("ippan_chosa_view2", flush=True)
        building_list = None
        building_list = BUILDING.objects.raw("""SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if building_list:
                for j, building in enumerate(building_list):
                    ws_building[i].cell(row=j+1, column=1).value = building.building_code
                    ws_building[i].cell(row=j+1, column=2).value = str(building.building_name) + ":" + str(building.building_code)

        ### 1010: 都道府県シート
        print("ippan_chosa_view3", flush=True)
        ken_list = None
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if ken_list:
                for j, ken in enumerate(ken_list):
                    ws_ken[i].cell(row=j+1, column=1).value = ken.ken_code
                    ws_ken[i].cell(row=j+1, column=2).value = str(ken.ken_name) + ":" + str(ken.ken_code)
        
        ### 1020: 市区町村シート
        print("ippan_chosa_view4_1", flush=True)
        cities_list = []
        if ken_list:
            for i, ken in enumerate(ken_list):
                cities_list.append(CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken.ken_code, ]))
        
        print("ippan_chosa_view4_3", flush=True)
        for i, _ in enumerate(city_code_request):
            if cities_list:
                for j, cities in enumerate(cities_list):
                    if cities:
                        for k, city in enumerate(cities):
                            ws_city[i].cell(row=k+1, column=j*5+1).value = city.city_code
                            ws_city[i].cell(row=k+1, column=j*5+2).value = str(city.city_name) + ":" + str(city.city_code)
                            ws_city[i].cell(row=k+1, column=j*5+3).value = city.ken_code
                            ws_city[i].cell(row=k+1, column=j*5+4).value = city.city_population
                            ws_city[i].cell(row=k+1, column=j*5+5).value = city.city_area

        ### 1030: 水害発生地点工種（河川海岸区分）
        print("ippan_chosa_view5", flush=True)
        kasen_kaigan_list = None
        kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if kasen_kaigan_list:
                for j, kasen_kaigan in enumerate(kasen_kaigan_list):
                    ws_kasen_kaigan[i].cell(row=j+1, column=1).value = kasen_kaigan.kasen_kaigan_code
                    ws_kasen_kaigan[i].cell(row=j+1, column=2).value = kasen_kaigan.kasen_kaigan_name + ":" + kasen_kaigan.kasen_kaigan_code

        ### 1040: 水系（水系・沿岸）
        print("ippan_chosa_view6", flush=True)
        suikei_list = None
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if suikei_list:
                for j, suikei in enumerate(suikei_list):
                    ws_suikei[i].cell(row=j+1, column=1).value = suikei.suikei_code
                    ws_suikei[i].cell(row=j+1, column=2).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)
                    ws_suikei[i].cell(row=j+1, column=3).value = suikei.suikei_type_code

        ### 1050: 水系種別（水系・沿岸種別）
        print("ippan_chosa_view7", flush=True)
        suikei_type_list = None
        suikei_type_list = SUIKEI_TYPE.objects.raw("""SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if suikei_type_list:
                for j, suikei_type in enumerate(suikei_type_list):
                    ws_suikei_type[i].cell(row=j+1, column=1).value = suikei_type.suikei_type_code
                    ws_suikei_type[i].cell(row=j+1, column=2).value = str(suikei_type.suikei_type_name) + ":" + str(suikei_type.suikei_type_code)

        ### 1060: 河川（河川・海岸）、連動プルダウン用
        print("ippan_chosa_view8_1", flush=True)
        kasens_list = []
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                kasens_list.append(KASEN.objects.raw("""SELECT * FROM KASEN WHERE SUIKEI_CODE=%s ORDER BY CAST(KASEN_CODE AS INTEGER)""", [suikei.suikei_code, ]))

        print("ippan_chosa_view8_3", flush=True)
        for i, _ in enumerate(city_code_request):
            if kasens_list:
                for j, kasens in enumerate(kasens_list):
                    if kasens:
                        for k, kasen in enumerate(kasens):
                            ws_kasen[i].cell(row=k+1, column=j*5+1).value = kasen.kasen_code
                            ws_kasen[i].cell(row=k+1, column=j*5+2).value = str(kasen.kasen_name) + ":" + str(kasen.kasen_code)
                            ws_kasen[i].cell(row=k+1, column=j*5+3).value = kasen.kasen_type_code
                            ws_kasen[i].cell(row=k+1, column=j*5+4).value = kasen.suikei_code

        ### 1070: 河川種別（河川・海岸種別）
        print("ippan_chosa_view9", flush=True)
        kasen_type_list = None
        kasen_type_list = KASEN_TYPE.objects.raw("""SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if kasen_type_list:
                for j, kasen_type in enumerate(kasen_type_list):
                    ws_kasen_type[i].cell(row=j+1, column=1).value = kasen_type.kasen_type_code
                    ws_kasen_type[i].cell(row=j+1, column=2).value = str(kasen_type.kasen_type_name) + ":" + str(kasen_type.kasen_type_code)
        
        ### 1080: 水害原因
        print("ippan_chosa_view10", flush=True)
        cause_list = None
        cause_list = CAUSE.objects.raw("""SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if cause_list:
                for j, cause in enumerate(cause_list):
                    ws_cause[i].cell(row=j+1, column=1).value = cause.cause_code
                    ws_cause[i].cell(row=j+1, column=2).value = str(cause.cause_name) + ":" + str(cause.cause_code)
                
        ### 1090: 地上地下区分
        print("ippan_chosa_view11", flush=True)
        underground_list = None
        underground_list = UNDERGROUND.objects.raw("""SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if underground_list:
                for j, underground in enumerate(underground_list):
                    ws_underground[i].cell(row=j+1, column=1).value = underground.underground_code
                    ws_underground[i].cell(row=j+1, column=2).value = str(underground.underground_name) + ":" + str(underground.underground_code)
        
        ### 1100: 地下空間の利用形態
        print("ippan_chosa_view12", flush=True)
        usage_list = None
        usage_list = USAGE.objects.raw("""SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if usage_list:
                for j, usage in enumerate(usage_list):
                    ws_usage[i].cell(row=j+1, column=1).value = usage.usage_code
                    ws_usage[i].cell(row=j+1, column=2).value = str(usage.usage_name) + ":" + str(usage.usage_code)
        
        ### 1110: 浸水土砂区分
        print("ippan_chosa_view13", flush=True)
        flood_sediment_list = None
        flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if flood_sediment_list:
                for j, flood_sediment in enumerate(flood_sediment_list):
                    ws_flood_sediment[i].cell(row=j+1, column=1).value = flood_sediment.flood_sediment_code
                    ws_flood_sediment[i].cell(row=j+1, column=2).value = str(flood_sediment.flood_sediment_name) + ":" + str(flood_sediment.flood_sediment_code)
        
        ### 1120: 地盤勾配区分
        print("ippan_chosa_view14", flush=True)
        gradient_list = None
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if gradient_list:
                for j, gradient in enumerate(gradient_list):
                    ws_gradient[i].cell(row=j+1, column=1).value = gradient.gradient_code
                    ws_gradient[i].cell(row=j+1, column=2).value = str(gradient.gradient_name) + ":" + str(gradient.gradient_code)
        
        ### 1130: 産業分類
        print("ippan_chosa_view15", flush=True)
        industry_list = None
        industry_list = INDUSTRY.objects.raw("""SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if industry_list:
                for j, industry in enumerate(industry_list):
                    ws_industry[i].cell(row=j+1, column=1).value = industry.industry_code
                    ws_industry[i].cell(row=j+1, column=2).value = str(industry.industry_name) + ":" + str(industry.industry_code)

        ### 7000: 入力データ_水害区域
        print("ippan_chosa_view16", flush=True)
        area_list = None
        area_list = AREA.objects.raw("""SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if area_list:
                for j, area in enumerate(area_list):
                    ws_area[i].cell(row=j+1, column=1).value = area.area_id
                    ws_area[i].cell(row=j+1, column=2).value = str(area.area_name) + ":" + str(area.area_id)

        ### 7010: 入力データ_異常気象
        print("ippan_chosa_view17", flush=True)
        weather_list = None
        weather_list = WEATHER.objects.raw("""SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if weather_list:
                for j, weather in enumerate(weather_list):
                    ws_weather[i].cell(row=j+1, column=1).value = weather.weather_id
                    ws_weather[i].cell(row=j+1, column=2).value = str(weather.weather_name) + ":" + str(weather.weather_id)
        
        ### 7020: 入力データ_ヘッダ部分、水害
        print("ippan_chosa_view18", flush=True)
        suigai_list = None
        suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])
        for i, _ in enumerate(city_code_request):
            if suigai_list:
                for j, suigai in enumerate(suigai_list):
                    ws_suigai[i].cell(row=j+1, column=1).value = suigai.suigai_id
                    ws_suigai[i].cell(row=j+1, column=2).value = str(suigai.suigai_name) + ":" + str(suigai.suigai_id)
                    ws_suigai[i].cell(row=j+1, column=3).value = suigai.ken_code
                    ws_suigai[i].cell(row=j+1, column=4).value = suigai.city_code
                    ws_suigai[i].cell(row=j+1, column=5).value = suigai.begin_date
                    ws_suigai[i].cell(row=j+1, column=6).value = suigai.end_date
                    ws_suigai[i].cell(row=j+1, column=7).value = suigai.cause_1_code
                    ws_suigai[i].cell(row=j+1, column=8).value = suigai.cause_2_code
                    ws_suigai[i].cell(row=j+1, column=9).value = suigai.cause_3_code
                    ws_suigai[i].cell(row=j+1, column=10).value = suigai.area_id
                    ws_suigai[i].cell(row=j+1, column=11).value = suigai.suikei_code
                    ws_suigai[i].cell(row=j+1, column=12).value = suigai.kasen_code
                    ws_suigai[i].cell(row=j+1, column=13).value = suigai.gradient_code
                    ws_suigai[i].cell(row=j+1, column=14).value = suigai.residential_area
                    ws_suigai[i].cell(row=j+1, column=15).value = suigai.agricultural_area
                    ws_suigai[i].cell(row=j+1, column=16).value = suigai.underground_area
                    ws_suigai[i].cell(row=j+1, column=17).value = suigai.kasen_kaigan_code
                    ws_suigai[i].cell(row=j+1, column=18).value = suigai.crop_damage
                    ws_suigai[i].cell(row=j+1, column=19).value = suigai.weather_id
        
        #######################################################################
        ### DBアクセス処理(0050)
        ### EXCEL入出力処理(0050)
        ### (1)DBから建物区分等のマスタデータを取得する。
        ### (2)EXCELのVLOKUP用のシートのセルに、DBから取得した都道府県等のマスタデータを埋め込む。
        ### =VLOOKUP(B10,SUIKEI_TYPE_VLOOKUP!A:B,2,0)
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 6/12.', 'INFO')
        
        ### 1020: 市区町村VLOOKUP
        ken_list = None
        cities_list = []

        print("ippan_chosa_view19", flush=True)
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        if ken_list:
            for i, ken in enumerate(ken_list):
                cities_list.append(CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken.ken_code,]))
        
        print("ippan_chosa_view20", flush=True)
        for i, _ in enumerate(city_code_request):
            if ken_list and cities_list:
                for j, ken in enumerate(ken_list):
                    ws_city_vlook[i].cell(row=j+1, column=1).value = str(ken.ken_name) + ":" + str(ken.ken_code)
        
                for j, cities in enumerate(cities_list):
                    ws_city_vlook[i].cell(row=j+1, column=2).value = 'CITY!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(cities)

        ### 1060: 河川（河川・海岸）VLOOKUP
        suikei_list = None
        kasens_list = []
        
        print("ippan_chosa_view21", flush=True)
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                kasens_list.append(KASEN.objects.raw("""SELECT * FROM KASEN WHERE SUIKEI_CODE=%s ORDER BY CAST(KASEN_CODE AS INTEGER)""", [suikei.suikei_code,]))

        print("ippan_chosa_view22", flush=True)
        for i, _ in enumerate(city_code_request):
            if suikei_list and kasens_list:
                for j, suikei in enumerate(suikei_list):
                    ws_kasen_vlook[i].cell(row=j+1, column=1).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)

                for j, kasens in enumerate(kasens_list):
                    ws_kasen_vlook[i].cell(row=j+1, column=2).value = 'KASEN!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(kasens)

        #######################################################################
        ### EXCEL入出力処理(0060)
        ### (1)EXCELのヘッダ部のセルに、キャプションのテキストを埋め込む。
        ### (2)EXCELの一覧部のセルに、キャプションのテキストを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 7/12.', 'INFO')
        print("ippan_chosa_view19", flush=True)
        for i, _ in enumerate(city_code_request):
            for j in range(suigai_count_list[i] + 10 + 1):
                ws_ippan[i][j].cell(row=5, column=2).value = '都道府県'
                ws_ippan[i][j].cell(row=5, column=3).value = '市区町村'
                ws_ippan[i][j].cell(row=5, column=4).value = '水害発生年月日'
                ws_ippan[i][j].cell(row=5, column=5).value = '水害終了年月日'
                ws_ippan[i][j].cell(row=5, column=6).value = '水害原因'
                ws_ippan[i][j].cell(row=5, column=9).value = '水害区域番号'
                ws_ippan[i][j].cell(row=6, column=6).value = '1'
                ws_ippan[i][j].cell(row=6, column=7).value = '2'
                ws_ippan[i][j].cell(row=6, column=8).value = '3'
                ws_ippan[i][j].cell(row=9, column=2).value = '水系・沿岸名'
                ws_ippan[i][j].cell(row=9, column=3).value = '水系種別'
                ws_ippan[i][j].cell(row=9, column=4).value = '河川・海岸名'
                ws_ippan[i][j].cell(row=9, column=5).value = '河川種別'
                ws_ippan[i][j].cell(row=9, column=6).value = '地盤勾配区分※1'
                ws_ippan[i][j].cell(row=12, column=2).value = '水害区域面積（m2）'
                ws_ippan[i][j].cell(row=12, column=6).value = '工種'
                ws_ippan[i][j].cell(row=12, column=8).value = '農作物被害額（千円）'
                ws_ippan[i][j].cell(row=12, column=10).value = '異常気象コード'
                ws_ippan[i][j].cell(row=16, column=2).value = '町丁名・大字名'
                ws_ippan[i][j].cell(row=16, column=3).value = '名称'
                ws_ippan[i][j].cell(row=16, column=4).value = '地上・地下被害の区分※2'
                ws_ippan[i][j].cell(row=16, column=5).value = '浸水土砂被害の区分※3'
                ws_ippan[i][j].cell(row=16, column=6).value = '被害建物棟数'
                ws_ippan[i][j].cell(row=16, column=12).value = '被害建物の延床面積（m2）'
                ws_ippan[i][j].cell(row=16, column=13).value = '被災世帯数'
                ws_ippan[i][j].cell(row=16, column=14).value = '被災事業所数'
                ws_ippan[i][j].cell(row=16, column=15).value = '被害建物内での農業家又は事業所活動'
                ws_ippan[i][j].cell(row=16, column=25).value = '事業所の産業区分※7'
                ws_ippan[i][j].cell(row=16, column=26).value = '地下空間の利用形態※8'
                ws_ippan[i][j].cell(row=16, column=27).value = '備考'
                ws_ippan[i][j].cell(row=17, column=7).value = '床上浸水・土砂堆積・地下浸水'
                ws_ippan[i][j].cell(row=17, column=15).value = '農家・漁家戸数※5'
                ws_ippan[i][j].cell(row=17, column=20).value = '事業所従業者数※6'
                ws_ippan[i][j].cell(row=18, column=16).value = '床上浸水'
                ws_ippan[i][j].cell(row=18, column=21).value = '床上浸水'
                ws_ippan[i][j].cell(row=20, column=7).value = '1cm〜49cm'
                ws_ippan[i][j].cell(row=20, column=8).value = '50cm〜99cm'
                ws_ippan[i][j].cell(row=20, column=9).value = '1m以上'
                ws_ippan[i][j].cell(row=20, column=10).value = '半壊※4'
                ws_ippan[i][j].cell(row=20, column=11).value = '全壊・流失※4'
                ws_ippan[i][j].cell(row=20, column=16).value = '1cm〜49cm'
                ws_ippan[i][j].cell(row=20, column=17).value = '50cm〜99cm'
                ws_ippan[i][j].cell(row=20, column=18).value = '1m以上半壊'
                ws_ippan[i][j].cell(row=20, column=19).value = '全壊・流失'
                ws_ippan[i][j].cell(row=20, column=21).value = '1cm〜49cm'
                ws_ippan[i][j].cell(row=20, column=22).value = '50cm〜99cm'
                ws_ippan[i][j].cell(row=20, column=23).value = '1m以上半壊'
                ws_ippan[i][j].cell(row=20, column=24).value = '全壊・流失'
                ws_ippan[i][j].cell(row=7, column=2).value = ""
                ws_ippan[i][j].cell(row=7, column=3).value = ""
                ws_ippan[i][j].cell(row=7, column=4).value = ""
                ws_ippan[i][j].cell(row=7, column=5).value = ""
                ws_ippan[i][j].cell(row=7, column=6).value = ""
                ws_ippan[i][j].cell(row=7, column=7).value = ""
                ws_ippan[i][j].cell(row=7, column=8).value = ""
                ws_ippan[i][j].cell(row=7, column=9).value = ""
                ws_ippan[i][j].cell(row=10, column=2).value = ""
                ws_ippan[i][j].cell(row=10, column=3).value = ""
                ws_ippan[i][j].cell(row=10, column=4).value = ""
                ws_ippan[i][j].cell(row=10, column=5).value = ""
                ws_ippan[i][j].cell(row=10, column=6).value = ""
                ws_ippan[i][j].cell(row=14, column=2).value = ""
                ws_ippan[i][j].cell(row=14, column=3).value = ""
                ws_ippan[i][j].cell(row=14, column=4).value = ""
                ws_ippan[i][j].cell(row=14, column=6).value = ""
                ws_ippan[i][j].cell(row=14, column=8).value = ""
                ws_ippan[i][j].cell(row=14, column=10).value = ""
                ws_ippan[i][j].cell(row=20, column=2).value = ""
                ws_ippan[i][j].cell(row=20, column=3).value = ""
                ws_ippan[i][j].cell(row=20, column=4).value = ""
                ws_ippan[i][j].cell(row=20, column=5).value = ""
                ws_ippan[i][j].cell(row=20, column=6).value = ""
                ws_ippan[i][j].cell(row=20, column=7).value = ""
                ws_ippan[i][j].cell(row=20, column=8).value = ""
                ws_ippan[i][j].cell(row=20, column=9).value = ""
                ws_ippan[i][j].cell(row=20, column=10).value = ""
                ws_ippan[i][j].cell(row=20, column=11).value = ""
                ws_ippan[i][j].cell(row=20, column=12).value = ""
                ws_ippan[i][j].cell(row=20, column=13).value = ""
                ws_ippan[i][j].cell(row=20, column=14).value = ""
                ws_ippan[i][j].cell(row=20, column=15).value = ""
                ws_ippan[i][j].cell(row=20, column=16).value = ""
                ws_ippan[i][j].cell(row=20, column=17).value = ""
                ws_ippan[i][j].cell(row=20, column=18).value = ""
                ws_ippan[i][j].cell(row=20, column=19).value = ""
                ws_ippan[i][j].cell(row=20, column=20).value = ""
                ws_ippan[i][j].cell(row=20, column=21).value = ""
                ws_ippan[i][j].cell(row=20, column=22).value = ""
                ws_ippan[i][j].cell(row=20, column=23).value = ""
                ws_ippan[i][j].cell(row=20, column=24).value = ""
                ws_ippan[i][j].cell(row=20, column=25).value = ""
                ws_ippan[i][j].cell(row=20, column=26).value = ""
                ws_ippan[i][j].cell(row=20, column=27).value = ""

        #######################################################################
        ### EXCEL入出力処理(0070)
        ### (1)EXCELのセルに、建物区分に応じて、背景灰色、背景白色を変化させる条件付き形式を埋め込む。
        ### (2)ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 8/12.', 'INFO')
        print("ippan_chosa_view20", flush=True)
        gray_fill = PatternFill(bgColor='C0C0C0', fill_type='solid')
        white_fill = PatternFill(bgColor='FFFFFF', fill_type='solid')
        
        for i, _ in enumerate(city_code_request):
            for j in range(suigai_count_list[i] + 10):
                ### ws_ippan[i][suigai_index].conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="戸建住宅:1"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('N20:Y1000', FormulaRule(formula=['$C20="戸建住宅:1"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('N20:Y1000', FormulaRule(formula=['$C20="共同住宅:2"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('N20:Y1000', FormulaRule(formula=['$C20="事業所併用住宅:3"'], fill=white_fill))
                ws_ippan[i][j].conditional_formatting.add('M20:M1000', FormulaRule(formula=['$C20="事業所:4"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('M20:N1000', FormulaRule(formula=['$C20="その他建物:5"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('T20:Y1000', FormulaRule(formula=['$C20="その他建物:5"'], fill=gray_fill))
                ws_ippan[i][j].conditional_formatting.add('F20:Z1000', FormulaRule(formula=['$C20="建物以外:6"'], fill=gray_fill))

        #######################################################################
        ### EXCEL入出力処理(0080)
        ### (1)EXCELのヘッダ部のセルに、単純プルダウン、連動プルダウンの設定を埋め込む。
        ### (2)EXCELの一覧部のセルに、単純プルダウンの設定を埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 9/12.', 'INFO')
        ### ループの回数＝EXCELファイルの数
        ### ※ _ は city_code がセットされているが、使わないため _ としている。
        for i, _ in enumerate(city_code_request):
            ### ループの回数＝EXCELシートの数
            ### ※新規追加用に10シート分余分に生成する。
            for j in range(suigai_count_list[i] + 10):
                
                ### 1000: 建物区分
                dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$%d" % len(building_list))
                dv_building.ranges = 'C20:C1000'
                ws_ippan[i][j].add_data_validation(dv_building)
        
                ### 1010: 都道府県
                dv_ken = DataValidation(type="list", formula1="KEN!$B$1:$B$%d" % len(ken_list))
                dv_ken.ranges = 'B7:B7'
                ws_ippan[i][j].add_data_validation(dv_ken)
                
                ### 1020: 市区町村
                dv_city = DataValidation(type="list", formula1="=INDIRECT(AD3)")
                dv_city.ranges = 'C7:C7'
                ws_ippan[i][j].add_data_validation(dv_city)
                ### ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK.A:B,2,0)" ### FOR LINUX?
                ws_ippan[i][j].cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK!A:B,2,0)" ### FOR WINDOWS
                
                ### 1030: 水害発生地点工種（河川海岸区分）
                dv_kasen_kaigan = DataValidation(type="list", formula1="KASEN_KAIGAN!$B$1:$B$%d" % len(kasen_kaigan_list))
                dv_kasen_kaigan.ranges = 'F14:F14'
                ws_ippan[i][j].add_data_validation(dv_kasen_kaigan)
                
                ### 1040: 水系（水系・沿岸）
                dv_suikei = DataValidation(type="list", formula1="SUIKEI!$B$1:$B$%d" % len(suikei_list))
                dv_suikei.ranges = 'B10:B10'
                ws_ippan[i][j].add_data_validation(dv_suikei)
                
                ### 1050: 水系種別（水系・沿岸種別）
                dv_suikei_type = DataValidation(type="list", formula1="SUIKEI_TYPE!$B$1:$B$%d" % len(suikei_type_list))
                dv_suikei_type.ranges = 'C10:C10'
                ws_ippan[i][j].add_data_validation(dv_suikei_type)
                
                ### 1060: 河川（河川・海岸）
                dv_kasen = DataValidation(type="list", formula1="=INDIRECT(AD4)")
                dv_kasen.ranges = 'D10:D10'
                ws_ippan[i][j].add_data_validation(dv_kasen)
                ### ws_ippan.cell(row=4, column=30).value = "=VLOOKUP(B10,KASEN_VLOOK.A:B,2,0)" ### FOR LINUX?
                ws_ippan[i][j].cell(row=4, column=30).value = "=VLOOKUP(B10,KASEN_VLOOK!A:B,2,0)" ### FOR WINDOWS
                
                ### 1070: 河川種別（河川・海岸種別）
                dv_kasen_type = DataValidation(type="list", formula1="KASEN_TYPE!$B$1:$B$%d" % len(kasen_type_list))
                dv_kasen_type.ranges = 'E10:E10'
                ws_ippan[i][j].add_data_validation(dv_kasen_type)
                
                ### 1080: 水害原因
                dv_cause = DataValidation(type="list", formula1="CAUSE!$B$1:$B$%d" % len(cause_list))
                dv_cause.ranges = 'F7:H7'
                ws_ippan[i][j].add_data_validation(dv_cause)
                
                ### 1090: 地上地下区分
                dv_underground = DataValidation(type="list", formula1="UNDERGROUND!$B$1:$B$%d" % len(underground_list))
                dv_underground.ranges = 'D20:D1000'
                ws_ippan[i][j].add_data_validation(dv_underground)
                
                ### 1100: 地下空間の利用形態
                dv_usage = DataValidation(type="list", formula1="USAGE!$B$1:$B$%d" % len(usage_list))
                dv_usage.ranges = 'Z20:Z1000'
                ws_ippan[i][j].add_data_validation(dv_usage)
                
                ### 1110: 浸水土砂区分
                dv_flood_sediment = DataValidation(type="list", formula1="FLOOD_SEDIMENT!$B$1:$B$%d" % len(flood_sediment_list))
                dv_flood_sediment.ranges = 'E20:E1000'
                ws_ippan[i][j].add_data_validation(dv_flood_sediment)
                
                ### 1120: 地盤勾配区分
                dv_gradient = DataValidation(type="list", formula1="GRADIENT!$B$1:$B$%d" % len(gradient_list))
                dv_gradient.ranges = 'F10:F10'
                ws_ippan[i][j].add_data_validation(dv_gradient)
                
                ### 1130: 産業分類
                dv_industry = DataValidation(type="list", formula1="INDUSTRY!$B$1:$B$%d" % len(industry_list))
                dv_industry.ranges = 'Y20:Y1000'
                ws_ippan[i][j].add_data_validation(dv_industry)

                ### 7000: 入力データ_水害区域
                dv_area = DataValidation(type="list", formula1="AREA!$B$1:$B$%d" % len(area_list))
                dv_area.ranges = 'I7:I7'
                ws_ippan[i][j].add_data_validation(dv_area)
                
                ### 7010: 入力データ_異常気象
                dv_weather = DataValidation(type="list", formula1="WEATHER!$B$1:$B$%d" % len(weather_list))
                dv_weather.ranges = 'J14:J14'
                ws_ippan[i][j].add_data_validation(dv_weather)
        
        #######################################################################
        ### DBアクセス処理(0090)
        ### (1)DBから水害のデータを取得する。
        ### (2)DBから一般資産調査票（調査員）のデータを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 10/12.', 'INFO')

        ### 7020: 入力データ_ヘッダ部分、水害
        print("ippan_chosa_view38_1", flush=True)
        for i, _ in enumerate(city_code_request):
            for j in range(suigai_count_list[i]):
        
                ###############################################################
                ### DBアクセス処理(0100)
                ### DBから入力データ_ヘッダ部分のデータを取得する。
                ###############################################################
                suigai_list = None
                suigai_list = SUIGAI.objects.raw("""
                    SELECT 
                        SG1.suigai_id AS suigai_id,
                        SG1.suigai_name AS suigai_name,
                        SG1.ken_code AS ken_code, 
                        KE1.ken_name AS ken_name,
                        SG1.city_code AS city_code,
                        CI1.city_name AS city_name,
                        SG1.begin_date AS begin_date,
                        SG1.end_date AS end_date,
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
                        ST1.suikei_type_code AS suikei_type_code,
                        ST1.suikei_type_name AS suikei_type_name,
                        SG1.kasen_code AS kasen_code,
                        KA1.kasen_name AS kasen_name,
                        KT1.kasen_type_code AS kasen_type_code,
                        KT1.kasen_type_name AS kasen_type_name,
                        SG1.gradient_code AS gradient_code,
                        GR1.gradient_name AS gradient_name,
                        SG1.residential_area AS residential_area,
                        SG1.agricultural_area AS agricultural_area,
                        SG1.underground_area AS underground_area,
                        SG1.kasen_kaigan_code AS kasen_kaigan_code,
                        KK1.kasen_kaigan_name AS kasen_kaigan_name,
                        SG1.crop_damage AS crop_damage,
                        SG1.weather_id AS weather_id,
                        WE1.weather_name as weather_name
                    FROM SUIGAI SG1 
                    LEFT JOIN KEN KE1 ON SG1.ken_code = KE1.ken_code 
                    LEFT JOIN CITY CI1 ON SG1.city_code = CI1.city_code 
                    LEFT JOIN CAUSE CA1 ON SG1.cause_1_code = CA1.cause_code 
                    LEFT JOIN CAUSE CA2 ON SG1.cause_2_code = CA2.cause_code 
                    LEFT JOIN CAUSE CA3 ON SG1.cause_3_code = CA3.cause_code 
                    LEFT JOIN AREA AR1 ON SG1.area_id = AR1.area_id 
                    LEFT JOIN SUIKEI SK1 ON SG1.suikei_code = SK1.suikei_code 
                    LEFT JOIN SUIKEI_TYPE ST1 ON SK1.suikei_type_code = ST1.suikei_type_code 
                    LEFT JOIN KASEN KA1 ON SG1.kasen_code = KA1.kasen_code 
                    LEFT JOIN KASEN_TYPE KT1 ON KA1.kasen_type_code = KT1.kasen_type_code 
                    LEFT JOIN GRADIENT GR1 ON SG1.gradient_code = GR1.gradient_code 
                    LEFT JOIN KASEN_KAIGAN KK1 ON SG1.kasen_kaigan_code = KK1.kasen_kaigan_code 
                    LEFT JOIN WEATHER WE1 ON SG1.weather_id = WE1.weather_id 
                    WHERE SG1.suigai_id = %s 
                    """, [suigai_id_list[i][j]])
        
                ###############################################################
                ### DBアクセス処理(0110)
                ### DBから入力データ_一覧表部分のデータを取得する。
                ###############################################################
                ippan_list = None
                ippan_list = IPPAN.objects.raw("""
                    SELECT 
                        IV1.ippan_id AS ippan_id,
                        IV1.ippan_name AS ippan_name,
                        IV1.building_code AS building_code,
                        IV1.building_name AS building_Name,
                        IV1.underground_code AS underground_code,
                        IV1.underground_name AS underground_name,
                        IV1.flood_sediment_code AS flood_sediment_code,
                        IV1.flood_sediment_name AS flood_sediment_name,
                        IV1.building_lv00 AS building_lv00,
                        IV1.building_lv01_49 AS building_lv01_49,
                        IV1.building_lv50_99 AS building_lv50_99,
                        IV1.building_lv100 AS building_lv100,
                        IV1.building_half AS building_half,
                        IV1.building_full AS building_full,
                        IV1.floor_area AS floor_area,
                        IV1.family AS family,
                        IV1.office AS office,
                        IV1.floor_area_lv00 AS floor_area_lv00,
                        IV1.floor_area_lv01_49 AS floor_area_lv01_49,
                        IV1.floor_area_lv50_99 AS floor_area_lv50_99,
                        IV1.floor_area_lv100 AS floor_area_lv100,
                        IV1.floor_area_half AS floor_area_half,
                        IV1.floor_area_full AS floor_area_full,
                        IV1.family_lv00 AS family_lv00,
                        IV1.family_lv01_49 AS family_lv01_49,
                        IV1.family_lv50_99 AS family_lv50_99,
                        IV1.family_lv100 AS family_lv100,
                        IV1.family_half AS family_half,
                        IV1.family_full AS family_full,
                        IV1.office_lv00 AS office_lv00,
                        IV1.office_lv01_49 AS office_lv01_49,
                        IV1.office_lv50_99 AS office_lv50_99,
                        IV1.office_lv100 AS office_lv100,
                        IV1.office_half AS office_half,
                        IV1.office_full AS office_full,
                        IV1.farmer_fisher_lv00 AS farmer_fisher_lv00,
                        IV1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49,
                        IV1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99,
                        IV1.farmer_fisher_lv100 AS farmer_fisher_lv100,
                        IV1.farmer_fisher_full AS farmer_fisher_full,
                        IV1.employee_lv00 AS employee_lv00,
                        IV1.employee_lv01_49 AS employee_lv01_49,
                        IV1.employee_lv50_99 AS employee_lv50_99,
                        IV1.employee_lv100 AS employee_lv100,
                        IV1.employee_full AS employee_full,
                        IV1.industry_code AS industry_code,
                        IV1.industry_name AS industry_name,
                        IV1.usage_code as usage_code,
                        IV1.usage_name as usage_name,
                        IV1.comment as comment 
                    FROM IPPAN_VIEW IV1 
                    WHERE IV1.suigai_id = %s
                    ORDER BY CAST (IV1.IPPAN_ID AS INTEGER)            
                    """, [suigai_id_list[i][j]])
        
                ###############################################################
                ### EXCEL入出力処理(0120)
                ### EXCELのヘッダ部のセルに、DBから取得した入力データ_ヘッダ部分の値を埋め込む。
                ###############################################################
                if suigai_list:
                    for k, suigai in enumerate(suigai_list):
                        ws_ippan[i][j].cell(row=7, column=2).value = str(suigai.ken_name) + ":" + str(suigai.ken_code)
                        ws_ippan[i][j].cell(row=7, column=3).value = str(suigai.city_name) + ":" + str(suigai.city_code)
                        ws_ippan[i][j].cell(row=7, column=4).value = str(suigai.begin_date)
                        ws_ippan[i][j].cell(row=7, column=5).value = str(suigai.end_date)
                        ws_ippan[i][j].cell(row=7, column=6).value = str(suigai.cause_1_name) + ":" + str(suigai.cause_1_code)
                        ws_ippan[i][j].cell(row=7, column=7).value = str(suigai.cause_2_name) + ":" + str(suigai.cause_2_code)
                        ws_ippan[i][j].cell(row=7, column=8).value = str(suigai.cause_3_name) + ":" + str(suigai.cause_3_code)
                        ws_ippan[i][j].cell(row=7, column=9).value = str(suigai.area_name) + ":" + str(suigai.area_id)
                        ws_ippan[i][j].cell(row=10, column=2).value = str(suigai.suikei_name) + ":" + str(suigai.suikei_code)
                        ws_ippan[i][j].cell(row=10, column=3).value = str(suigai.suikei_type_name) + ":" + str(suigai.suikei_type_code)
                        ws_ippan[i][j].cell(row=10, column=4).value = str(suigai.kasen_name) + ":" + str(suigai.kasen_code)
                        ws_ippan[i][j].cell(row=10, column=5).value = str(suigai.kasen_type_name) + ":" + str(suigai.kasen_type_code)
                        ws_ippan[i][j].cell(row=10, column=6).value = str(suigai.gradient_name) + ":" + str(suigai.gradient_code)
                        ws_ippan[i][j].cell(row=14, column=2).value = str(suigai.residential_area)
                        ws_ippan[i][j].cell(row=14, column=3).value = str(suigai.agricultural_area)
                        ws_ippan[i][j].cell(row=14, column=4).value = str(suigai.underground_area)
                        ws_ippan[i][j].cell(row=14, column=6).value = str(suigai.kasen_kaigan_name) + ":" + str(suigai.kasen_kaigan_code)
                        ws_ippan[i][j].cell(row=14, column=8).value = str(suigai.crop_damage)
                        ws_ippan[i][j].cell(row=14, column=10).value = str(suigai.weather_name) + ":" + str(suigai.weather_id)

                        ws_ippan[i][j].cell(row=3, column=28).value = suigai.suigai_id
                        
                ###############################################################
                ### EXCEL入出力処理(0130)
                ### EXCELの一覧部のセルに、DBから取得した一般資産調査票（調査員）の値を埋め込む。
                ###############################################################
                if ippan_list:
                    for k, ippan in enumerate(ippan_list):
                        ws_ippan[i][j].cell(row=k+20, column=2).value = str(ippan.ippan_name) + ":" + str(ippan.ippan_id)
                        ws_ippan[i][j].cell(row=k+20, column=3).value = str(ippan.building_name) + ":" + str(ippan.building_code)
                        ws_ippan[i][j].cell(row=k+20, column=4).value = str(ippan.underground_name) + ":" + str(ippan.underground_code)
                        ws_ippan[i][j].cell(row=k+20, column=5).value = str(ippan.flood_sediment_name) + ":" + str(ippan.flood_sediment_code)
                        ws_ippan[i][j].cell(row=k+20, column=6).value = ippan.building_lv00
                        ws_ippan[i][j].cell(row=k+20, column=7).value = ippan.building_lv01_49
                        ws_ippan[i][j].cell(row=k+20, column=8).value = ippan.building_lv50_99
                        ws_ippan[i][j].cell(row=k+20, column=9).value = ippan.building_lv100
                        ws_ippan[i][j].cell(row=k+20, column=10).value = ippan.building_half
                        ws_ippan[i][j].cell(row=k+20, column=11).value = ippan.building_full
                        ws_ippan[i][j].cell(row=k+20, column=12).value = ippan.floor_area
                        ws_ippan[i][j].cell(row=k+20, column=13).value = ippan.family
                        ws_ippan[i][j].cell(row=k+20, column=14).value = ippan.office
                        ws_ippan[i][j].cell(row=k+20, column=15).value = ippan.farmer_fisher_lv00
                        ws_ippan[i][j].cell(row=k+20, column=16).value = ippan.farmer_fisher_lv01_49
                        ws_ippan[i][j].cell(row=k+20, column=17).value = ippan.farmer_fisher_lv50_99
                        ws_ippan[i][j].cell(row=k+20, column=18).value = ippan.farmer_fisher_lv100
                        ws_ippan[i][j].cell(row=k+20, column=19).value = ippan.farmer_fisher_full
                        ws_ippan[i][j].cell(row=k+20, column=20).value = ippan.employee_lv00
                        ws_ippan[i][j].cell(row=k+20, column=21).value = ippan.employee_lv01_49
                        ws_ippan[i][j].cell(row=k+20, column=22).value = ippan.employee_lv50_99
                        ws_ippan[i][j].cell(row=k+20, column=23).value = ippan.employee_lv100
                        ws_ippan[i][j].cell(row=k+20, column=24).value = ippan.employee_full
                        ws_ippan[i][j].cell(row=k+20, column=25).value = str(ippan.industry_name) + ":" + str(ippan.industry_code)
                        ws_ippan[i][j].cell(row=k+20, column=26).value = str(ippan.usage_name) + ":" + str(ippan.usage_code)
                        ws_ippan[i][j].cell(row=k+20, column=27).value = ippan.comment

                        ws_ippan[i][j].cell(row=k+20, column=28).value = ippan.ippan_id
                        
        #######################################################################
        ### EXCEL入出力処理(0140)
        ### ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 11/13.', 'INFO')
        print("ippan_chosa_view38_2", flush=True)
        for i, _ in enumerate(city_code_request):
            wb[i].save(download_file_path[i])

        #######################################################################
        ### EXCEL入出力処理(0150)
        ### 複数のEXCELファイルを1つに固めて保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 12/13.', 'INFO')
        
        #######################################################################
        ### レスポンスセット処理(0160)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 13/13.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb[0]), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_city_view(request, lock)
### 一般資産調査票（市区町村担当者用）
### urlpattern：path('ippan_city/', views.ippan_city_view, name='ippan_city_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_city_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        ### (2)GETメソッドの場合、関数を抜ける。
        ### (3)POSTリクエストの市区町村数が0件の場合、関数を抜ける。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 ken_code_hidden= {}'.format(request.POST.get('ken_code_hidden')), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 1/12.', 'INFO')

        if request.method == 'GET':
            print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        if request.POST.get('ken_code_hidden') is None:
            print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        ken_code_request = [x.strip() for x in request.POST.get('ken_code_hidden').split(',')][:-1]

        if ken_code_request:
            if len(ken_code_request) == 0:
                print_log('[WARN] P0200ExcelDownload.ippan_city_view()関数で警告が発生しました。', 'WARN')
                return render(request, 'warning.html')

        #######################################################################
        ### 局所定数セット処理(0010)
        ### VLOOKUP用の局所定数をセットする。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 2/12.', 'INFO')
        VLOOK_VALUE = [
            'B', 'G', 'L', 'Q', 'V', 'AA', 'AF', 'AK', 'AP', 'AU', 
            'AZ', 'BE', 'BJ', 'BO', 'BT', 'BY', 'CD', 'CI', 'CN', 'CS', 
            'CX', 'DC', 'DH', 'DM', 'DR', 'DW', 'EB', 'EG', 'EL', 'EQ', 
            'EV', 'FA', 'FF', 'FK', 'FP', 'FU', 'FZ', 'GE', 'GJ', 'GO', 
            'GT', 'GY', 'HD', 'HI', 'HN', 'HS', 'HX', 'IC', 'IH', 'IM', 
            'IR', 'IW', 'JB', 'JG', 'JL', 'JQ', 'JV', 'KA', 'KF', 'KK', 
            'KP', 'KU', 'KZ', 'LE', 'LJ', 'LO', 'LT', 'LY', 'MD', 'MI', 
            'MN', 'MS', 'MX', 'NC', 'NH', 'NM', 'NR', 'NW', 'OB', 'OG', 
            'OL', 'OQ', 'OV', 'PA', 'PF', 'PK', 'PP', 'PU', 'PZ', 'QE', 
            'QJ', 'QO', 'QT', 'QY', 'RD', 'RI', 'RN', 'RS', 'RX', 'SC', 
            'SH', 'SM', 'SR', 'SW', 'TB', 'TG', 'TL', 'TQ', 'TV', 'UA', 
            'UF', 'UK', 'UP', 'UU', 'UZ', 'VE', 'VJ', 'VO', 'VT', 'VY', 
            'WD', 'WI', 'WN', 'WS', 'WX', 'XC', 'XH', 'XM', 'XR', 'XW', 
            'YB', 'YG', 'YL', 'YQ', 'YV', 'ZA', 'ZF', 'ZK', 'ZP', 'ZU', 
            'ZZ', 'AAE', 'AAJ', 'AAO', 'AAT', 'AAY', 'ABD', 'ABI', 'ABN', 'ABS', 
            'ABX', 'ACC', 'ACH', 'ACM', 'ACR', 'ACW', 'ADB', 'ADG', 'ADL', 'ADQ', 
            'ADV', 'AEA', 'AEF', 'AEK', 'AEP', 'AEU', 'AEZ', 'AFE', 'AFJ', 'AFO', 
            'AFT', 'AFY', 'AGD', 'AGI', 'AGN', 'AGS', 'AGX', 'AHC', 'AHH', 'AHM', 
            'AHR', 'AHW', 'AIB', 'AIG', 'AIL', 'AIQ', 'AIV', 'AJA', 'AJF', 'AJK', 
            'AJP', 'AJU', 'AJZ', 'AKE', 'AKJ', 'AKO', 'AKT', 'AKY', 'ALD', 'ALI', 
            'ALN', 'ALS', 'ALX', 'AMC', 'AMH', 'AMM', 'AMR', 'AMW', 'ANB', 'ANG', 
            'ANL', 'ANQ', 'ANV', 'AOA', 'AOF', 'AOK', 'AOP', 'AOU', 'AOZ', 'APE', 
            'APJ', 'APO', 'APT', 'APY', 'AQD', 'AQI', 'AQN', 'AQS', 'AQX', 'ARC', 
            'ARH', 'ARM', 'ARR', 'ARW', 'ASB', 'ASG', 'ASL', 'ASQ', 'ASV', 'ATA', 
            'ATF', 'ATK', 'ATP', 'ATU', 'ATZ', 'AUE', 'AUJ', 'AUO', 'AUT', 'AUY', 
            'AVD', 'AVI', 'AVN', 'AVS', 'AVX', 'AWC', 'AWH', 'AWM', 'AWR', 'AWW', 
            'AXB', 'AXG', 'AXL', 'AXQ', 'AXV', 'AYA', 'AYF', 'AYK', 'AYP', 'AYU', 
            'AYZ', 'AZE', 'AZJ', 'AZO', 'AZT', 'AZY'
            ]

        #######################################################################
        ### DBアクセス処理(0020)
        ### DBから都道府県コード毎の水害データの件数を取得する。
        ### ※関数のメインの処理の前に、EXCELのファイル数、シート数を確定するため。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 3/12.', 'INFO')
        
        #######################################################################
        ### EXCEL入出力処理(0030)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        ### ※都道府県毎にEXCELファイルを作成する。
        ### ※水害毎にEXCELシートを作成する。
        ### ※0件の場合、入力用にIPPANシートを10枚作成する。
        ### ※5件の場合、既存データ用にIPPANシートを5枚作成する。
        ### ※5件の場合、入力用にIPPANシートを10枚作成する。（合計15枚作成する。）
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 4/12.', 'INFO')
        download_file_path = []
        wb = []
        ws_ippan = []
        ws_building = []
        ws_ken = []
        ws_city = []
        ws_kasen_kaigan = []
        ws_suikei = []
        ws_suikei_type = []
        ws_kasen = []
        ws_kasen_type = []
        ws_cause = []
        ws_underground = []
        ws_usage = []
        ws_flood_sediment = []
        ws_gradient = []
        ws_industry = []
        ws_suigai = []
        ws_weather = []
        ws_area = []
        ws_city_vlook = []
        ws_kasen_vlook = []
        
        ### len(ken_code_request)=ワークブックの数=EXCELファイルの数
        ### EXCELファイル毎に、テーブル毎に１シートとする。
        for i, ken_code in enumerate(ken_code_request):
            template_file_path = 'static/template_ippan_city.xlsx'
            download_file_path.append('static/download_ippan_city_' + ken_code + '.xlsx')
            
            wb.append(openpyxl.load_workbook(template_file_path, keep_vba=False))
            
            ws_ippan.append(wb[i]["IPPAN"])
            ws_building.append(wb[i]["BUILDING"])
            ws_ken.append(wb[i]["KEN"])
            ws_city.append(wb[i]["CITY"])
            ws_kasen_kaigan.append(wb[i]["KASEN_KAIGAN"])
            ws_suikei.append(wb[i]["SUIKEI"])
            ws_suikei_type.append(wb[i]["SUIKEI_TYPE"])
            ws_kasen.append(wb[i]["KASEN"])
            ws_kasen_type.append(wb[i]["KASEN_TYPE"])
            ws_cause.append(wb[i]["CAUSE"])
            ws_underground.append(wb[i]["UNDERGROUND"])
            ws_usage.append(wb[i]["USAGE"])
            ws_flood_sediment.append(wb[i]["FLOOD_SEDIMENT"])
            ws_gradient.append(wb[i]["GRADIENT"])
            ws_industry.append(wb[i]["INDUSTRY"])
            ws_suigai.append(wb[i]["SUIGAI"])
            ws_weather.append(wb[i]["WEATHER"])
            ws_area.append(wb[i]["AREA"])
            ws_city_vlook.append(wb[i]["CITY_VLOOK"])
            ws_kasen_vlook.append(wb[i]["KASEN_VLOOK"])

        #######################################################################
        ### DBアクセス処理(0040)
        ### EXCEL入出力処理(0040)
        ### (1)DBから建物区分等のマスタデータを取得する。
        ### (2)EXCELのマスタ用のシートのセルに、DBから取得した建物区分等のマスタデータを埋め込む。
        ### (3)EXCELのVLOKUP用のシートのセルに、DBから取得した都道府県等のマスタデータを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 5/12.', 'INFO')

        ### 1000: 建物区分
        print("ippan_ken_view2", flush=True)
        building_list = None
        building_list = BUILDING.objects.raw("""SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if building_list:
                for j, building in enumerate(building_list):
                    ws_building[i].cell(row=j+1, column=1).value = building.building_code
                    ws_building[i].cell(row=j+1, column=2).value = str(building.building_name) + ":" + str(building.building_code)

        ### 1010: 都道府県
        print("ippan_ken_view3", flush=True)
        ken_list = None
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if ken_list:
                for j, ken in enumerate(ken_list):
                    ws_ken[i].cell(row=j+1, column=1).value = ken.ken_code
                    ws_ken[i].cell(row=j+1, column=2).value = str(ken.ken_name) + ":" + str(ken.ken_code)
                    ws_city_vlook[i].cell(row=j+1, column=1).value = str(ken.ken_name) + ":" + str(ken.ken_code)

        ### 1020: 市区町村
        print("ippan_ken_view4", flush=True)
        city_list = []
        if ken_list:
            for i, ken in enumerate(ken_list):
                city_list.append(CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken.ken_code, ]))

        for i, _ in enumerate(ken_code_request):
            if city_list:
                for j, city in enumerate(city_list):
                    ws_city_vlook[i].cell(row=j+1, column=2).value = 'CITY!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(city)

        for i, _ in enumerate(ken_code_request):
            if city_list:
                for j, city in enumerate(city_list):
                    if city:
                        for k, c in enumerate(city):
                            ws_city[i].cell(row=k+1, column=j*5+1).value = c.city_code
                            ws_city[i].cell(row=k+1, column=j*5+2).value = str(c.city_name) + ":" + str(c.city_code)
                            ws_city[i].cell(row=k+1, column=j*5+3).value = c.ken_code
                            ws_city[i].cell(row=k+1, column=j*5+4).value = c.city_population
                            ws_city[i].cell(row=k+1, column=j*5+5).value = c.city_area

        ### 1030: 水害発生地点工種（河川海岸区分）
        print("ippan_ken_view5", flush=True)
        kasen_kaigan_list = None
        kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_kaigan_list:
                for j, kasen_kaigan in enumerate(kasen_kaigan_list):
                    ws_kasen_kaigan[i].cell(row=j+1, column=1).value = kasen_kaigan.kasen_kaigan_code
                    ws_kasen_kaigan[i].cell(row=j+1, column=2).value = kasen_kaigan.kasen_kaigan_name + ":" + kasen_kaigan.kasen_kaigan_code

        ### 1040: 水系（水系・沿岸）
        print("ippan_ken_view6", flush=True)
        suikei_list = None
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suikei_list:
                for j, suikei in enumerate(suikei_list):
                    ws_suikei[i].cell(row=j+1, column=1).value = suikei.suikei_code
                    ws_suikei[i].cell(row=j+1, column=2).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)
                    ws_suikei[i].cell(row=j+1, column=3).value = suikei.suikei_type_code
                    ws_kasen_vlook[i].cell(row=j+1, column=1).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)

        ### 1050: 水系種別（水系・沿岸種別）
        print("ippan_ken_view7", flush=True)
        suikei_type_list = None
        suikei_type_list = SUIKEI_TYPE.objects.raw("""SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suikei_type_list:
                for j, suikei_type in enumerate(suikei_type_list):
                    ws_suikei_type[i].cell(row=j+1, column=1).value = suikei_type.suikei_type_code
                    ws_suikei_type[i].cell(row=j+1, column=2).value = str(suikei_type.suikei_type_name) + ":" + str(suikei_type.suikei_type_code)

        ### 1060: 河川（河川・海岸）
        print("ippan_ken_view8", flush=True)
        kasen_list = []
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                kasen_list.append(KASEN.objects.raw("""SELECT * FROM KASEN WHERE SUIKEI_CODE=%s ORDER BY CAST(KASEN_CODE AS INTEGER)""", [suikei.suikei_code, ]))

        for i, _ in enumerate(ken_code_request):
            if kasen_list:
                for j, kasen in enumerate(kasen_list):
                    ws_kasen_vlook[i].cell(row=j+1, column=2).value = 'KASEN!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(kasen)
                
        ### kasen_list = KASEN.objects.raw("""SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_list:
                for j, kasen in enumerate(kasen_list):
                    if kasen:
                        for k, ka_ in enumerate(kasen):
                            ws_kasen[i].cell(row=k+1, column=j*5+1).value = ka_.kasen_code
                            ws_kasen[i].cell(row=k+1, column=j*5+2).value = str(ka_.kasen_name) + ":" + str(ka_.kasen_code)
                            ws_kasen[i].cell(row=k+1, column=j*5+3).value = ka_.kasen_type_code
                            ws_kasen[i].cell(row=k+1, column=j*5+4).value = ka_.suikei_code
                
        ### 1070: 河川種別（河川・海岸種別）
        print("ippan_ken_view9", flush=True)
        kasen_type_list = None
        kasen_type_list = KASEN_TYPE.objects.raw("""SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_type_list:
                for j, kasen_type in enumerate(kasen_type_list):
                    ws_kasen_type[i].cell(row=j+1, column=1).value = kasen_type.kasen_type_code
                    ws_kasen_type[i].cell(row=j+1, column=2).value = str(kasen_type.kasen_type_name) + ":" + str(kasen_type.kasen_type_code)
        
        ### 1080: 水害原因
        print("ippan_ken_view10", flush=True)
        cause_list = None
        cause_list = CAUSE.objects.raw("""SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if cause_list:
                for j, cause in enumerate(cause_list):
                    ws_cause[i].cell(row=j+1, column=1).value = cause.cause_code
                    ws_cause[i].cell(row=j+1, column=2).value = str(cause.cause_name) + ":" + str(cause.cause_code)
                
        ### 1090: 地上地下区分
        print("ippan_ken_view11", flush=True)
        underground_list = None
        underground_list = UNDERGROUND.objects.raw("""SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if underground_list:
                for j, underground in enumerate(underground_list):
                    ws_underground[i].cell(row=j+1, column=1).value = underground.underground_code
                    ws_underground[i].cell(row=j+1, column=2).value = str(underground.underground_name) + ":" + str(underground.underground_code)
        
        ### 1100: 地下空間の利用形態
        print("ippan_ken_view12", flush=True)
        usage_list = None
        usage_list = USAGE.objects.raw("""SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if usage_list:
                for j, usage in enumerate(usage_list):
                    ws_usage[i].cell(row=j+1, column=1).value = usage.usage_code
                    ws_usage[i].cell(row=j+1, column=2).value = str(usage.usage_name) + ":" + str(usage.usage_code)
        
        ### 1110: 浸水土砂区分
        print("ippan_ken_view13", flush=True)
        flood_sediment_list = None
        flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if flood_sediment_list:
                for j, flood_sediment in enumerate(flood_sediment_list):
                    ws_flood_sediment[i].cell(row=j+1, column=1).value = flood_sediment.flood_sediment_code
                    ws_flood_sediment[i].cell(row=j+1, column=2).value = str(flood_sediment.flood_sediment_name) + ":" + str(flood_sediment.flood_sediment_code)
        
        ### 1120: 地盤勾配区分
        print("ippan_ken_view14", flush=True)
        gradient_list = None
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if gradient_list:
                for j, gradient in enumerate(gradient_list):
                    ws_gradient[i].cell(row=j+1, column=1).value = gradient.gradient_code
                    ws_gradient[i].cell(row=j+1, column=2).value = str(gradient.gradient_name) + ":" + str(gradient.gradient_code)
        
        ### 1130: 産業分類
        print("ippan_ken_view15", flush=True)
        industry_list = None
        industry_list = INDUSTRY.objects.raw("""SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if industry_list:
                for j, industry in enumerate(industry_list):
                    ws_industry[i].cell(row=j+1, column=1).value = industry.industry_code
                    ws_industry[i].cell(row=j+1, column=2).value = str(industry.industry_name) + ":" + str(industry.industry_code)

        ### 7000: 入力データ_水害区域
        print("ippan_ken_view16", flush=True)
        area_list = None
        area_list = AREA.objects.raw("""SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if area_list:
                for j, area in enumerate(area_list):
                    ws_area[i].cell(row=j+1, column=1).value = area.area_id
                    ws_area[i].cell(row=j+1, column=2).value = str(area.area_name) + ":" + str(area.area_id)

        ### 7010: 入力データ_異常気象
        print("ippan_ken_view17", flush=True)
        weather_list = None
        weather_list = WEATHER.objects.raw("""SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if weather_list:
                for j, weather in enumerate(weather_list):
                    ws_weather[i].cell(row=j+1, column=1).value = weather.weather_id
                    ws_weather[i].cell(row=j+1, column=2).value = str(weather.weather_name) + ":" + str(weather.weather_id)
        
        ### 7020: 入力データ_ヘッダ部分、水害
        print("ippan_ken_view18", flush=True)
        suigai_list = None
        suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suigai_list:
                for j, suigai in enumerate(suigai_list):
                    ws_suigai[i].cell(row=j+1, column=1).value = suigai.suigai_id
                    ws_suigai[i].cell(row=j+1, column=2).value = str(suigai.suigai_name) + ":" + str(suigai.suigai_id)
                    ws_suigai[i].cell(row=j+1, column=3).value = suigai.ken_code
                    ws_suigai[i].cell(row=j+1, column=4).value = suigai.city_code
                    ws_suigai[i].cell(row=j+1, column=5).value = suigai.begin_date
                    ws_suigai[i].cell(row=j+1, column=6).value = suigai.end_date
                    ws_suigai[i].cell(row=j+1, column=7).value = suigai.cause_1_code
                    ws_suigai[i].cell(row=j+1, column=8).value = suigai.cause_2_code
                    ws_suigai[i].cell(row=j+1, column=9).value = suigai.cause_3_code
                    ws_suigai[i].cell(row=j+1, column=10).value = suigai.area_id
                    ws_suigai[i].cell(row=j+1, column=11).value = suigai.suikei_code
                    ws_suigai[i].cell(row=j+1, column=12).value = suigai.kasen_code
                    ws_suigai[i].cell(row=j+1, column=13).value = suigai.gradient_code
                    ws_suigai[i].cell(row=j+1, column=14).value = suigai.residential_area
                    ws_suigai[i].cell(row=j+1, column=15).value = suigai.agricultural_area
                    ws_suigai[i].cell(row=j+1, column=16).value = suigai.underground_area
                    ws_suigai[i].cell(row=j+1, column=17).value = suigai.kasen_kaigan_code
                    ws_suigai[i].cell(row=j+1, column=18).value = suigai.crop_damage
                    ws_suigai[i].cell(row=j+1, column=19).value = suigai.weather_id

        #######################################################################
        ### EXCEL入出力処理(0050)
        ### (1)EXCELのヘッダ部のセルに、キャプションのテキストを埋め込む。
        ### (2)EXCELの一覧部のセルに、キャプションのテキストを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 6/12.', 'INFO')
        ### len(ken_code_request)=ワークブックの数=EXCELファイルの数
        ### for i, _ in enumerate(ken_code_request):
        ###     ws_ippan[i].cell(row=6, column=1).value = 'NO.'
        ###     ws_ippan[i].cell(row=6, column=2).value = 'ファイル名'
        ###     ws_ippan[i].cell(row=6, column=3).value = ''
        ###     ws_ippan[i].cell(row=6, column=4).value = '都道府県[全角]'
        ###     ws_ippan[i].cell(row=6, column=5).value = '市区町村名[全角]'
        ###     ws_ippan[i].cell(row=6, column=6).value = '水害発生月日'
        ###     ws_ippan[i].cell(row=6, column=7).value = ''
        ###     ws_ippan[i].cell(row=6, column=8).value = '水害終了月日'
        ###     ws_ippan[i].cell(row=6, column=9).value = ''
        ###     ws_ippan[i].cell(row=6, column=10).value = '水害原因'
        ###     ws_ippan[i].cell(row=6, column=11).value = ''
        ###     ws_ippan[i].cell(row=6, column=12).value = ''
        ###     ws_ippan[i].cell(row=6, column=13).value = '水害区域番号'
        ###     ws_ippan[i].cell(row=6, column=14).value = '水系・沿岸名全角'
        ###     ws_ippan[i].cell(row=6, column=15).value = '水系種別全角'
        ###     ws_ippan[i].cell(row=6, column=16).value = '河川・海岸名全角'
        ###     ws_ippan[i].cell(row=6, column=17).value = '河川種別全角'
        ###     ws_ippan[i].cell(row=6, column=18).value = '地盤勾配区分'
        ###     ws_ippan[i].cell(row=6, column=19).value = '町丁名・大字名全角'
        ###     ws_ippan[i].cell(row=6, column=20).value = '名称全角'
        ###     ws_ippan[i].cell(row=6, column=21).value = '地上地下区分'
        ###     ws_ippan[i].cell(row=6, column=22).value = '浸水土砂区分'
        ###     ws_ippan[i].cell(row=6, column=23).value = '被害建物棟数'
        ###     ws_ippan[i].cell(row=6, column=24).value = ''
        ###     ws_ippan[i].cell(row=6, column=25).value = ''
        ###     ws_ippan[i].cell(row=6, column=26).value = ''
        ###     ws_ippan[i].cell(row=6, column=27).value = ''
        ###     ws_ippan[i].cell(row=6, column=28).value = ''
        ###     ws_ippan[i].cell(row=6, column=29).value = '被害建物の延床面積'
        ###     ws_ippan[i].cell(row=6, column=30).value = '被災世帯数'
        ###     ws_ippan[i].cell(row=6, column=31).value = '被災事業所数'
        ###     ws_ippan[i].cell(row=6, column=32).value = '農家・漁家戸数'
        ###     ws_ippan[i].cell(row=6, column=33).value = ''
        ###     ws_ippan[i].cell(row=6, column=34).value = ''
        ###     ws_ippan[i].cell(row=6, column=35).value = ''
        ###     ws_ippan[i].cell(row=6, column=36).value = ''
        ###     ws_ippan[i].cell(row=6, column=37).value = '事業所従業者数'
        ###     ws_ippan[i].cell(row=6, column=38).value = ''
        ###     ws_ippan[i].cell(row=6, column=39).value = ''
        ###     ws_ippan[i].cell(row=6, column=40).value = ''
        ###     ws_ippan[i].cell(row=6, column=41).value = ''
        ###     ws_ippan[i].cell(row=6, column=42).value = '事業所の産業分類'
        ###     ws_ippan[i].cell(row=6, column=43).value = '地下空間の利用形態'
        ###     ws_ippan[i].cell(row=6, column=44).value = '備考1'
        ###     ws_ippan[i].cell(row=6, column=45).value = '備考2'
        ###     ws_ippan[i].cell(row=6, column=46).value = '水害区域面積(宅地)'
        ###     ws_ippan[i].cell(row=6, column=47).value = '水害区域面積(農地)'
        ###     ws_ippan[i].cell(row=6, column=48).value = '水害区域面積(地下)'
        ###     ws_ippan[i].cell(row=6, column=49).value = '工種'
        ###     ws_ippan[i].cell(row=6, column=50).value = '農作物被害額(千円)'
        ###     ws_ippan[i].cell(row=6, column=51).value = '異常気象コード'
        ###     ws_ippan[i].cell(row=6, column=52).value = '調査票シート名'
        ###     ws_ippan[i].cell(row=6, column=53).value = ''
        ###     ws_ippan[i].cell(row=6, column=54).value = 'ファイル最終更新日時'
        ###     ws_ippan[i].cell(row=6, column=55).value = 'ファイルパス'

        ###     ws_ippan[i].cell(row=7, column=1).value = ''
        ###     ws_ippan[i].cell(row=7, column=2).value = ''
        ###     ws_ippan[i].cell(row=7, column=3).value = ''
        ###     ws_ippan[i].cell(row=7, column=4).value = ''
        ###     ws_ippan[i].cell(row=7, column=5).value = ''
        ###     ws_ippan[i].cell(row=7, column=6).value = '月'
        ###     ws_ippan[i].cell(row=7, column=7).value = '日'
        ###     ws_ippan[i].cell(row=7, column=8).value = '月'
        ###     ws_ippan[i].cell(row=7, column=9).value = '日'
        ###     ws_ippan[i].cell(row=7, column=10).value = '1'
        ###     ws_ippan[i].cell(row=7, column=11).value = '2'
        ###     ws_ippan[i].cell(row=7, column=12).value = '3'
        ###     ws_ippan[i].cell(row=7, column=13).value = ''
        ###     ws_ippan[i].cell(row=7, column=14).value = ''
        ###     ws_ippan[i].cell(row=7, column=15).value = ''
        ###     ws_ippan[i].cell(row=7, column=16).value = ''
        ###     ws_ippan[i].cell(row=7, column=17).value = ''
        ###     ws_ippan[i].cell(row=7, column=18).value = ''
        ###     ws_ippan[i].cell(row=7, column=19).value = ''
        ###     ws_ippan[i].cell(row=7, column=20).value = ''
        ###     ws_ippan[i].cell(row=7, column=21).value = ''
        ###     ws_ippan[i].cell(row=7, column=22).value = ''
        ###     ws_ippan[i].cell(row=7, column=23).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=24).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=25).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=26).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=27).value = '半壊'
        ###     ws_ippan[i].cell(row=7, column=28).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=29).value = ''
        ###     ws_ippan[i].cell(row=7, column=30).value = ''
        ###     ws_ippan[i].cell(row=7, column=31).value = ''
        ###     ws_ippan[i].cell(row=7, column=32).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=33).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=34).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=35).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=36).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=37).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=38).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=39).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=40).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=41).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=42).value = ''
        ###     ws_ippan[i].cell(row=7, column=43).value = ''
        ###     ws_ippan[i].cell(row=7, column=44).value = ''
        ###     ws_ippan[i].cell(row=7, column=45).value = ''
        ###     ws_ippan[i].cell(row=7, column=46).value = ''
        ###     ws_ippan[i].cell(row=7, column=47).value = ''
        ###     ws_ippan[i].cell(row=7, column=48).value = ''
        ###     ws_ippan[i].cell(row=7, column=49).value = ''
        ###     ws_ippan[i].cell(row=7, column=50).value = ''
        ###     ws_ippan[i].cell(row=7, column=51).value = ''
        ###     ws_ippan[i].cell(row=7, column=52).value = ''
        ###     ws_ippan[i].cell(row=7, column=53).value = ''
        ###     ws_ippan[i].cell(row=7, column=54).value = ''
        ###     ws_ippan[i].cell(row=7, column=55).value = ''

        #######################################################################
        ### EXCEL入出力処理(0060)
        ### (1)EXCELのセルに、建物区分に応じて、背景灰色、背景白色を変化させる条件付き形式を埋め込む。
        ### (2)ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 7/12.', 'INFO')

        #######################################################################
        ### EXCEL入出力処理(0070)
        ### (1)EXCELのヘッダ部のセルに、単純プルダウン、連動プルダウンの設定を埋め込む。
        ### (2)EXCELの一覧部のセルに、単純プルダウンの設定を埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 8/12.', 'INFO')
        for i, ken_code in enumerate(ken_code_request):
            ippan_view_list = IPPAN_VIEW.objects.raw("""SELECT * FROM IPPAN_VIEW WHERE ken_code=%s ORDER BY CAST(suigai_id AS INTEGER), CAST(ippan_id AS INTEGER)""", [ken_code,])
            
            if ippan_view_list:
                for j, ippan in enumerate(ippan_view_list):
                    ws_ippan[i].cell(row=8+j, column=1).value = str(ippan.suigai_id) + ":" + str(ippan.ippan_id)
                    ws_ippan[i].cell(row=8+j, column=2).value = ""
                    ws_ippan[i].cell(row=8+j, column=3).value = ""
                    ws_ippan[i].cell(row=8+j, column=4).value = str(ippan.ken_name) + str(ippan.ken_code)
                    ws_ippan[i].cell(row=8+j, column=5).value = str(ippan.city_name) + ":" + str(ippan.city_code)
                    ws_ippan[i].cell(row=8+j, column=6).value = str(ippan.begin_date)
                    ws_ippan[i].cell(row=8+j, column=7).value = str(ippan.begin_date)
                    ws_ippan[i].cell(row=8+j, column=8).value = str(ippan.end_date)
                    ws_ippan[i].cell(row=8+j, column=9).value = str(ippan.end_date)
                    ws_ippan[i].cell(row=8+j, column=10).value = str(ippan.cause_1_name) + ":" + str(ippan.cause_1_code)
                    ws_ippan[i].cell(row=8+j, column=11).value = str(ippan.cause_2_name) + ":" + str(ippan.cause_2_code)
                    ws_ippan[i].cell(row=8+j, column=12).value = str(ippan.cause_3_name) + ":" + str(ippan.cause_3_code)
                    ws_ippan[i].cell(row=8+j, column=13).value = str(ippan.area_name) + ":" + str(ippan.area_id)
                    ws_ippan[i].cell(row=8+j, column=14).value = str(ippan.suikei_name) + ":" + str(ippan.suikei_code)
                    ws_ippan[i].cell(row=8+j, column=15).value = str(ippan.suikei_type_name) + ":" + str(ippan.suikei_type_code)
                    ws_ippan[i].cell(row=8+j, column=16).value = str(ippan.kasen_name) + ":" + str(ippan.kasen_code)
                    ws_ippan[i].cell(row=8+j, column=17).value = str(ippan.kasen_type_name) + ":" + str(ippan.kasen_type_code)
                    ws_ippan[i].cell(row=8+j, column=18).value = str(ippan.gradient_name) + ":" + str(ippan.gradient_code)
                    ws_ippan[i].cell(row=8+j, column=19).value = str(ippan.ippan_name) + ":" + str(ippan.ippan_id) 
                    ws_ippan[i].cell(row=8+j, column=20).value = str(ippan.building_name) + ":" + str(ippan.building_code)
                    ws_ippan[i].cell(row=8+j, column=21).value = str(ippan.underground_name) + ":" + str(ippan.underground_code)
                    ws_ippan[i].cell(row=8+j, column=22).value = str(ippan.flood_sediment_name) + ":" + str(ippan.flood_sediment_code)
                    ws_ippan[i].cell(row=8+j, column=23).value = ippan.building_lv00
                    ws_ippan[i].cell(row=8+j, column=24).value = ippan.building_lv01_49
                    ws_ippan[i].cell(row=8+j, column=25).value = ippan.building_lv50_99
                    ws_ippan[i].cell(row=8+j, column=26).value = ippan.building_lv100
                    ws_ippan[i].cell(row=8+j, column=27).value = ippan.building_half
                    ws_ippan[i].cell(row=8+j, column=28).value = ippan.building_full
                    ws_ippan[i].cell(row=8+j, column=29).value = ippan.floor_area
                    ws_ippan[i].cell(row=8+j, column=30).value = ippan.family
                    ws_ippan[i].cell(row=8+j, column=31).value = ippan.office
                    ws_ippan[i].cell(row=8+j, column=32).value = ippan.farmer_fisher_lv00
                    ws_ippan[i].cell(row=8+j, column=33).value = ippan.farmer_fisher_lv01_49
                    ws_ippan[i].cell(row=8+j, column=34).value = ippan.farmer_fisher_lv50_99
                    ws_ippan[i].cell(row=8+j, column=35).value = ippan.farmer_fisher_lv100
                    ws_ippan[i].cell(row=8+j, column=36).value = ippan.farmer_fisher_full
                    ws_ippan[i].cell(row=8+j, column=37).value = ippan.employee_lv00
                    ws_ippan[i].cell(row=8+j, column=38).value = ippan.employee_lv01_49
                    ws_ippan[i].cell(row=8+j, column=39).value = ippan.employee_lv50_99
                    ws_ippan[i].cell(row=8+j, column=40).value = ippan.employee_lv100
                    ws_ippan[i].cell(row=8+j, column=41).value = ippan.employee_full
                    ws_ippan[i].cell(row=8+j, column=42).value = str(ippan.industry_name) + ":" + str(ippan.industry_code)
                    ws_ippan[i].cell(row=8+j, column=43).value = str(ippan.usage_name) + ":" + str(ippan.usage_code)
                    ws_ippan[i].cell(row=8+j, column=44).value = ippan.comment
                    ws_ippan[i].cell(row=8+j, column=45).value = ""
                    ws_ippan[i].cell(row=8+j, column=46).value = ippan.residential_area
                    ws_ippan[i].cell(row=8+j, column=47).value = ippan.agricultural_area
                    ws_ippan[i].cell(row=8+j, column=48).value = ippan.underground_area
                    ws_ippan[i].cell(row=8+j, column=49).value = str(ippan.kasen_kaigan_name) + ":" + str(ippan.kasen_kaigan_code)
                    ws_ippan[i].cell(row=8+j, column=50).value = ippan.crop_damage
                    ws_ippan[i].cell(row=8+j, column=51).value = ""
                    ws_ippan[i].cell(row=8+j, column=52).value = ""
                    ws_ippan[i].cell(row=8+j, column=53).value = ""
                    ws_ippan[i].cell(row=8+j, column=54).value = ""
                    ws_ippan[i].cell(row=8+j, column=55).value = ""
        
        #######################################################################
        ### DBアクセス処理(0080)
        ### (1)DBから水害のデータを取得する。
        ### (2)DBから一般資産調査票（調査員）のデータを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 9/12.', 'INFO')

        #######################################################################
        ### EXCEL入出力処理(0090)
        ### ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 10/12.', 'INFO')
        for i, _ in enumerate(ken_code_request):
            wb[i].save(download_file_path[i])

        #######################################################################
        ### EXCEL入出力処理(0100)
        ### 複数のEXCELファイルを1つに固めて保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 11/12.', 'INFO')
        
        #######################################################################
        ### レスポンスセット処理(0110)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 STEP 12/12.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb[0]), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_city.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_ken_view(request, lock)
### 一般資産調査票（都道府県担当者用）
### urlpattern：path('ippan_ken/', views.ippan_ken_view, name='ippan_ken_view')
### template：
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_ken_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        ### (2)GETメソッドの場合、関数を抜ける。
        ### (3)POSTリクエストの市区町村数が0件の場合、関数を抜ける。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 ken_code_hidden= {}'.format(request.POST.get('ken_code_hidden')), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 1/12.', 'INFO')

        if request.method == 'GET':
            print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        if request.POST.get('ken_code_hidden') is None:
            print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数でエラーが発生しました。', 'ERROR')
            return render(request, 'error.html')

        ken_code_request = [x.strip() for x in request.POST.get('ken_code_hidden').split(',')][:-1]

        if ken_code_request:
            if len(ken_code_request) == 0:
                print_log('[WARN] P0200ExcelDownload.ippan_ken_view()関数で警告が発生しました。', 'WARN')
                return render(request, 'warning.html')

        #######################################################################
        ### 局所定数セット処理(0010)
        ### VLOOKUP用の局所定数をセットする。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 2/12.', 'INFO')
        VLOOK_VALUE = [
            'B', 'G', 'L', 'Q', 'V', 'AA', 'AF', 'AK', 'AP', 'AU', 
            'AZ', 'BE', 'BJ', 'BO', 'BT', 'BY', 'CD', 'CI', 'CN', 'CS', 
            'CX', 'DC', 'DH', 'DM', 'DR', 'DW', 'EB', 'EG', 'EL', 'EQ', 
            'EV', 'FA', 'FF', 'FK', 'FP', 'FU', 'FZ', 'GE', 'GJ', 'GO', 
            'GT', 'GY', 'HD', 'HI', 'HN', 'HS', 'HX', 'IC', 'IH', 'IM', 
            'IR', 'IW', 'JB', 'JG', 'JL', 'JQ', 'JV', 'KA', 'KF', 'KK', 
            'KP', 'KU', 'KZ', 'LE', 'LJ', 'LO', 'LT', 'LY', 'MD', 'MI', 
            'MN', 'MS', 'MX', 'NC', 'NH', 'NM', 'NR', 'NW', 'OB', 'OG', 
            'OL', 'OQ', 'OV', 'PA', 'PF', 'PK', 'PP', 'PU', 'PZ', 'QE', 
            'QJ', 'QO', 'QT', 'QY', 'RD', 'RI', 'RN', 'RS', 'RX', 'SC', 
            'SH', 'SM', 'SR', 'SW', 'TB', 'TG', 'TL', 'TQ', 'TV', 'UA', 
            'UF', 'UK', 'UP', 'UU', 'UZ', 'VE', 'VJ', 'VO', 'VT', 'VY', 
            'WD', 'WI', 'WN', 'WS', 'WX', 'XC', 'XH', 'XM', 'XR', 'XW', 
            'YB', 'YG', 'YL', 'YQ', 'YV', 'ZA', 'ZF', 'ZK', 'ZP', 'ZU', 
            'ZZ', 'AAE', 'AAJ', 'AAO', 'AAT', 'AAY', 'ABD', 'ABI', 'ABN', 'ABS', 
            'ABX', 'ACC', 'ACH', 'ACM', 'ACR', 'ACW', 'ADB', 'ADG', 'ADL', 'ADQ', 
            'ADV', 'AEA', 'AEF', 'AEK', 'AEP', 'AEU', 'AEZ', 'AFE', 'AFJ', 'AFO', 
            'AFT', 'AFY', 'AGD', 'AGI', 'AGN', 'AGS', 'AGX', 'AHC', 'AHH', 'AHM', 
            'AHR', 'AHW', 'AIB', 'AIG', 'AIL', 'AIQ', 'AIV', 'AJA', 'AJF', 'AJK', 
            'AJP', 'AJU', 'AJZ', 'AKE', 'AKJ', 'AKO', 'AKT', 'AKY', 'ALD', 'ALI', 
            'ALN', 'ALS', 'ALX', 'AMC', 'AMH', 'AMM', 'AMR', 'AMW', 'ANB', 'ANG', 
            'ANL', 'ANQ', 'ANV', 'AOA', 'AOF', 'AOK', 'AOP', 'AOU', 'AOZ', 'APE', 
            'APJ', 'APO', 'APT', 'APY', 'AQD', 'AQI', 'AQN', 'AQS', 'AQX', 'ARC', 
            'ARH', 'ARM', 'ARR', 'ARW', 'ASB', 'ASG', 'ASL', 'ASQ', 'ASV', 'ATA', 
            'ATF', 'ATK', 'ATP', 'ATU', 'ATZ', 'AUE', 'AUJ', 'AUO', 'AUT', 'AUY', 
            'AVD', 'AVI', 'AVN', 'AVS', 'AVX', 'AWC', 'AWH', 'AWM', 'AWR', 'AWW', 
            'AXB', 'AXG', 'AXL', 'AXQ', 'AXV', 'AYA', 'AYF', 'AYK', 'AYP', 'AYU', 
            'AYZ', 'AZE', 'AZJ', 'AZO', 'AZT', 'AZY'
            ]

        #######################################################################
        ### DBアクセス処理(0020)
        ### DBから都道府県コード毎の水害データの件数を取得する。
        ### ※関数のメインの処理の前に、EXCELのファイル数、シート数を確定するため。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 3/12.', 'INFO')
        
        #######################################################################
        ### EXCEL入出力処理(0030)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        ### ※都道府県毎にEXCELファイルを作成する。
        ### ※水害毎にEXCELシートを作成する。
        ### ※0件の場合、入力用にIPPANシートを10枚作成する。
        ### ※5件の場合、既存データ用にIPPANシートを5枚作成する。
        ### ※5件の場合、入力用にIPPANシートを10枚作成する。（合計15枚作成する。）
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 4/12.', 'INFO')
        download_file_path = []
        wb = []
        ws_ippan = []
        ws_building = []
        ws_ken = []
        ws_city = []
        ws_kasen_kaigan = []
        ws_suikei = []
        ws_suikei_type = []
        ws_kasen = []
        ws_kasen_type = []
        ws_cause = []
        ws_underground = []
        ws_usage = []
        ws_flood_sediment = []
        ws_gradient = []
        ws_industry = []
        ws_suigai = []
        ws_weather = []
        ws_area = []
        ws_city_vlook = []
        ws_kasen_vlook = []
        
        ### len(ken_code_request)=ワークブックの数=EXCELファイルの数
        ### EXCELファイル毎に、テーブル毎に１シートとする。
        for i, ken_code in enumerate(ken_code_request):
            template_file_path = 'static/template_ippan_ken.xlsx'
            download_file_path.append('static/download_ippan_ken_' + ken_code + '.xlsx')
            
            wb.append(openpyxl.load_workbook(template_file_path, keep_vba=False))
            
            ws_ippan.append(wb[i]["IPPAN"])
            ws_building.append(wb[i]["BUILDING"])
            ws_ken.append(wb[i]["KEN"])
            ws_city.append(wb[i]["CITY"])
            ws_kasen_kaigan.append(wb[i]["KASEN_KAIGAN"])
            ws_suikei.append(wb[i]["SUIKEI"])
            ws_suikei_type.append(wb[i]["SUIKEI_TYPE"])
            ws_kasen.append(wb[i]["KASEN"])
            ws_kasen_type.append(wb[i]["KASEN_TYPE"])
            ws_cause.append(wb[i]["CAUSE"])
            ws_underground.append(wb[i]["UNDERGROUND"])
            ws_usage.append(wb[i]["USAGE"])
            ws_flood_sediment.append(wb[i]["FLOOD_SEDIMENT"])
            ws_gradient.append(wb[i]["GRADIENT"])
            ws_industry.append(wb[i]["INDUSTRY"])
            ws_suigai.append(wb[i]["SUIGAI"])
            ws_weather.append(wb[i]["WEATHER"])
            ws_area.append(wb[i]["AREA"])
            ws_city_vlook.append(wb[i]["CITY_VLOOK"])
            ws_kasen_vlook.append(wb[i]["KASEN_VLOOK"])

        #######################################################################
        ### DBアクセス処理(0040)
        ### EXCEL入出力処理(0040)
        ### (1)DBから建物区分等のマスタデータを取得する。
        ### (2)EXCELのマスタ用のシートのセルに、DBから取得した建物区分等のマスタデータを埋め込む。
        ### (3)EXCELのVLOKUP用のシートのセルに、DBから取得した都道府県等のマスタデータを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 5/12.', 'INFO')

        ### 1000: 建物区分
        print("ippan_ken_view2", flush=True)
        building_list = None
        building_list = BUILDING.objects.raw("""SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if building_list:
                for j, building in enumerate(building_list):
                    ws_building[i].cell(row=j+1, column=1).value = building.building_code
                    ws_building[i].cell(row=j+1, column=2).value = str(building.building_name) + ":" + str(building.building_code)

        ### 1010: 都道府県
        print("ippan_ken_view3", flush=True)
        ken_list = None
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if ken_list:
                for j, ken in enumerate(ken_list):
                    ws_ken[i].cell(row=j+1, column=1).value = ken.ken_code
                    ws_ken[i].cell(row=j+1, column=2).value = str(ken.ken_name) + ":" + str(ken.ken_code)
                    ws_city_vlook[i].cell(row=j+1, column=1).value = str(ken.ken_name) + ":" + str(ken.ken_code)

        ### 1020: 市区町村
        print("ippan_ken_view4", flush=True)
        city_list = []
        if ken_list:
            for i, ken in enumerate(ken_list):
                city_list.append(CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken.ken_code, ]))

        for i, _ in enumerate(ken_code_request):
            if city_list:
                for j, city in enumerate(city_list):
                    ws_city_vlook[i].cell(row=j+1, column=2).value = 'CITY!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(city)

        for i, _ in enumerate(ken_code_request):
            if city_list:
                for j, city in enumerate(city_list):
                    if city:
                        for k, c in enumerate(city):
                            ws_city[i].cell(row=k+1, column=j*5+1).value = c.city_code
                            ws_city[i].cell(row=k+1, column=j*5+2).value = str(c.city_name) + ":" + str(c.city_code)
                            ws_city[i].cell(row=k+1, column=j*5+3).value = c.ken_code
                            ws_city[i].cell(row=k+1, column=j*5+4).value = c.city_population
                            ws_city[i].cell(row=k+1, column=j*5+5).value = c.city_area

        ### 1030: 水害発生地点工種（河川海岸区分）
        print("ippan_ken_view5", flush=True)
        kasen_kaigan_list = None
        kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_kaigan_list:
                for j, kasen_kaigan in enumerate(kasen_kaigan_list):
                    ws_kasen_kaigan[i].cell(row=j+1, column=1).value = kasen_kaigan.kasen_kaigan_code
                    ws_kasen_kaigan[i].cell(row=j+1, column=2).value = kasen_kaigan.kasen_kaigan_name + ":" + kasen_kaigan.kasen_kaigan_code

        ### 1040: 水系（水系・沿岸）
        print("ippan_ken_view6", flush=True)
        suikei_list = None
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suikei_list:
                for j, suikei in enumerate(suikei_list):
                    ws_suikei[i].cell(row=j+1, column=1).value = suikei.suikei_code
                    ws_suikei[i].cell(row=j+1, column=2).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)
                    ws_suikei[i].cell(row=j+1, column=3).value = suikei.suikei_type_code
                    ws_kasen_vlook[i].cell(row=j+1, column=1).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)

        ### 1050: 水系種別（水系・沿岸種別）
        print("ippan_ken_view7", flush=True)
        suikei_type_list = None
        suikei_type_list = SUIKEI_TYPE.objects.raw("""SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suikei_type_list:
                for j, suikei_type in enumerate(suikei_type_list):
                    ws_suikei_type[i].cell(row=j+1, column=1).value = suikei_type.suikei_type_code
                    ws_suikei_type[i].cell(row=j+1, column=2).value = str(suikei_type.suikei_type_name) + ":" + str(suikei_type.suikei_type_code)

        ### 1060: 河川（河川・海岸）
        print("ippan_ken_view8", flush=True)
        kasen_list = []
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                kasen_list.append(KASEN.objects.raw("""SELECT * FROM KASEN WHERE SUIKEI_CODE=%s ORDER BY CAST(KASEN_CODE AS INTEGER)""", [suikei.suikei_code, ]))

        for i, _ in enumerate(ken_code_request):
            if kasen_list:
                for j, kasen in enumerate(kasen_list):
                    ws_kasen_vlook[i].cell(row=j+1, column=2).value = 'KASEN!$' + VLOOK_VALUE[j] + '$1:$' + VLOOK_VALUE[j] + '$%d' % len(kasen)
                
        ### kasen_list = KASEN.objects.raw("""SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_list:
                for j, kasen in enumerate(kasen_list):
                    if kasen:
                        for k, ka_ in enumerate(kasen):
                            ws_kasen[i].cell(row=k+1, column=j*5+1).value = ka_.kasen_code
                            ws_kasen[i].cell(row=k+1, column=j*5+2).value = str(ka_.kasen_name) + ":" + str(ka_.kasen_code)
                            ws_kasen[i].cell(row=k+1, column=j*5+3).value = ka_.kasen_type_code
                            ws_kasen[i].cell(row=k+1, column=j*5+4).value = ka_.suikei_code
                
        ### 1070: 河川種別（河川・海岸種別）
        print("ippan_ken_view9", flush=True)
        kasen_type_list = None
        kasen_type_list = KASEN_TYPE.objects.raw("""SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if kasen_type_list:
                for j, kasen_type in enumerate(kasen_type_list):
                    ws_kasen_type[i].cell(row=j+1, column=1).value = kasen_type.kasen_type_code
                    ws_kasen_type[i].cell(row=j+1, column=2).value = str(kasen_type.kasen_type_name) + ":" + str(kasen_type.kasen_type_code)
        
        ### 1080: 水害原因
        print("ippan_ken_view10", flush=True)
        cause_list = None
        cause_list = CAUSE.objects.raw("""SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if cause_list:
                for j, cause in enumerate(cause_list):
                    ws_cause[i].cell(row=j+1, column=1).value = cause.cause_code
                    ws_cause[i].cell(row=j+1, column=2).value = str(cause.cause_name) + ":" + str(cause.cause_code)
                
        ### 1090: 地上地下区分
        print("ippan_ken_view11", flush=True)
        underground_list = None
        underground_list = UNDERGROUND.objects.raw("""SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if underground_list:
                for j, underground in enumerate(underground_list):
                    ws_underground[i].cell(row=j+1, column=1).value = underground.underground_code
                    ws_underground[i].cell(row=j+1, column=2).value = str(underground.underground_name) + ":" + str(underground.underground_code)
        
        ### 1100: 地下空間の利用形態
        print("ippan_ken_view12", flush=True)
        usage_list = None
        usage_list = USAGE.objects.raw("""SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if usage_list:
                for j, usage in enumerate(usage_list):
                    ws_usage[i].cell(row=j+1, column=1).value = usage.usage_code
                    ws_usage[i].cell(row=j+1, column=2).value = str(usage.usage_name) + ":" + str(usage.usage_code)
        
        ### 1110: 浸水土砂区分
        print("ippan_ken_view13", flush=True)
        flood_sediment_list = None
        flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if flood_sediment_list:
                for j, flood_sediment in enumerate(flood_sediment_list):
                    ws_flood_sediment[i].cell(row=j+1, column=1).value = flood_sediment.flood_sediment_code
                    ws_flood_sediment[i].cell(row=j+1, column=2).value = str(flood_sediment.flood_sediment_name) + ":" + str(flood_sediment.flood_sediment_code)
        
        ### 1120: 地盤勾配区分
        print("ippan_ken_view14", flush=True)
        gradient_list = None
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if gradient_list:
                for j, gradient in enumerate(gradient_list):
                    ws_gradient[i].cell(row=j+1, column=1).value = gradient.gradient_code
                    ws_gradient[i].cell(row=j+1, column=2).value = str(gradient.gradient_name) + ":" + str(gradient.gradient_code)
        
        ### 1130: 産業分類
        print("ippan_ken_view15", flush=True)
        industry_list = None
        industry_list = INDUSTRY.objects.raw("""SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if industry_list:
                for j, industry in enumerate(industry_list):
                    ws_industry[i].cell(row=j+1, column=1).value = industry.industry_code
                    ws_industry[i].cell(row=j+1, column=2).value = str(industry.industry_name) + ":" + str(industry.industry_code)

        ### 7000: 入力データ_水害区域
        print("ippan_ken_view16", flush=True)
        area_list = None
        area_list = AREA.objects.raw("""SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if area_list:
                for j, area in enumerate(area_list):
                    ws_area[i].cell(row=j+1, column=1).value = area.area_id
                    ws_area[i].cell(row=j+1, column=2).value = str(area.area_name) + ":" + str(area.area_id)

        ### 7010: 入力データ_異常気象
        print("ippan_ken_view17", flush=True)
        weather_list = None
        weather_list = WEATHER.objects.raw("""SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if weather_list:
                for j, weather in enumerate(weather_list):
                    ws_weather[i].cell(row=j+1, column=1).value = weather.weather_id
                    ws_weather[i].cell(row=j+1, column=2).value = str(weather.weather_name) + ":" + str(weather.weather_id)
        
        ### 7020: 入力データ_ヘッダ部分、水害
        print("ippan_ken_view18", flush=True)
        suigai_list = None
        suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])
        for i, _ in enumerate(ken_code_request):
            if suigai_list:
                for j, suigai in enumerate(suigai_list):
                    ws_suigai[i].cell(row=j+1, column=1).value = suigai.suigai_id
                    ws_suigai[i].cell(row=j+1, column=2).value = str(suigai.suigai_name) + ":" + str(suigai.suigai_id)
                    ws_suigai[i].cell(row=j+1, column=3).value = suigai.ken_code
                    ws_suigai[i].cell(row=j+1, column=4).value = suigai.city_code
                    ws_suigai[i].cell(row=j+1, column=5).value = suigai.begin_date
                    ws_suigai[i].cell(row=j+1, column=6).value = suigai.end_date
                    ws_suigai[i].cell(row=j+1, column=7).value = suigai.cause_1_code
                    ws_suigai[i].cell(row=j+1, column=8).value = suigai.cause_2_code
                    ws_suigai[i].cell(row=j+1, column=9).value = suigai.cause_3_code
                    ws_suigai[i].cell(row=j+1, column=10).value = suigai.area_id
                    ws_suigai[i].cell(row=j+1, column=11).value = suigai.suikei_code
                    ws_suigai[i].cell(row=j+1, column=12).value = suigai.kasen_code
                    ws_suigai[i].cell(row=j+1, column=13).value = suigai.gradient_code
                    ws_suigai[i].cell(row=j+1, column=14).value = suigai.residential_area
                    ws_suigai[i].cell(row=j+1, column=15).value = suigai.agricultural_area
                    ws_suigai[i].cell(row=j+1, column=16).value = suigai.underground_area
                    ws_suigai[i].cell(row=j+1, column=17).value = suigai.kasen_kaigan_code
                    ws_suigai[i].cell(row=j+1, column=18).value = suigai.crop_damage
                    ws_suigai[i].cell(row=j+1, column=19).value = suigai.weather_id

        #######################################################################
        ### EXCEL入出力処理(0050)
        ### (1)EXCELのヘッダ部のセルに、キャプションのテキストを埋め込む。
        ### (2)EXCELの一覧部のセルに、キャプションのテキストを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 6/12.', 'INFO')
        ### len(ken_code_request)=ワークブックの数=EXCELファイルの数
        ### for i, _ in enumerate(ken_code_request):
        ###     ws_ippan[i].cell(row=6, column=1).value = 'NO.'
        ###     ws_ippan[i].cell(row=6, column=2).value = 'ファイル名'
        ###     ws_ippan[i].cell(row=6, column=3).value = ''
        ###     ws_ippan[i].cell(row=6, column=4).value = '都道府県[全角]'
        ###     ws_ippan[i].cell(row=6, column=5).value = '市区町村名[全角]'
        ###     ws_ippan[i].cell(row=6, column=6).value = '水害発生月日'
        ###     ws_ippan[i].cell(row=6, column=7).value = ''
        ###     ws_ippan[i].cell(row=6, column=8).value = '水害終了月日'
        ###     ws_ippan[i].cell(row=6, column=9).value = ''
        ###     ws_ippan[i].cell(row=6, column=10).value = '水害原因'
        ###     ws_ippan[i].cell(row=6, column=11).value = ''
        ###     ws_ippan[i].cell(row=6, column=12).value = ''
        ###     ws_ippan[i].cell(row=6, column=13).value = '水害区域番号'
        ###     ws_ippan[i].cell(row=6, column=14).value = '水系・沿岸名全角'
        ###     ws_ippan[i].cell(row=6, column=15).value = '水系種別全角'
        ###     ws_ippan[i].cell(row=6, column=16).value = '河川・海岸名全角'
        ###     ws_ippan[i].cell(row=6, column=17).value = '河川種別全角'
        ###     ws_ippan[i].cell(row=6, column=18).value = '地盤勾配区分'
        ###     ws_ippan[i].cell(row=6, column=19).value = '町丁名・大字名全角'
        ###     ws_ippan[i].cell(row=6, column=20).value = '名称全角'
        ###     ws_ippan[i].cell(row=6, column=21).value = '地上地下区分'
        ###     ws_ippan[i].cell(row=6, column=22).value = '浸水土砂区分'
        ###     ws_ippan[i].cell(row=6, column=23).value = '被害建物棟数'
        ###     ws_ippan[i].cell(row=6, column=24).value = ''
        ###     ws_ippan[i].cell(row=6, column=25).value = ''
        ###     ws_ippan[i].cell(row=6, column=26).value = ''
        ###     ws_ippan[i].cell(row=6, column=27).value = ''
        ###     ws_ippan[i].cell(row=6, column=28).value = ''
        ###     ws_ippan[i].cell(row=6, column=29).value = '被害建物の延床面積'
        ###     ws_ippan[i].cell(row=6, column=30).value = '被災世帯数'
        ###     ws_ippan[i].cell(row=6, column=31).value = '被災事業所数'
        ###     ws_ippan[i].cell(row=6, column=32).value = '農家・漁家戸数'
        ###     ws_ippan[i].cell(row=6, column=33).value = ''
        ###     ws_ippan[i].cell(row=6, column=34).value = ''
        ###     ws_ippan[i].cell(row=6, column=35).value = ''
        ###     ws_ippan[i].cell(row=6, column=36).value = ''
        ###     ws_ippan[i].cell(row=6, column=37).value = '事業所従業者数'
        ###     ws_ippan[i].cell(row=6, column=38).value = ''
        ###     ws_ippan[i].cell(row=6, column=39).value = ''
        ###     ws_ippan[i].cell(row=6, column=40).value = ''
        ###     ws_ippan[i].cell(row=6, column=41).value = ''
        ###     ws_ippan[i].cell(row=6, column=42).value = '事業所の産業分類'
        ###     ws_ippan[i].cell(row=6, column=43).value = '地下空間の利用形態'
        ###     ws_ippan[i].cell(row=6, column=44).value = ''
        ###     ws_ippan[i].cell(row=6, column=45).value = ''
        ###     ws_ippan[i].cell(row=6, column=46).value = ''
        ###     ws_ippan[i].cell(row=6, column=47).value = ''
        ###     ws_ippan[i].cell(row=6, column=48).value = '備考1'
        ###     ws_ippan[i].cell(row=6, column=49).value = '備考2'
        ###     ws_ippan[i].cell(row=6, column=50).value = '水害区域面積(宅地)'
        ###     ws_ippan[i].cell(row=6, column=51).value = '水害区域面積(農地)'
        ###     ws_ippan[i].cell(row=6, column=52).value = '水害区域面積(地下)'
        ###     ws_ippan[i].cell(row=6, column=53).value = '工種'
        ###     ws_ippan[i].cell(row=6, column=54).value = '農作物被害額(千円)'
        ###     ws_ippan[i].cell(row=6, column=55).value = '異常気象コード'
        ###     ws_ippan[i].cell(row=6, column=56).value = '調査票シート名'
        ###     ws_ippan[i].cell(row=6, column=57).value = ''
        ###     ws_ippan[i].cell(row=6, column=58).value = 'ファイル最終更新日時'
        ###     ws_ippan[i].cell(row=6, column=59).value = 'ファイルパス'

        ###     ws_ippan[i].cell(row=7, column=1).value = ''
        ###     ws_ippan[i].cell(row=7, column=2).value = ''
        ###     ws_ippan[i].cell(row=7, column=3).value = ''
        ###     ws_ippan[i].cell(row=7, column=4).value = ''
        ###     ws_ippan[i].cell(row=7, column=5).value = ''
        ###     ws_ippan[i].cell(row=7, column=6).value = '月'
        ###     ws_ippan[i].cell(row=7, column=7).value = '日'
        ###     ws_ippan[i].cell(row=7, column=8).value = '月'
        ###     ws_ippan[i].cell(row=7, column=9).value = '日'
        ###     ws_ippan[i].cell(row=7, column=10).value = '1'
        ###     ws_ippan[i].cell(row=7, column=11).value = '2'
        ###     ws_ippan[i].cell(row=7, column=12).value = '3'
        ###     ws_ippan[i].cell(row=7, column=13).value = ''
        ###     ws_ippan[i].cell(row=7, column=14).value = ''
        ###     ws_ippan[i].cell(row=7, column=15).value = ''
        ###     ws_ippan[i].cell(row=7, column=16).value = ''
        ###     ws_ippan[i].cell(row=7, column=17).value = ''
        ###     ws_ippan[i].cell(row=7, column=18).value = ''
        ###     ws_ippan[i].cell(row=7, column=19).value = ''
        ###     ws_ippan[i].cell(row=7, column=20).value = ''
        ###     ws_ippan[i].cell(row=7, column=21).value = ''
        ###     ws_ippan[i].cell(row=7, column=22).value = ''
        ###     ws_ippan[i].cell(row=7, column=23).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=24).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=25).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=26).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=27).value = '半壊'
        ###     ws_ippan[i].cell(row=7, column=28).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=29).value = ''
        ###     ws_ippan[i].cell(row=7, column=30).value = ''
        ###     ws_ippan[i].cell(row=7, column=31).value = ''
        ###     ws_ippan[i].cell(row=7, column=32).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=33).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=34).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=35).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=36).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=37).value = '床下'
        ###     ws_ippan[i].cell(row=7, column=38).value = '1〜49cm'
        ###     ws_ippan[i].cell(row=7, column=39).value = '50〜99cm'
        ###     ws_ippan[i].cell(row=7, column=40).value = '1m以上'
        ###     ws_ippan[i].cell(row=7, column=41).value = '全壊'
        ###     ws_ippan[i].cell(row=7, column=42).value = ''
        ###     ws_ippan[i].cell(row=7, column=43).value = ''
        ###     ws_ippan[i].cell(row=7, column=44).value = ''
        ###     ws_ippan[i].cell(row=7, column=45).value = ''
        ###     ws_ippan[i].cell(row=7, column=46).value = ''
        ###     ws_ippan[i].cell(row=7, column=47).value = ''
        ###     ws_ippan[i].cell(row=7, column=48).value = ''
        ###     ws_ippan[i].cell(row=7, column=49).value = ''
        ###     ws_ippan[i].cell(row=7, column=50).value = ''
        ###     ws_ippan[i].cell(row=7, column=51).value = ''
        ###     ws_ippan[i].cell(row=7, column=52).value = ''
        ###     ws_ippan[i].cell(row=7, column=53).value = ''
        ###     ws_ippan[i].cell(row=7, column=54).value = ''
        ###     ws_ippan[i].cell(row=7, column=55).value = ''
        ###     ws_ippan[i].cell(row=7, column=56).value = ''
        ###     ws_ippan[i].cell(row=7, column=57).value = ''
        ###     ws_ippan[i].cell(row=7, column=58).value = ''
        ###     ws_ippan[i].cell(row=7, column=59).value = ''

        #######################################################################
        ### EXCEL入出力処理(0060)
        ### (1)EXCELのセルに、建物区分に応じて、背景灰色、背景白色を変化させる条件付き形式を埋め込む。
        ### (2)ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 7/12.', 'INFO')

        #######################################################################
        ### EXCEL入出力処理(0070)
        ### (1)EXCELのヘッダ部のセルに、単純プルダウン、連動プルダウンの設定を埋め込む。
        ### (2)EXCELの一覧部のセルに、単純プルダウンの設定を埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 8/12.', 'INFO')
        for i, ken_code in enumerate(ken_code_request):
            ippan_view_list = IPPAN_VIEW.objects.raw("""SELECT * FROM IPPAN_VIEW WHERE ken_code=%s ORDER BY CAST(suigai_id AS INTEGER), CAST(ippan_id AS INTEGER)""", [ken_code,])
            
            if ippan_view_list:
                for j, ippan in enumerate(ippan_view_list):
                    ws_ippan[i].cell(row=8+j, column=1).value = str(ippan.suigai_id) + ":" + str(ippan.ippan_id)
                    ws_ippan[i].cell(row=8+j, column=2).value = ""
                    ws_ippan[i].cell(row=8+j, column=3).value = ""
                    ws_ippan[i].cell(row=8+j, column=4).value = str(ippan.ken_name) + str(ippan.ken_code)
                    ws_ippan[i].cell(row=8+j, column=5).value = str(ippan.city_name) + ":" + str(ippan.city_code)
                    ws_ippan[i].cell(row=8+j, column=6).value = str(ippan.begin_date)
                    ws_ippan[i].cell(row=8+j, column=7).value = str(ippan.begin_date)
                    ws_ippan[i].cell(row=8+j, column=8).value = str(ippan.end_date)
                    ws_ippan[i].cell(row=8+j, column=9).value = str(ippan.end_date)
                    ws_ippan[i].cell(row=8+j, column=10).value = str(ippan.cause_1_name) + ":" + str(ippan.cause_1_code)
                    ws_ippan[i].cell(row=8+j, column=11).value = str(ippan.cause_2_name) + ":" + str(ippan.cause_2_code)
                    ws_ippan[i].cell(row=8+j, column=12).value = str(ippan.cause_3_name) + ":" + str(ippan.cause_3_code)
                    ws_ippan[i].cell(row=8+j, column=13).value = str(ippan.area_name) + ":" + str(ippan.area_id)
                    ws_ippan[i].cell(row=8+j, column=14).value = str(ippan.suikei_name) + ":" + str(ippan.suikei_code)
                    ws_ippan[i].cell(row=8+j, column=15).value = str(ippan.suikei_type_name) + ":" + str(ippan.suikei_type_code)
                    ws_ippan[i].cell(row=8+j, column=16).value = str(ippan.kasen_name) + ":" + str(ippan.kasen_code)
                    ws_ippan[i].cell(row=8+j, column=17).value = str(ippan.kasen_type_name) + ":" + str(ippan.kasen_type_code)
                    ws_ippan[i].cell(row=8+j, column=18).value = str(ippan.gradient_name) + ":" + str(ippan.gradient_code)
                    ws_ippan[i].cell(row=8+j, column=19).value = str(ippan.ippan_name) + ":" + str(ippan.ippan_id) 
                    ws_ippan[i].cell(row=8+j, column=20).value = str(ippan.building_name) + ":" + str(ippan.building_code)
                    ws_ippan[i].cell(row=8+j, column=21).value = str(ippan.underground_name) + ":" + str(ippan.underground_code)
                    ws_ippan[i].cell(row=8+j, column=22).value = str(ippan.flood_sediment_name) + ":" + str(ippan.flood_sediment_code)
                    ws_ippan[i].cell(row=8+j, column=23).value = ippan.building_lv00
                    ws_ippan[i].cell(row=8+j, column=24).value = ippan.building_lv01_49
                    ws_ippan[i].cell(row=8+j, column=25).value = ippan.building_lv50_99
                    ws_ippan[i].cell(row=8+j, column=26).value = ippan.building_lv100
                    ws_ippan[i].cell(row=8+j, column=27).value = ippan.building_half
                    ws_ippan[i].cell(row=8+j, column=28).value = ippan.building_full
                    ws_ippan[i].cell(row=8+j, column=29).value = ippan.floor_area
                    ws_ippan[i].cell(row=8+j, column=30).value = ippan.family
                    ws_ippan[i].cell(row=8+j, column=31).value = ippan.office
                    ws_ippan[i].cell(row=8+j, column=32).value = ippan.farmer_fisher_lv00
                    ws_ippan[i].cell(row=8+j, column=33).value = ippan.farmer_fisher_lv01_49
                    ws_ippan[i].cell(row=8+j, column=34).value = ippan.farmer_fisher_lv50_99
                    ws_ippan[i].cell(row=8+j, column=35).value = ippan.farmer_fisher_lv100
                    ws_ippan[i].cell(row=8+j, column=36).value = ippan.farmer_fisher_full
                    ws_ippan[i].cell(row=8+j, column=37).value = ippan.employee_lv00
                    ws_ippan[i].cell(row=8+j, column=38).value = ippan.employee_lv01_49
                    ws_ippan[i].cell(row=8+j, column=39).value = ippan.employee_lv50_99
                    ws_ippan[i].cell(row=8+j, column=40).value = ippan.employee_lv100
                    ws_ippan[i].cell(row=8+j, column=41).value = ippan.employee_full
                    ws_ippan[i].cell(row=8+j, column=42).value = str(ippan.industry_name) + ":" + str(ippan.industry_code)
                    ws_ippan[i].cell(row=8+j, column=43).value = str(ippan.usage_name) + ":" + str(ippan.usage_code)
                    ws_ippan[i].cell(row=8+j, column=44).value = ""
                    ws_ippan[i].cell(row=8+j, column=45).value = ""
                    ws_ippan[i].cell(row=8+j, column=46).value = ""
                    ws_ippan[i].cell(row=8+j, column=47).value = ""
                    ws_ippan[i].cell(row=8+j, column=48).value = ippan.comment
                    ws_ippan[i].cell(row=8+j, column=49).value = ""
                    ws_ippan[i].cell(row=8+j, column=50).value = ippan.residential_area
                    ws_ippan[i].cell(row=8+j, column=51).value = ippan.agricultural_area
                    ws_ippan[i].cell(row=8+j, column=52).value = ippan.underground_area
                    ws_ippan[i].cell(row=8+j, column=53).value = str(ippan.kasen_kaigan_name) + ":" + str(ippan.kasen_kaigan_code)
                    ws_ippan[i].cell(row=8+j, column=54).value = ippan.crop_damage
                    ws_ippan[i].cell(row=8+j, column=55).value = ""
                    ws_ippan[i].cell(row=8+j, column=56).value = ""
                    ws_ippan[i].cell(row=8+j, column=57).value = ""
                    ws_ippan[i].cell(row=8+j, column=58).value = ""
                    ws_ippan[i].cell(row=8+j, column=59).value = ""
        
        #######################################################################
        ### DBアクセス処理(0080)
        ### (1)DBから水害のデータを取得する。
        ### (2)DBから一般資産調査票（調査員）のデータを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 9/12.', 'INFO')

        #######################################################################
        ### EXCEL入出力処理(0090)
        ### ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 10/12.', 'INFO')
        for i, _ in enumerate(ken_code_request):
            wb[i].save(download_file_path[i])

        #######################################################################
        ### EXCEL入出力処理(0100)
        ### 複数のEXCELファイルを1つに固めて保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 11/12.', 'INFO')
        
        #######################################################################
        ### レスポンスセット処理(0110)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 STEP 12/12.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb[0]), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_ken.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
