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

from P0000Common.models import IPPAN_VIEW

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
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 1/6.', 'INFO')

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
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 2/6.', 'INFO')
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
                OA1.office_dep_asset AS office_dep_asset, 
                OA1.office_inv_asset AS office_inv_asset, 
                OA1.office_va_asset AS office_va_asset, 
                IN1.industry_name AS industry_name 
            FROM OFFICE_ASSET OA1 
            LEFT JOIN INDUSTRY IN1 ON OA1.industry_code = IN1.industry_code 
            ORDER BY CAST(OA1.OFFICE_ASSET_CODE AS INTEGER)
            """, [])
        
        office_damage = OFFICE_DAMAGE.objects.raw("""SELECT * FROM OFFICE_DAMAGE ORDER BY CAST(OFFICE_DAMAGE_CODE AS INTEGER)""", [])[0]
        office_cost = OFFICE_COST.objects.raw("""SELECT * FROM OFFICE_COST ORDER BY CAST(OFFICE_COST_CODE AS INTEGER)""", [])[0]
        farmer_fisher_damage = FARMER_FISHER_DAMAGE.objects.raw("""SELECT * FROM FARMER_FISHER_DAMAGE ORDER BY CAST(FARMER_FISHER_DAMAGE_CODE AS INTEGER)""", [])[0]
        
        ### print_log('[INFO] P0800Dashboard.category_view()関数 STEP 3/6.', 'INFO')
        ### ippan_list = IPPAN.objects.raw("""
        ###     SELECT 
        ###         IP1.ippan_id AS ippan_id, 
        ###         IP1.ippan_name AS ippan_name, 
        ###         IP1.suigai_id AS suigai_id, 
        ###         IP1.building_code AS building_code, 
        ###         IP1.underground_code AS underground_code, 
        ###         IP1.flood_sediment_code AS flood_sediment_code, 
        ###         IP1.industry_code AS industry_code, 
        ###         IP1.usage_code AS usage_code, 
        ###         -- IP1.comment AS comment, 
        ###         BD1.building_name AS building_name, 
        ###         UD1.underground_name AS underground_name, 
        ###         FL1.flood_sediment_name AS flood_sediment_name, 
        ###         IN1.industry_name AS industry_name, 
        ###         US1.usage_name AS usage_name, 
        ###         IP1.building_lv00 AS building_lv00, 
        ###         IP1.building_lv01_49 AS building_lv01_49, 
        ###         IP1.building_lv50_99 AS building_lv50_99, 
        ###         IP1.building_lv100 AS building_lv100, 
        ###         IP1.building_half AS building_half, 
        ###         IP1.building_full AS building_full, 
        ###         CASE WHEN (IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full) <= 0 THEN NULL ELSE (IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full) END AS sum_building, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv00/IP1.floor_area) END AS building_lv00_reverse, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv01_49/IP1.floor_area) END AS building_lv01_49_reverse, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv50_99/IP1.floor_area) END AS building_lv50_99_reverse, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_lv100/IP1.floor_area) END AS building_lv100_reverse, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_half/IP1.floor_area) END AS building_half_reverse, 
        ###         CASE WHEN (IP1.floor_area) <= 0 THEN NULL ELSE ((IP1.building_lv00+IP1.building_lv01_49+IP1.building_lv50_99+IP1.building_lv100+IP1.building_half+IP1.building_full)*IP1.floor_area_full/IP1.floor_area) END AS building_full_reverse, 
        ###         IP1.floor_area AS floor_area, 
        ###         IP1.family AS family, 
        ###         IP1.office AS office, 
        ###         IP1.floor_area_lv00 AS floor_area_lv00, 
        ###         IP1.floor_area_lv01_49 AS floor_area_lv01_49, 
        ###         IP1.floor_area_lv50_99 AS floor_area_lv50_99, 
        ###         IP1.floor_area_lv100 AS floor_area_lv100, 
        ###         IP1.floor_area_half AS floor_area_half, 
        ###         IP1.floor_area_full AS floor_area_full, 
        ###         IP1.family_lv00 AS family_lv00, 
        ###         IP1.family_lv01_49 AS family_lv01_49, 
        ###         IP1.family_lv50_99 AS family_lv50_99, 
        ###         IP1.family_lv100 AS family_lv100, 
        ###         IP1.family_half AS family_half, 
        ###         IP1.family_full AS family_full, 
        ###         IP1.office_lv00 AS office_lv00, 
        ###         IP1.office_lv01_49 AS office_lv01_49, 
        ###         IP1.office_lv50_99 AS office_lv50_99, 
        ###         IP1.office_lv100 AS office_lv100, 
        ###         IP1.office_half AS office_half, 
        ###         IP1.office_full AS office_full, 
        ###         IP1.farmer_fisher_lv00 AS farmer_fisher_lv00, 
        ###         IP1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49, 
        ###         IP1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99, 
        ###         IP1.farmer_fisher_lv100 AS farmer_fisher_lv100, 
        ###         -- IP1.farmer_fisher_half AS farmer_fisher_half, 
        ###         IP1.farmer_fisher_full AS farmer_fisher_full, 
        ###         IP1.employee_lv00 AS employee_lv00, 
        ###         IP1.employee_lv01_49 AS employee_lv01_49, 
        ###         IP1.employee_lv50_99 AS employee_lv50_99, 
        ###         IP1.employee_lv100 AS employee_lv100, 
        ###         -- IP1.employee_half AS employee_half, 
        ###         IP1.employee_full AS employee_full 
        ###     FROM IPPAN IP1 
        ###     LEFT JOIN BUILDING BD1 ON IP1.building_code = BD1.building_code 
        ###     LEFT JOIN UNDERGROUND UD1 ON IP1.underground_code = UD1.underground_code 
        ###     LEFT JOIN FLOOD_SEDIMENT FL1 ON IP1.flood_sediment_code = FL1.flood_sediment_code 
        ###     LEFT JOIN INDUSTRY IN1 ON IP1.industry_code = IN1.industry_code 
        ###     LEFT JOIN USAGE US1 ON IP1.usage_code = US1.usage_code 
        ###     ORDER BY CAST(IP1.IPPAN_ID AS INTEGER)
        ###     """, [])
 
        ####################################################################### 
        ### 延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
        ####################################################################### 
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 4/6.', 'INFO')
        ippan_reverse_list = None
            
        ippan_reverse_list = IPPAN_VIEW.objects.raw("""
            SELECT 
                SUB1.ippan_id AS ippan_id, 
                SUB1.ippan_name AS ippan_name, 
                SUB1.suigai_id AS suigai_id, 
                SUB1.suigai_name AS suigai_name, 
                SUB1.ken_code AS ken_code, 
                SUB1.ken_name AS ken_name, 
                SUB1.city_code AS city_code, 
                SUB1.city_name AS city_name, 
                SUB1.cause_1_code AS cause_1_code, 
                SUB1.cause_1_name AS cause_1_name, 
                SUB1.cause_2_code AS cause_2_code, 
                SUB1.cause_2_name AS cause_2_name, 
                SUB1.cause_3_code AS cause_3_code, 
                SUB1.cause_3_name AS cause_3_name, 
                SUB1.area_id AS area_id, 
                SUB1.area_name AS area_name, 
                
                SUB1.suikei_code AS suikei_code, 
                SUB1.suikei_name AS suikei_name, 
                SUB1.kasen_code AS kasen_code, 
                SUB1.kasen_name AS kasen_name, 
                SUB1.gradient_code AS gradient_code, 
                SUB1.gradient_name AS gradient_name, 

                SUB1.residential_area AS residential_area, 
                SUB1.agricultural_area AS agricultural_area, 
                SUB1.underground_area AS underground_area, 
                SUB1.kasen_kaigan_code AS kasen_kaigan_code, 
                SUB1.kasen_kaigan_name AS kasen_kaigan_name, 
                SUB1.crop_damage AS crop_damage, 
                SUB1.weather_id AS weather_id, 
                SUB1.weather_name AS weather_name, 
                
                SUB1.building_code AS building_code, 
                SUB1.building_name AS building_name, 
                SUB1.underground_code AS underground_code, 
                SUB1.underground_name AS underground_name, 
                SUB1.flood_sediment_code AS flood_sediment_code, 
                SUB1.flood_sediment_name AS flood_sediment_name, 
                
                SUB1.building_lv00 AS building_lv00, 
                SUB1.building_lv01_49 AS building_lv01_49, 
                SUB1.building_lv50_99 AS building_lv50_99, 
                SUB1.building_lv100 AS building_lv100, 
                SUB1.building_half AS building_half, 
                SUB1.building_full AS building_full, 
                SUB1.building_total AS building_total, 
 
                SUB1.floor_area AS floor_area, 
                SUB1.family AS family, 
                SUB1.office AS office, 

                SUB1.floor_area_lv00 AS floor_area_lv00, 
                SUB1.floor_area_lv01_49 AS floor_area_lv01_49, 
                SUB1.floor_area_lv50_99 AS floor_area_lv50_99, 
                SUB1.floor_area_lv100 AS floor_area_lv100, 
                SUB1.floor_area_half AS floor_area_half, 
                SUB1.floor_area_full AS floor_area_full, 
                SUB1.floor_area_total AS floor_area_total, 
                
                SUB1.family_lv00 AS family_lv00, 
                SUB1.family_lv01_49 AS family_lv01_49, 
                SUB1.family_lv50_99 AS family_lv50_99, 
                SUB1.family_lv100 AS family_lv100, 
                SUB1.family_half AS family_half, 
                SUB1.family_full AS family_full, 
                SUB1.family_total AS family_total, 
               
                SUB1.office_lv00 AS office_lv00, 
                SUB1.office_lv01_49 AS office_lv01_49, 
                SUB1.office_lv50_99 AS office_lv50_99, 
                SUB1.office_lv100 AS office_lv100, 
                SUB1.office_half AS office_half, 
                SUB1.office_full AS office_full, 
                SUB1.office_total AS office_total, 

                SUB1.farmer_fisher_lv00 AS farmer_fisher_lv00, 
                SUB1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49, 
                SUB1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99, 
                SUB1.farmer_fisher_lv100 AS farmer_fisher_lv100, 
                -- SUB1.farmer_fisher_half AS farmer_fisher_half, 
                SUB1.farmer_fisher_full AS farmer_fisher_full, 
                SUB1.farmer_fisher_total AS farmer_fisher_total, 

                SUB1.employee_lv00 AS employee_lv00, 
                SUB1.employee_lv01_49 AS employee_lv01_49, 
                SUB1.employee_lv50_99 AS employee_lv50_99, 
                SUB1.employee_lv100 AS employee_lv100, 
                -- SUB1.employee_half AS employee_half, 
                SUB1.employee_full AS employee_full,
                SUB1.employee_total AS employee_total, 

                SUB1.industry_code AS industry_code, 
                SUB1.industry_name AS industry_name, 
                SUB1.usage_code AS usage_code,
                SUB1.usage_name AS usage_name, 

                -- 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_lv00 / SUB1.floor_area_total) END AS building_lv00_reverse_floor_area, 
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_lv01_49 / SUB1.floor_area_total) END AS building_lv01_49_reverse_floor_area, 
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_lv50_99 / SUB1.floor_area_total) END AS building_lv50_99_reverse_floor_area, 
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_lv100 / SUB1.floor_area_total) END AS building_lv100_reverse_floor_area, 
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_half / SUB1.floor_area_total) END AS building_half_reverse_floor_area, 
                CASE WHEN (SUB1.floor_area_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.floor_area_full / SUB1.floor_area_total) END AS building_full_reverse_floor_area, 

                -- 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_lv00 / SUB1.family_total) END AS building_lv00_reverse_family, 
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_lv01_49 / SUB1.family_total) END AS building_lv01_49_reverse_family, 
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_lv50_99 / SUB1.family_total) END AS building_lv50_99_reverse_family, 
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_lv100 / SUB1.family_total) END AS building_lv100_reverse_family, 
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_half / SUB1.family_total) END AS building_half_reverse_family, 
                CASE WHEN (SUB1.family_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.family_full / SUB1.family_total) END AS building_full_reverse_family, 

                -- 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_lv00 / SUB1.office_total) END AS building_lv00_reverse_office, 
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_lv01_49 / SUB1.office_total) END AS building_lv01_49_reverse_office, 
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_lv50_99 / SUB1.office_total) END AS building_lv50_99_reverse_office, 
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_lv100 / SUB1.office_total) END AS building_lv100_reverse_office, 
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_half / SUB1.office_total) END AS building_half_reverse_office, 
                CASE WHEN (SUB1.office_total) <= 0 THEN NULL ELSE ((SUB1.building_total) * SUB1.office_full / SUB1.office_total) END AS building_full_reverse_office, 
                
                -- 家屋被害額(集計DB) 
                SUB1.house_summary_lv00 AS house_summary_lv00, 
                SUB1.house_summary_lv01_49 AS house_summary_lv01_49, 
                SUB1.house_summary_lv50_99 AS house_summary_lv50_99, 
                SUB1.house_summary_lv100 AS house_summary_lv100, 
                SUB1.house_summary_half AS house_summary_half, 
                SUB1.house_summary_full AS house_summary_full, 
                
                -- 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv00) <= 0 THEN NULL ELSE (SUB1.house_summary_lv00 / (SUB1.house_asset * SUB1.house_rate_lv00)) END AS floor_area_lv00_reverse_house_summary, 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv00_50) <= 0 THEN NULL ELSE (SUB1.house_summary_lv01_49 / (SUB1.house_asset * SUB1.house_rate_lv00_50)) END AS floor_area_lv01_49_reverse_house_summary, 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv50_100) <= 0 THEN NULL ELSE (SUB1.house_summary_lv50_99 / (SUB1.house_asset * SUB1.house_rate_lv50_100)) END AS floor_area_lv50_99_reverse_house_summary, 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv100_200) <= 0 THEN NULL ELSE (SUB1.house_summary_lv100 / (SUB1.house_asset * SUB1.house_rate_lv100_200)) END AS floor_area_lv100_reverse_house_summary, 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv200_300) <= 0 THEN NULL ELSE (SUB1.house_summary_half / (SUB1.house_asset * SUB1.house_rate_lv200_300)) END AS floor_area_half_reverse_house_summary, 
                CASE WHEN (SUB1.house_asset * SUB1.house_rate_lv300) <= 0 THEN NULL ELSE (SUB1.house_summary_full / (SUB1.house_asset * SUB1.house_rate_lv300)) END AS floor_area_full_reverse_house_summary, 
                
                -- 家庭用品自動車以外被害額(集計DB) 
                SUB1.household_summary_lv00 AS household_summary_lv00,
                SUB1.household_summary_lv01_49 AS household_summary_lv01_49, 
                SUB1.household_summary_lv50_99 AS household_summary_lv50_99, 
                SUB1.household_summary_lv100 AS household_summary_lv100, 
                SUB1.household_summary_half AS household_summary_half, 
                SUB1.household_summary_full AS household_summary_full, 

                -- 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv00) <= 0 THEN NULL ELSE (SUB1.household_summary_lv00 / (SUB1.household_asset * SUB1.household_rate_lv00)) END AS family_lv00_reverse_household_summary, 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv00_50) <= 0 THEN NULL ELSE (SUB1.household_summary_lv01_49 / (SUB1.household_asset * SUB1.household_rate_lv00_50)) END AS family_lv01_49_reverse_household_summary, 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv50_100) <= 0 THEN NULL ELSE (SUB1.household_summary_lv50_99 / (SUB1.household_asset * SUB1.household_rate_lv50_100)) END AS family_lv50_99_reverse_household_summary, 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv100_200) <= 0 THEN NULL ELSE (SUB1.household_summary_lv100 / (SUB1.household_asset * SUB1.household_rate_lv100_200)) END AS family_lv100_reverse_household_summary, 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv200_300) <= 0 THEN NULL ELSE (SUB1.household_summary_half / (SUB1.household_asset * SUB1.household_rate_lv200_300)) END AS family_half_reverse_household_summary, 
                CASE WHEN (SUB1.household_asset * SUB1.household_rate_lv300) <= 0 THEN NULL ELSE (SUB1.household_summary_full / (SUB1.household_asset * SUB1.household_rate_lv300)) END AS family_full_reverse_household_summary, 
                
                -- 家庭用品自動車被害額(集計DB) 
                SUB1.car_summary_lv00 AS car_summary_lv00, 
                SUB1.car_summary_lv01_49 AS car_summary_lv01_49, 
                SUB1.car_summary_lv50_99 AS car_summary_lv50_99, 
                SUB1.car_summary_lv100 AS car_summary_lv100, 
                SUB1.car_summary_half AS car_summary_half, 
                SUB1.car_summary_full AS car_summary_full, 

                -- 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv00) <= 0 THEN NULL ELSE (SUB1.car_summary_lv00 / (SUB1.car_asset * SUB1.car_rate_lv00)) END AS family_lv00_reverse_car_summary, 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv00_50) <= 0 THEN NULL ELSE (SUB1.car_summary_lv01_49 / (SUB1.car_asset * SUB1.car_rate_lv00_50)) END AS family_lv01_49_reverse_car_summary, 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv50_100) <= 0 THEN NULL ELSE (SUB1.car_summary_lv50_99 / (SUB1.car_asset * SUB1.car_rate_lv50_100)) END AS family_lv50_99_reverse_car_summary, 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv100_200) <= 0 THEN NULL ELSE (SUB1.car_summary_lv100 / (SUB1.car_asset * SUB1.car_rate_lv100_200)) END AS family_lv100_reverse_car_summary, 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv200_300) <= 0 THEN NULL ELSE (SUB1.car_summary_half / (SUB1.car_asset * SUB1.car_rate_lv200_300)) END AS family_half_reverse_car_summary, 
                CASE WHEN (SUB1.car_asset * SUB1.car_rate_lv300) <= 0 THEN NULL ELSE (SUB1.car_summary_full / (SUB1.car_asset * SUB1.car_rate_lv300)) END AS family_full_reverse_car_summary, 

                -- 家庭応急対策費_代替活動費(集計DB) 
                SUB1.house_alt_summary_lv00 AS house_alt_summary_lv00, 
                SUB1.house_alt_summary_lv01_49 AS house_alt_summary_lv01_49, 
                SUB1.house_alt_summary_lv50_99 AS house_alt_summary_lv50_99, 
                SUB1.house_alt_summary_lv100 AS house_alt_summary_lv100, 
                SUB1.house_alt_summary_half AS house_alt_summary_half, 
                SUB1.house_alt_summary_full AS house_alt_summary_full, 

                -- 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                CASE WHEN (SUB1.house_alt_lv00) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_lv00 / SUB1.house_alt_lv00) END AS family_lv00_reverse_house_alt_summary, 
                CASE WHEN (SUB1.house_alt_lv00_50) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_lv01_49 / SUB1.house_alt_lv00_50) END AS family_lv01_49_reverse_house_alt_summary, 
                CASE WHEN (SUB1.house_alt_lv50_100) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_lv50_99 / SUB1.house_alt_lv50_100) END AS family_lv50_99_reverse_house_alt_summary, 
                CASE WHEN (SUB1.house_alt_lv100_200) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_lv100 / SUB1.house_alt_lv100_200) END AS family_lv100_reverse_house_alt_summary, 
                CASE WHEN (SUB1.house_alt_lv200_300) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_half / SUB1.house_alt_lv200_300) END AS family_half_reverse_house_alt_summary, 
                CASE WHEN (SUB1.house_alt_lv300) <= 0 THEN NULL ELSE (SUB1.house_alt_summary_full / SUB1.house_alt_lv300) END AS family_full_reverse_house_alt_summary, 

                -- 家庭応急対策費_清掃費(集計DB) 
                SUB1.house_clean_summary_lv00 AS house_clean_summary_lv00, 
                SUB1.house_clean_summary_lv01_49 AS house_clean_summary_lv01_49, 
                SUB1.house_clean_summary_lv50_99 AS house_clean_summary_lv50_99, 
                SUB1.house_clean_summary_lv100 AS house_clean_summary_lv100, 
                SUB1.house_clean_summary_half AS house_clean_summary_half, 
                SUB1.house_clean_summary_full AS house_clean_summary_full, 

                -- 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv00) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_lv00 / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv00)) END AS family_lv00_reverse_house_clean_summary, 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv00_50) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_lv01_49 / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv00_50)) END AS family_lv01_49_reverse_house_clean_summary, 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv50_100) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_lv50_99 / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv50_100)) END AS family_lv50_99_reverse_house_clean_summary, 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv100_200) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_lv100 / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv100_200)) END AS family_lv100_reverse_house_clean_summary, 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv200_300) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_half / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv200_300)) END AS family_half_reverse_house_clean_summary, 
                CASE WHEN (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv300) <= 0 THEN NULL ELSE (SUB1.house_clean_summary_full / (SUB1.house_clean_unit_cost * SUB1.house_clean_days_lv300)) END AS family_full_reverse_house_clean_summary, 

                -- 事業所被害額_償却資産被害額(集計DB) 
                SUB1.office_dep_summary_lv00 AS office_dep_summary_lv00, 
                SUB1.office_dep_summary_lv01_49 AS office_dep_summary_lv01_49, 
                SUB1.office_dep_summary_lv50_99 AS office_dep_summary_lv50_99, 
                SUB1.office_dep_summary_lv100 AS office_dep_summary_lv100, 
                -- SUB1.office_dep_summary_half AS office_dep_summary_half, 
                SUB1.office_dep_summary_full AS office_dep_summary_full, 
                
                -- 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv00) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_lv00 / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv00)) END AS employee_lv00_reverse_office_dep_summary, 
                CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv00_50) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_lv01_49 / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv00_50)) END AS employee_lv01_49_reverse_office_dep_summary, 
                CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv50_100) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_lv50_99 / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv50_100)) END AS employee_lv50_99_reverse_office_dep_summary, 
                CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv100_200) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_lv100 / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv100_200)) END AS employee_lv100_reverse_office_dep_summary, 
                -- CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv200_300) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_half / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv200_300)) END AS employee_half_reverse_office_dep_summary, 
                CASE WHEN (SUB1.office_dep_asset * SUB1.office_dep_rate_lv300) <= 0 THEN NULL ELSE (SUB1.office_dep_summary_full / (SUB1.office_dep_asset * SUB1.office_dep_rate_lv300)) END AS employee_full_reverse_office_dep_summary, 

                -- 事業所被害額_在庫資産被害額(集計DB) 
                SUB1.office_inv_summary_lv00 AS office_inv_summary_lv00, 
                SUB1.office_inv_summary_lv01_49 AS office_inv_summary_lv01_49, 
                SUB1.office_inv_summary_lv50_99 AS office_inv_summary_lv50_99, 
                SUB1.office_inv_summary_lv100 AS office_inv_summary_lv100, 
                -- SUB1.office_inv_summary_half AS office_inv_summary_half, 
                SUB1.office_inv_summary_full AS office_inv_summary_full, 
                
                -- 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv00) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_lv00 / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv00)) END AS employee_lv00_reverse_office_inv_summary, 
                CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv00_50) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_lv01_49 / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv00_50)) END AS employee_lv01_49_reverse_office_inv_summary, 
                CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv50_100) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_lv50_99 / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv50_100)) END AS employee_lv50_99_reverse_office_inv_summary, 
                CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv100_200) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_lv100 / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv100_200)) END AS employee_lv100_reverse_office_inv_summary, 
                -- CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv200_300) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_half / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv200_300)) END AS employee_half_reverse_office_inv_summary, 
                CASE WHEN (SUB1.office_inv_asset * SUB1.office_inv_rate_lv300) <= 0 THEN NULL ELSE (SUB1.office_inv_summary_full / (SUB1.office_inv_asset * SUB1.office_inv_rate_lv300)) END AS employee_full_reverse_office_inv_summary, 

                -- 事業所被害額_営業停止に伴う損失額(集計DB) 
                SUB1.office_sus_summary_lv00 AS office_sus_summary_lv00, 
                SUB1.office_sus_summary_lv01_49 AS office_sus_summary_lv01_49, 
                SUB1.office_sus_summary_lv50_99 AS office_sus_summary_lv50_99, 
                SUB1.office_sus_summary_lv100 AS office_sus_summary_lv100, 
                -- SUB1.office_sus_summary_half AS office_sus_summary_half, 
                SUB1.office_sus_summary_full AS office_sus_summary_full, 

                -- 事業所被害額_営業停止に伴う損失額(集計DB)から逆計算により被災従業者数を求めた結果 

                -- 事業所被害額_営業停滞に伴う損失額(集計DB) 
                SUB1.office_stg_summary_lv00 AS office_stg_summary_lv00, 
                SUB1.office_stg_summary_lv01_49 AS office_stg_summary_lv01_49, 
                SUB1.office_stg_summary_lv50_99 AS office_stg_summary_lv50_99, 
                SUB1.office_stg_summary_lv100 AS office_stg_summary_lv100, 
                -- SUB1.office_stg_summary_half AS office_stg_summary_half, 
                SUB1.office_stg_summary_full AS office_stg_summary_full, 

                -- 事業所被害額_営業停滞に伴う損失額(集計DB)から逆計算により被災従業者数を求めた結果 

                -- 農漁家被害額_償却資産被害額(集計DB) 
                SUB1.farmer_fisher_dep_summary_lv00 AS farmer_fisher_dep_summary_lv00, 
                SUB1.farmer_fisher_dep_summary_lv01_49 AS farmer_fisher_dep_summary_lv01_49, 
                SUB1.farmer_fisher_dep_summary_lv50_99 AS farmer_fisher_dep_summary_lv50_99, 
                SUB1.farmer_fisher_dep_summary_lv100 AS farmer_fisher_dep_summary_lv100, 
                -- SUB1.farmer_fisher_dep_summary_half AS farmer_fisher_dep_summary_half, 
                SUB1.farmer_fisher_dep_summary_full AS farmer_fisher_dep_summary_full, 

                -- 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 

                -- 農漁家被害額_在庫資産被害額(集計DB) 
                SUB1.farmer_fisher_inv_summary_lv00 AS farmer_fisher_inv_summary_lv00, 
                SUB1.farmer_fisher_inv_summary_lv01_49 AS farmer_fisher_inv_summary_lv01_49, 
                SUB1.farmer_fisher_inv_summary_lv50_99 AS farmer_fisher_inv_summary_lv50_99, 
                SUB1.farmer_fisher_inv_summary_lv100 AS farmer_fisher_inv_summary_lv100, 
                -- SUB1.farmer_fisher_inv_summary_half AS farmer_fisher_inv_summary_half, 
                SUB1.farmer_fisher_inv_summary_full AS farmer_fisher_inv_summary_full, 

                -- 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 

                -- 事業所応急対策費_代替活動費(集計DB) 
                SUB1.office_alt_summary_lv00 AS office_alt_summary_lv00, 
                SUB1.office_alt_summary_lv01_49 AS office_alt_summary_lv01_49, 
                SUB1.office_alt_summary_lv50_99 AS office_alt_summary_lv50_99, 
                SUB1.office_alt_summary_lv100 AS office_alt_summary_lv100, 
                -- SUB1.office_alt_summary_half AS office_alt_summary_half, 
                SUB1.office_alt_summary_full AS office_alt_summary_full,

                -- 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 






                
                -- 県別家屋評価額(マスタDB) 
                SUB1.house_asset AS house_asset, 
                
                -- 家屋被害率(マスタDB) 
                SUB1.house_rate_lv00 AS house_rate_lv00, 
                SUB1.house_rate_lv00_50 AS house_rate_lv00_50, 
                SUB1.house_rate_lv50_100 AS house_rate_lv50_100, 
                SUB1.house_rate_lv100_200 AS house_rate_lv100_200, 
                SUB1.house_rate_lv200_300 AS house_rate_lv200_300, 
                SUB1.house_rate_lv300 AS house_rate_lv300, 
                
                -- 家庭用品自動車以外所有額(マスタDB) 
                SUB1.household_asset AS household_asset, 
                
                -- 家庭用品自動車以外被害率(マスタDB) 
                SUB1.household_rate_lv00 AS household_rate_lv00, 
                SUB1.household_rate_lv00_50 AS household_rate_lv00_50, 
                SUB1.household_rate_lv50_100 AS household_rate_lv50_100, 
                SUB1.household_rate_lv100_200 AS household_rate_lv100_200, 
                SUB1.household_rate_lv200_300 AS household_rate_lv200_300, 
                SUB1.household_rate_lv300 AS household_rate_lv300, 
                
                -- 家庭用品自動車所有額(マスタDB) 
                SUB1.car_asset AS car_asset, 

                -- 家庭用品自動車被害率(マスタDB) 
                SUB1.car_rate_lv00 AS car_rate_lv00, 
                SUB1.car_rate_lv00_50 AS car_rate_lv00_50, 
                SUB1.car_rate_lv50_100 AS car_rate_lv50_100, 
                SUB1.car_rate_lv100_200 AS car_rate_lv100_200, 
                SUB1.car_rate_lv200_300 AS car_rate_lv200_300, 
                SUB1.car_rate_lv300 AS car_rate_lv300, 
                
                -- 家庭応急対策費_代替活動費(マスタDB)
                SUB1.house_alt_lv00 AS house_alt_lv00, 
                SUB1.house_alt_lv00_50 AS house_alt_lv00_50, 
                SUB1.house_alt_lv50_100 AS house_alt_lv50_100, 
                SUB1.house_alt_lv100_200 AS house_alt_lv100_200, 
                SUB1.house_alt_lv200_300 AS house_alt_lv200_300, 
                SUB1.house_alt_lv300 AS house_alt_lv300, 

                -- 家庭応急対策費_清掃労働単価(マスタDB) 
                SUB1.house_clean_unit_cost AS house_clean_unit_cost, 

                -- 家庭応急対策費_清掃日数(マスタDB) 
                SUB1.house_clean_days_lv00 AS house_clean_days_lv00, 
                SUB1.house_clean_days_lv00_50 AS house_clean_days_lv00_50, 
                SUB1.house_clean_days_lv50_100 AS house_clean_days_lv50_100, 
                SUB1.house_clean_days_lv100_200 AS house_clean_days_lv100_200, 
                SUB1.house_clean_days_lv200_300 AS house_clean_days_lv200_300, 
                SUB1.house_clean_days_lv300 AS house_clean_days_lv300, 
                
                -- 事業所資産額_償却資産額(マスタDB) 
                SUB1.office_dep_asset AS office_dep_asset, 
                
                -- 事業所被害率_償却資産被害率(マスタDB) 
                SUB1.office_dep_rate_lv00 AS office_dep_rate_lv00, 
                SUB1.office_dep_rate_lv00_50 AS office_dep_rate_lv00_50, 
                SUB1.office_dep_rate_lv50_100 AS office_dep_rate_lv50_100, 
                SUB1.office_dep_rate_lv100_200 AS office_dep_rate_lv100_200, 
                -- SUB1.office_dep_rate_lv200_300 AS office_dep_rate_lv200_300, 
                SUB1.office_dep_rate_lv300 AS office_dep_rate_lv300, 

                -- 事業所資産額_在庫資産額(マスタDB) 
                SUB1.office_inv_asset AS office_inv_asset, 

                -- 事業所被害率_在庫資産被害率(マスタDB) 
                SUB1.office_inv_rate_lv00 AS office_inv_rate_lv00, 
                SUB1.office_inv_rate_lv00_50 AS office_inv_rate_lv00_50, 
                SUB1.office_inv_rate_lv50_100 AS office_inv_rate_lv50_100, 
                SUB1.office_inv_rate_lv100_200 AS office_inv_rate_lv100_200, 
                -- SUB1.office_inv_rate_lv200_300 AS office_inv_rate_lv200_300, 
                SUB1.office_inv_rate_lv300 AS office_inv_rate_lv300 
                
            FROM 
            (
                SELECT 
                    IV1.ippan_id AS ippan_id, 
                    IV1.ippan_name AS ippan_name, 
                    IV1.suigai_id AS suigai_id, 
                    IV1.suigai_name AS suigai_name, 
                    IV1.ken_code AS ken_code, 
                    IV1.ken_name AS ken_name, 
                    IV1.city_code AS city_code, 
                    IV1.city_name AS city_name, 
                    IV1.cause_1_code AS cause_1_code, 
                    IV1.cause_1_name AS cause_1_name, 
                    IV1.cause_2_code AS cause_2_code, 
                    IV1.cause_2_name AS cause_2_name, 
                    IV1.cause_3_code AS cause_3_code, 
                    IV1.cause_3_name AS cause_3_name, 
                    IV1.area_id AS area_id, 
                    IV1.area_name AS area_name, 
                    
                    IV1.suikei_code AS suikei_code, 
                    IV1.suikei_name AS suikei_name, 
                    IV1.kasen_code AS kasen_code, 
                    IV1.kasen_name AS kasen_name, 
                    IV1.gradient_code AS gradient_code, 
                    IV1.gradient_name AS gradient_name, 
                    
                    IV1.residential_area AS residential_area, 
                    IV1.agricultural_area AS agricultural_area, 
                    IV1.underground_area AS underground_area, 
                    IV1.kasen_kaigan_code AS kasen_kaigan_code, 
                    IV1.kasen_kaigan_name AS kasen_kaigan_name, 
                    IV1.crop_damage AS crop_damage, 
                    IV1.weather_id AS weather_id, 
                    IV1.weather_name AS weather_name, 
                    
                    IV1.building_code AS building_code, 
                    IV1.building_name AS building_name, 
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
                    IV1.building_total AS building_total, 
     
                    IV1.floor_area AS floor_area, 
                    IV1.family AS family, 
                    IV1.office AS office, 
    
                    IV1.floor_area_lv00 AS floor_area_lv00, 
                    IV1.floor_area_lv01_49 AS floor_area_lv01_49, 
                    IV1.floor_area_lv50_99 AS floor_area_lv50_99, 
                    IV1.floor_area_lv100 AS floor_area_lv100, 
                    IV1.floor_area_half AS floor_area_half, 
                    IV1.floor_area_full AS floor_area_full, 
                    IV1.floor_area_total AS floor_area_total, 
                    
                    IV1.family_lv00 AS family_lv00, 
                    IV1.family_lv01_49 AS family_lv01_49, 
                    IV1.family_lv50_99 AS family_lv50_99, 
                    IV1.family_lv100 AS family_lv100, 
                    IV1.family_half AS family_half, 
                    IV1.family_full AS family_full, 
                    IV1.family_total AS family_total, 
                   
                    IV1.office_lv00 AS office_lv00, 
                    IV1.office_lv01_49 AS office_lv01_49, 
                    IV1.office_lv50_99 AS office_lv50_99, 
                    IV1.office_lv100 AS office_lv100, 
                    IV1.office_half AS office_half, 
                    IV1.office_full AS office_full, 
                    IV1.office_total AS office_total, 
    
                    IV1.farmer_fisher_lv00 AS farmer_fisher_lv00, 
                    IV1.farmer_fisher_lv01_49 AS farmer_fisher_lv01_49, 
                    IV1.farmer_fisher_lv50_99 AS farmer_fisher_lv50_99, 
                    IV1.farmer_fisher_lv100 AS farmer_fisher_lv100, 
                    -- IV1.farmer_fisher_half AS farmer_fisher_half, 
                    IV1.farmer_fisher_full AS farmer_fisher_full, 
                    IV1.farmer_fisher_total AS farmer_fisher_total, 
    
                    IV1.employee_lv00 AS employee_lv00, 
                    IV1.employee_lv01_49 AS employee_lv01_49, 
                    IV1.employee_lv50_99 AS employee_lv50_99, 
                    IV1.employee_lv100 AS employee_lv100, 
                    -- IV1.employee_half AS employee_half, 
                    IV1.employee_full AS employee_full,
                    IV1.employee_total AS employee_total, 
    
                    IV1.industry_code AS industry_code, 
                    IV1.industry_name AS industry_name, 
                    IV1.usage_code AS usage_code,
                    IV1.usage_name AS usage_name, 
                    
                    IS1.ippan_summary_id AS ippan_summary_id, 
                    
                    -- 家屋被害額(集計DB) 
                    IS1.house_summary_lv00 AS house_summary_lv00, 
                    IS1.house_summary_lv01_49 AS house_summary_lv01_49, 
                    IS1.house_summary_lv50_99 AS house_summary_lv50_99, 
                    IS1.house_summary_lv100 AS house_summary_lv100, 
                    IS1.house_summary_half AS house_summary_half, 
                    IS1.house_summary_full AS house_summary_full, 
        
                    -- 家庭用品自動車以外被害額(集計DB) 
                    IS1.household_summary_lv00 AS household_summary_lv00,
                    IS1.household_summary_lv01_49 AS household_summary_lv01_49, 
                    IS1.household_summary_lv50_99 AS household_summary_lv50_99, 
                    IS1.household_summary_lv100 AS household_summary_lv100, 
                    IS1.household_summary_half AS household_summary_half, 
                    IS1.household_summary_full AS household_summary_full, 
    
                    -- 家庭用品自動車被害額(集計DB) 
                    IS1.car_summary_lv00 AS car_summary_lv00, 
                    IS1.car_summary_lv01_49 AS car_summary_lv01_49, 
                    IS1.car_summary_lv50_99 AS car_summary_lv50_99, 
                    IS1.car_summary_lv100 AS car_summary_lv100, 
                    IS1.car_summary_half AS car_summary_half, 
                    IS1.car_summary_full AS car_summary_full, 
    
                    -- 家庭応急対策費_代替活動費(集計DB) 
                    IS1.house_alt_summary_lv00 AS house_alt_summary_lv00, 
                    IS1.house_alt_summary_lv01_49 AS house_alt_summary_lv01_49, 
                    IS1.house_alt_summary_lv50_99 AS house_alt_summary_lv50_99, 
                    IS1.house_alt_summary_lv100 AS house_alt_summary_lv100, 
                    IS1.house_alt_summary_half AS house_alt_summary_half, 
                    IS1.house_alt_summary_full AS house_alt_summary_full, 
    
                    -- 家庭応急対策費_清掃費(集計DB) 
                    IS1.house_clean_summary_lv00 AS house_clean_summary_lv00, 
                    IS1.house_clean_summary_lv01_49 AS house_clean_summary_lv01_49, 
                    IS1.house_clean_summary_lv50_99 AS house_clean_summary_lv50_99, 
                    IS1.house_clean_summary_lv100 AS house_clean_summary_lv100, 
                    IS1.house_clean_summary_half AS house_clean_summary_half, 
                    IS1.house_clean_summary_full AS house_clean_summary_full, 
                    
                    -- 事業所被害額_償却資産被害額(集計DB) 
                    IS1.office_dep_summary_lv00 AS office_dep_summary_lv00, 
                    IS1.office_dep_summary_lv01_49 AS office_dep_summary_lv01_49, 
                    IS1.office_dep_summary_lv50_99 AS office_dep_summary_lv50_99, 
                    IS1.office_dep_summary_lv100 AS office_dep_summary_lv100, 
                    -- IS1.office_dep_summary_half AS office_dep_summary_half, 
                    IS1.office_dep_summary_full AS office_dep_summary_full, 
    
                    -- 事業所被害額_在庫資産被害額(集計DB) 
                    IS1.office_inv_summary_lv00 AS office_inv_summary_lv00, 
                    IS1.office_inv_summary_lv01_49 AS office_inv_summary_lv01_49, 
                    IS1.office_inv_summary_lv50_99 AS office_inv_summary_lv50_99, 
                    IS1.office_inv_summary_lv100 AS office_inv_summary_lv100, 
                    -- IS1.office_inv_summary_half AS office_inv_summary_half, 
                    IS1.office_inv_summary_full AS office_inv_summary_full, 
    
                    -- 事業所被害額_営業停止に伴う損失額(集計DB) 
                    IS1.office_sus_summary_lv00 AS office_sus_summary_lv00, 
                    IS1.office_sus_summary_lv01_49 AS office_sus_summary_lv01_49, 
                    IS1.office_sus_summary_lv50_99 AS office_sus_summary_lv50_99, 
                    IS1.office_sus_summary_lv100 AS office_sus_summary_lv100, 
                    -- IS1.office_sus_summary_half AS office_sus_summary_half, 
                    IS1.office_sus_summary_full AS office_sus_summary_full, 
    
                    -- 事業所被害額_営業停滞に伴う損失額(集計DB) 
                    IS1.office_stg_summary_lv00 AS office_stg_summary_lv00, 
                    IS1.office_stg_summary_lv01_49 AS office_stg_summary_lv01_49, 
                    IS1.office_stg_summary_lv50_99 AS office_stg_summary_lv50_99, 
                    IS1.office_stg_summary_lv100 AS office_stg_summary_lv100, 
                    -- IS1.office_stg_summary_half AS office_stg_summary_half, 
                    IS1.office_stg_summary_full AS office_stg_summary_full, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB) 
                    IS1.farmer_fisher_dep_summary_lv00 AS farmer_fisher_dep_summary_lv00, 
                    IS1.farmer_fisher_dep_summary_lv01_49 AS farmer_fisher_dep_summary_lv01_49, 
                    IS1.farmer_fisher_dep_summary_lv50_99 AS farmer_fisher_dep_summary_lv50_99, 
                    IS1.farmer_fisher_dep_summary_lv100 AS farmer_fisher_dep_summary_lv100, 
                    -- IS1.farmer_fisher_dep_summary_half AS farmer_fisher_dep_summary_half, 
                    IS1.farmer_fisher_dep_summary_full AS farmer_fisher_dep_summary_full, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB) 
                    IS1.farmer_fisher_inv_summary_lv00 AS farmer_fisher_inv_summary_lv00, 
                    IS1.farmer_fisher_inv_summary_lv01_49 AS farmer_fisher_inv_summary_lv01_49, 
                    IS1.farmer_fisher_inv_summary_lv50_99 AS farmer_fisher_inv_summary_lv50_99, 
                    IS1.farmer_fisher_inv_summary_lv100 AS farmer_fisher_inv_summary_lv100, 
                    -- IS1.farmer_fisher_inv_summary_half AS farmer_fisher_inv_summary_half, 
                    IS1.farmer_fisher_inv_summary_full AS farmer_fisher_inv_summary_full, 
    
                    -- 事業所応急対策費_代替活動費(集計DB) 
                    IS1.office_alt_summary_lv00 AS office_alt_summary_lv00, 
                    IS1.office_alt_summary_lv01_49 AS office_alt_summary_lv01_49, 
                    IS1.office_alt_summary_lv50_99 AS office_alt_summary_lv50_99, 
                    IS1.office_alt_summary_lv100 AS office_alt_summary_lv100, 
                    -- IS1.office_alt_summary_half AS office_alt_summary_half, 
                    IS1.office_alt_summary_full AS office_alt_summary_full, 


                    
                    -- 県別家屋評価額(マスタDB) 
                    HA1.house_asset AS house_asset, 
                    
                    -- 家屋被害率(マスタDB) 
                    HR1.house_rate_lv00 AS house_rate_lv00, 
                    HR1.house_rate_lv00_50 AS house_rate_lv00_50, 
                    HR1.house_rate_lv50_100 AS house_rate_lv50_100, 
                    HR1.house_rate_lv100_200 AS house_rate_lv100_200, 
                    HR1.house_rate_lv200_300 AS house_rate_lv200_300, 
                    HR1.house_rate_lv300 AS house_rate_lv300, 

                    -- 家庭用品自動車以外所有額(マスタDB) 
                    HHA1.household_asset AS household_asset, 
                    
                    -- 家庭用品自動車以外被害率(マスタDB) 
                    HHR1.household_rate_lv00 AS household_rate_lv00, 
                    HHR1.household_rate_lv00_50 AS household_rate_lv00_50, 
                    HHR1.household_rate_lv50_100 AS household_rate_lv50_100, 
                    HHR1.household_rate_lv100_200 AS household_rate_lv100_200, 
                    HHR1.household_rate_lv200_300 AS household_rate_lv200_300, 
                    HHR1.household_rate_lv300 AS household_rate_lv300, 

                    -- 家庭用品自動車所有額(マスタDB) 
                    CA1.car_asset AS car_asset, 

                    -- 家庭用品自動車被害率(マスタDB) 
                    CR1.car_rate_lv00 AS car_rate_lv00, 
                    CR1.car_rate_lv00_50 AS car_rate_lv00_50, 
                    CR1.car_rate_lv50_100 AS car_rate_lv50_100, 
                    CR1.car_rate_lv100_200 AS car_rate_lv100_200, 
                    CR1.car_rate_lv200_300 AS car_rate_lv200_300, 
                    CR1.car_rate_lv300 AS car_rate_lv300, 

                    -- 家庭応急対策費_代替活動費(マスタDB)
                    HAL1.house_alt_lv00 AS house_alt_lv00, 
                    HAL1.house_alt_lv00_50 AS house_alt_lv00_50, 
                    HAL1.house_alt_lv50_100 AS house_alt_lv50_100, 
                    HAL1.house_alt_lv100_200 AS house_alt_lv100_200, 
                    HAL1.house_alt_lv200_300 AS house_alt_lv200_300, 
                    HAL1.house_alt_lv300 AS house_alt_lv300, 

                    -- 家庭応急対策費_清掃労働単価(マスタDB) 
                    HCL1.house_clean_unit_cost AS house_clean_unit_cost, 
    
                    -- 家庭応急対策費_清掃日数(マスタDB) 
                    HCL1.house_clean_days_lv00 AS house_clean_days_lv00, 
                    HCL1.house_clean_days_lv00_50 AS house_clean_days_lv00_50, 
                    HCL1.house_clean_days_lv50_100 AS house_clean_days_lv50_100, 
                    HCL1.house_clean_days_lv100_200 AS house_clean_days_lv100_200, 
                    HCL1.house_clean_days_lv200_300 AS house_clean_days_lv200_300, 
                    HCL1.house_clean_days_lv300 AS house_clean_days_lv300, 

                    -- 事業所資産額_償却資産額(マスタDB) 
                    OA1.office_dep_asset AS office_dep_asset, 
                    
                    -- 事業所被害率_償却資産被害率(マスタDB) 
                    OR1.office_dep_rate_lv00 AS office_dep_rate_lv00, 
                    OR1.office_dep_rate_lv00_50 AS office_dep_rate_lv00_50, 
                    OR1.office_dep_rate_lv50_100 AS office_dep_rate_lv50_100, 
                    OR1.office_dep_rate_lv100_200 AS office_dep_rate_lv100_200, 
                    -- OR1.office_dep_rate_lv200_300 AS office_dep_rate_lv200_300, 
                    OR1.office_dep_rate_lv300 AS office_dep_rate_lv300, 
    
                    -- 事業所資産額_在庫資産額(マスタDB) 
                    OA1.office_inv_asset AS office_inv_asset, 
    
                    -- 事業所被害率_在庫資産被害率(マスタDB) 
                    OR1.office_inv_rate_lv00 AS office_inv_rate_lv00, 
                    OR1.office_inv_rate_lv00_50 AS office_inv_rate_lv00_50, 
                    OR1.office_inv_rate_lv50_100 AS office_inv_rate_lv50_100, 
                    OR1.office_inv_rate_lv100_200 AS office_inv_rate_lv100_200, 
                    -- OR1.office_inv_rate_lv200_300 AS office_inv_rate_lv200_300, 
                    OR1.office_inv_rate_lv300 AS office_inv_rate_lv300 
                    
                FROM IPPAN_VIEW IV1 
                LEFT JOIN IPPAN_SUMMARY IS1 ON IV1.ippan_id = IS1.ippan_id 
                LEFT JOIN HOUSE_ASSET HA1 ON IV1.ken_code = HA1.ken_code 
                LEFT JOIN HOUSE_RATE HR1 ON IV1.flood_sediment_code = HR1.flood_sediment_code AND IV1.gradient_code = HR1.gradient_code 
                LEFT JOIN HOUSEHOLD_RATE HHR1 ON IV1.flood_sediment_code = HHR1.flood_sediment_code 
                LEFT JOIN OFFICE_ASSET OA1 ON IV1.industry_code = OA1.industry_code 
                LEFT JOIN OFFICE_RATE OR1 ON IV1.flood_sediment_code = OR1.flood_sediment_code, 
                HOUSEHOLD_ASSET HHA1, 
                CAR_ASSET CA1, 
                CAR_RATE CR1, 
                HOUSE_ALT HAL1, 
                HOUSE_CLEAN HCL1 
                
                ORDER BY CAST(IV1.IPPAN_ID AS INTEGER)
            ) SUB1 
            """, [])

        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 5/6.', 'INFO')
        gradient_list = GRADIENT.objects.raw("""SELECT * FROM GRADIENT ORDER BY CAST(GRADIENT_CODE AS INTEGER)""", [])

        #######################################################################
        ### レスポンスセット処理(0010)
        ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0800Dashboard.category_view()関数 STEP 6/6.', 'INFO')
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
            ### 'ippan_list': ippan_list, 
            'ippan_reverse_list': ippan_reverse_list, 
            'gradient_list': gradient_list, 
        }
        print_log('[INFO] P0800Dashboard.category_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0800Dashboard.category_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
