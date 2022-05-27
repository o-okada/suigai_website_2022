#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0800Dashboard/views.py
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
        print_log('[INFO] P0800Dashboard.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0800Dashboard.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0800Dashboard.index_view()関数 STEP 1/2.', 'INFO')

        #######################################################################
        ### レスポンスセット処理(0010)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0800Dashboard.index_view()関数 STEP 2/2.', 'INFO')
        template = loader.get_template('P0800Dashboard/index.html')
        context = {}
        print_log('[INFO] P0800Dashboard.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0800Dashboard.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Dashboard.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：category_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def category_view(request, category_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### (1)ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0800Dashboard.category_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0800Dashboard.category_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0800Dashboard.category_view()関数 category_code = {}'.format(category_code), 'INFO')
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 1/3.', 'INFO')

        #######################################################################
        ### DBアクセス処理(0010)
        ### (1)DBにアクセスして、下記の計算式に用いるデータを取得する。
        ### (1)家屋被害額 = 延床面積 x 家屋評価額 x 浸水または土砂ごとの勾配差による被害率
        ### (2)家庭用品自動車以外被害額 = 世帯数 x 浸水または土砂ごとの家庭用品被害率家庭用品所有額
        ### (3)家庭用品自動車被害額 = 世帯数 x 自動車被害率 x 家庭用品所有額
        ### (4)家庭応急対策費 = (世帯数 x 活動費) + (世帯数 x 清掃日数 x 清掃労働単価)
        ### (5)事業所被害額 = 従業者数 x 産業分類ごとの償却資産 x 浸水または土砂ごとの被害率 + 
        ### 　　　　　　　　　従業者数 x 産業分類ごとの在庫資産 x 浸水または土砂ごとの被害率
        ### (6)事業所営業損失額 = 従業者数 x (営業停止日数 + 停滞日数/2) x 付加価値額
        ### (7)農漁家被害額 = 農漁家戸数 x 農漁家の償却資産 x 浸水または土砂ごとの被害率 + 
        ###                   農漁家戸数 x 農漁家の在庫資産 x 浸水または土砂ごとの被害率
        ### (8)事業所応急対策費 = 事業所数 x 代替活動費
        #######################################################################
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 2/3.', 'INFO')
        house_asset_list = HOUSE_ASSET.objects.raw("""SELECT * FROM HOUSE_ASSET ORDER BY CAST(HOUSE_ASSET_CODE AS INTEGER)""", [])
        house_damage_list = HOUSE_DAMAGE.objects.raw("""SELECT * FROM HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)""", [])
        household_damage_list = HOUSEHOLD_DAMAGE.objects.raw("""SELECT * FROM HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)""", [])
        car_damage_list = CAR_DAMAGE.objects.raw("""SELECT * FROM CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)""", [])
        house_cost_list = HOUSE_COST.objects.raw("""SELECT * FROM HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)""", [])
        office_asset_list = OFFICE_ASSET.objects.raw("""SELECT * FROM OFFICE_ASSET ORDER BY CAST(OFFICE_ASSET_CODE AS INTEGER)""", [])
        office_damage_list = OFFICE_DAMAGE.objects.raw("""SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)""", [])
        office_cost_list = OFFICE_COST.objects.raw("""SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)""", [])
        farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.raw("""SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)""", [])
        ippan_list = IPPAN.objects.raw("""SELECT * FROM IPPAN ORDER BY CAST(IPPAN_ID)""", [])

        #######################################################################
        ### レスポンスセット処理(0010)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0800Dashboard/index.html')
        context = {
            'category_code': category_code, 
            'house_asset_list': house_asset_list, 
            'house_damage_list': house_damage_list, 
            'household_damage_list': household_damage_list, 
            'car_damage_list': car_damage_list, 
            'house_cost_list': house_cost_list, 
            'office_asset_list': office_asset_list, 
            'office_damage_list': office_damage_list, 
            'office_cost_list': office_cost_list, 
            'farmer_fisher_damage_list': farmer_fisher_damage_list, 
            'ippan_list': ippan_list, 
        }
        print_log('[INFO] P0800Dashboard.category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
