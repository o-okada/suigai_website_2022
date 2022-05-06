#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import Http404
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

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
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

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################
from P0000Common.models import HOUSE_ASSET             ### 15: 県別家屋評価額
from P0000Common.models import HOUSE_DAMAGE            ### 16: 家屋被害率
from P0000Common.models import HOUSEHOLD_DAMAGE        ### 17: 家庭用品自動車以外被害率
from P0000Common.models import CAR_DAMAGE              ### 18: 家庭用品自動車被害率
from P0000Common.models import HOUSE_COST              ### 19: 家庭応急対策費
from P0000Common.models import OFFICE_ASSET            ### 20: 産業分類別資産額
from P0000Common.models import OFFICE_DAMAGE           ### 21: 事業所被害率
from P0000Common.models import OFFICE_COST             ### 22: 事業所営業停止損失
from P0000Common.models import FARMER_FISHER_DAMAGE    ### 23: 農漁家被害率

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import WEATHER                 ### 24: 異常気象（ほぼ、水害）
from P0000Common.models import AREA                    ### 25: 区域
from P0000Common.models import IPPAN                   ### 26: 一般資産調査票

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import RESTORATION             ### 27: 復旧事業工種

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import KOKYO                   ### 28: 公共土木調査票
from P0000Common.models import KOEKI                   ### 29: 公益事業調査票

from P0000Common.common_function import print_log

### Imaginary function to handle an uploaded file.
### from somewhere import handle_uploaded_file
### class IndexView(generic.TemplateView):
###     template_name = "index1.html"
### def index(request):
###     try:
###         latest_question_list = P0200Question.objects.order_by('-pub_date')[:5]
###         template = loader.get_template('P0200ExcelDownload/index1.html')
###         context = {
###             'latest_question_list': latest_question_list,
###         }
###     except:
###         raise Http404("P0200Question does not exist.")
###     return HttpResponse(template.render(context, request))

