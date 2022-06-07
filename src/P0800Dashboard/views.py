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
        ### (2)家庭用品自動車以外被害額 = 世帯数 x 浸水または土砂ごとの家庭用品被害率 x 家庭用品自動車以外所有額
        ### (3)家庭用品自動車被害額 = 世帯数 x 自動車被害率 x 家庭用品自動車所有額
        ### (4)家庭応急対策費 = (世帯数 x 活動費) + (世帯数 x 清掃日数 x 清掃労働単価)
        ### (5)事業所被害額 = 従業者数 x 産業分類ごとの償却資産 x 浸水または土砂ごとの被害率 + 
        ### 　　　　　　　　　従業者数 x 産業分類ごとの在庫資産 x 浸水または土砂ごとの被害率
        ### (6)事業所営業損失額 = 従業者数 x (営業停止日数 + 停滞日数/2) x 付加価値額
        ### (7)農漁家被害額 = 農漁家戸数 x 農漁家の償却資産 x 浸水または土砂ごとの被害率 + 
        ###                   農漁家戸数 x 農漁家の在庫資産 x 浸水または土砂ごとの被害率
        ### (8)事業所応急対策費 = 事業所数 x 代替活動費
        #######################################################################
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 2/3.', 'INFO')
        house_asset_list = None
        house_asset_list = HOUSE_ASSET.objects.raw("""
            SELECT 
                HA1.house_asset_code AS house_asset_code, 
                HA1.ken_code AS ken_code, 
                HA1.house_asset AS house_asset, 
                KE1.ken_name AS ken_name 
            FROM HOUSE_ASSET HA1 
            LEFT JOIN KEN KE1 ON HA1.ken_code = KE1.ken_code 
            ORDER BY CAST(HA1.HOUSE_ASSET_CODE AS INTEGER)
            """, [])
        house_damage = HOUSE_DAMAGE.objects.raw("""SELECT * FROM HOUSE_DAMAGE ORDER BY CAST(HOUSE_DAMAGE_CODE AS INTEGER)""", [])[0]
        household_damage = HOUSEHOLD_DAMAGE.objects.raw("""SELECT * FROM HOUSEHOLD_DAMAGE ORDER BY CAST(HOUSEHOLD_DAMAGE_CODE AS INTEGER)""", [])[0]
        car_damage = CAR_DAMAGE.objects.raw("""SELECT * FROM CAR_DAMAGE ORDER BY CAST(CAR_DAMAGE_CODE AS INTEGER)""", [])[0]
        house_cost = HOUSE_COST.objects.raw("""SELECT * FROM HOUSE_COST ORDER BY CAST(HOUSE_COST_CODE AS INTEGER)""", [])[0]
        
        office_asset_list = OFFICE_ASSET.objects.raw("""
            SELECT 
                OA1.office_asset_code AS office_asset_code, 
                OA1.depreciable_asset AS depreciable_asset, 
                OA1.inventory_asset AS inventory_asset, 
                OA1.value_added AS value_added, 
                IN1.industry_name AS industry_name 
            FROM OFFICE_ASSET OA1 
            LEFT JOIN INDUSTRY IN1 ON OA1.industry_code = IN1.industry_code 
            ORDER BY CAST(OA1.OFFICE_ASSET_CODE AS INTEGER)
            """, [])
        
        office_damage = OFFICE_DAMAGE.objects.raw("""SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)""", [])[0]
        office_cost = OFFICE_COST.objects.raw("""SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)""", [])[0]
        farmer_fisher_damage = FARMER_FISHER_DAMAGE.objects.raw("""SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)""", [])[0]
        
        ippan_list = IPPAN.objects.raw("""
            SELECT 
                IP1.ippan_id AS ippan_id, 
                IP1.ippan_name AS ippan_name, 
                IP1.suigai_id AS suigai_id, 
                IP1.building_code AS building_code, 
                IP1.underground_code AS underground_code, 
                IP1.flood_sediment_code AS flood_sediment_code, 
                IP1.industry_code AS industry_code, 
                IP1.usage_code AS usage_code, 
                -- IP1.comment AS comment, 
                
                BD1.building_name AS building_name, 
                UD1.underground_name AS underground_name, 
                FL1.flood_sediment_name AS flood_sediment_name, 
                IN1.industry_name AS industry_name, 
                US1.usage_name AS usage_name, 
                
                IP1.building_lv00 AS building_lv00, 
                IP1.building_lv01_49 AS building_lv01_49, 
                IP1.building_lv50_99 AS building_lv50_99, 
                IP1.building_lv100 AS building_lv100, 
                IP1.building_half AS building_half, 
                IP1.building_full AS building_full, 

                CASE WHEN (IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full) <= 0 THEN NULL ELSE (IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full) END AS sum_building, 
                
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv00/IP1.floor_area) END AS building_lv00_reverse, 
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv01_49/IP1.floor_area) END AS building_lv01_49_reverse, 
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv50_99/IP1.floor_area) END AS building_lv50_99_reverse, 
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv100/IP1.floor_area) END AS building_lv100_reverse, 
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_half/IP1.floor_area) END AS building_half_reverse, 
                CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_full/IP1.floor_area) END AS building_full_reverse, 
                
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
                -- IP1.farmer_fisher_half AS farmer_fisher_half, 
                IP1.farmer_fisher_full AS farmer_fisher_full, 
                
                IP1.employee_lv00 AS employee_lv00, 
                IP1.employee_lv01_49 AS employee_lv01_49, 
                IP1.employee_lv50_99 AS employee_lv50_99, 
                IP1.employee_lv100 AS employee_lv100, 
                -- IP1.employee_half AS employee_half, 
                IP1.employee_full AS employee_full 
                
            FROM IPPAN IP1 
            LEFT JOIN BUILDING BD1 ON IP1.building_code = BD1.building_code 
            LEFT JOIN UNDERGROUND UD1 ON IP1.underground_code = UD1.underground_code 
            LEFT JOIN FLOOD_SEDIMENT FL1 ON IP1.flood_sediment_code = FL1.flood_sediment_code 
            LEFT JOIN INDUSTRY IN1 ON IP1.industry_code = IN1.industry_code 
            LEFT JOIN USAGE US1 ON IP1.usage_code = US1.usage_code 
            ORDER BY CAST(IP1.IPPAN_ID AS INTEGER)
            """, [])

        ### ippan_view_list = IPPAN_VIEW.objects.raw("""
        ###     SELECT 
        ###         IP1.ippan_id AS ippan_id, 
        ###         IP1.ippan_name AS ippan_name, 
        ###         IP1.suigai_id AS suigai_id, 
        ###         IP1.building_code AS building_code, 
        ###         IP1.building_name AS building_name, 
        ###         IP1.underground_code AS underground_code, 
        ###         IP1.underground_name AS underground_name, 
        ###         IP1.flood_sediment_code AS flood_sediment_code, 
        ###         IP1.flood_sediment_name AS flood_sediment_name, 
        ###         IP1.industry_code AS industry_code, 
        ###         IP1.industry_name AS industry_name, 
        ###         IP1.usage_code AS usage_code, 
        ###         IP1.usage_name AS usage_name, 
        ###         -- IP1.comment AS comment, 
        ###         
        ###         IP1.building_lv00 AS building_lv00, 
        ###         IP1.building_lv01_49 AS building_lv01_49, 
        ###         IP1.building_lv50_99 AS building_lv50_99, 
        ###         IP1.building_lv100 AS building_lv100, 
        ###         IP1.building_half AS building_half, 
        ###         IP1.building_full AS building_full, 
        ###         IP1.total_building AS total_building, 
 
        ###         IP1.floor_area AS floor_area, 
        ###         IP1.family AS family, 
        ###         IP1.office AS office, 

        ###         IP1.floor_area_lv00 AS floor_area_lv00, 
        ###         IP1.floor_area_lv01_49 AS floor_area_lv01_49, 
        ###         IP1.floor_area_lv50_99 AS floor_area_lv50_99, 
        ###         IP1.floor_area_lv100 AS floor_area_lv100, 
        ###         IP1.floor_area_half AS floor_area_half, 
        ###         IP1.floor_area_full AS floor_area_full, 
        ###         IP1.total_floor_area AS total_floor_area, 
                
        ###         IP1.family_lv00 AS family_lv00, 
        ###         IP1.family_lv01_49 AS family_lv01_49, 
        ###         IP1.family_lv50_99 AS family_lv50_99, 
        ###         IP1.family_lv100 AS family_lv100, 
        ###         IP1.family_half AS family_half, 
        ###         IP1.family_full AS family_full, 
        ###         IP1.total_family AS total_family, 
                
        ###         IP1.office_lv00 AS office_lv00, 
        ###         IP1.office_lv01_49 AS office_lv01_49, 
        ###         IP1.office_lv50_99 AS office_lv50_99, 
        ###         IP1.office_lv100 AS office_lv100, 
        ###         IP1.office_half AS office_half, 
        ###         IP1.office_full AS office_full, 
        ###         IP1.total_office AS total_office, 
                
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_lv00 / IP1.floor_area) END AS building_lv00_reverse_floor_area, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_lv01_49 / IP1.floor_area) END AS building_lv01_49_reverse_floor_area, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_lv50_99 / IP1.floor_area) END AS building_lv50_99_reverse_floor_area, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_lv100 / IP1.floor_area) END AS building_lv100_reverse_floor_area, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_half / IP1.floor_area) END AS building_half_reverse_floor_area, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.floor_area_full / IP1.floor_area) END AS building_full_reverse_floor_area, 

        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_lv00 / IP1.family) END AS building_lv00_reverse_family, 
        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_lv01_49 / IP1.family) END AS building_lv01_49_reverse_family, 
        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_lv50_99 / IP1.family) END AS building_lv50_99_reverse_family, 
        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_lv100 / IP1.family) END AS building_lv100_reverse_family, 
        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_half / IP1.family) END AS building_half_reverse_family, 
        ###         CASE WHEN (IP1.family) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.family_full / IP1.family) END AS building_full_reverse_family, 

        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_lv00 / IP1.office) END AS building_lv00_reverse_office, 
        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_lv01_49 / IP1.office) END AS building_lv01_49_reverse_office, 
        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_lv50_99 / IP1.office) END AS building_lv50_99_reverse_office, 
        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_lv100 / IP1.office) END AS building_lv100_reverse_office, 
        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_half / IP1.office) END AS building_half_reverse_office, 
        ###         CASE WHEN (IP1.office) <= 0 THEN NULL ELSE ((IP1.total_building) * IP1.office_full / IP1.office) END AS building_full_reverse_office, 
                
        ###         CASE 
        ###         WHEN IP1.flood_sediment_code = '1' THEN 
        ###             CASE 
        ###             WHEN IP1.gradient_code = '1' THEN 
        ###                 CASE WHEN (IS1.house_asset * IS1.fl_gr1_lv00) <= 0 THEN NULL ELSE (IS1.house_damage_lv00 / (IS1.house_asset * IS1.fl_gr1_lv00)) END AS floor_area_lv00_reverse_house_damage, 
        ###             WHEN IP1.gradient_code = '2' THEN 
        ###                 CASE WHEN (IS1.house_asset * IS1.fl_gr2_lv00) <= 0 THEN NULL ELSE (IS1.house_damage_lv00 / (IS1.house_asset * IS1.fl_gr2_lv00)) END AS floor_area_lv00_reverse_house_damage, 
        ###             WHEN IP1.gradient_code = '3' THEN 
        ###                 CASE WHEN (IS1.house_asset * IS1.fl_gr3_lv00) <= 0 THEN NULL ELSE (IS1.house_damage_lv00 / (IS1.house_asset * IS1.fl_gr3_lv00)) END AS floor_area_lv00_reverse_house_damage, 
        ###             END             
        ###         WHEN IP1.flood_sediment_code = '2' THEN 
        ###             CASE 
        ###             WHEN () <= 0 THEN NULL ELSE () END AS floor_area_lv01_49_reverse_house_damage, 
        ###         END 
                
        ###         IP1.farmer_fisher_lv00 AS farmer_fisher_lv00, 
        ###         IP1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49, 
        ###         IP1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99, 
        ###         IP1.farmer_fisher_lv100 AS farmer_fisher_lv100, 
        ###         -- IP1.farmer_fisher_half AS farmer_fisher_half, 
        ###         IP1.farmer_fisher_full AS farmer_fisher_full, 
        ###         IP1.total_farmer_fisher AS total_farmer_fisher, 
                
        ###         IP1.employee_lv00 AS employee_lv00, 
        ###         IP1.employee_lv01_49 AS employee_lv01_49, 
        ###         IP1.employee_lv50_99 AS employee_lv50_99, 
        ###         IP1.employee_lv100 AS employee_lv100, 
        ###         -- IP1.employee_half AS employee_half, 
        ###         IP1.employee_full AS employee_full,
        ###         IP1.total_employee AS total_employee 
        ###         
        ###     FROM IPPAN_VIEW IP1 
        ###     ORDER BY CAST(IP1.IPPAN_ID AS INTEGER)
        ###     """, [])


        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])

        #######################################################################
        ### レスポンスセット処理(0010)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0800Dashboard/index.html')
        context = {
            'category_code': category_code, 
            'house_asset_list': house_asset_list, 
            'house_damage': house_damage, 
            'household_damage': household_damage, 
            'car_damage': car_damage, 
            'house_cost': house_cost, 
            'office_asset_list': office_asset_list, 
            'office_damage': office_damage, 
            'office_cost': office_cost, 
            'farmer_fisher_damage': farmer_fisher_damage, 
            'ippan_list': ippan_list, 
            'gradient_list': gradient_list, 
        }
        print_log('[INFO] P0800Dashboard.category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
