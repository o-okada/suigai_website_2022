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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
        print_log('[INFO] P0200ExcelDownload.index_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：building_view
### 001: 建物区分
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def building_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.building_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、建物区分データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：ken_view
### 002: 都道府県
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ken_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ken_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、都道府県データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：city_view
### 003: 市区町村
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def city_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、市区町村データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.city_view()関数 STEP 2/4.', 'INFO')
        city_list = CITY.objects.raw("""SELECT * FROM CITY ORDER BY CAST(CITY_CODE AS INTEGER)""", [])
        
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
        ws.cell(row=1, column=4).value = '市区町村人口'
        ws.cell(row=1, column=5).value = '市区町村面積'
        
        if city_list:
            for i, city in enumerate(city_list):
                ws.cell(row=i+2, column=1).value = city.city_code
                ws.cell(row=i+2, column=2).value = city.city_name
                ws.cell(row=i+2, column=3).value = city.ken_code
                ws.cell(row=i+2, column=4).value = city.city_population
                ws.cell(row=i+2, column=5).value = city.city_area
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：kasen_kaigan_view
### 004: 水害発生地点工種（河川海岸区分）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_kaigan_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_kaigan_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、水害発生地点工種（河川海岸区分）データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：suikei_view
### 005: 水系（水系・沿岸）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suikei_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、水系（水系・沿岸）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suikei_view()関数 STEP 2/4.', 'INFO')
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
    
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
        
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws.cell(row=i+2, column=1).value = suikei.suikei_code
                ws.cell(row=i+2, column=2).value = suikei.suikei_name
                ws.cell(row=i+2, column=3).value = suikei.suikei_type_code
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：suikei_type_view
### 006: 水系種別（水系・沿岸種別）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suikei_type_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suikei_type_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、水系種別（水系・沿岸種別）データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：kasen_view
### 007: 河川（河川・海岸）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、河川（河川・海岸）データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kasen_view()関数 STEP 2/4.', 'INFO')
        kasen_list = KASEN.objects.raw("""SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)""", [])
    
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
        ws.cell(row=1, column=4).value = '水系コード'
        
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws.cell(row=i+2, column=1).value = kasen.kasen_code
                ws.cell(row=i+2, column=2).value = kasen.kasen_name
                ws.cell(row=i+2, column=3).value = kasen.kasen_type_code
                ws.cell(row=i+2, column=4).value = kasen.suikei_code
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：kasen_type_view
### 008: 河川種別（河川・海岸種別）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kasen_type_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kasen_type_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、河川種別（河川・海岸種別）データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：cause_view
### 009: 水害原因
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def cause_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.cause_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、水害原因データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：underground_view
### 010: 地上地下区分
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def underground_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.underground_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、地上地下区分データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：usage_view
### 011: 地下空間の利用形態
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def usage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.usage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、地下空間の利用形態データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：flood_sediment_view
### 012: 浸水土砂区分
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def flood_sediment_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.flood_sediment_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、浸水土砂区分データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：gradient_view
### 013: 地盤勾配区分
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def gradient_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.gradient_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、地盤勾配区分データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：industry_view
### 014: 産業分類
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def industry_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.industry_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、産業分類データを取得する。
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
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：restoration_view
### 015: 復旧事業工種
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def restoration_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、復旧事業工種データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 STEP 2/4.', 'INFO')
        restoration_list = RESTORATION.objects.raw("""SELECT * FROM RESTORATION ORDER BY CAST(RESTORATION_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_restoration.xlsx'
        download_file_path = 'static/download_restoration.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '復旧事業工種'
        ws.cell(row=1, column=1).value = '復旧事業工種コード'
        ws.cell(row=1, column=2).value = '復旧事業工種名'
        
        if restoration_list:
            for i, restoration in enumerate(restoration_list):
                ws.cell(row=i+2, column=1).value = restoration.restoration_code
                ws.cell(row=i+2, column=2).value = restoration.restoration_name
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.restoration_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="restoration.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.restoration_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.restoration_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_asset_view
### 100: 県別家屋評価額
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、県別家屋評価額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_asset_view()関数 STEP 2/4.', 'INFO')
        house_asset_list = HOUSE_ASSET.objects.raw("""SELECT * FROM HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)""", [])
    
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
        ws.title = '県別家屋被害'
        ws.cell(row=1, column=1).value = '県別家屋被害コード'
        ws.cell(row=1, column=2).value = '県コード'
        ws.cell(row=1, column=3).value = '県別家屋被害対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        ws.cell(row=1, column=6).value = '県別家屋評価額'
        
        if house_asset_list:
            for i, house_asset in enumerate(house_asset_list):
                ws.cell(row=i+2, column=1).value = house_asset.house_asset_code
                ws.cell(row=i+2, column=2).value = house_asset.ken_code
                ws.cell(row=i+2, column=3).value = house_asset.house_asset_year
                ws.cell(row=i+2, column=4).value = house_asset.begin_date
                ws.cell(row=i+2, column=5).value = house_asset.end_date
                ws.cell(row=i+2, column=6).value = house_asset.house_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：house_damage_view
### 101: 家屋被害率
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_damage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、家屋被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 STEP 2/4.', 'INFO')
        house_damage_list = HOUSE_DAMAGE.objects.raw("""SELECT * FROM HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_damage.xlsx'
        download_file_path = 'static/download_house_damage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家屋被害率'
        ws.cell(row=1, column=1).value = '家屋被害率コード'
        ws.cell(row=1, column=2).value = '家屋被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_勾配1_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_勾配1_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_勾配1_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_勾配1_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_勾配1_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_勾配1_300cm以上'

        ws.cell(row=1, column=11).value = '被害率_浸水_勾配2_床下'
        ws.cell(row=1, column=12).value = '被害率_浸水_勾配2_0から50cm未満'
        ws.cell(row=1, column=13).value = '被害率_浸水_勾配2_50から100cm未満'
        ws.cell(row=1, column=14).value = '被害率_浸水_勾配2_100から200cm未満'
        ws.cell(row=1, column=15).value = '被害率_浸水_勾配2_200から300cm未満'
        ws.cell(row=1, column=16).value = '被害率_浸水_勾配2_300cm以上'

        ws.cell(row=1, column=17).value = '被害率_浸水_勾配3_床下'
        ws.cell(row=1, column=18).value = '被害率_浸水_勾配3_0から50cm未満'
        ws.cell(row=1, column=19).value = '被害率_浸水_勾配3_50から100cm未満'
        ws.cell(row=1, column=20).value = '被害率_浸水_勾配3_100から200cm未満'
        ws.cell(row=1, column=21).value = '被害率_浸水_勾配3_200から300cm未満'
        ws.cell(row=1, column=22).value = '被害率_浸水_勾配3_300cm以上'

        ws.cell(row=1, column=23).value = '被害率_土砂_勾配1_床下'
        ws.cell(row=1, column=24).value = '被害率_土砂_勾配1_0から50cm未満'
        ws.cell(row=1, column=25).value = '被害率_土砂_勾配1_50から100cm未満'
        ws.cell(row=1, column=26).value = '被害率_土砂_勾配1_100から200cm未満'
        ws.cell(row=1, column=27).value = '被害率_土砂_勾配1_200から300cm未満'
        ws.cell(row=1, column=28).value = '被害率_土砂_勾配1_300cm以上'

        ws.cell(row=1, column=29).value = '被害率_土砂_勾配2_床下'
        ws.cell(row=1, column=30).value = '被害率_土砂_勾配2_0から50cm未満'
        ws.cell(row=1, column=31).value = '被害率_土砂_勾配2_50から100cm未満'
        ws.cell(row=1, column=32).value = '被害率_土砂_勾配2_100から200cm未満'
        ws.cell(row=1, column=33).value = '被害率_土砂_勾配2_200から300cm未満'
        ws.cell(row=1, column=34).value = '被害率_土砂_勾配2_300cm以上'

        ws.cell(row=1, column=35).value = '被害率_土砂_勾配3_床下'
        ws.cell(row=1, column=36).value = '被害率_土砂_勾配3_0から50cm未満'
        ws.cell(row=1, column=37).value = '被害率_土砂_勾配3_50から100cm未満'
        ws.cell(row=1, column=38).value = '被害率_土砂_勾配3_100から200cm未満'
        ws.cell(row=1, column=39).value = '被害率_土砂_勾配3_200から300cm未満'
        ws.cell(row=1, column=40).value = '被害率_土砂_勾配3_300cm以上'
        
        if house_damage_list:
            for i, house_damage in enumerate(house_damage_list):
                ws.cell(row=i+2, column=1).value = house_damage.house_damage_code
                ws.cell(row=i+2, column=2).value = house_damage.house_damage_year
                ws.cell(row=i+2, column=3).value = house_damage.begin_date
                ws.cell(row=i+2, column=4).value = house_damage.end_date
                
                ws.cell(row=i+2, column=5).value = house_damage.fl_gr1_lv00
                ws.cell(row=i+2, column=6).value = house_damage.fl_gr1_lv00_50
                ws.cell(row=i+2, column=7).value = house_damage.fl_gr1_lv50_100
                ws.cell(row=i+2, column=8).value = house_damage.fl_gr1_lv100_200
                ws.cell(row=i+2, column=9).value = house_damage.fl_gr1_lv200_300
                ws.cell(row=i+2, column=10).value = house_damage.fl_gr1_lv300
        
                ws.cell(row=i+2, column=11).value = house_damage.fl_gr2_lv00
                ws.cell(row=i+2, column=12).value = house_damage.fl_gr2_lv00_50
                ws.cell(row=i+2, column=13).value = house_damage.fl_gr2_lv50_100
                ws.cell(row=i+2, column=14).value = house_damage.fl_gr2_lv100_200
                ws.cell(row=i+2, column=15).value = house_damage.fl_gr2_lv200_300
                ws.cell(row=i+2, column=16).value = house_damage.fl_gr2_lv300

                ws.cell(row=i+2, column=17).value = house_damage.fl_gr3_lv00
                ws.cell(row=i+2, column=18).value = house_damage.fl_gr3_lv00_50
                ws.cell(row=i+2, column=19).value = house_damage.fl_gr3_lv50_100
                ws.cell(row=i+2, column=20).value = house_damage.fl_gr3_lv100_200
                ws.cell(row=i+2, column=21).value = house_damage.fl_gr3_lv200_300
                ws.cell(row=i+2, column=22).value = house_damage.fl_gr3_lv300
        
                ws.cell(row=i+2, column=23).value = house_damage.sd_gr1_lv00
                ws.cell(row=i+2, column=24).value = house_damage.sd_gr1_lv00_50
                ws.cell(row=i+2, column=25).value = house_damage.sd_gr1_lv50_100
                ws.cell(row=i+2, column=26).value = house_damage.sd_gr1_lv100_200
                ws.cell(row=i+2, column=27).value = house_damage.sd_gr1_lv200_300
                ws.cell(row=i+2, column=28).value = house_damage.sd_gr1_lv300
        
                ws.cell(row=i+2, column=29).value = house_damage.sd_gr2_lv00
                ws.cell(row=i+2, column=30).value = house_damage.sd_gr2_lv00_50
                ws.cell(row=i+2, column=31).value = house_damage.sd_gr2_lv50_100
                ws.cell(row=i+2, column=32).value = house_damage.sd_gr2_lv100_200
                ws.cell(row=i+2, column=33).value = house_damage.sd_gr2_lv200_300
                ws.cell(row=i+2, column=34).value = house_damage.sd_gr2_lv300

                ws.cell(row=i+2, column=35).value = house_damage.sd_gr3_lv00
                ws.cell(row=i+2, column=36).value = house_damage.sd_gr3_lv00_50
                ws.cell(row=i+2, column=37).value = house_damage.sd_gr3_lv50_100
                ws.cell(row=i+2, column=38).value = house_damage.sd_gr3_lv100_200
                ws.cell(row=i+2, column=39).value = house_damage.sd_gr3_lv200_300
                ws.cell(row=i+2, column=40).value = house_damage.sd_gr3_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_damage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_damage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_damage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_damage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：household_damage_view
### 102: 家庭用品自動車以外被害率
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def household_damage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、家庭用品自動車以外被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 STEP 2/4.', 'INFO')
        household_damage_list = HOUSEHOLD_DAMAGE.objects.raw("""SELECT * FROM HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_household_damage.xlsx'
        download_file_path = 'static/download_household_damage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭用品自動車以外被害率'
        ws.cell(row=1, column=1).value = '家庭用品自動車以外被害率コード'
        ws.cell(row=1, column=2).value = '家庭用品自動車以外被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '被害率_土砂_床下'
        ws.cell(row=1, column=12).value = '被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '被害率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '家庭用品自動車以外所有額'
        
        if household_damage_list:
            for i, household_damage in enumerate(household_damage_list):
                ws.cell(row=i+2, column=1).value = household_damage.household_damage_code
                ws.cell(row=i+2, column=2).value = household_damage.household_damage_year
                ws.cell(row=i+2, column=3).value = household_damage.begin_date
                ws.cell(row=i+2, column=4).value = household_damage.end_date
                
                ws.cell(row=i+2, column=5).value = household_damage.fl_lv00
                ws.cell(row=i+2, column=6).value = household_damage.fl_lv00_50
                ws.cell(row=i+2, column=7).value = household_damage.fl_lv50_100
                ws.cell(row=i+2, column=8).value = household_damage.fl_lv100_200
                ws.cell(row=i+2, column=9).value = household_damage.fl_lv200_300
                ws.cell(row=i+2, column=10).value = household_damage.fl_lv300
        
                ws.cell(row=i+2, column=11).value = household_damage.sd_lv00
                ws.cell(row=i+2, column=12).value = household_damage.sd_lv00_50
                ws.cell(row=i+2, column=13).value = household_damage.sd_lv50_100
                ws.cell(row=i+2, column=14).value = household_damage.sd_lv100_200
                ws.cell(row=i+2, column=15).value = household_damage.sd_lv200_300
                ws.cell(row=i+2, column=16).value = household_damage.sd_lv300

                ws.cell(row=i+2, column=17).value = household_damage.household_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.household_damage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_damage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_damage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.household_damage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：car_damage_view
### 103: 家庭用品自動車被害率
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def car_damage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、家庭用品自動車被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 STEP 2/4.', 'INFO')
        car_damage_list = CAR_DAMAGE.objects.raw("""SELECT * FROM CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_car_damage.xlsx'
        download_file_path = 'static/download_car_damage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '自動車被害率'
        ws.cell(row=1, column=1).value = '自動車被害率コード'
        ws.cell(row=1, column=2).value = '自動車被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '家庭用品自動車所有額'
        
        if car_damage_list:
            for i, car_damage in enumerate(car_damage_list):
                ws.cell(row=i+2, column=1).value = car_damage.car_damage_code
                ws.cell(row=i+2, column=2).value = car_damage.car_damage_year
                ws.cell(row=i+2, column=3).value = car_damage.begin_date
                ws.cell(row=i+2, column=4).value = car_damage.end_date
                
                ws.cell(row=i+2, column=5).value = car_damage.fl_lv00
                ws.cell(row=i+2, column=6).value = car_damage.fl_lv00_50
                ws.cell(row=i+2, column=7).value = car_damage.fl_lv50_100
                ws.cell(row=i+2, column=8).value = car_damage.fl_lv100_200
                ws.cell(row=i+2, column=9).value = car_damage.fl_lv200_300
                ws.cell(row=i+2, column=10).value = car_damage.fl_lv300

                ws.cell(row=i+2, column=11).value = car_damage.car_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.car_damage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car_damage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_damage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.car_damage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：house_cost_view
### 104: 家庭応急対策費
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def house_cost_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、家庭応急対策費データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 STEP 2/4.', 'INFO')
        house_cost_list = HOUSE_COST.objects.raw("""SELECT * FROM HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_house_cost.xlsx'
        download_file_path = 'static/download_house_cost.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '家庭応急対策費'
        ws.cell(row=1, column=1).value = '家庭応急対策費コード'
        ws.cell(row=1, column=2).value = '家庭応急対策費対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '代替活動費_床下'
        ws.cell(row=1, column=6).value = '代替活動費_0から50cm未満'
        ws.cell(row=1, column=7).value = '代替活動費_50から100cm未満'
        ws.cell(row=1, column=8).value = '代替活動費_100から200cm未満'
        ws.cell(row=1, column=9).value = '代替活動費_200から300cm未満'
        ws.cell(row=1, column=10).value = '代替活動費_300cm以上'

        ws.cell(row=1, column=11).value = '清掃費_床下'
        ws.cell(row=1, column=12).value = '清掃費_0から50cm未満'
        ws.cell(row=1, column=13).value = '清掃費_50から100cm未満'
        ws.cell(row=1, column=14).value = '清掃費_100から200cm未満'
        ws.cell(row=1, column=15).value = '清掃費_200から300cm未満'
        ws.cell(row=1, column=16).value = '清掃費_300cm以上'

        ws.cell(row=1, column=17).value = '清掃労働単価'
        
        if house_cost_list:
            for i, house_cost in enumerate(house_cost_list):
                ws.cell(row=i+2, column=1).value = house_cost.house_cost_code
                ws.cell(row=i+2, column=2).value = house_cost.house_cost_year
                ws.cell(row=i+2, column=3).value = house_cost.begin_date
                ws.cell(row=i+2, column=4).value = house_cost.end_date
                
                ws.cell(row=i+2, column=5).value = house_cost.alt_lv00
                ws.cell(row=i+2, column=6).value = house_cost.alt_lv00_50
                ws.cell(row=i+2, column=7).value = house_cost.alt_lv50_100
                ws.cell(row=i+2, column=8).value = house_cost.alt_lv100_200
                ws.cell(row=i+2, column=9).value = house_cost.alt_lv200_300
                ws.cell(row=i+2, column=10).value = house_cost.alt_lv300

                ws.cell(row=i+2, column=11).value = house_cost.clean_lv00
                ws.cell(row=i+2, column=12).value = house_cost.clean_lv00_50
                ws.cell(row=i+2, column=13).value = house_cost.clean_lv50_100
                ws.cell(row=i+2, column=14).value = house_cost.clean_lv100_200
                ws.cell(row=i+2, column=15).value = house_cost.clean_lv200_300
                ws.cell(row=i+2, column=16).value = house_cost.clean_lv300

                ws.cell(row=i+2, column=17).value = house_cost.house_cost
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.house_cost_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_cost.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_cost_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.house_cost_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_asset_view
### 105: 産業分類別資産額
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_asset_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、産業分類別資産額データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_asset_view()関数 STEP 2/4.', 'INFO')
        office_asset_list = OFFICE_ASSET.objects.raw("""SELECT * FROM OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)""", [])
    
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
        ws.title = '産業分類別資産額'
        ws.cell(row=1, column=1).value = '産業分類別資産額コード'
        ws.cell(row=1, column=2).value = '産業分類コード'
        ws.cell(row=1, column=3).value = '産業分類別資産額対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        
        ws.cell(row=1, column=6).value = '償却資産額'
        ws.cell(row=1, column=7).value = '在庫資産額'
        ws.cell(row=1, column=8).value = '付加価値額'
        
        if office_asset_list:
            for i, office_asset in enumerate(office_asset_list):
                ws.cell(row=i+2, column=1).value = office_asset.office_asset_code
                ws.cell(row=i+2, column=2).value = office_asset.industry_code
                ws.cell(row=i+2, column=3).value = office_asset.office_asset_year
                ws.cell(row=i+2, column=4).value = office_asset.begin_date
                ws.cell(row=i+2, column=5).value = office_asset.end_date
                
                ws.cell(row=i+2, column=6).value = office_asset.depreciable_asset
                ws.cell(row=i+2, column=7).value = office_asset.inventory_asset
                ws.cell(row=i+2, column=8).value = office_asset.value_added
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：office_damage_view
### 106: 事業所被害率
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_damage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、事業所被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 STEP 2/4.', 'INFO')
        office_damage_list = OFFICE_DAMAGE.objects.raw("""SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_damage.xlsx'
        download_file_path = 'static/download_office_damage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所被害率'
        ws.cell(row=1, column=1).value = '事業所被害率コード'
        ws.cell(row=1, column=2).value = '事業所被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '償却資産率_浸水_床下'
        ws.cell(row=1, column=6).value = '償却資産率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '償却資産率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '償却資産率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '償却資産率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '償却資産率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '償却資産率_土砂_床下'
        ws.cell(row=1, column=12).value = '償却資産率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '償却資産率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '償却資産率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '償却資産率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '償却資産率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '在庫資産率_浸水_床下'
        ws.cell(row=1, column=18).value = '在庫資産率_浸水_0から50cm未満'
        ws.cell(row=1, column=19).value = '在庫資産率_浸水_50から100cm未満'
        ws.cell(row=1, column=20).value = '在庫資産率_浸水_100から200cm未満'
        ws.cell(row=1, column=21).value = '在庫資産率_浸水_200から300cm未満'
        ws.cell(row=1, column=22).value = '在庫資産率_浸水_300cm以上'

        ws.cell(row=1, column=23).value = '在庫資産率_土砂_床下'
        ws.cell(row=1, column=24).value = '在庫資産率_土砂_0から50cm未満'
        ws.cell(row=1, column=25).value = '在庫資産率_土砂_50から100cm未満'
        ws.cell(row=1, column=26).value = '在庫資産率_土砂_100から200cm未満'
        ws.cell(row=1, column=27).value = '在庫資産率_土砂_200から300cm未満'
        ws.cell(row=1, column=28).value = '在庫資産率_土砂_300cm以上'
        
        if office_damage_list:
            for i, office_damage in enumerate(office_damage_list):
                ws.cell(row=i+2, column=1).value = office_damage.office_damage_code
                ws.cell(row=i+2, column=2).value = office_damage.office_damage_year
                ws.cell(row=i+2, column=3).value = office_damage.begin_date
                ws.cell(row=i+2, column=4).value = office_damage.end_date
                
                ws.cell(row=i+2, column=5).value = office_damage.dep_fl_lv00
                ws.cell(row=i+2, column=6).value = office_damage.dep_fl_lv00_50
                ws.cell(row=i+2, column=7).value = office_damage.dep_fl_lv50_100
                ws.cell(row=i+2, column=8).value = office_damage.dep_fl_lv100_200
                ws.cell(row=i+2, column=9).value = office_damage.dep_fl_lv200_300
                ws.cell(row=i+2, column=10).value = office_damage.dep_fl_lv300

                ws.cell(row=i+2, column=11).value = office_damage.dep_sd_lv00
                ws.cell(row=i+2, column=12).value = office_damage.dep_sd_lv00_50
                ws.cell(row=i+2, column=13).value = office_damage.dep_sd_lv50_100
                ws.cell(row=i+2, column=14).value = office_damage.dep_sd_lv100_200
                ws.cell(row=i+2, column=15).value = office_damage.dep_sd_lv200_300
                ws.cell(row=i+2, column=16).value = office_damage.dep_sd_lv300

                ws.cell(row=i+2, column=17).value = office_damage.inv_fl_lv00
                ws.cell(row=i+2, column=18).value = office_damage.inv_fl_lv00_50
                ws.cell(row=i+2, column=19).value = office_damage.inv_fl_lv50_100
                ws.cell(row=i+2, column=20).value = office_damage.inv_fl_lv100_200
                ws.cell(row=i+2, column=21).value = office_damage.inv_fl_lv200_300
                ws.cell(row=i+2, column=22).value = office_damage.inv_fl_lv300

                ws.cell(row=i+2, column=23).value = office_damage.inv_sd_lv00
                ws.cell(row=i+2, column=24).value = office_damage.inv_sd_lv00_50
                ws.cell(row=i+2, column=25).value = office_damage.inv_sd_lv50_100
                ws.cell(row=i+2, column=26).value = office_damage.inv_sd_lv100_200
                ws.cell(row=i+2, column=27).value = office_damage.inv_sd_lv200_300
                ws.cell(row=i+2, column=28).value = office_damage.inv_sd_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0000)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_damage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_damage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_damage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_damage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：office_cost_view
### 107: 事業所営業停止損失
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def office_cost_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、事業所営業停止損失データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 STEP 2/4.', 'INFO')
        office_cost_list = OFFICE_COST.objects.raw("""SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理
        ### （１）テンプレート用のEXCELファイルを読み込む。
        ### （２）セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_office_cost.xlsx'
        download_file_path = 'static/download_office_cost.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '事業所営業損失'
        ws.cell(row=1, column=1).value = '事業所営業損失コード'
        ws.cell(row=1, column=2).value = '事業所営業損失対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '営業停止日数_床下'
        ws.cell(row=1, column=6).value = '営業停止日数_0から50cm未満'
        ws.cell(row=1, column=7).value = '営業停止日数_50から100cm未満'
        ws.cell(row=1, column=8).value = '営業停止日数_100から200cm未満'
        ws.cell(row=1, column=9).value = '営業停止日数_200から300cm未満'
        ws.cell(row=1, column=10).value = '営業停止日数_300cm以上'

        ws.cell(row=1, column=11).value = '営業停滞日数_床下'
        ws.cell(row=1, column=12).value = '営業停滞日数_0から50cm未満'
        ws.cell(row=1, column=13).value = '営業停滞日数_50から100cm未満'
        ws.cell(row=1, column=14).value = '営業停滞日数_100から200cm未満'
        ws.cell(row=1, column=15).value = '営業停滞日数_200から300cm未満'
        ws.cell(row=1, column=16).value = 'cccccc'
        
        if office_cost_list:
            for i, office_cost in enumerate(office_cost_list):
                ws.cell(row=i+2, column=1).value = office_cost.office_cost_code
                ws.cell(row=i+2, column=2).value = office_cost.office_cost_year
                ws.cell(row=i+2, column=3).value = office_cost.begin_date
                ws.cell(row=i+2, column=4).value = office_cost.end_date
                
                ws.cell(row=i+2, column=5).value = office_cost.suspend_lv00
                ws.cell(row=i+2, column=6).value = office_cost.suspend_lv00_50
                ws.cell(row=i+2, column=7).value = office_cost.suspend_lv50_100
                ws.cell(row=i+2, column=8).value = office_cost.suspend_lv100_200
                ws.cell(row=i+2, column=9).value = office_cost.suspend_lv200_300
                ws.cell(row=i+2, column=10).value = office_cost.suspend_lv300

                ws.cell(row=i+2, column=11).value = office_cost.stagnate_lv00
                ws.cell(row=i+2, column=12).value = office_cost.stagnate_lv00_50
                ws.cell(row=i+2, column=13).value = office_cost.stagnate_lv50_100
                ws.cell(row=i+2, column=14).value = office_cost.stagnate_lv100_200
                ws.cell(row=i+2, column=15).value = office_cost.stagnate_lv200_300
                ws.cell(row=i+2, column=16).value = office_cost.stagnate_lv300
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.office_cost_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_cost.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_cost_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.office_cost_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：farmer_fisher_damage_view
### 108: 農漁家被害率
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def farmer_fisher_damage_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_damage_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_damage_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、農漁家被害率データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_view()関数 STEP 2/4.', 'INFO')
        farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.raw("""SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_view()関数 STEP 3/4.', 'INFO')
        template_file_path = 'static/template_farmer_fisher_damage.xlsx'
        download_file_path = 'static/download_farmer_fisher_damage.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '農漁家被害率'
        ws.cell(row=1, column=1).value = '農漁家被害率コード'
        ws.cell(row=1, column=2).value = '農漁家被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '償却資産被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '償却資産被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '償却資産被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '償却資産被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '償却資産被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '償却資産被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '償却資産被害率_土砂_床下'
        ws.cell(row=1, column=12).value = '償却資産被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '償却資産被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '償却資産被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '償却資産被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '償却資産被害率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '在庫資産被害率_浸水_床下'
        ws.cell(row=1, column=18).value = '在庫資産被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=19).value = '在庫資産被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=20).value = '在庫資産被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=21).value = '在庫資産被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=22).value = '在庫資産被害率_浸水_300cm以上'

        ws.cell(row=1, column=23).value = '在庫資産被害率_土砂_床下'
        ws.cell(row=1, column=24).value = '在庫資産被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=25).value = '在庫資産被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=26).value = '在庫資産被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=27).value = '在庫資産被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=28).value = '在庫資産被害率_土砂_300cm以上'

        ws.cell(row=1, column=29).value = '農漁家償却資産額'
        ws.cell(row=1, column=30).value = '農漁家在庫資産額'
        
        if farmer_fisher_damage_list:
            for i, farmer_fisher_damage in enumerate(farmer_fisher_damage_list):
                ws.cell(row=i+2, column=1).value = farmer_fisher_damage.farmer_fisher_damage_code
                ws.cell(row=i+2, column=2).value = farmer_fisher_damage.farmer_fisher_damage_year
                ws.cell(row=i+2, column=3).value = farmer_fisher_damage.begin_date
                ws.cell(row=i+2, column=4).value = farmer_fisher_damage.end_date
                
                ws.cell(row=i+2, column=5).value = farmer_fisher_damage.dep_fl_lv00
                ws.cell(row=i+2, column=6).value = farmer_fisher_damage.dep_fl_lv00_50
                ws.cell(row=i+2, column=7).value = farmer_fisher_damage.dep_fl_lv50_100
                ws.cell(row=i+2, column=8).value = farmer_fisher_damage.dep_fl_lv100_200
                ws.cell(row=i+2, column=9).value = farmer_fisher_damage.dep_fl_lv200_300
                ws.cell(row=i+2, column=10).value = farmer_fisher_damage.dep_fl_lv300

                ws.cell(row=i+2, column=11).value = farmer_fisher_damage.dep_sd_lv00
                ws.cell(row=i+2, column=12).value = farmer_fisher_damage.dep_sd_lv00_50
                ws.cell(row=i+2, column=13).value = farmer_fisher_damage.dep_sd_lv50_100
                ws.cell(row=i+2, column=14).value = farmer_fisher_damage.dep_sd_lv100_200
                ws.cell(row=i+2, column=15).value = farmer_fisher_damage.dep_sd_lv200_300
                ws.cell(row=i+2, column=16).value = farmer_fisher_damage.dep_sd_lv300
        
                ws.cell(row=i+2, column=17).value = farmer_fisher_damage.inv_fl_lv00
                ws.cell(row=i+2, column=18).value = farmer_fisher_damage.inv_fl_lv00_50
                ws.cell(row=i+2, column=19).value = farmer_fisher_damage.inv_fl_lv50_100
                ws.cell(row=i+2, column=20).value = farmer_fisher_damage.inv_fl_lv100_200
                ws.cell(row=i+2, column=21).value = farmer_fisher_damage.inv_fl_lv200_300
                ws.cell(row=i+2, column=22).value = farmer_fisher_damage.inv_fl_lv300

                ws.cell(row=i+2, column=23).value = farmer_fisher_damage.inv_sd_lv00
                ws.cell(row=i+2, column=24).value = farmer_fisher_damage.inv_sd_lv00_50
                ws.cell(row=i+2, column=25).value = farmer_fisher_damage.inv_sd_lv50_100
                ws.cell(row=i+2, column=26).value = farmer_fisher_damage.inv_sd_lv100_200
                ws.cell(row=i+2, column=27).value = farmer_fisher_damage.inv_sd_lv200_300
                ws.cell(row=i+2, column=28).value = farmer_fisher_damage.inv_sd_lv300

                ws.cell(row=i+2, column=29).value = farmer_fisher_damage.depreciable_asset
                ws.cell(row=i+2, column=30).value = farmer_fisher_damage.inventory_asset
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_view()関数 STEP 4/4.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.farmer_fisher_damage_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="farmer_fisher_damage.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_damage_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.farmer_fisher_damage_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：suigai_view
### 200 水害
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def suigai_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、水害データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.suigai_view()関数 STEP 2/4.', 'INFO')
        suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])
    
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
        ws.title = '水害'
        ws.cell(row=1, column=1).value = '水害ID'
        ws.cell(row=1, column=2).value = '水害名'
        ws.cell(row=1, column=3).value = '都道府県コード'
        ws.cell(row=1, column=4).value = '市区町村コード'
        ws.cell(row=1, column=5).value = '開始日'
        ws.cell(row=1, column=6).value = '終了日'
        ws.cell(row=1, column=7).value = '水害原因_1_コード'
        ws.cell(row=1, column=8).value = '水害原因_2_コード'
        ws.cell(row=1, column=9).value = '水害原因_3_コード'
        ws.cell(row=1, column=10).value = '区域ID'
        ws.cell(row=1, column=11).value = '水系コード'
        ws.cell(row=1, column=12).value = '河川コード'
        ws.cell(row=1, column=13).value = '地盤勾配区分コード'
        ws.cell(row=1, column=14).value = '宅地面積（単位m2）'
        ws.cell(row=1, column=15).value = '農地面積（単位m2）'
        ws.cell(row=1, column=16).value = '地下面積（単位m2）'
        ws.cell(row=1, column=17).value = '河川海岸（工種）コード'
        ws.cell(row=1, column=18).value = '農作物被害額（単位千円）'
        ws.cell(row=1, column=19).value = '異常気象ID'
        
        if suigai_list:
            for i, suigai in enumerate(suigai_list):
                ws.cell(row=i+2, column=1).value = suigai.suigai_id
                ws.cell(row=i+2, column=2).value = suigai.suigai_name
                ws.cell(row=i+2, column=3).value = suigai.ken_code
                ws.cell(row=i+2, column=4).value = suigai.city_code
                ws.cell(row=i+2, column=5).value = suigai.begin_date
                ws.cell(row=i+2, column=6).value = suigai.end_date
                ws.cell(row=i+2, column=7).value = suigai.cause_1_code
                ws.cell(row=i+2, column=8).value = suigai.cause_2_code
                ws.cell(row=i+2, column=9).value = suigai.cause_3_code
                ws.cell(row=i+2, column=10).value = suigai.area_id
                ws.cell(row=i+2, column=11).value = suigai.suikei_code
                ws.cell(row=i+2, column=12).value = suigai.kasen_code
                ws.cell(row=i+2, column=13).value = suigai.gradient_code
                ws.cell(row=i+2, column=14).value = suigai.residential_area
                ws.cell(row=i+2, column=15).value = suigai.agricultural_area
                ws.cell(row=i+2, column=16).value = suigai.underground_area
                ws.cell(row=i+2, column=17).value = suigai.kasen_kaigan_code
                ws.cell(row=i+2, column=18).value = suigai.crop_damage
                ws.cell(row=i+2, column=19).value = suigai.weather_id
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：weather_view
### 201: 異常気象
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def weather_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、異常気象データを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.weather_view()関数 STEP 2/4.', 'INFO')
        weather_list = WEATHER.objects.raw("""SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
    
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
        ws.title = '異常気象'
        ws.cell(row=1, column=1).value = '異常気象ID'
        ws.cell(row=1, column=2).value = '異常気象名'
        ws.cell(row=1, column=3).value = '異常気象対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        
        if weather_list:
            for i, weather in enumerate(weather_list):
                ws.cell(row=i+2, column=1).value = weather.weather_id
                ws.cell(row=i+2, column=2).value = weather.weather_name
                ws.cell(row=i+2, column=3).value = weather.weather_year
                ws.cell(row=i+2, column=4).value = weather.begin_date
                ws.cell(row=i+2, column=5).value = weather.end_date
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：area_view
### 202: 区域
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def area_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.area_view()関数 STEP 1/4.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、区域データを取得する。
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
        ws.title = '区域'
        ws.cell(row=1, column=1).value = '区域ID'
        ws.cell(row=1, column=2).value = '区域名'
        ws.cell(row=1, column=3).value = '区域対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        ws.cell(row=1, column=6).value = '農地面積'
        ws.cell(row=1, column=7).value = '地下面積'
        ws.cell(row=1, column=8).value = '農作物被害額'
        
        if area_list:
            for i, area in enumerate(area_list):
                ws.cell(row=i+2, column=1).value = area.area_id
                ws.cell(row=i+2, column=2).value = area.area_name
                ws.cell(row=i+2, column=3).value = area.area_year
                ws.cell(row=i+2, column=4).value = area.begin_date
                ws.cell(row=i+2, column=5).value = area.end_date
                ws.cell(row=i+2, column=6).value = area.agri_area
                ws.cell(row=i+2, column=7).value = area.underground_area
                ws.cell(row=i+2, column=8).value = area.crop_damage
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
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
### 関数名：ippan_chosa_view
### 203: 一般資産調査票（調査員用）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_chosa_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 lock = {}'.format(lock), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 1/9.', 'INFO')
        
        #######################################################################
        ### EXCEL入出力処理(0010)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 2/9.', 'INFO')
        template_file_path = 'static/template_ippan_chosa.xlsx'
        download_file_path = 'static/download_ippan_chosa.xlsx'
        wb = openpyxl.load_workbook(template_file_path, keep_vba=False)

        ws_building = wb["BUILDING"]
        ws_ken = wb["KEN"]
        ws_city = wb["CITY"]
        ws_kasen_kaigan = wb["KASEN_KAIGAN"]
        ws_suikei = wb["SUIKEI"]
        ws_suikei_type = wb["SUIKEI_TYPE"]
        ws_kasen = wb["KASEN"]
        ws_kasen_type = wb["KASEN_TYPE"]
        ws_cause = wb["CAUSE"]
        ws_underground = wb["UNDERGROUND"]
        ws_usage = wb["USAGE"]
        ws_flood_sediment = wb["FLOOD_SEDIMENT"]
        ws_gradient = wb["GRADIENT"]
        ws_industry = wb["INDUSTRY"]
        ws_suigai = wb["SUIGAI"]
        ws_weather = wb["WEATHER"]
        ws_area = wb["AREA"]
        ws_ippan = wb["IPPAN"]
        ws_city_vlook = wb["CITY_VLOOK"]
        ws_kasen_vlook = wb["KASEN_VLOOK"]

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
        ### EXCEL入出力処理(0020)
        ### (1)DBから建物区分等のマスタデータを取得する。
        ### (2)EXCELのマスタ用のシートのセルに、DBから取得した建物区分等のマスタデータを埋め込む。
        ### (3)EXCELのVLOKUP用のシートのセルに、DBから取得した都道府県等のマスタデータを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 3/9.', 'INFO')
        ### 01: 建物区分
        print("ippan_chosa_view2", flush=True)
        building_list = BUILDING.objects.raw("""SELECT * FROM BUILDING ORDER BY CAST(BUILDING_CODE AS INTEGER)""", [])
        if building_list:
            for i, building in enumerate(building_list):
                ws_building.cell(row=i+1, column=1).value = building.building_code
                ws_building.cell(row=i+1, column=2).value = str(building.building_name) + ":" + str(building.building_code)

        ### 02: 都道府県
        print("ippan_chosa_view3", flush=True)
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws_ken.cell(row=i+1, column=1).value = ken.ken_code
                ws_ken.cell(row=i+1, column=2).value = str(ken.ken_name) + ":" + str(ken.ken_code)
                
                ws_city_vlook.cell(row=i+1, column=1).value = str(ken.ken_name) + ":" + str(ken.ken_code)
        
        ### 03: 市区町村
        print("ippan_chosa_view4_1", flush=True)
        city_list = []
        if ken_list:
            for i, ken in enumerate(ken_list):
                city_list.append(CITY.objects.raw("""SELECT * FROM CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)""", [ken.ken_code, ]))
        
        print("ippan_chosa_view4_2", flush=True)
        if city_list:
            for i, city in enumerate(city_list):
                ws_city_vlook.cell(row=i+1, column=2).value = 'CITY!$' + VLOOK_VALUE[i] + '$1:$' + VLOOK_VALUE[i] + '$%d' % len(city)

        print("ippan_chosa_view4_3", flush=True)
        if city_list:
            for i, city in enumerate(city_list):
                if city:
                    for j, c in enumerate(city):
                        ws_city.cell(row=j+1, column=i*5+1).value = c.city_code
                        ws_city.cell(row=j+1, column=i*5+2).value = str(c.city_name) + ":" + str(c.city_code)
                        ws_city.cell(row=j+1, column=i*5+3).value = c.ken_code
                        ws_city.cell(row=j+1, column=i*5+4).value = c.city_population
                        ws_city.cell(row=j+1, column=i*5+5).value = c.city_area

        ### 04: 水害発生地点工種（河川海岸区分）
        print("ippan_chosa_view5", flush=True)
        kasen_kaigan_list = KASEN_KAIGAN.objects.raw("""SELECT * FROM KASEN_KAIGAN ORDER BY CAST(KASEN_KAIGAN_CODE AS INTEGER)""", [])
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws_kasen_kaigan.cell(row=i+1, column=1).value = kasen_kaigan.kasen_kaigan_code
                ws_kasen_kaigan.cell(row=i+1, column=2).value = kasen_kaigan.kasen_kaigan_name + ":" + kasen_kaigan.kasen_kaigan_code

        ### 05: 水系（水系・沿岸）
        print("ippan_chosa_view6", flush=True)
        suikei_list = SUIKEI.objects.raw("""SELECT * FROM SUIKEI ORDER BY CAST(SUIKEI_CODE AS INTEGER)""", [])
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws_suikei.cell(row=i+1, column=1).value = suikei.suikei_code
                ws_suikei.cell(row=i+1, column=2).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)
                ws_suikei.cell(row=i+1, column=3).value = suikei.suikei_type_code

                ws_kasen_vlook.cell(row=i+1, column=1).value = str(suikei.suikei_name) + ":" + str(suikei.suikei_code)

        ### 06: 水系種別（水系・沿岸種別）
        print("ippan_chosa_view7", flush=True)
        suikei_type_list = SUIKEI_TYPE.objects.raw("""SELECT * FROM SUIKEI_TYPE ORDER BY CAST(SUIKEI_TYPE_CODE AS INTEGER)""", [])
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws_suikei_type.cell(row=i+1, column=1).value = suikei_type.suikei_type_code
                ws_suikei_type.cell(row=i+1, column=2).value = str(suikei_type.suikei_type_name) + ":" + str(suikei_type.suikei_type_code)

        ### 07: 河川（河川・海岸）
        print("ippan_chosa_view8_1", flush=True)
        kasen_list = []
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                kasen_list.append(KASEN.objects.raw("""SELECT * FROM KASEN WHERE SUIKEI_CODE=%s ORDER BY CAST(KASEN_CODE AS INTEGER)""", [suikei.suikei_code, ]))

        print("ippan_chosa_view8_2", flush=True)
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws_kasen_vlook.cell(row=i+1, column=2).value = 'KASEN!$' + VLOOK_VALUE[i] + '$1:$' + VLOOK_VALUE[i] + '$%d' % len(kasen)
                
        print("ippan_chosa_view8_3", flush=True)
        ### kasen_list = KASEN.objects.raw("""SELECT * FROM KASEN ORDER BY CAST(KASEN_CODE AS INTEGER)""", [])
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                if kasen:
                    for j, k in enumerate(kasen):
                        ws_kasen.cell(row=j+1, column=i*5+1).value = k.kasen_code
                        ws_kasen.cell(row=j+1, column=i*5+2).value = str(k.kasen_name) + ":" + str(k.kasen_code)
                        ws_kasen.cell(row=j+1, column=i*5+3).value = k.kasen_type_code
                        ws_kasen.cell(row=j+1, column=i*5+4).value = k.suikei_code
                
        ### 08: 河川種別（河川・海岸種別）
        print("ippan_chosa_view9", flush=True)
        kasen_type_list = KASEN_TYPE.objects.raw("""SELECT * FROM KASEN_TYPE ORDER BY CAST(KASEN_TYPE_CODE AS INTEGER)""", [])
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws_kasen_type.cell(row=i+1, column=1).value = kasen_type.kasen_type_code
                ws_kasen_type.cell(row=i+1, column=2).value = str(kasen_type.kasen_type_name) + ":" + str(kasen_type.kasen_type_code)
        
        ### 09: 水害原因
        print("ippan_chosa_view10", flush=True)
        cause_list = CAUSE.objects.raw("""SELECT * FROM CAUSE ORDER BY CAST(CAUSE_CODE AS INTEGER)""", [])
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws_cause.cell(row=i+1, column=1).value = cause.cause_code
                ws_cause.cell(row=i+1, column=2).value = str(cause.cause_name) + ":" + str(cause.cause_code)
                
        ### 10: 地上地下区分
        print("ippan_chosa_view11", flush=True)
        underground_list = UNDERGROUND.objects.raw("""SELECT * FROM UNDERGROUND ORDER BY CAST(UNDERGROUND_CODE AS INTEGER)""", [])
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws_underground.cell(row=i+1, column=1).value = underground.underground_code
                ws_underground.cell(row=i+1, column=2).value = str(underground.underground_name) + ":" + str(underground.underground_code)
        
        ### 11: 地下空間の利用形態
        print("ippan_chosa_view12", flush=True)
        usage_list = USAGE.objects.raw("""SELECT * FROM USAGE ORDER BY CAST(USAGE_CODE AS INTEGER)""", [])
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws_usage.cell(row=i+1, column=1).value = usage.usage_code
                ws_usage.cell(row=i+1, column=2).value = str(usage.usage_name) + ":" + str(usage.usage_code)
        
        ### 12: 浸水土砂区分
        print("ippan_chosa_view13", flush=True)
        flood_sediment_list = FLOOD_SEDIMENT.objects.raw("""SELECT * FROM FLOOD_SEDIMENT ORDER BY CAST(FLOOD_SEDIMENT_CODE AS INTEGER)""", [])
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws_flood_sediment.cell(row=i+1, column=1).value = flood_sediment.flood_sediment_code
                ws_flood_sediment.cell(row=i+1, column=2).value = str(flood_sediment.flood_sediment_name) + ":" + str(flood_sediment.flood_sediment_code)
        
        ### 13: 地盤勾配区分
        print("ippan_chosa_view14", flush=True)
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws_gradient.cell(row=i+1, column=1).value = gradient.gradient_code
                ws_gradient.cell(row=i+1, column=2).value = str(gradient.gradient_name) + ":" + str(gradient.gradient_code)
        
        ### 14: 産業分類
        print("ippan_chosa_view15", flush=True)
        industry_list = INDUSTRY.objects.raw("""SELECT * FROM INDUSTRY ORDER BY CAST(INDUSTRY_CODE AS INTEGER)""", [])
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws_industry.cell(row=i+1, column=1).value = industry.industry_code
                ws_industry.cell(row=i+1, column=2).value = str(industry.industry_name) + ":" + str(industry.industry_code)
        
        ### 200: 水害
        print("ippan_chosa_view16", flush=True)
        suigai_list = SUIGAI.objects.raw("""SELECT * FROM SUIGAI ORDER BY CAST(SUIGAI_ID AS INTEGER)""", [])
        if suigai_list:
            for i, suigai in enumerate(suigai_list):
                ws_suigai.cell(row=i+1, column=1).value = suigai.suigai_id
                ws_suigai.cell(row=i+1, column=2).value = str(suigai.suigai_name) + ":" + str(suigai.suigai_id)
                ws_suigai.cell(row=i+1, column=3).value = suigai.ken_code
                ws_suigai.cell(row=i+1, column=4).value = suigai.city_code
                ws_suigai.cell(row=i+1, column=5).value = suigai.begin_date
                ws_suigai.cell(row=i+1, column=6).value = suigai.end_date
                ws_suigai.cell(row=i+1, column=7).value = suigai.cause_1_code
                ws_suigai.cell(row=i+1, column=8).value = suigai.cause_2_code
                ws_suigai.cell(row=i+1, column=9).value = suigai.cause_3_code
                ws_suigai.cell(row=i+1, column=10).value = suigai.area_id
                ws_suigai.cell(row=i+1, column=11).value = suigai.suikei_code
                ws_suigai.cell(row=i+1, column=12).value = suigai.kasen_code
                ws_suigai.cell(row=i+1, column=13).value = suigai.gradient_code
                ws_suigai.cell(row=i+1, column=14).value = suigai.residential_area
                ws_suigai.cell(row=i+1, column=15).value = suigai.agricultural_area
                ws_suigai.cell(row=i+1, column=16).value = suigai.underground_area
                ws_suigai.cell(row=i+1, column=17).value = suigai.kasen_kaigan_code
                ws_suigai.cell(row=i+1, column=18).value = suigai.crop_damage
                ws_suigai.cell(row=i+1, column=19).value = suigai.weather_id

        ### 201: 異常気象
        print("ippan_chosa_view17", flush=True)
        weather_list = WEATHER.objects.raw("""SELECT * FROM WEATHER ORDER BY CAST(WEATHER_ID AS INTEGER)""", [])
        if weather_list:
            for i, weather in enumerate(weather_list):
                ws_weather.cell(row=i+1, column=1).value = weather.weather_id
                ws_weather.cell(row=i+1, column=2).value = str(weather.weather_name) + ":" + str(weather.weather_id)

        ### 202: 区域
        print("ippan_chosa_view18", flush=True)
        area_list = AREA.objects.raw("""SELECT * FROM AREA ORDER BY CAST(AREA_ID AS INTEGER)""", [])
        if area_list:
            for i, area in enumerate(area_list):
                ws_area.cell(row=i+1, column=1).value = area.area_id
                ws_area.cell(row=i+1, column=2).value = str(area.area_name) + ":" + str(area.area_id)
        
        #######################################################################
        ### DBアクセス処理(0030)
        ### (1)DBから水害のデータを取得する。
        ### (2)DBから一般資産調査票（調査員）のデータを取得する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 4/9.', 'INFO')
        ### 200: 水害
        print("ippan_chosa_view19_1", flush=True)
        suigai_list = SUIGAI.objects.raw("""
            SELECT 
            SU1.suigai_id AS suigai_id,
            SU1.suigai_name AS suigai_name,
            SU1.ken_code AS ken_code, 
            KE1.ken_name AS ken_name,
            SU1.city_code AS city_code,
            CI1.city_name AS city_name,
            SU1.begin_date AS begin_date,
            SU1.end_date AS end_date,
            SU1.cause_1_code AS cause_1_code,
            CA1.cause_name AS cause_1_name,
            SU1.cause_2_code AS cause_2_code,
            CA2.cause_name AS cause_2_name,
            SU1.cause_3_code AS cause_3_code,
            CA3.cause_name AS cause_3_name,
            SU1.area_id AS area_id,
            AR1.area_name AS area_name,
            SU1.suikei_code AS suikei_code,
            SK1.suikei_name AS suikei_name,
            M1.suikei_type_code AS suikei_type_code,
            M1.suikei_type_name AS suikei_type_name,
            SU1.kasen_code AS kasen_code,
            KA1.kasen_name AS kasen_name,
            M2.kasen_type_code AS kasen_type_code,
            M2.kasen_type_name AS kasen_type_name,
            SU1.gradient_code AS gradient_code,
            GR1.gradient_name AS gradient_name,
            SU1.residential_area AS residential_area,
            SU1.agricultural_area AS agricultural_area,
            SU1.underground_area AS underground_area,
            SU1.kasen_kaigan_code AS kasen_kaigan_code,
            KK1.kasen_kaigan_name AS kasen_kaigan_name,
            SU1.crop_damage AS crop_damage,
            SU1.weather_id AS weather_id,
            WE1.weather_name as weather_name
            FROM SUIGAI SU1 
            LEFT JOIN KEN KE1 ON SU1.ken_code = KE1.ken_code 
            LEFT JOIN CITY CI1 ON SU1.city_code = CI1.city_code 
            LEFT JOIN CAUSE CA1 ON SU1.cause_1_code = CA1.cause_code 
            LEFT JOIN CAUSE CA2 ON SU1.cause_2_code = CA2.cause_code 
            LEFT JOIN CAUSE CA3 ON SU1.cause_3_code = CA3.cause_code 
            LEFT JOIN AREA AR1 ON SU1.area_id = AR1.area_id 
            LEFT JOIN SUIKEI SK1 ON SU1.suikei_code = SK1.suikei_code 
            LEFT JOIN (
                SELECT 
                MU1.suikei_code AS suikei_code,
                MT1.suikei_type_code AS suikei_type_code,
                MT1.suikei_type_name As suikei_type_name 
                FROM SUIKEI MU1 
                LEFT JOIN SUIKEI_TYPE MT1 ON MU1.suikei_type_code = MT1.suikei_type_code
            ) M1 ON SU1.suikei_code = M1.suikei_code 
            LEFT JOIN KASEN KA1 ON SU1.kasen_code = KA1.kasen_code 
            LEFT JOIN (
                SELECT 
                MA2.kasen_code AS kasen_code, 
                MT2.kasen_type_code AS kasen_type_code, 
                MT2.kasen_type_name AS kasen_type_name 
                FROM KASEN MA2 
                LEFT JOIN KASEN_TYPE MT2 ON MA2.kasen_type_code = MT2.kasen_type_code
            ) M2 ON SU1.kasen_code = M2.kasen_code 
            LEFT JOIN GRADIENT GR1 ON SU1.gradient_code = GR1.gradient_code 
            LEFT JOIN KASEN_KAIGAN KK1 ON SU1.kasen_kaigan_code = KK1.kasen_kaigan_code 
            LEFT JOIN WEATHER WE1 ON SU1.weather_id = WE1.weather_id 
            ORDER BY CAST (SU1.SUIGAI_ID AS INTEGER)            
            """, [])

        print("ippan_chosa_view19_2", flush=True)
        ippan_list = IPPAN.objects.raw("""
            SELECT 
            IP1.ippan_id AS ippan_id,
            IP1.ippan_name AS ippan_name,
            IP1.building_code AS building_code,
            BU1.building_name AS building_Name,
            IP1.underground_code AS underground_code,
            UN1.underground_name AS underground_name,
            IP1.flood_sediment_code AS flood_sediment_code,
            FL1.flood_sediment_name AS flood_sediment_name,
            IP1.building_lv00 AS building_lv00,
            IP1.building_lv01_49 AS building_lv01_49,
            IP1.building_lv50_99 AS building_lv50_99,
            IP1.building_lv100 AS building_lv100,
            IP1.building_half AS building_half,
            IP1.building_full AS building_full,
            IP1.floor_area AS floor_area,
            IP1.family AS family,
            IP1.office AS office,
            IP1.floor_area_lv00 AS floor_area_lv00,
            IP1.floor_area_lv01_49 AS floor_area_lv01_49,
            IP1.floor_area_lv50_99 AS floor_area_lv50_99,
            IP1.floor_area_lv100 AS floor_area_lv100,
            IP1.floor_area_half AS floor_area_half,
            IP1.floor_area_full AS floor_area_full,
            IP1.family_lv00 AS family_lv00,
            IP1.family_lv01_49 AS family_lv01_49,
            IP1.family_lv50_99 AS family_lv50_99,
            IP1.family_lv100 AS family_lv100,
            IP1.family_half AS family_half,
            IP1.family_full AS family_full,
            IP1.office_lv00 AS office_lv00,
            IP1.office_lv01_49 AS office_lv01_49,
            IP1.office_lv50_99 AS office_lv50_99,
            IP1.office_lv100 AS office_lv100,
            IP1.office_half AS office_half,
            IP1.office_full AS office_full,
            IP1.farmer_fisher_lv00 AS farmer_fisher_lv00,
            IP1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49,
            IP1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99,
            IP1.farmer_fisher_lv100 AS farmer_fisher_lv100,
            IP1.farmer_fisher_full AS farmer_fisher_full,
            IP1.employee_lv00 AS employee_lv00,
            IP1.employee_lv01_49 AS employee_lv01_49,
            IP1.employee_lv50_99 AS employee_lv50_99,
            IP1.employee_lv100 AS employee_lv100,
            IP1.employee_full AS employee_full,
            IP1.industry_code AS industry_code,
            IN1.industry_name AS industry_name,
            IP1.usage_code as usage_code,
            US1.usage_name as usage_name,
            IP1.comment as comment 
            FROM IPPAN IP1 
            LEFT JOIN BUILDING BU1 ON IP1.building_code = BU1.building_code 
            LEFT JOIN UNDERGROUND UN1 ON IP1.underground_code = UN1.underground_code 
            LEFT JOIN FLOOD_SEDIMENT FL1 ON IP1.flood_sediment_code = FL1.flood_sediment_code 
            LEFT JOIN INDUSTRY IN1 ON IP1.industry_code = IN1.industry_code 
            LEFT JOIN USAGE US1 ON IP1.usage_code = US1.usage_code 
            ORDER BY CAST (IP1.IPPAN_ID AS INTEGER)            
            """, [])
            
        #######################################################################
        ### EXCEL入出力処理(0040)
        ### (1)EXCELのヘッダ部のセルに、キャプションのテキストを埋め込む。
        ### (2)EXCELの一覧部のセルに、キャプションのテキストを埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 5/9.', 'INFO')
        print("ippan_chosa_view20_1", flush=True)
        ws_ippan.cell(row=5, column=2).value = '都道府県'
        ws_ippan.cell(row=5, column=3).value = '市区町村'
        ws_ippan.cell(row=5, column=4).value = '水害発生年月日'
        ws_ippan.cell(row=5, column=5).value = '水害終了年月日'
        ws_ippan.cell(row=5, column=6).value = '水害原因'
        ws_ippan.cell(row=5, column=9).value = '水害区域番号'
        ws_ippan.cell(row=6, column=6).value = '1'
        ws_ippan.cell(row=6, column=7).value = '2'
        ws_ippan.cell(row=6, column=8).value = '3'
        ws_ippan.cell(row=9, column=2).value = '水系・沿岸名'
        ws_ippan.cell(row=9, column=3).value = '水系種別'
        ws_ippan.cell(row=9, column=4).value = '河川・海岸名'
        ws_ippan.cell(row=9, column=5).value = '河川種別'
        ws_ippan.cell(row=9, column=6).value = '地盤勾配区分※1'
        
        print("ippan_chosa_view20_2", flush=True)
        ws_ippan.cell(row=12, column=2).value = '水害区域面積（m2）'
        ws_ippan.cell(row=12, column=6).value = '工種'
        ws_ippan.cell(row=12, column=8).value = '農作物被害額（千円）'
        ws_ippan.cell(row=12, column=10).value = '異常気象コード'
        ws_ippan.cell(row=16, column=2).value = '町丁名・大字名'
        ws_ippan.cell(row=16, column=3).value = '名称'
        ws_ippan.cell(row=16, column=4).value = '地上・地下被害の区分※2'
        ws_ippan.cell(row=16, column=5).value = '浸水土砂被害の区分※3'
        ws_ippan.cell(row=16, column=6).value = '被害建物棟数'
        ws_ippan.cell(row=16, column=12).value = '被害建物の延床面積（m2）'
        ws_ippan.cell(row=16, column=13).value = '被災世帯数'
        ws_ippan.cell(row=16, column=14).value = '被災事業所数'
        ws_ippan.cell(row=16, column=15).value = '被害建物内での農業家又は事業所活動'
        ws_ippan.cell(row=16, column=25).value = '事業所の産業区分※7'
        ws_ippan.cell(row=16, column=26).value = '地下空間の利用形態※8'
        ws_ippan.cell(row=16, column=27).value = '備考'
        ws_ippan.cell(row=17, column=7).value = '床上浸水・土砂堆積・地下浸水'
        ws_ippan.cell(row=17, column=15).value = '農家・漁家戸数※5'
        ws_ippan.cell(row=17, column=20).value = '事業所従業者数※6'
        ws_ippan.cell(row=18, column=16).value = '床上浸水'
        ws_ippan.cell(row=18, column=21).value = '床上浸水'
        ws_ippan.cell(row=20, column=7).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=8).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=9).value = '1m以上'
        ws_ippan.cell(row=20, column=10).value = '半壊※4'
        ws_ippan.cell(row=20, column=11).value = '全壊・流失※4'
        ws_ippan.cell(row=20, column=16).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=17).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=18).value = '1m以上半壊'
        ws_ippan.cell(row=20, column=19).value = '全壊・流失'
        ws_ippan.cell(row=20, column=21).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=22).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=23).value = '1m以上半壊'
        ws_ippan.cell(row=20, column=24).value = '全壊・流失'

        #######################################################################
        ### EXCEL入出力処理(0050)
        ### (1)EXCELのヘッダ部のセルに、単純プルダウン、連動プルダウンの設定を埋め込む。
        ### (2)EXCELの一覧部のセルに、単純プルダウンの設定を埋め込む。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 6/9.', 'INFO')
        ### 01: 建物区分
        print("ippan_chosa_view21", flush=True)
        dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$%d" % len(building_list))
        dv_building.ranges = 'C20:C1048576'
        ws_ippan.add_data_validation(dv_building)

        ### 02: 都道府県
        print("ippan_chosa_view22", flush=True)
        dv_ken = DataValidation(type="list", formula1="KEN!$B$1:$B$%d" % len(ken_list))
        dv_ken.ranges = 'B7:B7'
        ws_ippan.add_data_validation(dv_ken)
        
        ### 03: 市区町村
        print("ippan_chosa_view23", flush=True)
        ### ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK.A:B,2,0)" ### FOR LINUX?
        ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK!A:B,2,0)" ### FOR WINDOWS
        dv_city = DataValidation(type="list", formula1="=INDIRECT(AD3)")
        dv_city.ranges = 'C7:C7'
        ws_ippan.add_data_validation(dv_city)
        
        ### 04: 水害発生地点工種（河川海岸区分）
        print("ippan_chosa_view24", flush=True)
        dv_kasen_kaigan = DataValidation(type="list", formula1="KASEN_KAIGAN!$B$1:$B$%d" % len(kasen_kaigan_list))
        dv_kasen_kaigan.ranges = 'F14:F14'
        ws_ippan.add_data_validation(dv_kasen_kaigan)
        
        ### 05: 水系（水系・沿岸）
        print("ippan_chosa_view25", flush=True)
        dv_suikei = DataValidation(type="list", formula1="SUIKEI!$B$1:$B$%d" % len(suikei_list))
        dv_suikei.ranges = 'B10:B10'
        ws_ippan.add_data_validation(dv_suikei)
        
        ### 06: 水系種別（水系・沿岸種別）
        print("ippan_chosa_view26", flush=True)
        dv_suikei_type = DataValidation(type="list", formula1="SUIKEI_TYPE!$B$1:$B$%d" % len(suikei_type_list))
        dv_suikei_type.ranges = 'C10:C10'
        ws_ippan.add_data_validation(dv_suikei_type)
        
        ### 07: 河川（河川・海岸）
        print("ippan_chosa_view27", flush=True)
        ### ws_ippan.cell(row=4, column=30).value = "=VLOOKUP(B10,KASEN_VLOOK.A:B,2,0)" ### FOR LINUX?
        ws_ippan.cell(row=4, column=30).value = "=VLOOKUP(B10,KASEN_VLOOK!A:B,2,0)" ### FOR WINDOWS
        dv_kasen = DataValidation(type="list", formula1="=INDIRECT(AD4)")
        dv_kasen.ranges = 'D10:D10'
        ws_ippan.add_data_validation(dv_kasen)
        
        ### 08: 河川種別（河川・海岸種別）
        print("ippan_chosa_view28", flush=True)
        dv_kasen_type = DataValidation(type="list", formula1="KASEN_TYPE!$B$1:$B$%d" % len(kasen_type_list))
        dv_kasen_type.ranges = 'E10:E10'
        ws_ippan.add_data_validation(dv_kasen_type)
        
        ### 09: 水害原因
        print("ippan_chosa_view29", flush=True)
        dv_cause = DataValidation(type="list", formula1="CAUSE!$B$1:$B$%d" % len(cause_list))
        dv_cause.ranges = 'F7:H7'
        ws_ippan.add_data_validation(dv_cause)
        
        ### 10: 地上地下区分
        print("ippan_chosa_view30", flush=True)
        dv_underground = DataValidation(type="list", formula1="UNDERGROUND!$B$1:$B$%d" % len(underground_list))
        dv_underground.ranges = 'D20:D1048576'
        ws_ippan.add_data_validation(dv_underground)
        
        ### 11: 地下空間の利用形態
        print("ippan_chosa_view31", flush=True)
        dv_usage = DataValidation(type="list", formula1="USAGE!$B$1:$B$%d" % len(usage_list))
        dv_usage.ranges = 'Z20:Z1048576'
        ws_ippan.add_data_validation(dv_usage)
        
        ### 12: 浸水土砂区分
        print("ippan_chosa_view32", flush=True)
        dv_flood_sediment = DataValidation(type="list", formula1="FLOOD_SEDIMENT!$B$1:$B$%d" % len(flood_sediment_list))
        dv_flood_sediment.ranges = 'E20:E1048576'
        ws_ippan.add_data_validation(dv_flood_sediment)
        
        ### 13: 地盤勾配区分
        print("ippan_chosa_view33", flush=True)
        dv_gradient = DataValidation(type="list", formula1="GRADIENT!$B$1:$B$%d" % len(gradient_list))
        dv_gradient.ranges = 'F10:F10'
        ws_ippan.add_data_validation(dv_gradient)
        
        ### 14: 産業分類
        print("ippan_chosa_view34", flush=True)
        dv_industry = DataValidation(type="list", formula1="INDUSTRY!$B$1:$B$%d" % len(industry_list))
        dv_industry.ranges = 'Y20:Y1048576'
        ws_ippan.add_data_validation(dv_industry)
        
        ### 200: 水害
        print("ippan_chosa_view35", flush=True)
        
        ### 201: 異常気象
        print("ippan_chosa_view36", flush=True)
        dv_weather = DataValidation(type="list", formula1="WEATHER!$B$1:$B$%d" % len(weather_list))
        dv_weather.ranges = 'J14:J14'
        ws_ippan.add_data_validation(dv_weather)
        
        ### 202: 区域
        print("ippan_chosa_view37", flush=True)
        dv_area = DataValidation(type="list", formula1="AREA!$B$1:$B$%d" % len(area_list))
        dv_area.ranges = 'I7:I7'
        ws_ippan.add_data_validation(dv_area)
        
        #######################################################################
        ### EXCEL入出力処理(0060)
        ### (1)EXCELのヘッダ部のセルに、DBから取得した水害の値を埋め込む。
        ### (2)EXCELの一覧部のセルに、DBから取得した一般資産調査票（調査員）の値を埋め込む。
        ### TO-DO: 各IPPANデータは異なる県名、県コード、水系名、水系コード、発生日などを取り得る。
        ### TO-DO: IPPANデータの県名、県コード、水系名、水系コード、発生日などが異なる場合、この帳票フォーマットでは1シートでは表現できない。
        ### TO-DO: IPPANデータの県名、県コード、水系名、水系コード、発生日などが異なる場合、GROUP BYして、シート、EXCELファイルを分ける必要がある。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 7/9.', 'INFO')
        print("ippan_chosa_view38_1", flush=True)
        ws_ippan.cell(row=7, column=2).value = str(suigai_list[0].ken_name) + ":" + str(suigai_list[0].ken_code)
        ws_ippan.cell(row=7, column=3).value = str(suigai_list[0].city_name) + ":" + str(suigai_list[0].city_code)
        ws_ippan.cell(row=7, column=4).value = str(suigai_list[0].begin_date)
        ws_ippan.cell(row=7, column=5).value = str(suigai_list[0].end_date)
        ws_ippan.cell(row=7, column=6).value = str(suigai_list[0].cause_1_name) + ":" + str(suigai_list[0].cause_1_code)
        ws_ippan.cell(row=7, column=7).value = str(suigai_list[0].cause_2_name) + ":" + str(suigai_list[0].cause_2_code)
        ws_ippan.cell(row=7, column=8).value = str(suigai_list[0].cause_3_name) + ":" + str(suigai_list[0].cause_3_code)
        ws_ippan.cell(row=7, column=9).value = str(suigai_list[0].area_name) + ":" + str(suigai_list[0].area_id)
        
        ws_ippan.cell(row=10, column=2).value = str(suigai_list[0].suikei_name) + ":" + str(suigai_list[0].suikei_code)
        ws_ippan.cell(row=10, column=3).value = str(suigai_list[0].suikei_type_name) + ":" + str(suigai_list[0].suikei_type_code)
        ws_ippan.cell(row=10, column=4).value = str(suigai_list[0].kasen_name) + ":" + str(suigai_list[0].kasen_code)
        ws_ippan.cell(row=10, column=5).value = str(suigai_list[0].kasen_type_name) + ":" + str(suigai_list[0].kasen_type_code)
        ws_ippan.cell(row=10, column=6).value = str(suigai_list[0].gradient_name) + ":" + str(suigai_list[0].gradient_code)
        
        ws_ippan.cell(row=14, column=2).value = str(suigai_list[0].residential_area)
        ws_ippan.cell(row=14, column=3).value = str(suigai_list[0].agricultural_area)
        ws_ippan.cell(row=14, column=4).value = str(suigai_list[0].underground_area)
        ws_ippan.cell(row=14, column=6).value = str(suigai_list[0].kasen_kaigan_name) + ":" + str(suigai_list[0].kasen_kaigan_code)
        ws_ippan.cell(row=14, column=8).value = str(suigai_list[0].crop_damage)
        ws_ippan.cell(row=14, column=10).value = str(suigai_list[0].weather_name) + ":" + str(suigai_list[0].weather_id)

        print("ippan_chosa_view38_2", flush=True)
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws_ippan.cell(row=i+20, column=2).value = ippan.ippan_name
                ws_ippan.cell(row=i+20, column=3).value = str(ippan.building_name) + ":" + str(ippan.building_code) ### '戸建住宅'
                ws_ippan.cell(row=i+20, column=4).value = str(ippan.underground_name) + ":" + str(ippan.underground_code) ### '地上のみ'
                ws_ippan.cell(row=i+20, column=5).value = str(ippan.flood_sediment_name) + ":" + str(ippan.flood_sediment_code) ### '浸水'
                ws_ippan.cell(row=i+20, column=6).value = ippan.building_lv00
                ws_ippan.cell(row=i+20, column=7).value = ippan.building_lv01_49
                ws_ippan.cell(row=i+20, column=8).value = ippan.building_lv50_99
                ws_ippan.cell(row=i+20, column=9).value = ippan.building_lv100
                ws_ippan.cell(row=i+20, column=10).value = ippan.building_half
                ws_ippan.cell(row=i+20, column=11).value = ippan.building_full
                ws_ippan.cell(row=i+20, column=12).value = ippan.floor_area
                ws_ippan.cell(row=i+20, column=13).value = ippan.family
                ws_ippan.cell(row=i+20, column=14).value = ippan.office
                ws_ippan.cell(row=i+20, column=15).value = ippan.farmer_fisher_lv00
                ws_ippan.cell(row=i+20, column=16).value = ippan.farmer_fisher_lv01_49
                ws_ippan.cell(row=i+20, column=17).value = ippan.farmer_fisher_lv50_99
                ws_ippan.cell(row=i+20, column=18).value = ippan.farmer_fisher_lv100
                ws_ippan.cell(row=i+20, column=19).value = ippan.farmer_fisher_full
                ws_ippan.cell(row=i+20, column=20).value = ippan.employee_lv00
                ws_ippan.cell(row=i+20, column=21).value = ippan.employee_lv01_49
                ws_ippan.cell(row=i+20, column=22).value = ippan.employee_lv50_99
                ws_ippan.cell(row=i+20, column=23).value = ippan.employee_lv100
                ws_ippan.cell(row=i+20, column=24).value = ippan.employee_full
                ws_ippan.cell(row=i+20, column=25).value = str(ippan.industry_name) + ":" + str(ippan.industry_code) ### '建設業'
                ws_ippan.cell(row=i+20, column=26).value = str(ippan.usage_name) + ":" + str(ippan.usage_code) ### '住居'
                ws_ippan.cell(row=i+20, column=27).value = ippan.comment
        
        #######################################################################
        ### EXCEL入出力処理(0070)
        ### (1)EXCELのセルに、建物区分に応じて、背景灰色、背景白色を変化させる条件付き形式を埋め込む。
        ### (2)ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 8/9.', 'INFO')
        print("ippan_chosa_view39_1", flush=True)
        gray_fill = PatternFill(bgColor='C0C0C0', fill_type='solid')
        white_fill = PatternFill(bgColor='FFFFFF', fill_type='solid')
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="戸建住宅:1"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="共同住宅:2"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="事業所併用住宅:3"'], fill=white_fill))
        ws_ippan.conditional_formatting.add('M20:M1048576', FormulaRule(formula=['$C20="事業所:4"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('M20:N1048576', FormulaRule(formula=['$C20="その他建物:5"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('T20:Y1048576', FormulaRule(formula=['$C20="その他建物:5"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('F20:Z1048576', FormulaRule(formula=['$C20="建物以外:6"'], fill=gray_fill))

        print("ippan_chosa_view39_2", flush=True)
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0080)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数 STEP 9/9.', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_chosa_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_chosa_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_city_view
### 204: 一般資産調査票（市区町村用）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_city_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数 lock = {}'.format(lock), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ippan_list = IPPAN.objects.raw("""SELECT * FROM IPPAN ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        template_file_path = 'static/template_ippan_city.xlsx'
        download_file_path = 'static/download_ippan_city.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '一般資産調査票'
        ws.cell(row=1, column=1).value = '一般資産調査票ID'
        ws.cell(row=1, column=2).value = '一般資産調査票名'
        
        ws.cell(row=1, column=3).value = '建物区分コード'
        
        ws.cell(row=1, column=4).value = '浸水土砂区分コード'
        ws.cell(row=1, column=5).value = '地盤勾配区分コード'
        ws.cell(row=1, column=6).value = '産業分類コード'
        
        ws.cell(row=1, column=7).value = '都道府県コード'
        ws.cell(row=1, column=8).value = '市区町村コード'
        ws.cell(row=1, column=9).value = '異常気象ID'
        ws.cell(row=1, column=10).value = '区域ID'
        ws.cell(row=1, column=11).value = '水害原因_1_コード'
        ws.cell(row=1, column=12).value = '水害原因_2_コード'
        ws.cell(row=1, column=13).value = '水害原因_3_コード'
        
        ws.cell(row=1, column=14).value = '水系コード'
        ws.cell(row=1, column=15).value = '河川コード'
        ws.cell(row=1, column=16).value = '河川海岸コード'

        ws.cell(row=1, column=17).value = '地上地下区分コード'
        ws.cell(row=1, column=18).value = '地下空間の利用形態コード'
        
        ws.cell(row=1, column=19).value = '被害建物棟数_床下'
        ws.cell(row=1, column=20).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=21).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=22).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=23).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=24).value = '被害建物棟数_全壊'

        ws.cell(row=1, column=25).value = '延床面積'
        ws.cell(row=1, column=26).value = '被災世帯数'
        ws.cell(row=1, column=27).value = '被災事業所数'
        
        ws.cell(row=1, column=28).value = '延床面積_床下'
        ws.cell(row=1, column=29).value = '延床面積_01から49cm'
        ws.cell(row=1, column=30).value = '延床面積_50から99cm'
        ws.cell(row=1, column=31).value = '延床面積_100cm以上'
        ws.cell(row=1, column=32).value = '延床面積_半壊'
        ws.cell(row=1, column=33).value = '延床面積_全壊'
        
        ws.cell(row=1, column=34).value = '被災世帯数_床下'
        ws.cell(row=1, column=35).value = '被災世帯数_01から49cm'
        ws.cell(row=1, column=36).value = '被災世帯数_50から99cm'
        ws.cell(row=1, column=37).value = '被災世帯数_100cm以上'
        ws.cell(row=1, column=38).value = '被災世帯数_半壊'
        ws.cell(row=1, column=39).value = '被災世帯数_全壊'

        ws.cell(row=1, column=40).value = '被災事業所数_床下'
        ws.cell(row=1, column=41).value = '被災事業所数_01から49cm'
        ws.cell(row=1, column=42).value = '被災事業所数_50から99cm'
        ws.cell(row=1, column=43).value = '被災事業所数_100cm以上'
        ws.cell(row=1, column=44).value = '被災事業所数_半壊'
        ws.cell(row=1, column=45).value = '被災事業所数_全壊'

        ws.cell(row=1, column=46).value = '被災従業者数_床下'
        ws.cell(row=1, column=47).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=48).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=49).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=50).value = '被災従業者数_全壊'

        ws.cell(row=1, column=51).value = '農漁家戸数_床下'
        ws.cell(row=1, column=52).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=53).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=54).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=55).value = '農漁家戸数_全壊'
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws.cell(row=i+2, column=1).value = ippan.ippan_id
                ws.cell(row=i+2, column=2).value = ippan.ippan_name
                
                ws.cell(row=i+2, column=3).value = ippan.building_code
                
                ws.cell(row=i+2, column=4).value = ippan.flood_sediment_code
                ws.cell(row=i+2, column=5).value = ippan.gradient_code
                ws.cell(row=i+2, column=6).value = ippan.industry_code
                
                ws.cell(row=i+2, column=7).value = ippan.ken_code
                ws.cell(row=i+2, column=8).value = ippan.city_code
                ws.cell(row=i+2, column=9).value = ippan.weather_id
                ws.cell(row=i+2, column=10).value = ippan.area_id
                ws.cell(row=i+2, column=11).value = ippan.cause_1_code
                ws.cell(row=i+2, column=12).value = ippan.cause_2_code
                ws.cell(row=i+2, column=13).value = ippan.cause_3_code
                
                ws.cell(row=i+2, column=14).value = ippan.suikei_code
                ws.cell(row=i+2, column=15).value = ippan.kasen_code
                ws.cell(row=i+2, column=16).value = ippan.kasen_kaigan_code

                ws.cell(row=i+2, column=17).value = ippan.underground_code
                ws.cell(row=i+2, column=18).value = ippan.usage_code
                
                ws.cell(row=i+2, column=19).value = ippan.building_lv00
                ws.cell(row=i+2, column=20).value = ippan.building_lv01_49
                ws.cell(row=i+2, column=21).value = ippan.building_lv50_99
                ws.cell(row=i+2, column=22).value = ippan.building_lv100
                ws.cell(row=i+2, column=23).value = ippan.building_half
                ws.cell(row=i+2, column=24).value = ippan.building_full

                ws.cell(row=i+2, column=25).value = ippan.floor_area
                ws.cell(row=i+2, column=26).value = ippan.family
                ws.cell(row=i+2, column=27).value = ippan.office
                
                ws.cell(row=i+2, column=28).value = ippan.floor_area_lv00
                ws.cell(row=i+2, column=29).value = ippan.floor_area_lv01_49
                ws.cell(row=i+2, column=30).value = ippan.floor_area_lv50_99
                ws.cell(row=i+2, column=31).value = ippan.floor_area_lv100
                ws.cell(row=i+2, column=32).value = ippan.floor_area_half
                ws.cell(row=i+2, column=33).value = ippan.floor_area_full
                
                ws.cell(row=i+2, column=34).value = ippan.family_lv00
                ws.cell(row=i+2, column=35).value = ippan.family_lv01_49
                ws.cell(row=i+2, column=36).value = ippan.family_lv50_99
                ws.cell(row=i+2, column=37).value = ippan.family_lv100
                ws.cell(row=i+2, column=38).value = ippan.family_half
                ws.cell(row=i+2, column=39).value = ippan.family_full

                ws.cell(row=i+2, column=40).value = ippan.office_lv00
                ws.cell(row=i+2, column=41).value = ippan.office_lv01_49
                ws.cell(row=i+2, column=42).value = ippan.office_lv50_99
                ws.cell(row=i+2, column=43).value = ippan.office_lv100
                ws.cell(row=i+2, column=44).value = ippan.office_half
                ws.cell(row=i+2, column=45).value = ippan.office_full

                ws.cell(row=i+2, column=46).value = ippan.employee_lv00
                ws.cell(row=i+2, column=47).value = ippan.employee_lv01_49
                ws.cell(row=i+2, column=48).value = ippan.employee_lv50_99
                ws.cell(row=i+2, column=49).value = ippan.employee_lv100
                ws.cell(row=i+2, column=50).value = ippan.employee_full
        
                ws.cell(row=i+2, column=51).value = ippan.farmer_fisher_lv00
                ws.cell(row=i+2, column=52).value = ippan.farmer_fisher_lv01_49
                ws.cell(row=i+2, column=53).value = ippan.farmer_fisher_lv50_99
                ws.cell(row=i+2, column=54).value = ippan.farmer_fisher_lv100
                ws.cell(row=i+2, column=55).value = ippan.farmer_fisher_full

        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_city_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_city.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ippan_ken_view