###############################################################################
### index 関数
###############################################################################
def index(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.index()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.index()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.order_by('ken_code')[:]
        city_list01 = CITY.objects.filter(ken_code='01').order_by('city_code')
        city_list02 = CITY.objects.filter(ken_code='02').order_by('city_code')
        city_list03 = CITY.objects.filter(ken_code='03').order_by('city_code')
        city_list04 = CITY.objects.filter(ken_code='04').order_by('city_code')
        city_list05 = CITY.objects.filter(ken_code='05').order_by('city_code')
        city_list06 = CITY.objects.filter(ken_code='06').order_by('city_code')
        city_list07 = CITY.objects.filter(ken_code='07').order_by('city_code')
        city_list08 = CITY.objects.filter(ken_code='08').order_by('city_code')
        city_list09 = CITY.objects.filter(ken_code='09').order_by('city_code')
        city_list10 = CITY.objects.filter(ken_code='10').order_by('city_code')
        city_list11 = CITY.objects.filter(ken_code='11').order_by('city_code')
        city_list12 = CITY.objects.filter(ken_code='12').order_by('city_code')
        city_list13 = CITY.objects.filter(ken_code='13').order_by('city_code')
        city_list14 = CITY.objects.filter(ken_code='14').order_by('city_code')
        city_list15 = CITY.objects.filter(ken_code='15').order_by('city_code')
        city_list16 = CITY.objects.filter(ken_code='16').order_by('city_code')
        city_list17 = CITY.objects.filter(ken_code='17').order_by('city_code')
        city_list18 = CITY.objects.filter(ken_code='18').order_by('city_code')
        city_list19 = CITY.objects.filter(ken_code='19').order_by('city_code')
        city_list20 = CITY.objects.filter(ken_code='20').order_by('city_code')
        city_list21 = CITY.objects.filter(ken_code='21').order_by('city_code')
        city_list22 = CITY.objects.filter(ken_code='22').order_by('city_code')
        city_list23 = CITY.objects.filter(ken_code='23').order_by('city_code')
        city_list24 = CITY.objects.filter(ken_code='24').order_by('city_code')
        city_list25 = CITY.objects.filter(ken_code='25').order_by('city_code')
        city_list26 = CITY.objects.filter(ken_code='26').order_by('city_code')
        city_list27 = CITY.objects.filter(ken_code='27').order_by('city_code')
        city_list28 = CITY.objects.filter(ken_code='28').order_by('city_code')
        city_list29 = CITY.objects.filter(ken_code='29').order_by('city_code')
        city_list30 = CITY.objects.filter(ken_code='30').order_by('city_code')
        city_list31 = CITY.objects.filter(ken_code='31').order_by('city_code')
        city_list32 = CITY.objects.filter(ken_code='32').order_by('city_code')
        city_list33 = CITY.objects.filter(ken_code='33').order_by('city_code')
        city_list34 = CITY.objects.filter(ken_code='34').order_by('city_code')
        city_list35 = CITY.objects.filter(ken_code='35').order_by('city_code')
        city_list36 = CITY.objects.filter(ken_code='36').order_by('city_code')
        city_list37 = CITY.objects.filter(ken_code='37').order_by('city_code')
        city_list38 = CITY.objects.filter(ken_code='38').order_by('city_code')
        city_list39 = CITY.objects.filter(ken_code='39').order_by('city_code')
        city_list40 = CITY.objects.filter(ken_code='40').order_by('city_code')
        city_list41 = CITY.objects.filter(ken_code='41').order_by('city_code')
        city_list42 = CITY.objects.filter(ken_code='42').order_by('city_code')
        city_list43 = CITY.objects.filter(ken_code='43').order_by('city_code')
        city_list44 = CITY.objects.filter(ken_code='44').order_by('city_code')
        city_list45 = CITY.objects.filter(ken_code='45').order_by('city_code')
        city_list46 = CITY.objects.filter(ken_code='46').order_by('city_code')
        city_list47 = CITY.objects.filter(ken_code='47').order_by('city_code')
        
        #######################################################################
        ### HttpResponse処理
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
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
        print_log('[INFO] P0200ExcelDownload.index()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.index()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

### def upload_file(request):
###     if request.method == 'POST':
###         form = UploadFileForm(request.POST, request.FILES)
###         if form.is_valid():
###             handle_uploaded_file(request.FILES['file'])
###             return HttpResponseRedirect('/success/url/')
###     else:
###         form = UploadFileForm()
###     return render(request, 'upload.html', {'form': form})
### def handle_uploaded_file(f):
###     with open('some/file/name.txt', 'wb+') as destination:
###         for chunk in f.chunks():
###             destination.write(chunk)
### def download_file(request):
###     try:
###         file_path_to_load = 'static/example.xlsx'
###         file_path_to_save = 'static/example2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         ws['A1'].value = 12345.6789
###         ws['A2'].value = 12345.6789
###         ws['A3'].value = '=sum(A1:A2)'
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="your_book.xlsx"'
###     except:
###         raise Http404("[ERROR] download_file().")
###     return response

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 00: 
### def download_p0200prefecture(request):
###     try:
###         p0200prefecture_list = P0200Prefecture.objects.order_by('CODE')[:]
###         file_path_to_load = 'static/p0200prefecture.xlsx'
###         file_path_to_save = 'static/p0200prefecture2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         if p0200prefecture_list:
###             for i, p0200prefecture in enumerate(p0200prefecture_list):
###                 ws.cell(row=i+1, column=1).value = p0200prefecture.CODE
###                 ws.cell(row=i+1, column=2).value = p0200prefecture.NAME
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="p0200prefecture.xlsx"'
###     except:
###         raise Http404("[ERROR] download_p0200prefecture().")
###     return response
### 00: 
### def download_p0200city(request):
###     try:
###         p0200city_list = P0200CITY.objects.order_by('CODE')[:]
###         file_path_to_load = 'static/p0200city.xlsx'
###         file_path_to_save = 'static/p0200city2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         if p0200city_list:
###             for i, p0200city in enumerate(p0200city_list):
###                 ws.cell(row=i+1, column=1).value = p0200city.CODE
###                 ws.cell(row=i+1, column=2).value = p0200city.PREF_CODE
###                 ws.cell(row=i+1, column=3).value = p0200city.NAME
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="p0200city.xlsx"'
###     except:
###         raise Http404("[ERROR] download_p0200city().")
###     return response

###############################################################################
### download_building関数
### 01: 建物区分
###############################################################################
def download_building(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_building()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_building()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        building_list = BUILDING.objects.order_by('building_code')[:]
        
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/building.xlsx'
        file_path_to_save = 'static/building2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '建物区分'
        ws.cell(row=1, column=1).value = '建物区分コード'
        ws.cell(row=1, column=2).value = '建物区分名'
        
        if building_list:
            for i, building in enumerate(building_list):
                ws.cell(row=i+2, column=1).value = building.building_code
                ws.cell(row=i+2, column=2).value = building.building_name

        # dv = DataValidation(type="list", formula1='"A,B,C"')
        ### dv.add(ws.cell(1, 1))
        ### dv.add(ws.cell(2, 1))
        ### dv.add(ws.cell(3, 1))
        # dv.ranges = 'A1:A100'
        # ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_building()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="building.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_building().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_building()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_building()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_ken関数
### 02: 都道府県
###############################################################################
def download_ken(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ken()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ken()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        ken_list = KEN.objects.order_by('ken_code')[:]
        
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/ken.xlsx'
        file_path_to_save = 'static/ken2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '都道府県'
        ws.cell(row=1, column=1).value = '都道府県コード'
        ws.cell(row=1, column=2).value = '都道府県名'
        
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws.cell(row=i+2, column=1).value = ken.ken_code
                ws.cell(row=i+2, column=2).value = ken.ken_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_ken()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ken.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_ken().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ken()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ken()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_city関数
### 03: 市区町村
###############################################################################
def download_city(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_city()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_city()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        city_list = CITY.objects.order_by('city_code')[:]
        
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/city.xlsx'
        file_path_to_save = 'static/city2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_city()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="city.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_city().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_city()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_city()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_kasen_kaigan関数
### 04: 水害発生地点工種（河川海岸区分）
###############################################################################
def download_kasen_kaigan(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen_kaigan()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen_kaigan()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        kasen_kaigan_list = KASEN_KAIGAN.objects.order_by('kasen_kaigan_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/kasen_kaigan.xlsx'
        file_path_to_save = 'static/kasen_kaigan2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '河川海岸区分'
        ws.cell(row=1, column=1).value = '河川海岸区分コード'
        ws.cell(row=1, column=2).value = '河川海岸区分名'
        
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws.cell(row=i+2, column=1).value = kasen_kaigan.kasen_kaigan_code
                ws.cell(row=i+2, column=2).value = kasen_kaigan.kasen_kaigan_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_kasen_kaigan()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_kaigan.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_kasen_kaigan().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen_kaigan()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen_kaigan()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_suikei関数
### 05: 水系（水系・沿岸）
###############################################################################
def download_suikei(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_suikei()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_suikei()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        suikei_list = SUIKEI.objects.order_by('suikei_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/suikei.xlsx'
        file_path_to_save = 'static/suikei2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_suikei()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_suikei().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_suikei()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_suikei()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_suikei_type関数
### 06: 水系種別（水系・沿岸種別）
###############################################################################
def download_suikei_type(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_suikei_type()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_suikei_type()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        suikei_type_list = SUIKEI_TYPE.objects.order_by('suikei_type_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/suikei_type.xlsx'
        file_path_to_save = 'static/suikei_type2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '水系種別'
        ws.cell(row=1, column=1).value = '水系種別コード'
        ws.cell(row=1, column=2).value = '水系種別名'
        
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws.cell(row=i+2, column=1).value = suikei_type.suikei_type_code
                ws.cell(row=i+2, column=2).value = suikei_type.suikei_type_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_suikei_type()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei_type.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_suikei_type().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_suikei_type()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_suikei_type()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_kasen関数
### 07: 河川（河川・海岸）
###############################################################################
def download_kasen(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        kasen_list = KASEN.objects.order_by('kasen_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/kasen.xlsx'
        file_path_to_save = 'static/kasen2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_kasen()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_kasen().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_kasen_type関数
### 08: 河川種別（河川・海岸種別）
###############################################################################
def download_kasen_type(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen_type()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kasen_type()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        kasen_type_list = KASEN_TYPE.objects.order_by('kasen_type_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/kasen_type.xlsx'
        file_path_to_save = 'static/kasen_type2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '河川種別'
        ws.cell(row=1, column=1).value = '河川種別コード'
        ws.cell(row=1, column=2).value = '河川種別名'
        
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws.cell(row=i+2, column=1).value = kasen_type.kasen_type_code
                ws.cell(row=i+2, column=2).value = kasen_type.kasen_type_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_kasen_type()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_type.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_kasen_type().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen_type()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kasen_type()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_cause関数
### 09: 水害原因
###############################################################################
def download_cause(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_cause()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_cause()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        cause_list = CAUSE.objects.order_by('cause_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/cause.xlsx'
        file_path_to_save = 'static/cause2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '水害原因'
        ws.cell(row=1, column=1).value = '水害原因コード'
        ws.cell(row=1, column=2).value = '水害原因名'
        
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws.cell(row=i+2, column=1).value = cause.cause_code
                ws.cell(row=i+2, column=2).value = cause.cause_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_cause()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cause.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_cause().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_cause()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_cause()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_underground関数
### 10: 地上地下区分
###############################################################################
def download_underground(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_underground()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_underground()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        underground_list = UNDERGROUND.objects.order_by('underground_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/underground.xlsx'
        file_path_to_save = 'static/underground2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '地上地下区分'
        ws.cell(row=1, column=1).value = '地上地下区分コード'
        ws.cell(row=1, column=2).value = '地上地下区分名'
        
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws.cell(row=i+2, column=1).value = underground.underground_code
                ws.cell(row=i+2, column=2).value = underground.underground_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_underground()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="underground.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_underground().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_underground()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_underground()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_usage関数
### 11: 地下空間の利用形態
###############################################################################
def download_usage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_usage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_usage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        usage_list = USAGE.objects.order_by('usage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/usage.xlsx'
        file_path_to_save = 'static/usage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '地下空間の利用形態'
        ws.cell(row=1, column=1).value = '地下空間の利用形態コード'
        ws.cell(row=1, column=2).value = '地下空間の利用形態名'
        
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws.cell(row=i+2, column=1).value = usage.usage_code
                ws.cell(row=i+2, column=2).value = usage.usage_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_usage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="usage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_usage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_usage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_usage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_flood_sediment関数
### 12: 浸水土砂区分
###############################################################################
def download_flood_sediment(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_flood_sediment()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_flood_sediment()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        flood_sediment_list = FLOOD_SEDIMENT.objects.order_by('flood_sediment_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/flood_sediment.xlsx'
        file_path_to_save = 'static/flood_sediment2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '浸水土砂区分'
        ws.cell(row=1, column=1).value = '浸水土砂区分コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分名'
        
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws.cell(row=i+2, column=1).value = flood_sediment.flood_sediment_code
                ws.cell(row=i+2, column=2).value = flood_sediment.flood_sediment_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_flood_sediment()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="flood_sediment.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_usage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_flood_sediment()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_flood_sediment()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_gradient関数
### 13: 地盤勾配区分
###############################################################################
def download_gradient(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_gradient()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_gradient()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        gradient_list = GRADIENT.objects.order_by('gradient_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/gradient.xlsx'
        file_path_to_save = 'static/gradient2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '地盤勾配区分'
        ws.cell(row=1, column=1).value = '地盤勾配区分コード'
        ws.cell(row=1, column=2).value = '地盤勾配区分名'
        
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws.cell(row=i+2, column=1).value = gradient.gradient_code
                ws.cell(row=i+2, column=2).value = gradient.gradient_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_gradient()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="gradient.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_gradient().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_gradient()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_gradient()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_industry関数
### 14: 産業分類
###############################################################################
def download_industry(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_industry()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_industry()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        industry_list = INDUSTRY.objects.order_by('industry_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/industry.xlsx'
        file_path_to_save = 'static/industry2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '産業分類'
        ws.cell(row=1, column=1).value = '産業分類コード'
        ws.cell(row=1, column=2).value = '産業分類名'
        
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws.cell(row=i+2, column=1).value = industry.industry_code
                ws.cell(row=i+2, column=2).value = industry.industry_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_industry()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="industry.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_industry().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_industry()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_industry()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################

###############################################################################
### download_house_asset関数
### 15: 県別家屋評価額
###############################################################################
def download_house_asset(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_asset()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_asset()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        house_asset_list = HOUSE_ASSET.objects.order_by('house_asset_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/house_asset.xlsx'
        file_path_to_save = 'static/house_asset2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_house_asset()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_asset.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_house_asset().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_asset()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_asset()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_house_damage関数
### 16: 家屋被害率
###############################################################################
def download_house_damage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_damage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_damage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        house_damage_list = HOUSE_DAMAGE.objects.order_by('house_damage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/house_damage.xlsx'
        file_path_to_save = 'static/house_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_house_damage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_damage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_house_damage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_damage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_damage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_household_damage関数
### 17: 家庭用品自動車以外被害率
###############################################################################
def download_household_damage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_household_damage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_household_damage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        household_damage_list = HOUSEHOLD_DAMAGE.objects.order_by('household_damage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/household_damage.xlsx'
        file_path_to_save = 'static/household_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
            for i, house_damage in enumerate(household_damage_list):
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_household_damage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_damage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_household_damage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_household_damage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_household_damage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_car_damage関数
### 18: 家庭用品自動車被害率
###############################################################################
def download_car_damage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_car_damage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_car_damage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        car_damage_list = CAR_DAMAGE.objects.order_by('car_damage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/car_damage.xlsx'
        file_path_to_save = 'static/car_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_car_damage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car_damage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_car_damage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_car_damage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_car_damage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_house_cost関数
### 19: 家庭応急対策費
###############################################################################
def download_house_cost(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_cost()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_house_cost()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        house_cost_list = HOUSE_COST.objects.order_by('house_cost_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/house_cost.xlsx'
        file_path_to_save = 'static/house_cost2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_house_cost()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_cost.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_house_cost().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_cost()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_house_cost()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_office_asset関数
### 20: 産業分類別資産額
###############################################################################
def download_office_asset(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_asset()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_asset()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        office_asset_list = OFFICE_ASSET.objects.order_by('office_asset_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/office_asset.xlsx'
        file_path_to_save = 'static/office_asset2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_office_asset()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_asset.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_office_asset().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_asset()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_asset()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_office_damage関数
### 21: 事業所被害率
###############################################################################
def download_office_damage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_damage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_damage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        office_damage_list = OFFICE_DAMAGE.objects.order_by('office_damage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/office_damage.xlsx'
        file_path_to_save = 'static/office_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
                ws.cell(row=i+2, column=2).value = office_damage.OFFICE_DAMAGE_YEAR
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_office_damage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_damage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_office_damage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_damage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_damage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_office_cost関数
### 22: 事業所営業停止損失
###############################################################################
def download_office_cost(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_cost()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_office_cost()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        office_cost_list = OFFICE_COST.objects.order_by('office_cost_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/office_cost.xlsx'
        file_path_to_save = 'static/office_cost2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_office_cost()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_cost.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_office_cost().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_cost()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_office_cost()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_farmer_fisher_damage関数
### 23: 農漁家被害率
###############################################################################
def download_farmer_fisher_damage(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_farmer_fisher_damage()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_farmer_fisher_damage()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.order_by('farmer_fisher_damage_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/farmer_fisher_damage.xlsx'
        file_path_to_save = 'static/farmer_fisher_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_farmer_fisher_damage()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="farmer_fisher_damage.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_farmer_fisher_damage().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_farmer_fisher_damage()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_farmer_fisher_damage()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_weather関数
### 24: 異常気象
###############################################################################
def download_weather(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_weather()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_weather()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        weather_list = WEATHER.objects.order_by('weather_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/weather.xlsx'
        file_path_to_save = 'static/weather2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_weather()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="weather.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_weather().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_weather()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_weather()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_area関数
### 25: 区域
###############################################################################
def download_area(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_area()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_area()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        area_list = AREA.objects.order_by('area_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/area.xlsx'
        file_path_to_save = 'static/area2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
                ws.cell(row=i+2, column=3).value = area.AREA_YEAR
                ws.cell(row=i+2, column=4).value = area.begin_date
                ws.cell(row=i+2, column=5).value = area.end_date
                ws.cell(row=i+2, column=6).value = area.agri_area
                ws.cell(row=i+2, column=7).value = area.underground_area
                ws.cell(row=i+2, column=8).value = area.crop_damage
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_area()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="area.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_area().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_area()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_area()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_ippan_chosa関数
### 2601: 一般資産調査票（調査員用）
###############################################################################
def download_ippan_chosa(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_chosa()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_chosa()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/ippan_chosa1.xlsx'
        file_path_to_save = 'static/ippan_chosa2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load, keep_vba=False)

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
        ws_area = wb["AREA"]
        ws_ippan = wb["IPPAN"]

        ws_city_vlook = wb["CITY_VLOOK"]
        
        ### 01: 建物区分
        building_list = BUILDING.objects.order_by('building_code')[:]
        if building_list:
            for i, building in enumerate(building_list):
                ws_building.cell(row=i+1, column=1).value = building.building_code
                ws_building.cell(row=i+1, column=2).value = building.building_name

        print("download_ippan_chosa3", flush=True)
        ### 02: 都道府県
        ken_list = KEN.objects.order_by('ken_code')[:]
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws_ken.cell(row=i+1, column=1).value = ken.ken_code
                ws_ken.cell(row=i+1, column=2).value = ken.ken_name
                
                ws_city_vlook.cell(row=i+1, column=1).value = ken.ken_name
        
        print("download_ippan_chosa4", flush=True)
        city_list01 = CITY.objects.filter(ken_code='01').order_by('city_code')
        city_list02 = CITY.objects.filter(ken_code='02').order_by('city_code')
        city_list03 = CITY.objects.filter(ken_code='03').order_by('city_code')
        city_list04 = CITY.objects.filter(ken_code='04').order_by('city_code')
        city_list05 = CITY.objects.filter(ken_code='05').order_by('city_code')
        city_list06 = CITY.objects.filter(ken_code='06').order_by('city_code')
        city_list07 = CITY.objects.filter(ken_code='07').order_by('city_code')
        city_list08 = CITY.objects.filter(ken_code='08').order_by('city_code')
        city_list09 = CITY.objects.filter(ken_code='09').order_by('city_code')
        city_list10 = CITY.objects.filter(ken_code='10').order_by('city_code')
        city_list11 = CITY.objects.filter(ken_code='11').order_by('city_code')
        city_list12 = CITY.objects.filter(ken_code='12').order_by('city_code')
        city_list13 = CITY.objects.filter(ken_code='13').order_by('city_code')
        city_list14 = CITY.objects.filter(ken_code='14').order_by('city_code')
        city_list15 = CITY.objects.filter(ken_code='15').order_by('city_code')
        city_list16 = CITY.objects.filter(ken_code='16').order_by('city_code')
        city_list17 = CITY.objects.filter(ken_code='17').order_by('city_code')
        city_list18 = CITY.objects.filter(ken_code='18').order_by('city_code')
        city_list19 = CITY.objects.filter(ken_code='19').order_by('city_code')
        city_list20 = CITY.objects.filter(ken_code='20').order_by('city_code')
        city_list21 = CITY.objects.filter(ken_code='21').order_by('city_code')
        city_list22 = CITY.objects.filter(ken_code='22').order_by('city_code')
        city_list23 = CITY.objects.filter(ken_code='23').order_by('city_code')
        city_list24 = CITY.objects.filter(ken_code='24').order_by('city_code')
        city_list25 = CITY.objects.filter(ken_code='25').order_by('city_code')
        city_list26 = CITY.objects.filter(ken_code='26').order_by('city_code')
        city_list27 = CITY.objects.filter(ken_code='27').order_by('city_code')
        city_list28 = CITY.objects.filter(ken_code='28').order_by('city_code')
        city_list29 = CITY.objects.filter(ken_code='29').order_by('city_code')
        city_list30 = CITY.objects.filter(ken_code='30').order_by('city_code')
        city_list31 = CITY.objects.filter(ken_code='31').order_by('city_code')
        city_list32 = CITY.objects.filter(ken_code='32').order_by('city_code')
        city_list33 = CITY.objects.filter(ken_code='33').order_by('city_code')
        city_list34 = CITY.objects.filter(ken_code='34').order_by('city_code')
        city_list35 = CITY.objects.filter(ken_code='35').order_by('city_code')
        city_list36 = CITY.objects.filter(ken_code='36').order_by('city_code')
        city_list37 = CITY.objects.filter(ken_code='37').order_by('city_code')
        city_list38 = CITY.objects.filter(ken_code='38').order_by('city_code')
        city_list39 = CITY.objects.filter(ken_code='39').order_by('city_code')
        city_list40 = CITY.objects.filter(ken_code='40').order_by('city_code')
        city_list41 = CITY.objects.filter(ken_code='41').order_by('city_code')
        city_list42 = CITY.objects.filter(ken_code='42').order_by('city_code')
        city_list43 = CITY.objects.filter(ken_code='43').order_by('city_code')
        city_list44 = CITY.objects.filter(ken_code='44').order_by('city_code')
        city_list45 = CITY.objects.filter(ken_code='45').order_by('city_code')
        city_list46 = CITY.objects.filter(ken_code='46').order_by('city_code')
        city_list47 = CITY.objects.filter(ken_code='47').order_by('city_code')
        
        ws_city_vlook.cell(row=1, column=2).value = 'CITY!$B$1:$B$%d' % len(city_list01)
        ws_city_vlook.cell(row=2, column=2).value = 'CITY!$G$1:$G$%d' % len(city_list02)
        ws_city_vlook.cell(row=3, column=2).value = 'CITY!$L$1:$L$%d' % len(city_list03)
        ws_city_vlook.cell(row=4, column=2).value = 'CITY!$Q$1:$Q$%d' % len(city_list04)
        ws_city_vlook.cell(row=5, column=2).value = 'CITY!$V$1:$V$%d' % len(city_list05)
        ws_city_vlook.cell(row=6, column=2).value = 'CITY!$AA$1:$AA$%d' % len(city_list06)
        ws_city_vlook.cell(row=7, column=2).value = 'CITY!$AF$1:$AF$%d' % len(city_list07)
        ws_city_vlook.cell(row=8, column=2).value = 'CITY!$AK$1:$AK$%d' % len(city_list08)
        ws_city_vlook.cell(row=9, column=2).value = 'CITY!$AP$1:$AP$%d' % len(city_list09)
        ws_city_vlook.cell(row=10, column=2).value = 'CITY!$AU$1:$AU$%d' % len(city_list10)
        ws_city_vlook.cell(row=11, column=2).value = 'CITY!$AZ$1:$AZ$%d' % len(city_list11)
        ws_city_vlook.cell(row=12, column=2).value = 'CITY!$BE$1:$BE$%d' % len(city_list12)
        ws_city_vlook.cell(row=13, column=2).value = 'CITY!$BJ$1:$BJ$%d' % len(city_list13)
        
        ws_city_vlook.cell(row=14, column=2).value = 'CITY!$BO$1:$BO$%d' % len(city_list14)
        ws_city_vlook.cell(row=15, column=2).value = 'CITY!$BT$1:$BT$%d' % len(city_list15)
        ws_city_vlook.cell(row=16, column=2).value = 'CITY!$BY$1:$BY$%d' % len(city_list16)
        ws_city_vlook.cell(row=17, column=2).value = 'CITY!$CD$1:$CD$%d' % len(city_list17)
        ws_city_vlook.cell(row=18, column=2).value = 'CITY!$CI$1:$CI$%d' % len(city_list18)
        ws_city_vlook.cell(row=19, column=2).value = 'CITY!$CN$1:$CN$%d' % len(city_list19)
        ws_city_vlook.cell(row=20, column=2).value = 'CITY!$CS$1:$CS$%d' % len(city_list20)
        ws_city_vlook.cell(row=21, column=2).value = 'CITY!$CX$1:$CX$%d' % len(city_list21)
        ws_city_vlook.cell(row=22, column=2).value = 'CITY!$DC$1:$DC$%d' % len(city_list22)
        ws_city_vlook.cell(row=23, column=2).value = 'CITY!$DH$1:$DH$%d' % len(city_list23)
        ws_city_vlook.cell(row=24, column=2).value = 'CITY!$DM$1:$DM$%d' % len(city_list24)
        ws_city_vlook.cell(row=25, column=2).value = 'CITY!$DR$1:$DR$%d' % len(city_list25)
        ws_city_vlook.cell(row=26, column=2).value = 'CITY!$DW$1:$DW$%d' % len(city_list26)
        
        ws_city_vlook.cell(row=27, column=2).value = 'CITY!$EB$1:$EB$%d' % len(city_list27)
        ws_city_vlook.cell(row=28, column=2).value = 'CITY!$EG$1:$EG$%d' % len(city_list28)
        ws_city_vlook.cell(row=29, column=2).value = 'CITY!$EL$1:$EL$%d' % len(city_list29)
        ws_city_vlook.cell(row=30, column=2).value = 'CITY!$EQ$1:$EQ$%d' % len(city_list30)
        ws_city_vlook.cell(row=31, column=2).value = 'CITY!$EV$1:$EV$%d' % len(city_list31)
        ws_city_vlook.cell(row=32, column=2).value = 'CITY!$FA$1:$FA$%d' % len(city_list32)
        ws_city_vlook.cell(row=33, column=2).value = 'CITY!$FF$1:$FF$%d' % len(city_list33)
        ws_city_vlook.cell(row=34, column=2).value = 'CITY!$FK$1:$FK$%d' % len(city_list34)
        ws_city_vlook.cell(row=35, column=2).value = 'CITY!$FP$1:$FP$%d' % len(city_list35)
        ws_city_vlook.cell(row=36, column=2).value = 'CITY!$FU$1:$FU$%d' % len(city_list36)
        ws_city_vlook.cell(row=37, column=2).value = 'CITY!$FZ$1:$FZ$%d' % len(city_list37)
        ws_city_vlook.cell(row=38, column=2).value = 'CITY!$GE$1:$GE$%d' % len(city_list38)
        ws_city_vlook.cell(row=39, column=2).value = 'CITY!$GJ$1:$GJ$%d' % len(city_list39)
        
        ws_city_vlook.cell(row=40, column=2).value = 'CITY!$GO$1:$GO$%d' % len(city_list40)
        ws_city_vlook.cell(row=41, column=2).value = 'CITY!$GT$1:$GT$%d' % len(city_list41)
        ws_city_vlook.cell(row=42, column=2).value = 'CITY!$GY$1:$GY$%d' % len(city_list42)
        ws_city_vlook.cell(row=43, column=2).value = 'CITY!$HD$1:$HD$%d' % len(city_list43)
        ws_city_vlook.cell(row=44, column=2).value = 'CITY!$HI$1:$HI$%d' % len(city_list44)
        ws_city_vlook.cell(row=45, column=2).value = 'CITY!$HN$1:$HN$%d' % len(city_list45)
        ws_city_vlook.cell(row=46, column=2).value = 'CITY!$HS$1:$HS$%d' % len(city_list46)
        ws_city_vlook.cell(row=47, column=2).value = 'CITY!$HX$1:$HX$%d' % len(city_list47)

        print("download_ippan_chosa5", flush=True)
        ### 03: 市区町村
        ### city_list = CITY.objects.order_by('city_code')[:]
        if city_list01:
            for i, city in enumerate(city_list01):
                ws_city.cell(row=i+1, column=1).value = city.city_code
                ws_city.cell(row=i+1, column=2).value = city.city_name
                ws_city.cell(row=i+1, column=3).value = city.ken_code
                ws_city.cell(row=i+1, column=4).value = city.city_population
                ws_city.cell(row=i+1, column=5).value = city.city_area

        if city_list02:
            for i, city in enumerate(city_list02):
                ws_city.cell(row=i+1, column=6).value = city.city_code
                ws_city.cell(row=i+1, column=7).value = city.city_name
                ws_city.cell(row=i+1, column=8).value = city.ken_code
                ws_city.cell(row=i+1, column=9).value = city.city_population
                ws_city.cell(row=i+1, column=10).value = city.city_area

        if city_list03:
            for i, city in enumerate(city_list03):
                ws_city.cell(row=i+1, column=11).value = city.city_code
                ws_city.cell(row=i+1, column=12).value = city.city_name
                ws_city.cell(row=i+1, column=13).value = city.ken_code
                ws_city.cell(row=i+1, column=14).value = city.city_population
                ws_city.cell(row=i+1, column=15).value = city.city_area

        if city_list04:
            for i, city in enumerate(city_list04):
                ws_city.cell(row=i+1, column=16).value = city.city_code
                ws_city.cell(row=i+1, column=17).value = city.city_name
                ws_city.cell(row=i+1, column=18).value = city.ken_code
                ws_city.cell(row=i+1, column=19).value = city.city_population
                ws_city.cell(row=i+1, column=20).value = city.city_area

        if city_list05:
            for i, city in enumerate(city_list05):
                ws_city.cell(row=i+1, column=21).value = city.city_code
                ws_city.cell(row=i+1, column=22).value = city.city_name
                ws_city.cell(row=i+1, column=23).value = city.ken_code
                ws_city.cell(row=i+1, column=24).value = city.city_population
                ws_city.cell(row=i+1, column=25).value = city.city_area

        if city_list06:
            for i, city in enumerate(city_list06):
                ws_city.cell(row=i+1, column=26).value = city.city_code
                ws_city.cell(row=i+1, column=27).value = city.city_name
                ws_city.cell(row=i+1, column=28).value = city.ken_code
                ws_city.cell(row=i+1, column=29).value = city.city_population
                ws_city.cell(row=i+1, column=30).value = city.city_area

        if city_list07:
            for i, city in enumerate(city_list07):
                ws_city.cell(row=i+1, column=31).value = city.city_code
                ws_city.cell(row=i+1, column=32).value = city.city_name
                ws_city.cell(row=i+1, column=33).value = city.ken_code
                ws_city.cell(row=i+1, column=34).value = city.city_population
                ws_city.cell(row=i+1, column=35).value = city.city_area

        if city_list08:
            for i, city in enumerate(city_list08):
                ws_city.cell(row=i+1, column=36).value = city.city_code
                ws_city.cell(row=i+1, column=37).value = city.city_name
                ws_city.cell(row=i+1, column=38).value = city.ken_code
                ws_city.cell(row=i+1, column=39).value = city.city_population
                ws_city.cell(row=i+1, column=40).value = city.city_area

        if city_list09:
            for i, city in enumerate(city_list09):
                ws_city.cell(row=i+1, column=41).value = city.city_code
                ws_city.cell(row=i+1, column=42).value = city.city_name
                ws_city.cell(row=i+1, column=43).value = city.ken_code
                ws_city.cell(row=i+1, column=44).value = city.city_population
                ws_city.cell(row=i+1, column=45).value = city.city_area

        if city_list10:
            for i, city in enumerate(city_list10):
                ws_city.cell(row=i+1, column=46).value = city.city_code
                ws_city.cell(row=i+1, column=47).value = city.city_name
                ws_city.cell(row=i+1, column=48).value = city.ken_code
                ws_city.cell(row=i+1, column=49).value = city.city_population
                ws_city.cell(row=i+1, column=50).value = city.city_area

        if city_list11:
            for i, city in enumerate(city_list11):
                ws_city.cell(row=i+1, column=51).value = city.city_code
                ws_city.cell(row=i+1, column=52).value = city.city_name
                ws_city.cell(row=i+1, column=53).value = city.ken_code
                ws_city.cell(row=i+1, column=54).value = city.city_population
                ws_city.cell(row=i+1, column=55).value = city.city_area

        if city_list12:
            for i, city in enumerate(city_list12):
                ws_city.cell(row=i+1, column=56).value = city.city_code
                ws_city.cell(row=i+1, column=57).value = city.city_name
                ws_city.cell(row=i+1, column=58).value = city.ken_code
                ws_city.cell(row=i+1, column=59).value = city.city_population
                ws_city.cell(row=i+1, column=60).value = city.city_area

        if city_list13:
            for i, city in enumerate(city_list13):
                ws_city.cell(row=i+1, column=61).value = city.city_code
                ws_city.cell(row=i+1, column=62).value = city.city_name
                ws_city.cell(row=i+1, column=63).value = city.ken_code
                ws_city.cell(row=i+1, column=64).value = city.city_population
                ws_city.cell(row=i+1, column=65).value = city.city_area

        if city_list14:
            for i, city in enumerate(city_list14):
                ws_city.cell(row=i+1, column=66).value = city.city_code
                ws_city.cell(row=i+1, column=67).value = city.city_name
                ws_city.cell(row=i+1, column=68).value = city.ken_code
                ws_city.cell(row=i+1, column=69).value = city.city_population
                ws_city.cell(row=i+1, column=70).value = city.city_area

        if city_list15:
            for i, city in enumerate(city_list15):
                ws_city.cell(row=i+1, column=71).value = city.city_code
                ws_city.cell(row=i+1, column=72).value = city.city_name
                ws_city.cell(row=i+1, column=73).value = city.ken_code
                ws_city.cell(row=i+1, column=74).value = city.city_population
                ws_city.cell(row=i+1, column=75).value = city.city_area

        if city_list16:
            for i, city in enumerate(city_list16):
                ws_city.cell(row=i+1, column=76).value = city.city_code
                ws_city.cell(row=i+1, column=77).value = city.city_name
                ws_city.cell(row=i+1, column=78).value = city.ken_code
                ws_city.cell(row=i+1, column=79).value = city.city_population
                ws_city.cell(row=i+1, column=80).value = city.city_area

        if city_list17:
            for i, city in enumerate(city_list17):
                ws_city.cell(row=i+1, column=81).value = city.city_code
                ws_city.cell(row=i+1, column=82).value = city.city_name
                ws_city.cell(row=i+1, column=83).value = city.ken_code
                ws_city.cell(row=i+1, column=84).value = city.city_population
                ws_city.cell(row=i+1, column=85).value = city.city_area

        if city_list18:
            for i, city in enumerate(city_list18):
                ws_city.cell(row=i+1, column=86).value = city.city_code
                ws_city.cell(row=i+1, column=87).value = city.city_name
                ws_city.cell(row=i+1, column=88).value = city.ken_code
                ws_city.cell(row=i+1, column=89).value = city.city_population
                ws_city.cell(row=i+1, column=90).value = city.city_area

        if city_list19:
            for i, city in enumerate(city_list19):
                ws_city.cell(row=i+1, column=91).value = city.city_code
                ws_city.cell(row=i+1, column=92).value = city.city_name
                ws_city.cell(row=i+1, column=93).value = city.ken_code
                ws_city.cell(row=i+1, column=94).value = city.city_population
                ws_city.cell(row=i+1, column=95).value = city.city_area

        if city_list20:
            for i, city in enumerate(city_list20):
                ws_city.cell(row=i+1, column=96).value = city.city_code
                ws_city.cell(row=i+1, column=97).value = city.city_name
                ws_city.cell(row=i+1, column=98).value = city.ken_code
                ws_city.cell(row=i+1, column=99).value = city.city_population
                ws_city.cell(row=i+1, column=100).value = city.city_area

        if city_list21:
            for i, city in enumerate(city_list21):
                ws_city.cell(row=i+1, column=101).value = city.city_code
                ws_city.cell(row=i+1, column=102).value = city.city_name
                ws_city.cell(row=i+1, column=103).value = city.ken_code
                ws_city.cell(row=i+1, column=104).value = city.city_population
                ws_city.cell(row=i+1, column=105).value = city.city_area

        if city_list22:
            for i, city in enumerate(city_list22):
                ws_city.cell(row=i+1, column=106).value = city.city_code
                ws_city.cell(row=i+1, column=107).value = city.city_name
                ws_city.cell(row=i+1, column=108).value = city.ken_code
                ws_city.cell(row=i+1, column=109).value = city.city_population
                ws_city.cell(row=i+1, column=110).value = city.city_area

        if city_list23:
            for i, city in enumerate(city_list23):
                ws_city.cell(row=i+1, column=111).value = city.city_code
                ws_city.cell(row=i+1, column=112).value = city.city_name
                ws_city.cell(row=i+1, column=113).value = city.ken_code
                ws_city.cell(row=i+1, column=114).value = city.city_population
                ws_city.cell(row=i+1, column=115).value = city.city_area

        if city_list24:
            for i, city in enumerate(city_list24):
                ws_city.cell(row=i+1, column=116).value = city.city_code
                ws_city.cell(row=i+1, column=117).value = city.city_name
                ws_city.cell(row=i+1, column=118).value = city.ken_code
                ws_city.cell(row=i+1, column=119).value = city.city_population
                ws_city.cell(row=i+1, column=120).value = city.city_area

        if city_list25:
            for i, city in enumerate(city_list25):
                ws_city.cell(row=i+1, column=121).value = city.city_code
                ws_city.cell(row=i+1, column=122).value = city.city_name
                ws_city.cell(row=i+1, column=123).value = city.ken_code
                ws_city.cell(row=i+1, column=124).value = city.city_population
                ws_city.cell(row=i+1, column=125).value = city.city_area

        if city_list26:
            for i, city in enumerate(city_list26):
                ws_city.cell(row=i+1, column=126).value = city.city_code
                ws_city.cell(row=i+1, column=127).value = city.city_name
                ws_city.cell(row=i+1, column=128).value = city.ken_code
                ws_city.cell(row=i+1, column=129).value = city.city_population
                ws_city.cell(row=i+1, column=130).value = city.city_area

        if city_list27:
            for i, city in enumerate(city_list27):
                ws_city.cell(row=i+1, column=131).value = city.city_code
                ws_city.cell(row=i+1, column=132).value = city.city_name
                ws_city.cell(row=i+1, column=133).value = city.ken_code
                ws_city.cell(row=i+1, column=134).value = city.city_population
                ws_city.cell(row=i+1, column=135).value = city.city_area

        if city_list28:
            for i, city in enumerate(city_list28):
                ws_city.cell(row=i+1, column=136).value = city.city_code
                ws_city.cell(row=i+1, column=137).value = city.city_name
                ws_city.cell(row=i+1, column=138).value = city.ken_code
                ws_city.cell(row=i+1, column=139).value = city.city_population
                ws_city.cell(row=i+1, column=140).value = city.city_area

        if city_list29:
            for i, city in enumerate(city_list29):
                ws_city.cell(row=i+1, column=141).value = city.city_code
                ws_city.cell(row=i+1, column=142).value = city.city_name
                ws_city.cell(row=i+1, column=143).value = city.ken_code
                ws_city.cell(row=i+1, column=144).value = city.city_population
                ws_city.cell(row=i+1, column=145).value = city.city_area

        if city_list30:
            for i, city in enumerate(city_list30):
                ws_city.cell(row=i+1, column=146).value = city.city_code
                ws_city.cell(row=i+1, column=147).value = city.city_name
                ws_city.cell(row=i+1, column=148).value = city.ken_code
                ws_city.cell(row=i+1, column=149).value = city.city_population
                ws_city.cell(row=i+1, column=150).value = city.city_area

        if city_list31:
            for i, city in enumerate(city_list31):
                ws_city.cell(row=i+1, column=151).value = city.city_code
                ws_city.cell(row=i+1, column=152).value = city.city_name
                ws_city.cell(row=i+1, column=153).value = city.ken_code
                ws_city.cell(row=i+1, column=154).value = city.city_population
                ws_city.cell(row=i+1, column=155).value = city.city_area

        if city_list32:
            for i, city in enumerate(city_list32):
                ws_city.cell(row=i+1, column=156).value = city.city_code
                ws_city.cell(row=i+1, column=157).value = city.city_name
                ws_city.cell(row=i+1, column=158).value = city.ken_code
                ws_city.cell(row=i+1, column=159).value = city.city_population
                ws_city.cell(row=i+1, column=160).value = city.city_area

        if city_list33:
            for i, city in enumerate(city_list33):
                ws_city.cell(row=i+1, column=161).value = city.city_code
                ws_city.cell(row=i+1, column=162).value = city.city_name
                ws_city.cell(row=i+1, column=163).value = city.ken_code
                ws_city.cell(row=i+1, column=164).value = city.city_population
                ws_city.cell(row=i+1, column=165).value = city.city_area

        if city_list34:
            for i, city in enumerate(city_list34):
                ws_city.cell(row=i+1, column=166).value = city.city_code
                ws_city.cell(row=i+1, column=167).value = city.city_name
                ws_city.cell(row=i+1, column=168).value = city.ken_code
                ws_city.cell(row=i+1, column=160).value = city.city_population
                ws_city.cell(row=i+1, column=170).value = city.city_area

        if city_list35:
            for i, city in enumerate(city_list35):
                ws_city.cell(row=i+1, column=171).value = city.city_code
                ws_city.cell(row=i+1, column=172).value = city.city_name
                ws_city.cell(row=i+1, column=173).value = city.ken_code
                ws_city.cell(row=i+1, column=174).value = city.city_population
                ws_city.cell(row=i+1, column=175).value = city.city_area

        if city_list36:
            for i, city in enumerate(city_list36):
                ws_city.cell(row=i+1, column=176).value = city.city_code
                ws_city.cell(row=i+1, column=177).value = city.city_name
                ws_city.cell(row=i+1, column=178).value = city.ken_code
                ws_city.cell(row=i+1, column=179).value = city.city_population
                ws_city.cell(row=i+1, column=180).value = city.city_area

        if city_list37:
            for i, city in enumerate(city_list37):
                ws_city.cell(row=i+1, column=181).value = city.city_code
                ws_city.cell(row=i+1, column=182).value = city.city_name
                ws_city.cell(row=i+1, column=183).value = city.ken_code
                ws_city.cell(row=i+1, column=184).value = city.city_population
                ws_city.cell(row=i+1, column=185).value = city.city_area

        if city_list38:
            for i, city in enumerate(city_list38):
                ws_city.cell(row=i+1, column=186).value = city.city_code
                ws_city.cell(row=i+1, column=187).value = city.city_name
                ws_city.cell(row=i+1, column=188).value = city.ken_code
                ws_city.cell(row=i+1, column=189).value = city.city_population
                ws_city.cell(row=i+1, column=190).value = city.city_area

        if city_list39:
            for i, city in enumerate(city_list39):
                ws_city.cell(row=i+1, column=191).value = city.city_code
                ws_city.cell(row=i+1, column=192).value = city.city_name
                ws_city.cell(row=i+1, column=193).value = city.ken_code
                ws_city.cell(row=i+1, column=194).value = city.city_population
                ws_city.cell(row=i+1, column=195).value = city.city_area

        if city_list40:
            for i, city in enumerate(city_list40):
                ws_city.cell(row=i+1, column=196).value = city.city_code
                ws_city.cell(row=i+1, column=197).value = city.city_name
                ws_city.cell(row=i+1, column=198).value = city.ken_code
                ws_city.cell(row=i+1, column=199).value = city.city_population
                ws_city.cell(row=i+1, column=200).value = city.city_area

        if city_list41:
            for i, city in enumerate(city_list41):
                ws_city.cell(row=i+1, column=201).value = city.city_code
                ws_city.cell(row=i+1, column=202).value = city.city_name
                ws_city.cell(row=i+1, column=203).value = city.ken_code
                ws_city.cell(row=i+1, column=204).value = city.city_population
                ws_city.cell(row=i+1, column=205).value = city.city_area

        if city_list42:
            for i, city in enumerate(city_list42):
                ws_city.cell(row=i+1, column=206).value = city.city_code
                ws_city.cell(row=i+1, column=207).value = city.city_name
                ws_city.cell(row=i+1, column=208).value = city.ken_code
                ws_city.cell(row=i+1, column=209).value = city.city_population
                ws_city.cell(row=i+1, column=210).value = city.city_area

        if city_list43:
            for i, city in enumerate(city_list43):
                ws_city.cell(row=i+1, column=211).value = city.city_code
                ws_city.cell(row=i+1, column=212).value = city.city_name
                ws_city.cell(row=i+1, column=213).value = city.ken_code
                ws_city.cell(row=i+1, column=214).value = city.city_population
                ws_city.cell(row=i+1, column=215).value = city.city_area

        if city_list44:
            for i, city in enumerate(city_list44):
                ws_city.cell(row=i+1, column=216).value = city.city_code
                ws_city.cell(row=i+1, column=217).value = city.city_name
                ws_city.cell(row=i+1, column=218).value = city.ken_code
                ws_city.cell(row=i+1, column=219).value = city.city_population
                ws_city.cell(row=i+1, column=220).value = city.city_area

        if city_list45:
            for i, city in enumerate(city_list45):
                ws_city.cell(row=i+1, column=221).value = city.city_code
                ws_city.cell(row=i+1, column=222).value = city.city_name
                ws_city.cell(row=i+1, column=223).value = city.ken_code
                ws_city.cell(row=i+1, column=224).value = city.city_population
                ws_city.cell(row=i+1, column=225).value = city.city_area

        if city_list46:
            for i, city in enumerate(city_list46):
                ws_city.cell(row=i+1, column=226).value = city.city_code
                ws_city.cell(row=i+1, column=227).value = city.city_name
                ws_city.cell(row=i+1, column=228).value = city.ken_code
                ws_city.cell(row=i+1, column=229).value = city.city_population
                ws_city.cell(row=i+1, column=230).value = city.city_area

        if city_list47:
            for i, city in enumerate(city_list47):
                ws_city.cell(row=i+1, column=231).value = city.city_code
                ws_city.cell(row=i+1, column=232).value = city.city_name
                ws_city.cell(row=i+1, column=233).value = city.ken_code
                ws_city.cell(row=i+1, column=234).value = city.city_population
                ws_city.cell(row=i+1, column=235).value = city.city_area

        print("download_ippan_chosa6", flush=True)
        ### 04: 水害発生地点工種（河川海岸区分）
        kasen_kaigan_list = KASEN_KAIGAN.objects.order_by('kasen_kaigan_code')[:]
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws_kasen_kaigan.cell(row=i+1, column=1).value = kasen_kaigan.kasen_kaigan_code
                ws_kasen_kaigan.cell(row=i+1, column=2).value = kasen_kaigan.kasen_kaigan_name

        print("download_ippan_chosa7", flush=True)
        ### 05: 水系（水系・沿岸）
        suikei_list = SUIKEI.objects.order_by('suikei_code')[:]
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws_suikei.cell(row=i+1, column=1).value = suikei.suikei_code
                ws_suikei.cell(row=i+1, column=2).value = suikei.suikei_name
                ws_suikei.cell(row=i+1, column=3).value = suikei.suikei_type_code

        print("download_ippan_chosa8", flush=True)
        ### 06: 水系種別（水系・沿岸種別）
        suikei_type_list = SUIKEI_TYPE.objects.order_by('suikei_type_code')[:]
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws_suikei_type.cell(row=i+1, column=1).value = suikei_type.suikei_type_code
                ws_suikei_type.cell(row=i+1, column=2).value = suikei_type.suikei_type_name

        print("download_ippan_chosa9", flush=True)
        ### 07: 河川（河川・海岸）
        kasen_list = KASEN.objects.order_by('kasen_code')[:]
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws_kasen.cell(row=i+1, column=1).value = kasen.kasen_code
                ws_kasen.cell(row=i+1, column=2).value = kasen.kasen_name
                ws_kasen.cell(row=i+1, column=3).value = kasen.kasen_type_code
                ws_kasen.cell(row=i+1, column=4).value = kasen.suikei_code
                
        print("download_ippan_chosa10", flush=True)
        ### 08: 河川種別（河川・海岸種別）
        kasen_type_list = KASEN_TYPE.objects.order_by('kasen_type_code')[:]
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws_kasen_type.cell(row=i+1, column=1).value = kasen_type.kasen_type_code
                ws_kasen_type.cell(row=i+1, column=2).value = kasen_type.kasen_type_name
        
        print("download_ippan_chosa11", flush=True)
        ### 09: 水害原因
        cause_list = CAUSE.objects.order_by('cause_code')[:]
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws_cause.cell(row=i+1, column=1).value = cause.cause_code
                ws_cause.cell(row=i+1, column=2).value = cause.cause_name
                
        print("download_ippan_chosa12", flush=True)
        ### 10: 地上地下区分
        underground_list = UNDERGROUND.objects.order_by('underground_code')[:]
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws_underground.cell(row=i+1, column=1).value = underground.underground_code
                ws_underground.cell(row=i+1, column=2).value = underground.underground_name
        
        print("download_ippan_chosa13", flush=True)
        ### 11: 地下空間の利用形態
        usage_list = USAGE.objects.order_by('usage_code')[:]
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws_usage.cell(row=i+1, column=1).value = usage.usage_code
                ws_usage.cell(row=i+1, column=2).value = usage.usage_name
        
        print("download_ippan_chosa14", flush=True)
        ### 12: 浸水土砂区分
        flood_sediment_list = FLOOD_SEDIMENT.objects.order_by('flood_sediment_code')[:]
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws_flood_sediment.cell(row=i+1, column=1).value = flood_sediment.flood_sediment_code
                ws_flood_sediment.cell(row=i+1, column=2).value = flood_sediment.flood_sediment_name
        
        print("download_ippan_chosa15", flush=True)
        ### 13: 地盤勾配区分
        gradient_list = GRADIENT.objects.order_by('gradient_code')[:]
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws_gradient.cell(row=i+1, column=1).value = gradient.gradient_code
                ws_gradient.cell(row=i+1, column=2).value = gradient.gradient_name
        
        print("download_ippan_chosa16", flush=True)
        ### 14: 産業分類
        industry_list = INDUSTRY.objects.order_by('industry_code')[:]
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws_industry.cell(row=i+1, column=1).value = industry.industry_code
                ws_industry.cell(row=i+1, column=2).value = industry.industry_name
        
        print("download_ippan_chosa17", flush=True)
        ### 25: 区域
        area_list = AREA.objects.order_by('area_id')[:]
        if area_list:
            for i, area in enumerate(area_list):
                ws_area.cell(row=i+1, column=1).value = area.area_id
                ws_area.cell(row=i+1, column=2).value = area.area_name
                ws_area.cell(row=i+1, column=3).value = area.area_year
                ws_area.cell(row=i+1, column=4).value = area.begin_date
                ws_area.cell(row=i+1, column=5).value = area.end_date
                ws_area.cell(row=i+1, column=6).value = area.agri_area
                ws_area.cell(row=i+1, column=7).value = area.underground_area
                ws_area.cell(row=i+1, column=8).value = area.crop_damage
        
        print("download_ippan_chosa18", flush=True)
        ippan_list = IPPAN.objects.order_by('ippan_id')[:]
        ws_ippan.cell(row=5, column=2).value = '都道府県'
        ws_ippan.cell(row=5, column=3).value = '市区町村'
        ws_ippan.cell(row=5, column=4).value = '水害発生月日'
        ws_ippan.cell(row=5, column=5).value = '水害終了月日'
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

        print("download_ippan_chosa19", flush=True)
        ### 01: 建物区分
        dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$%d" % len(building_list))
        dv_building.ranges = 'C20:C1048576'
        ws_ippan.add_data_validation(dv_building)

        print("download_ippan_chosa20", flush=True)
        ### 02: 都道府県
        dv_ken = DataValidation(type="list", formula1="KEN!$B$1:$B$%d" % len(ken_list))
        dv_ken.ranges = 'B7:B7'
        ws_ippan.add_data_validation(dv_ken)
        
        print("download_ippan_chosa21", flush=True)
        ### 03: 市区町村
        ### ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK.A:B,2,0)" ### FOR LINUX
        ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK!A:B,2,0)" ### FOR WINDOWS
        dv_city = DataValidation(type="list", formula1="=INDIRECT(AD3)")
        dv_city.ranges = 'C7:C7'
        ws_ippan.add_data_validation(dv_city)
        
        print("download_ippan_chosa22", flush=True)
        ### 04: 水害発生地点工種（河川海岸区分）
        dv_kasen_kaigan = DataValidation(type="list", formula1="KASEN_KAIGAN!$B$1:$B$%d" % len(kasen_kaigan_list))
        dv_kasen_kaigan.ranges = 'F14:F14'
        ws_ippan.add_data_validation(dv_kasen_kaigan)
        
        print("download_ippan_chosa23", flush=True)
        ### 05: 水系（水系・沿岸）
        dv_suikei = DataValidation(type="list", formula1="SUIKEI!$B$1:$B$%d" % len(suikei_list))
        dv_suikei.ranges = 'B10:B10'
        ws_ippan.add_data_validation(dv_suikei)
        
        print("download_ippan_chosa24", flush=True)
        ### 06: 水系種別（水系・沿岸種別）
        dv_suikei_type = DataValidation(type="list", formula1="SUIKEI_TYPE!$B$1:$B$%d" % len(suikei_type_list))
        dv_suikei_type.ranges = 'C10:C10'
        ws_ippan.add_data_validation(dv_suikei_type)
        
        print("download_ippan_chosa25", flush=True)
        ### 07: 河川（河川・海岸）
        dv_kasen = DataValidation(type="list", formula1="KASEN!$B$1:$B$%d" % len(kasen_list))
        dv_kasen.ranges = 'D10:D10'
        ws_ippan.add_data_validation(dv_kasen)
        
        print("download_ippan_chosa26", flush=True)
        ### 08: 河川種別（河川・海岸種別）
        dv_kasen_type = DataValidation(type="list", formula1="KASEN_TYPE!$B$1:$B$%d" % len(kasen_type_list))
        dv_kasen_type.ranges = 'E10:E10'
        ws_ippan.add_data_validation(dv_kasen_type)
        
        print("download_ippan_chosa27", flush=True)
        ### 09: 水害原因
        dv_cause = DataValidation(type="list", formula1="CAUSE!$B$1:$B$%d" % len(cause_list))
        dv_cause.ranges = 'F7:H7'
        ws_ippan.add_data_validation(dv_cause)
        
        print("download_ippan_chosa28", flush=True)
        ### 10: 地上地下区分
        dv_underground = DataValidation(type="list", formula1="UNDERGROUND!$B$1:$B$%d" % len(underground_list))
        dv_underground.ranges = 'D20:D1048576'
        ws_ippan.add_data_validation(dv_underground)
        
        print("download_ippan_chosa29", flush=True)
        ### 11: 地下空間の利用形態
        dv_usage = DataValidation(type="list", formula1="USAGE!$B$1:$B$%d" % len(usage_list))
        dv_usage.ranges = 'Z20:Z1048576'
        ws_ippan.add_data_validation(dv_usage)
        
        print("download_ippan_chosa30", flush=True)
        ### 12: 浸水土砂区分
        dv_flood_sediment = DataValidation(type="list", formula1="FLOOD_SEDIMENT!$B$1:$B$%d" % len(flood_sediment_list))
        dv_flood_sediment.ranges = 'E20:E1048576'
        ws_ippan.add_data_validation(dv_flood_sediment)
        
        print("download_ippan_chosa31", flush=True)
        ### 13: 地盤勾配区分
        dv_gradient = DataValidation(type="list", formula1="GRADIENT!$B$1:$B$%d" % len(gradient_list))
        dv_gradient.ranges = 'F10:F10'
        ws_ippan.add_data_validation(dv_gradient)
        
        print("download_ippan_chosa32", flush=True)
        ### 14: 産業分類
        dv_industry = DataValidation(type="list", formula1="INDUSTRY!$B$1:$B$%d" % len(industry_list))
        dv_industry.ranges = 'Y20:Y1048576'
        ws_ippan.add_data_validation(dv_industry)
        
        print("download_ippan_chosa33", flush=True)
        ### 25: 区域
        dv_area = DataValidation(type="list", formula1="AREA!$B$1:$B$%d" % len(area_list))
        dv_area.ranges = 'I7:I7'
        ws_ippan.add_data_validation(dv_area)
        
        print("download_ippan_chosa34", flush=True)
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws_ippan.cell(row=i+20, column=2).value = ippan.ippan_name
                ws_ippan.cell(row=i+20, column=3).value = '戸建住宅'
                ws_ippan.cell(row=i+20, column=4).value = '地上のみ'
                ws_ippan.cell(row=i+20, column=5).value = '浸水'
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
                ws_ippan.cell(row=i+20, column=25).value = '建設業'
                ws_ippan.cell(row=i+20, column=26).value = '住居'
                ws_ippan.cell(row=i+20, column=27).value = ''

        ### dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$6")
        ### dv_building.ranges = 'C20:C1048576'
        ### ws_ippan.add_data_validation(dv_building)
        
        gray_fill = PatternFill(bgColor='C0C0C0', fill_type='solid')
        white_fill = PatternFill(bgColor='FFFFFF', fill_type='solid')
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="戸建住宅"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="共同住宅"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="事業所併用住宅"'], fill=white_fill))
        ws_ippan.conditional_formatting.add('M20:M1048576', FormulaRule(formula=['$C20="事業所"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('M20:N1048576', FormulaRule(formula=['$C20="その他建物"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('T20:Y1048576', FormulaRule(formula=['$C20="その他建物"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('F20:Z1048576', FormulaRule(formula=['$C20="建物以外"'], fill=gray_fill))
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_ippan_chosa()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_ippan_chosa().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_chosa()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_chosa()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_ippan_city関数
### 2602: 一般資産調査票（市区町村用）
###############################################################################
def download_ippan_city(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_city()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_city()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        ippan_list = IPPAN.objects.order_by('ippan_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/ippan_city1.xlsx'
        file_path_to_save = 'static/ippan_city2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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

        ### dv = DataValidation(type="list", formula1="$B$1:$B$10")
        ### dv.ranges = 'F7:I7'
        ### ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_ippan_city()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_city.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_ippan_city().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_city()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_city()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_ippan_ken関数
### 2603: 一般資産調査票（都道府県用）
###############################################################################
def download_ippan_ken(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_ken()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_ippan_ken()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        ippan_list = IPPAN.objects.order_by('ippan_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/ippan_ken1.xlsx'
        file_path_to_save = 'static/ippan_ken2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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

        ### dv = DataValidation(type="list", formula1="$B$1:$B$10")
        ### dv.ranges = 'F7:I7'
        ### ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_ippan_ken()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_ken.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_ippan_ken().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_ken()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_ippan_ken()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_restoration関数
### 27: 復旧事業工種
###############################################################################
def download_restoration(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_restoration()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_restoration()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        restoration_list = RESTORATION.objects.order_by('restoration_code')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/restoration.xlsx'
        file_path_to_save = 'static/restoration2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '復旧事業工種'
        ws.cell(row=1, column=1).value = '復旧事業工種コード'
        ws.cell(row=1, column=2).value = '復旧事業工種名'
        
        if restoration_list:
            for i, restoration in enumerate(restoration_list):
                ws.cell(row=i+2, column=1).value = restoration.restoration_code
                ws.cell(row=i+2, column=2).value = restoration.restoration_name
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_restoration()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="restoration.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_restoration().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_restoration()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_restoration()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_kokyo関数
### 28: 公共土木調査票
###############################################################################
def download_kokyo(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kokyo()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_kokyo()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        kokyo_list = KOKYO.objects.order_by('kokyo_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/kokyo.xlsx'
        file_path_to_save = 'static/kokyo2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
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
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_kokyo()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kokyo.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_kokyo().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kokyo()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_kokyo()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### download_koeki関数
### 29: 公益事業調査票
###############################################################################
def download_koeki(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_koeki()関数が開始しました。', 'INFO')
        print_log('[INFO] P0200ExcelDownload.download_koeki()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### DBアクセス処理
        ### DBにアクセスして、データを取得する。
        #######################################################################
        koeki_list = KOEKI.objects.order_by('koeki_id')[:]
    
        #######################################################################
        ### EXCEL入出力処理
        ### テンプレート用のEXCELファイルを読み込む。
        ### セルにデータをセットして、ダウンロード用のEXCELファイルを保存する。
        #######################################################################
        file_path_to_load = 'static/koeki.xlsx'
        file_path_to_save = 'static/koeki2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = '公益事業調査票'
        ws.cell(row=i+1, column=1).value = '公益事業調査票ID'
        ws.cell(row=i+1, column=2).value = '都道府県コード'
        ws.cell(row=i+1, column=3).value = '市区町村コード'
        ws.cell(row=i+1, column=4).value = '異常気象ID'
        ws.cell(row=i+1, column=5).value = '公益事業調査対象年'
        ws.cell(row=i+1, column=6).value = '開始日'
        ws.cell(row=i+1, column=7).value = '終了日'
        
        if koeki_list:
            for i, koeki in enumerate(koeki_list):
                ws.cell(row=i+1, column=1).value = koeki.kokyo_id
                ws.cell(row=i+1, column=2).value = koeki.ken_code
                ws.cell(row=i+1, column=3).value = koeki.city_code
                ws.cell(row=i+1, column=4).value = koeki.weather_id
                ws.cell(row=i+1, column=5).value = koeki.koeki_year
                ws.cell(row=i+1, column=6).value = koeki.begin_date
                ws.cell(row=i+1, column=7).value = koeki.end_date
        
        wb.save(file_path_to_save)
        
        #######################################################################
        ### HttpResponse処理
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0200ExcelDownload.download_koeki()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="koeki.xlsx"'
        
    except:
        ### raise Http404("[ERROR] download_koeki().")
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_koeki()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0200ExcelDownload.download_koeki()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