### 205: 一般資産調査票（都道府県用）
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def ippan_ken_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数 lock = {}'.format(lock), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ippan_list = IPPAN.objects.raw("""SELECT * FROM IPPAN ORDER BY CAST(IPPAN_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        template_file_path = 'static/template_ippan_ken.xlsx'
        download_file_path = 'static/download_ippan_ken.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '一般資産調査票'
        ws.cell(row=1, column=1).value = '一般資産調査票ID'
        ws.cell(row=1, column=2).value = '一般資産調査票名'
        
        ws.cell(row=1, column=3).value = '建物区分コード'
        
        ws.cell(row=1, column=4).value = '浸水土砂区分コード'
        ws.cell(row=1, column=5).value = '地盤勾配区分コード'
        ws.cell(row=1, column=6).value = '産業分類コード'
        
        ws.cell(row=1, column=7).value = '都道府県コード'
        ws.cell(row=1, column=8).value = '市区町村コード'
        ws.cell(row=1, column=9).value = '異常気象ID'
        ws.cell(row=1, column=10).value = '区域ID'
        ws.cell(row=1, column=11).value = '水害原因_1_コード'
        ws.cell(row=1, column=12).value = '水害原因_2_コード'
        ws.cell(row=1, column=13).value = '水害原因_3_コード'
        
        ws.cell(row=1, column=14).value = '水系コード'
        ws.cell(row=1, column=15).value = '河川コード'
        ws.cell(row=1, column=16).value = '河川海岸コード'

        ws.cell(row=1, column=17).value = '地上地下区分コード'
        ws.cell(row=1, column=18).value = '地下空間の利用形態コード'
        
        ws.cell(row=1, column=19).value = '被害建物棟数_床下'
        ws.cell(row=1, column=20).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=21).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=22).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=23).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=24).value = '被害建物棟数_全壊'

        ws.cell(row=1, column=25).value = '延床面積'
        ws.cell(row=1, column=26).value = '被災世帯数'
        ws.cell(row=1, column=27).value = '被災事業所数'
        
        ws.cell(row=1, column=28).value = '延床面積_床下'
        ws.cell(row=1, column=29).value = '延床面積_01から49cm'
        ws.cell(row=1, column=30).value = '延床面積_50から99cm'
        ws.cell(row=1, column=31).value = '延床面積_100cm以上'
        ws.cell(row=1, column=32).value = '延床面積_半壊'
        ws.cell(row=1, column=33).value = '延床面積_全壊'
        
        ws.cell(row=1, column=34).value = '被災世帯数_床下'
        ws.cell(row=1, column=35).value = '被災世帯数_01から49cm'
        ws.cell(row=1, column=36).value = '被災世帯数_50から99cm'
        ws.cell(row=1, column=37).value = '被災世帯数_100cm以上'
        ws.cell(row=1, column=38).value = '被災世帯数_半壊'
        ws.cell(row=1, column=39).value = '被災世帯数_全壊'

        ws.cell(row=1, column=40).value = '被災事業所数_床下'
        ws.cell(row=1, column=41).value = '被災事業所数_01から49cm'
        ws.cell(row=1, column=42).value = '被災事業所数_50から99cm'
        ws.cell(row=1, column=43).value = '被災事業所数_100cm以上'
        ws.cell(row=1, column=44).value = '被災事業所数_半壊'
        ws.cell(row=1, column=45).value = '被災事業所数_全壊'

        ws.cell(row=1, column=46).value = '被災従業者数_床下'
        ws.cell(row=1, column=47).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=48).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=49).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=50).value = '被災従業者数_全壊'

        ws.cell(row=1, column=51).value = '農漁家戸数_床下'
        ws.cell(row=1, column=52).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=53).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=54).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=55).value = '農漁家戸数_全壊'
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws.cell(row=i+2, column=1).value = ippan.ippan_id
                ws.cell(row=i+2, column=2).value = ippan.ippan_name
                
                ws.cell(row=i+2, column=3).value = ippan.building_code
                
                ws.cell(row=i+2, column=4).value = ippan.flood_sediment_code
                ws.cell(row=i+2, column=5).value = ippan.gradient_code
                ws.cell(row=i+2, column=6).value = ippan.industry_code
                
                ws.cell(row=i+2, column=7).value = ippan.ken_code
                ws.cell(row=i+2, column=8).value = ippan.city_code
                ws.cell(row=i+2, column=9).value = ippan.weather_id
                ws.cell(row=i+2, column=10).value = ippan.area_id
                ws.cell(row=i+2, column=11).value = ippan.cause_1_code
                ws.cell(row=i+2, column=12).value = ippan.cause_2_code
                ws.cell(row=i+2, column=13).value = ippan.cause_3_code
                
                ws.cell(row=i+2, column=14).value = ippan.suikei_code
                ws.cell(row=i+2, column=15).value = ippan.kasen_code
                ws.cell(row=i+2, column=16).value = ippan.kasen_kaigan_code

                ws.cell(row=i+2, column=17).value = ippan.underground_code
                ws.cell(row=i+2, column=18).value = ippan.usage_code
                
                ws.cell(row=i+2, column=19).value = ippan.building_lv00
                ws.cell(row=i+2, column=20).value = ippan.building_lv01_49
                ws.cell(row=i+2, column=21).value = ippan.building_lv50_99
                ws.cell(row=i+2, column=22).value = ippan.building_lv100
                ws.cell(row=i+2, column=23).value = ippan.building_half
                ws.cell(row=i+2, column=24).value = ippan.building_full

                ws.cell(row=i+2, column=25).value = ippan.floor_area
                ws.cell(row=i+2, column=26).value = ippan.family
                ws.cell(row=i+2, column=27).value = ippan.office
                
                ws.cell(row=i+2, column=28).value = ippan.floor_area_lv00
                ws.cell(row=i+2, column=29).value = ippan.floor_area_lv01_49
                ws.cell(row=i+2, column=30).value = ippan.floor_area_lv50_99
                ws.cell(row=i+2, column=31).value = ippan.floor_area_lv100
                ws.cell(row=i+2, column=32).value = ippan.floor_area_half
                ws.cell(row=i+2, column=33).value = ippan.floor_area_full
                
                ws.cell(row=i+2, column=34).value = ippan.family_lv00
                ws.cell(row=i+2, column=35).value = ippan.family_lv01_49
                ws.cell(row=i+2, column=36).value = ippan.family_lv50_99
                ws.cell(row=i+2, column=37).value = ippan.family_lv100
                ws.cell(row=i+2, column=38).value = ippan.family_half
                ws.cell(row=i+2, column=39).value = ippan.family_full

                ws.cell(row=i+2, column=40).value = ippan.office_lv00
                ws.cell(row=i+2, column=41).value = ippan.office_lv01_49
                ws.cell(row=i+2, column=42).value = ippan.office_lv50_99
                ws.cell(row=i+2, column=43).value = ippan.office_lv100
                ws.cell(row=i+2, column=44).value = ippan.office_half
                ws.cell(row=i+2, column=45).value = ippan.office_full

                ws.cell(row=i+2, column=46).value = ippan.employee_lv00
                ws.cell(row=i+2, column=47).value = ippan.employee_lv01_49
                ws.cell(row=i+2, column=48).value = ippan.employee_lv50_99
                ws.cell(row=i+2, column=49).value = ippan.employee_lv100
                ws.cell(row=i+2, column=50).value = ippan.employee_full
        
                ws.cell(row=i+2, column=51).value = ippan.farmer_fisher_lv00
                ws.cell(row=i+2, column=52).value = ippan.farmer_fisher_lv01_49
                ws.cell(row=i+2, column=53).value = ippan.farmer_fisher_lv50_99
                ws.cell(row=i+2, column=54).value = ippan.farmer_fisher_lv100
                ws.cell(row=i+2, column=55).value = ippan.farmer_fisher_full

        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.ippan_ken_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_ken.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.ippan_ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：kokyo_view
### 206: 公共土木調査票
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def kokyo_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kokyo_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.kokyo_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.kokyo_view()関数 lock = {}'.format(lock), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        ### kokyo_list = KOKYO.objects.order_by('kokyo_id')[:]
        kokyo_list = KOKYO.objects.raw("""SELECT * FROM KOKYO ORDER BY CAST(KOKYO_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        template_file_path = 'static/template_kokyo.xlsx'
        download_file_path = 'static/download_kokyo.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '公共土木調査票'
        ws.cell(row=1, column=1).value = '公共土木調査票ID'
        ws.cell(row=1, column=2).value = '都道府県コード'
        ws.cell(row=1, column=3).value = '市区町村コード'
        ws.cell(row=1, column=4).value = '異常気象ID'
        ws.cell(row=1, column=5).value = '公共土木調査対象年'
        ws.cell(row=1, column=6).value = '開始日'
        ws.cell(row=1, column=7).value = '終了日'
        
        if kokyo_list:
            for i, kokyo in enumerate(kokyo_list):
                ws.cell(row=i+2, column=1).value = kokyo.kokyo_id
                ws.cell(row=i+2, column=2).value = kokyo.ken_code
                ws.cell(row=i+2, column=3).value = kokyo.city_code
                ws.cell(row=i+2, column=4).value = kokyo.weather_id
                ws.cell(row=i+2, column=5).value = kokyo.kokyo_year
                ws.cell(row=i+2, column=6).value = kokyo.begin_date
                ws.cell(row=i+2, column=7).value = kokyo.end_date
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.kokyo_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kokyo.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kokyo_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.kokyo_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：koeki_view
### 2907 公益事業調査票
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def koeki_view(request, lock):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.koeki_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.koeki_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0200ExcelDownload.koeki_view()関数 lock = {}'.format(lock), 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、データを取得する。
        #######################################################################
        koeki_list = KOEKI.objects.order_by('koeki_id')[:]
        ### koeki_list = KOEKI.objects.raw("""SELECT * FROM KOEKI ORDER BY CAST(KOEKI_ID AS INTEGER)""", [])
    
        #######################################################################
        ### EXCEL入出力処理(0020)
        ### (1)テンプレート用のEXCELファイルを読み込む。
        ### (2)セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        template_file_path = 'static/template_koeki.xlsx'
        download_file_path = 'static/download_koeki.xlsx'
        wb = openpyxl.load_workbook(template_file_path)
        ws = wb.active
        ws.title = '公益事業調査票'
        ws.cell(row=1, column=1).value = '公益事業調査票ID'
        ws.cell(row=1, column=2).value = '都道府県コード'
        ws.cell(row=1, column=3).value = '市区町村コード'
        ws.cell(row=1, column=4).value = '異常気象ID'
        ws.cell(row=1, column=5).value = '公益事業調査対象年'
        ws.cell(row=1, column=6).value = '開始日'
        ws.cell(row=1, column=7).value = '終了日'
        
        if koeki_list:
            for i, koeki in enumerate(koeki_list):
                ws.cell(row=i+1, column=1).value = koeki.koeki_id
                ws.cell(row=i+1, column=2).value = koeki.ken_code
                ws.cell(row=i+1, column=3).value = koeki.city_code
                ws.cell(row=i+1, column=4).value = koeki.weather_id
                ws.cell(row=i+1, column=5).value = koeki.koeki_year
                ws.cell(row=i+1, column=6).value = koeki.begin_date
                ws.cell(row=i+1, column=7).value = koeki.end_date
        
        wb.save(download_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0030)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.koeki_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="koeki.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.koeki_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.koeki_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

