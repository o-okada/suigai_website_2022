#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900CI/management/commands/action_07_reverse.py
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
from django.core.management.base import BaseCommand

import sys
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from P0000Common.models import BUILDING                ### 1000: 建物区分
from P0000Common.models import KEN                     ### 1010: 都道府県
from P0000Common.models import CITY                    ### 1020: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 1030: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 1040: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 1050: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 1060: 河川（河川・海岸）
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
from P0000Common.models import HOUSE_CLEAN             ### 2030: 家庭応急対策費_清掃日数

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

from P0000Common.models import AREA                    ### 7000: 一般資産入力データ_水害区域
from P0000Common.models import WEATHER                 ### 7010: 一般資産入力データ_異常気象
from P0000Common.models import SUIGAI                  ### 7020: 一般資産入力データ_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7030: 一般資産入力データ_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7040: 一般資産ビューデータ_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 一般資産集計データ

from P0000Common.models import ACTION                  ### 10000: アクション
from P0000Common.models import STATUS                  ### 10010: 状態
from P0000Common.models import TRIGGER                 ### 10020: トリガーメッセージ
from P0000Common.models import APPROVAL                ### 10030: 承認メッセージ
from P0000Common.models import FEEDBACK                ### 10040: フィードバックメッセージ
from P0000Common.models import REPOSITORY              ### 10050: EXCELファイルレポジトリ
### from P0000Common.models import EXECUTE             ### 10060: 実行管理

from P0000Common.common import print_log

###############################################################################
### クラス名： Command
###############################################################################
class Command(BaseCommand):
    
    ###########################################################################
    ### 関数名： handle
    ###########################################################################
    def handle(self, *args, **options):
        connection_cursor = connection.cursor()
        try:
            ###################################################################
            ### 引数チェック処理(0000)
            ### コマンドラインからの引数をチェックする。
            ###################################################################
            print_log('[INFO] ########################################', 'INFO')
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数が開始しました。', 'INFO')
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 1/10.', 'INFO')
    
            ###################################################################
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
            ### TRIGGERテーブルからSUIGAI_IDのリストを取得する。
            ### トリガーメッセージにアクションが発行されているかを検索する。
            ### 処理対象の水害IDを取得する。
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 2/10.', 'INFO')
            trigger_list = None
            trigger_id_list = None
            suigai_id_list = None
            repository_id_list = None
            ippan_reverse_list = None
            
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE ACTION_CODE='7' AND CONSUMED_AT IS NULL 
                ORDER BY CAST(TRIGGER_ID AS INTEGER) LIMIT 1""", [])

            print_log('trigger_list = {}'.format(trigger_list), 'INFO')

            if trigger_list is None:
                print_log('[INFO] P0900CI.action_07_reverse.handle()関数が正常終了しました。', 'INFO')
                return 0

            ###################################################################
            ### 計算処理(0020)
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 3/10.', 'INFO')
            trigger_id_list = [trigger.trigger_id for trigger in trigger_list]

            print_log('trigger_id_list = {}'.format(trigger_id_list), 'INFO')

            if len(trigger_id_list) <= 0:
                print_log('[INFO] P0900CI.action_07_reverse.handle()関数が正常終了しました。', 'INFO')
                return 0
            
            suigai_id_list = [trigger.suigai_id for trigger in trigger_list]
            repository_id_list = [trigger.repository_id for trigger in trigger_list]
            
            print_log('suigai_id_list = {}'.format(suigai_id_list), 'INFO')
            print_log('repository_id_list = {}'.format(repository_id_list), 'INFO')
            
            ###################################################################
            ### DBアクセス処理(0030)
            ###################################################################
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 4/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            ippan_reverse_list = IPPAN_VIEW.objects.raw("""
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
                    HALT1.house_alt_lv00 AS house_alt_lv00, 
                    HALT1.house_alt_lv00_50 AS house_alt_lv00_50, 
                    HALT1.house_alt_lv50_100 AS house_alt_lv50_100, 
                    HALT1.house_alt_lv100_200 AS house_alt_lv100_200, 
                    HALT1.house_alt_lv200_300 AS house_alt_lv200_300, 
                    HALT1.house_alt_lv300 AS house_alt_lv300, 
    
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
                    OR1.office_inv_rate_lv300 AS office_inv_rate_lv300, 
    
                    -- 事業所資産額_付加価値額(マスタDB) 
                    OA1.office_va_asset AS office_va_asset, 
    
                    -- 事業所被害額_営業停止に伴う被害額(マスタDB) 
                    OSUS1.office_sus_days_lv00 AS office_sus_days_lv00, 
                    OSUS1.office_sus_days_lv00_50 AS office_sus_days_lv00_50, 
                    OSUS1.office_sus_days_lv50_100 AS office_sus_days_lv50_100, 
                    OSUS1.office_sus_days_lv100_200 AS office_sus_days_lv100_200, 
                    -- OSUS1.office_sus_days_lv200_300 AS office_sus_days_lv200_300, 
                    OSUS1.office_sus_days_lv300 AS office_sus_days_lv300, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(マスタDB) 
                    OSTG1.office_stg_days_lv00 AS office_stg_days_lv00, 
                    OSTG1.office_stg_days_lv00_50 AS office_stg_days_lv00_50, 
                    OSTG1.office_stg_days_lv50_100 AS office_stg_days_lv50_100, 
                    OSTG1.office_stg_days_lv100_200 AS office_stg_days_lv100_200, 
                    -- OSTG1.office_stg_days_lv200_300 AS office_stg_days_lv200_300, 
                    OSTG1.office_stg_days_lv300 AS office_stg_days_lv300, 
                    
                    -- 農漁家資産額_償却資産額(マスタDB) 
                    FFA1.farmer_fisher_dep_asset AS farmer_fisher_dep_asset, 
                    
                    -- 農漁家被害率_償却資産被害率(マスタDB) 
                    FFR1.farmer_fisher_dep_rate_lv00 AS farmer_fisher_dep_rate_lv00, 
                    FFR1.farmer_fisher_dep_rate_lv00_50 AS farmer_fisher_dep_rate_lv00_50, 
                    FFR1.farmer_fisher_dep_rate_lv50_100 AS farmer_fisher_dep_rate_lv50_100, 
                    FFR1.farmer_fisher_dep_rate_lv100_200 AS farmer_fisher_dep_rate_lv100_200, 
                    -- FFR1.farmer_fisher_dep_rate_lv200_300 AS farmer_fisher_dep_rate_lv200_300, 
                    FFR1.farmer_fisher_dep_rate_lv300 AS farmer_fisher_dep_rate_lv300, 
    
                    -- 農漁家資産額_在庫資産額(マスタDB) 
                    FFA1.farmer_fisher_inv_asset AS farmer_fisher_inv_asset, 
                    
                    -- 農漁家被害率_在庫資産被害率(マスタDB) 
                    FFR1.farmer_fisher_inv_rate_lv00 AS farmer_fisher_inv_rate_lv00, 
                    FFR1.farmer_fisher_inv_rate_lv00_50 AS farmer_fisher_inv_rate_lv00_50, 
                    FFR1.farmer_fisher_inv_rate_lv50_100 AS farmer_fisher_inv_rate_lv50_100, 
                    FFR1.farmer_fisher_inv_rate_lv100_200 AS farmer_fisher_inv_rate_lv100_200, 
                    -- FFR1.farmer_fisher_inv_rate_lv200_300 AS farmer_fisher_inv_rate_lv200_300, 
                    FFR1.farmer_fisher_inv_rate_lv300 AS farmer_fisher_inv_rate_lv300, 
                    
                    -- 事業所応急対策費_代替活動費(マスタDB) 
                    OALT1.office_alt_lv00 AS office_alt_lv00, 
                    OALT1.office_alt_lv00_50 AS office_alt_lv00_50, 
                    OALT1.office_alt_lv50_100 AS office_alt_lv50_100, 
                    OALT1.office_alt_lv100_200 AS office_alt_lv100_200, 
                    OALT1.office_alt_lv200_300 AS office_alt_lv200_300, 
                    OALT1.office_alt_lv300 AS office_alt_lv300, 
                    
                    -- 家屋被害額(集計DB) 
                    IS1.house_summary_lv00 AS house_summary_lv00, 
                    IS1.house_summary_lv01_49 AS house_summary_lv01_49, 
                    IS1.house_summary_lv50_99 AS house_summary_lv50_99, 
                    IS1.house_summary_lv100 AS house_summary_lv100, 
                    IS1.house_summary_half AS house_summary_half, 
                    IS1.house_summary_full AS house_summary_full, 
                    
                    -- 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv00) <= 0 THEN NULL ELSE (IS1.house_summary_lv00 / (HA1.house_asset * HR1.house_rate_lv00)) END AS floor_area_lv00_reverse_house_summary, 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.house_summary_lv01_49 / (HA1.house_asset * HR1.house_rate_lv00_50)) END AS floor_area_lv01_49_reverse_house_summary, 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.house_summary_lv50_99 / (HA1.house_asset * HR1.house_rate_lv50_100)) END AS floor_area_lv50_99_reverse_house_summary, 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.house_summary_lv100 / (HA1.house_asset * HR1.house_rate_lv100_200)) END AS floor_area_lv100_reverse_house_summary, 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.house_summary_half / (HA1.house_asset * HR1.house_rate_lv200_300)) END AS floor_area_half_reverse_house_summary, 
                    CASE WHEN (HA1.house_asset * HR1.house_rate_lv300) <= 0 THEN NULL ELSE (IS1.house_summary_full / (HA1.house_asset * HR1.house_rate_lv300)) END AS floor_area_full_reverse_house_summary, 
                    
                    -- 家庭用品自動車以外被害額(集計DB) 
                    IS1.household_summary_lv00 AS household_summary_lv00,
                    IS1.household_summary_lv01_49 AS household_summary_lv01_49, 
                    IS1.household_summary_lv50_99 AS household_summary_lv50_99, 
                    IS1.household_summary_lv100 AS household_summary_lv100, 
                    IS1.household_summary_half AS household_summary_half, 
                    IS1.household_summary_full AS household_summary_full, 
    
                    -- 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv00) <= 0 THEN NULL ELSE (IS1.household_summary_lv00 / (HHA1.household_asset * HHR1.household_rate_lv00)) END AS family_lv00_reverse_household_summary, 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.household_summary_lv01_49 / (HHA1.household_asset * HHR1.household_rate_lv00_50)) END AS family_lv01_49_reverse_household_summary, 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.household_summary_lv50_99 / (HHA1.household_asset * HHR1.household_rate_lv50_100)) END AS family_lv50_99_reverse_household_summary, 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.household_summary_lv100 / (HHA1.household_asset * HHR1.household_rate_lv100_200)) END AS family_lv100_reverse_household_summary, 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.household_summary_half / (HHA1.household_asset * HHR1.household_rate_lv200_300)) END AS family_half_reverse_household_summary, 
                    CASE WHEN (HHA1.household_asset * HHR1.household_rate_lv300) <= 0 THEN NULL ELSE (IS1.household_summary_full / (HHA1.household_asset * HHR1.household_rate_lv300)) END AS family_full_reverse_household_summary, 
                    
                    -- 家庭用品自動車被害額(集計DB) 
                    IS1.car_summary_lv00 AS car_summary_lv00, 
                    IS1.car_summary_lv01_49 AS car_summary_lv01_49, 
                    IS1.car_summary_lv50_99 AS car_summary_lv50_99, 
                    IS1.car_summary_lv100 AS car_summary_lv100, 
                    IS1.car_summary_half AS car_summary_half, 
                    IS1.car_summary_full AS car_summary_full, 
    
                    -- 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv00) <= 0 THEN NULL ELSE (IS1.car_summary_lv00 / (CA1.car_asset * CR1.car_rate_lv00)) END AS family_lv00_reverse_car_summary, 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.car_summary_lv01_49 / (CA1.car_asset * CR1.car_rate_lv00_50)) END AS family_lv01_49_reverse_car_summary, 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.car_summary_lv50_99 / (CA1.car_asset * CR1.car_rate_lv50_100)) END AS family_lv50_99_reverse_car_summary, 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.car_summary_lv100 / (CA1.car_asset * CR1.car_rate_lv100_200)) END AS family_lv100_reverse_car_summary, 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.car_summary_half / (CA1.car_asset * CR1.car_rate_lv200_300)) END AS family_half_reverse_car_summary, 
                    CASE WHEN (CA1.car_asset * CR1.car_rate_lv300) <= 0 THEN NULL ELSE (IS1.car_summary_full / (CA1.car_asset * CR1.car_rate_lv300)) END AS family_full_reverse_car_summary, 
    
                    -- 家庭応急対策費_代替活動費(集計DB) 
                    IS1.house_alt_summary_lv00 AS house_alt_summary_lv00, 
                    IS1.house_alt_summary_lv01_49 AS house_alt_summary_lv01_49, 
                    IS1.house_alt_summary_lv50_99 AS house_alt_summary_lv50_99, 
                    IS1.house_alt_summary_lv100 AS house_alt_summary_lv100, 
                    IS1.house_alt_summary_half AS house_alt_summary_half, 
                    IS1.house_alt_summary_full AS house_alt_summary_full, 
    
                    -- 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN (HALT1.house_alt_lv00) <= 0 THEN NULL ELSE (IS1.house_alt_summary_lv00 / HALT1.house_alt_lv00) END AS family_lv00_reverse_house_alt_summary, 
                    CASE WHEN (HALT1.house_alt_lv00_50) <= 0 THEN NULL ELSE (IS1.house_alt_summary_lv01_49 / HALT1.house_alt_lv00_50) END AS family_lv01_49_reverse_house_alt_summary, 
                    CASE WHEN (HALT1.house_alt_lv50_100) <= 0 THEN NULL ELSE (IS1.house_alt_summary_lv50_99 / HALT1.house_alt_lv50_100) END AS family_lv50_99_reverse_house_alt_summary, 
                    CASE WHEN (HALT1.house_alt_lv100_200) <= 0 THEN NULL ELSE (IS1.house_alt_summary_lv100 / HALT1.house_alt_lv100_200) END AS family_lv100_reverse_house_alt_summary, 
                    CASE WHEN (HALT1.house_alt_lv200_300) <= 0 THEN NULL ELSE (IS1.house_alt_summary_half / HALT1.house_alt_lv200_300) END AS family_half_reverse_house_alt_summary, 
                    CASE WHEN (HALT1.house_alt_lv300) <= 0 THEN NULL ELSE (IS1.house_alt_summary_full / HALT1.house_alt_lv300) END AS family_full_reverse_house_alt_summary, 
    
                    -- 家庭応急対策費_清掃費(集計DB) 
                    IS1.house_clean_summary_lv00 AS house_clean_summary_lv00, 
                    IS1.house_clean_summary_lv01_49 AS house_clean_summary_lv01_49, 
                    IS1.house_clean_summary_lv50_99 AS house_clean_summary_lv50_99, 
                    IS1.house_clean_summary_lv100 AS house_clean_summary_lv100, 
                    IS1.house_clean_summary_half AS house_clean_summary_half, 
                    IS1.house_clean_summary_full AS house_clean_summary_full, 
    
                    -- 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00) <= 0 THEN NULL ELSE (IS1.house_clean_summary_lv00 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00)) END AS family_lv00_reverse_house_clean_summary, 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50) <= 0 THEN NULL ELSE (IS1.house_clean_summary_lv01_49 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50)) END AS family_lv01_49_reverse_house_clean_summary, 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100) <= 0 THEN NULL ELSE (IS1.house_clean_summary_lv50_99 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100)) END AS family_lv50_99_reverse_house_clean_summary, 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200) <= 0 THEN NULL ELSE (IS1.house_clean_summary_lv100 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200)) END AS family_lv100_reverse_house_clean_summary, 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300) <= 0 THEN NULL ELSE (IS1.house_clean_summary_half / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300)) END AS family_half_reverse_house_clean_summary, 
                    CASE WHEN (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300) <= 0 THEN NULL ELSE (IS1.house_clean_summary_full / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300)) END AS family_full_reverse_house_clean_summary, 
    
                    -- 事業所被害額_償却資産被害額(集計DB) 
                    IS1.office_dep_summary_lv00 AS office_dep_summary_lv00, 
                    IS1.office_dep_summary_lv01_49 AS office_dep_summary_lv01_49, 
                    IS1.office_dep_summary_lv50_99 AS office_dep_summary_lv50_99, 
                    IS1.office_dep_summary_lv100 AS office_dep_summary_lv100, 
                    -- IS1.office_dep_summary_half AS office_dep_summary_half, 
                    IS1.office_dep_summary_full AS office_dep_summary_full, 
                    
                    -- 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv00) <= 0 THEN NULL ELSE (IS1.office_dep_summary_lv00 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00)) END AS employee_lv00_reverse_office_dep_summary, 
                    CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.office_dep_summary_lv01_49 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00_50)) END AS employee_lv01_49_reverse_office_dep_summary, 
                    CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.office_dep_summary_lv50_99 / (OA1.office_dep_asset * OR1.office_dep_rate_lv50_100)) END AS employee_lv50_99_reverse_office_dep_summary, 
                    CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.office_dep_summary_lv100 / (OA1.office_dep_asset * OR1.office_dep_rate_lv100_200)) END AS employee_lv100_reverse_office_dep_summary, 
                    -- CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.office_dep_summary_half / (OA1.office_dep_asset * OR1.office_dep_rate_lv200_300)) END AS employee_half_reverse_office_dep_summary, 
                    CASE WHEN (OA1.office_dep_asset * OR1.office_dep_rate_lv300) <= 0 THEN NULL ELSE (IS1.office_dep_summary_full / (OA1.office_dep_asset * OR1.office_dep_rate_lv300)) END AS employee_full_reverse_office_dep_summary, 
    
                    -- 事業所被害額_在庫資産被害額(集計DB) 
                    IS1.office_inv_summary_lv00 AS office_inv_summary_lv00, 
                    IS1.office_inv_summary_lv01_49 AS office_inv_summary_lv01_49, 
                    IS1.office_inv_summary_lv50_99 AS office_inv_summary_lv50_99, 
                    IS1.office_inv_summary_lv100 AS office_inv_summary_lv100, 
                    -- IS1.office_inv_summary_half AS office_inv_summary_half, 
                    IS1.office_inv_summary_full AS office_inv_summary_full, 
                    
                    -- 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv00) <= 0 THEN NULL ELSE (IS1.office_inv_summary_lv00 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00)) END AS employee_lv00_reverse_office_inv_summary, 
                    CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.office_inv_summary_lv01_49 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00_50)) END AS employee_lv01_49_reverse_office_inv_summary, 
                    CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.office_inv_summary_lv50_99 / (OA1.office_inv_asset * OR1.office_inv_rate_lv50_100)) END AS employee_lv50_99_reverse_office_inv_summary, 
                    CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.office_inv_summary_lv100 / (OA1.office_inv_asset * OR1.office_inv_rate_lv100_200)) END AS employee_lv100_reverse_office_inv_summary, 
                    -- CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.office_inv_summary_half / (OA1.office_inv_asset * OR1.office_inv_rate_lv200_300)) END AS employee_half_reverse_office_inv_summary, 
                    CASE WHEN (OA1.office_inv_asset * OR1.office_inv_rate_lv300) <= 0 THEN NULL ELSE (IS1.office_inv_summary_full / (OA1.office_inv_asset * OR1.office_inv_rate_lv300)) END AS employee_full_reverse_office_inv_summary, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB) 
                    IS1.office_sus_summary_lv00 AS office_sus_summary_lv00, 
                    IS1.office_sus_summary_lv01_49 AS office_sus_summary_lv01_49, 
                    IS1.office_sus_summary_lv50_99 AS office_sus_summary_lv50_99, 
                    IS1.office_sus_summary_lv100 AS office_sus_summary_lv100, 
                    -- IS1.office_sus_summary_half AS office_sus_summary_half, 
                    IS1.office_sus_summary_full AS office_sus_summary_full, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN (OSUS1.office_sus_days_lv00 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_lv00 / (OSUS1.office_sus_days_lv00 * OA1.office_va_asset)) END AS employee_lv00_reverse_office_sus_summary, 
                    CASE WHEN (OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_lv01_49 / (OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset)) END AS employee_lv01_49_reverse_office_sus_summary, 
                    CASE WHEN (OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_lv50_99 / (OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset)) END AS employee_lv50_99_reverse_office_sus_summary, 
                    CASE WHEN (OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_lv100 / (OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset)) END AS employee_lv100_reverse_office_sus_summary, 
                    -- CASE WHEN (OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_half / (OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset)) END AS employee_half_reverse_office_sus_summary, 
                    CASE WHEN (OSUS1.office_sus_days_lv300 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_sus_summary_full / (OSUS1.office_sus_days_lv300 * OA1.office_va_asset)) END AS employee_full_reverse_office_sus_summary, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB) 
                    IS1.office_stg_summary_lv00 AS office_stg_summary_lv00, 
                    IS1.office_stg_summary_lv01_49 AS office_stg_summary_lv01_49, 
                    IS1.office_stg_summary_lv50_99 AS office_stg_summary_lv50_99, 
                    IS1.office_stg_summary_lv100 AS office_stg_summary_lv100, 
                    -- IS1.office_stg_summary_half AS office_stg_summary_half, 
                    IS1.office_stg_summary_full AS office_stg_summary_full, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN (OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_lv00 / (OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset)) END AS employee_lv00_reverse_office_stg_summary, 
                    CASE WHEN (OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_lv01_49 / (OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset)) END AS employee_lv01_49_reverse_office_stg_summary, 
                    CASE WHEN (OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_lv50_99 / (OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset)) END AS employee_lv50_99_reverse_office_stg_summary, 
                    CASE WHEN (OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_lv100 / (OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset)) END AS employee_lv100_reverse_office_stg_summary, 
                    -- CASE WHEN (OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_half / (OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset)) END AS employee_half_reverse_office_stg_summary, 
                    CASE WHEN (OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset) <= 0 THEN NULL ELSE (IS1.office_stg_summary_full / (OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset)) END AS employee_full_reverse_office_stg_summary, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB) 
                    IS1.farmer_fisher_dep_summary_lv00 AS farmer_fisher_dep_summary_lv00, 
                    IS1.farmer_fisher_dep_summary_lv01_49 AS farmer_fisher_dep_summary_lv01_49, 
                    IS1.farmer_fisher_dep_summary_lv50_99 AS farmer_fisher_dep_summary_lv50_99, 
                    IS1.farmer_fisher_dep_summary_lv100 AS farmer_fisher_dep_summary_lv100, 
                    -- IS1.farmer_fisher_dep_summary_half AS farmer_fisher_dep_summary_half, 
                    IS1.farmer_fisher_dep_summary_full AS farmer_fisher_dep_summary_full, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_lv00 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00)) END AS farmer_fisher_lv00_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_lv01_49 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_lv50_99 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_lv100 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200)) END AS farmer_fisher_lv100_reverse_farmer_fisher_dep_summary, 
                    -- CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_half / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300)) END AS farmer_fisher_half_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300) <= 0 THEN NULL ELSE (IS1.farmer_fisher_dep_summary_full / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300)) END AS farmer_fisher_full_reverse_farmer_fisher_dep_summary, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB) 
                    IS1.farmer_fisher_inv_summary_lv00 AS farmer_fisher_inv_summary_lv00, 
                    IS1.farmer_fisher_inv_summary_lv01_49 AS farmer_fisher_inv_summary_lv01_49, 
                    IS1.farmer_fisher_inv_summary_lv50_99 AS farmer_fisher_inv_summary_lv50_99, 
                    IS1.farmer_fisher_inv_summary_lv100 AS farmer_fisher_inv_summary_lv100, 
                    -- IS1.farmer_fisher_inv_summary_half AS farmer_fisher_inv_summary_half, 
                    IS1.farmer_fisher_inv_summary_full AS farmer_fisher_inv_summary_full, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_lv00 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00)) END AS farmer_fisher_lv00_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_lv01_49 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_lv50_99 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_lv100 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200)) END AS farmer_fisher_lv100_reverse_farmer_fisher_inv_summary, 
                    -- CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_half / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300)) END AS farmer_fisher_half_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300) <= 0 THEN NULL ELSE (IS1.farmer_fisher_inv_summary_full / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300)) END AS farmer_fisher_full_reverse_farmer_fisher_inv_summary, 
    
                    -- 事業所応急対策費_代替活動費(集計DB) 
                    IS1.office_alt_summary_lv00 AS office_alt_summary_lv00, 
                    IS1.office_alt_summary_lv01_49 AS office_alt_summary_lv01_49, 
                    IS1.office_alt_summary_lv50_99 AS office_alt_summary_lv50_99, 
                    IS1.office_alt_summary_lv100 AS office_alt_summary_lv100, 
                    IS1.office_alt_summary_half AS office_alt_summary_half, 
                    IS1.office_alt_summary_full AS office_alt_summary_full, 
    
                    -- 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 
                    CASE WHEN (OALT1.office_alt_lv00) <= 0 THEN NULL ELSE (IS1.office_alt_summary_lv00 / OALT1.office_alt_lv00) END AS office_lv00_reverse_office_alt_summary, 
                    CASE WHEN (OALT1.office_alt_lv00_50) <= 0 THEN NULL ELSE (IS1.office_alt_summary_lv01_49 / OALT1.office_alt_lv00_50) END AS office_lv01_49_reverse_office_alt_summary, 
                    CASE WHEN (OALT1.office_alt_lv50_100) <= 0 THEN NULL ELSE (IS1.office_alt_summary_lv50_99 / OALT1.office_alt_lv50_100) END AS office_lv50_99_reverse_office_alt_summary, 
                    CASE WHEN (OALT1.office_alt_lv100_200) <= 0 THEN NULL ELSE (IS1.office_alt_summary_lv100 / OALT1.office_alt_lv100_200) END AS office_lv100_reverse_office_alt_summary, 
                    CASE WHEN (OALT1.office_alt_lv200_300) <= 0 THEN NULL ELSE (IS1.office_alt_summary_half / OALT1.office_alt_lv200_300) END AS office_half_reverse_office_alt_summary, 
                    CASE WHEN (OALT1.office_alt_lv300) <= 0 THEN NULL ELSE (IS1.office_alt_summary_full / OALT1.office_alt_lv300) END AS office_full_reverse_office_alt_summary 
                    
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
                HOUSE_ALT HALT1, 
                HOUSE_CLEAN HCL1, 
                OFFICE_SUSPEND OSUS1, 
                OFFICE_STAGNATE OSTG1, 
                FARMER_FISHER_ASSET FFA1, 
                FARMER_FISHER_RATE FFR1, 
                OFFICE_ALT OALT1 
                WHERE IV1.SUIGAI_ID=%s 
                ORDER BY CAST(IV1.IPPAN_ID AS INTEGER)
                """, [suigai_id_list[0],])

            print_log('ippan_reverse_list'.format(ippan_reverse_list), 'INFO')

            if ippan_reverse_list is None:
                print_log('[INFO] P0900CI.action_07_reverse.handle()関数が警告終了しました。', 'INFO')
                return 4
    
            ###################################################################
            ### 計算処理(0040)
            ### 成功、失敗の数、レコード数をカウントする。
            ###################################################################
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 5/10.', 'INFO')
            print_log('ippan_reverse_list'.format(ippan_reverse_list), 'INFO')
            success_count = 0
            failure_count = 0
            epsilon = 0.0000001
                
            for ippan in ippan_reverse_list:
                print_log('suigai_id = {}'.format(ippan.suigai_id), 'INFO')
                ###############################################################
                ### 計算処理(0050)
                ### 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                ###############################################################
                if ippan.floor_area_lv00_reverse_house_summary is not None:
                    if float(ippan.floor_area_lv00_reverse_house_summary) - float(ippan.floor_area_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_lv00_reverse_house_summary = {}'.format(ippan.floor_area_lv00_reverse_house_summary), 'INFO')
                        print_log('floor_area_lv00 = {}'.format(ippan.floor_area_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.floor_area_lv01_49_reverse_house_summary is not None:
                    if float(ippan.floor_area_lv01_49_reverse_house_summary) - float(ippan.floor_area_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_lv01_49_reverse_house_summary = {}'.format(ippan.floor_area_lv01_49_reverse_house_summary), 'INFO')
                        print_log('floor_area_lv01_49 = {}'.format(ippan.floor_area_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.floor_area_lv50_99_reverse_house_summary is not None:
                    if float(ippan.floor_area_lv50_99_reverse_house_summary) - float(ippan.floor_area_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_lv50_99_reverse_house_summary = {}'.format(ippan.floor_area_lv50_99_reverse_house_summary), 'INFO')
                        print_log('floor_area_lv50_99 = {}'.format(ippan.floor_area_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.floor_area_lv100_reverse_house_summary is not None:
                    if float(ippan.floor_area_lv100_reverse_house_summary) - float(ippan.floor_area_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_lv100_reverse_house_summary = {}'.format(ippan.floor_area_lv100_reverse_house_summary), 'INFO')
                        print_log('floor_area_lv100 = {}'.format(ippan.floor_area_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.floor_area_half_reverse_house_summary is not None:
                    if float(ippan.floor_area_half_reverse_house_summary) - float(ippan.floor_area_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_half_reverse_house_summary = {}'.format(ippan.floor_area_half_reverse_house_summary), 'INFO')
                        print_log('floor_area_half = {}'.format(ippan.floor_area_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.floor_area_full_reverse_house_summary is not None:
                    if float(ippan.floor_area_full_reverse_house_summary) - float(ippan.floor_area_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('floor_area_full_reverse_house_summary = {}'.format(ippan.floor_area_full_reverse_house_summary), 'INFO')
                        print_log('floor_area_full = {}'.format(ippan.floor_area_full), 'INFO')
                        failure_count = failure_count + 1

                ###############################################################
                ### 計算処理(0060)
                ### 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                ###############################################################
                if ippan.family_lv00_reverse_household_summary is not None:
                    if float(ippan.family_lv00_reverse_household_summary) - float(ippan.family_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv00_reverse_household_summary = {}'.format(ippan.family_lv00_reverse_household_summary), 'INFO')
                        print_log('family_lv00 = {}'.format(ippan.family_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv01_49_reverse_household_summary is not None:
                    if float(ippan.family_lv01_49_reverse_household_summary) - float(ippan.family_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv01_49_reverse_household_summary = {}'.format(ippan.family_lv01_49_reverse_household_summary), 'INFO')
                        print_log('family_lv01_49 = {}'.format(ippan.family_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv50_99_reverse_household_summary is not None:
                    if float(ippan.family_lv50_99_reverse_household_summary) - float(ippan.family_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv50_99_reverse_household_summary = {}'.format(ippan.family_lv50_99_reverse_household_summary), 'INFO')
                        print_log('family_lv50_99 = {}'.format(ippan.family_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv100_reverse_household_summary is not None:
                    if float(ippan.family_lv100_reverse_household_summary) - float(ippan.family_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv100_reverse_household_summary = {}'.format(ippan.family_lv100_reverse_household_summary), 'INFO')
                        print_log('famly_lv100 = {}'.format(ippan.family_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_half_reverse_household_summary is not None:
                    if float(ippan.family_half_reverse_household_summary) - float(ippan.family_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_half_reverse_household_summary = {}'.format(ippan.family_half_reverse_household_summary), 'INFO')
                        print_log('family_half = {}'.format(ippan.family_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_full_reverse_household_summary is not None:
                    if float(ippan.family_full_reverse_household_summary) - float(ippan.family_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_full_reverse_household_summary = {}'.format(ippan.family_full_reverse_household_summary), 'INFO')
                        print_log('family_full = {}'.format(ippan.family_full), 'INFO')
                        failure_count = failure_count + 1

                ###############################################################
                ### 計算処理(0070)
                ### 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                ###############################################################
                if ippan.family_lv00_reverse_car_summary is not None: 
                    if float(ippan.family_lv00_reverse_car_summary) - float(ippan.family_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv00_reverse_car_summary = {}'.format(ippan.family_lv00_reverse_car_summary), 'INFO')
                        print_log('family_lv00 = {}'.format(ippan.family_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv01_49_reverse_car_summary is not None: 
                    if float(ippan.family_lv01_49_reverse_car_summary) - float(ippan.family_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv01_49_reverse_car_summary = {}'.format(ippan.family_lv01_49_reverse_car_summary), 'INFO')
                        print_log('family_lv01_49 = {}'.format(ippan.family_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv50_99_reverse_car_summary is not None:
                    if float(ippan.family_lv50_99_reverse_car_summary) - float(ippan.family_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv50_99_reverse_car_summary = {}'.format(ippan.family_lv50_99_reverse_car_summary), 'INFO')
                        print_log('family_lv50_99 = {}'.format(ippan.family_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv100_reverse_car_summary is not None:
                    if float(ippan.family_lv100_reverse_car_summary) - float(ippan.family_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv100_reverse_car_summary = {}'.format(ippan.family_lv100_reverse_car_summary), 'INFO')
                        print_log('family_lv100 = {}'.format(ippan.family_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_half_reverse_car_summary is not None:
                    if float(ippan.family_half_reverse_car_summary) - float(ippan.family_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_half_reverse_car_summary = {}'.format(ippan.family_half_reverse_car_summary), 'INFO')
                        print_log('family_half = {}'.format(ippan.family_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_full_reverse_car_summary is not None:
                    if float(ippan.family_full_reverse_car_summary) - float(ippan.family_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_full_reverse_car_summary = {}'.format(ippan.family_full_reverse_car_summary), 'INFO')
                        print_log('family_full = {}'.format(ippan.family_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0080)
                ### 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                ############################################################### 
                if ippan.family_lv00_reverse_house_alt_summary is not None: 
                    if float(ippan.family_lv00_reverse_house_alt_summary) - float(ippan.family_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv00_reverse_house_alt_summary = {}'.format(ippan.family_lv00_reverse_house_alt_summary), 'INFO')
                        print_log('family_lv00 = {}'.format(ippan.family_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv01_49_reverse_house_alt_summary is not None: 
                    if float(ippan.family_lv01_49_reverse_house_alt_summary) - float(ippan.family_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv01_49_reverse_house_alt_summary = {}'.format(ippan.family_lv01_49_reverse_house_alt_summary), 'INFO')
                        print_log('family_lv01_49 = {}'.format(ippan.family_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv50_99_reverse_house_alt_summary is not None:
                    if float(ippan.family_lv50_99_reverse_house_alt_summary) - float(ippan.family_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv50_99_reverse_house_alt_summary = {}'.format(ippan.family_lv50_99_reverse_house_alt_summary), 'INFO')
                        print_log('family_lv50_99 = {}'.format(ippan.family_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv100_reverse_house_alt_summary is not None:
                    if float(ippan.family_lv100_reverse_house_alt_summary) - float(ippan.family_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv100_reverse_house_alt_summary = {}'.format(ippan.family_lv100_reverse_house_alt_summary), 'INFO')
                        print_log('family_lv100 = {}'.format(ippan.family_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_half_reverse_house_alt_summary is not None:
                    if float(ippan.family_half_reverse_house_alt_summary) - float(ippan.family_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_half_reverse_house_alt_summary = {}'.format(ippan.family_half_reverse_house_alt_summary), 'INFO')
                        print_log('family_half = {}'.format(ippan.family_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_full_reverse_house_alt_summary is not None:
                    if float(ippan.family_full_reverse_house_alt_summary) - float(ippan.family_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_full_reverse_house_alt_summary = {}'.format(ippan.family_full_reverse_house_alt_summary), 'INFO')
                        print_log('family_full = {}'.format(ippan.family_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0090)
                ### 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                ############################################################### 
                if ippan.family_lv00_reverse_house_clean_summary is not None: 
                    if float(ippan.family_lv00_reverse_house_clean_summary) - float(ippan.family_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv00_reverse_house_clean_summary = {}'.format(ippan.family_lv00_reverse_house_clean_summary), 'INFO')
                        print_log('family_lv00 = {}'.format(ippan.family_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv01_49_reverse_house_clean_summary is not None: 
                    if float(ippan.family_lv01_49_reverse_house_clean_summary) - float(ippan.family_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv01_49_reverse_house_clean_summary = {}'.format(ippan.family_lv01_49_reverse_house_clean_summary), 'INFO')
                        print_log('family_lv01_49 = {}'.format(ippan.family_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv50_99_reverse_house_clean_summary is not None:
                    if float(ippan.family_lv50_99_reverse_house_clean_summary) - float(ippan.family_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv50_99_reverse_house_clean_summary = {}'.format(ippan.family_lv50_99_reverse_house_clean_summary), 'INFO')
                        print_log('family_lv50_99 = {}'.format(ippan.family_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_lv100_reverse_house_clean_summary is not None:
                    if float(ippan.family_lv100_reverse_house_clean_summary) - float(ippan.family_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_lv100_reverse_house_clean_summary = {}'.format(ippan.family_lv100_reverse_house_clean_summary), 'INFO')
                        print_log('family_lv100 = {}'.format(ippan.family_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_half_reverse_house_clean_summary is not None:
                    if float(ippan.family_half_reverse_house_clean_summary) - float(ippan.family_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_half_reverse_house_clean_summary = {}'.format(ippan.family_half_reverse_house_clean_summary), 'INFO')
                        print_log('family_half = {}'.format(ippan.family_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.family_full_reverse_house_clean_summary is not None:
                    if float(ippan.family_full_reverse_house_clean_summary) - float(ippan.family_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('family_full_reverse_house_clean_summary = {}'.format(ippan.family_full_reverse_house_clean_summary), 'INFO')
                        print_log('family_full = {}'.format(ippan.family_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0100)
                ### 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                ############################################################### 
                if ippan.employee_lv00_reverse_office_dep_summary is not None: 
                    if float(ippan.employee_lv00_reverse_office_dep_summary) - float(ippan.employee_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv00_reverse_office_dep_summary = {}'.format(ippan.employee_lv00_reverse_office_dep_summary), 'INFO')
                        print_log('employee_lv00 = {}'.format(ippan.employee_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv01_49_reverse_office_dep_summary is not None: 
                    if float(ippan.employee_lv01_49_reverse_office_dep_summary) - float(ippan.employee_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv01_49_reverse_office_dep_summary = {}'.format(ippan.employee_lv01_49_reverse_office_dep_summary), 'INFO')
                        print_log('employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv50_99_reverse_office_dep_summary is not None:
                    if float(ippan.employee_lv50_99_reverse_office_dep_summary) - float(ippan.employee_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv50_99_reverse_office_dep_summary = {}'.format(ippan.employee_lv50_99_reverse_office_dep_summary), 'INFO')
                        print_log('employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv100_reverse_office_dep_summary is not None:
                    if float(ippan.employee_lv100_reverse_office_dep_summary) - float(ippan.employee_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv100_reverse_office_dep_summary = {}'.format(ippan.employee_lv100_reverse_office_dep_summary), 'INFO')
                        print_log('employee_lv100 = {}'.format(ippan.employee_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.employee_half_reverse_office_dep_summary is not None:
                ###     if float(ippan.employee_half_reverse_office_dep_summary) - float(ippan.employee_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('employee_half_reverse_office_dep_summary = {}'.format(ippan.employee_half_reverse_office_dep_summary), 'INFO')
                ###         print_log('employee_half = {}'.format(ippan.employee_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.employee_full_reverse_office_dep_summary is not None:
                    if float(ippan.employee_full_reverse_office_dep_summary) - float(ippan.employee_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_full_reverse_office_dep_summary = {}'.format(ippan.employee_full_reverse_office_dep_summary), 'INFO')
                        print_log('employee_full = {}'.format(ippan.employee_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0110)
                ### 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                ############################################################### 
                if ippan.employee_lv00_reverse_office_inv_summary is not None: 
                    if float(ippan.employee_lv00_reverse_office_inv_summary) - float(ippan.employee_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv00_reverse_office_inv_summary = {}'.format(ippan.employee_lv00_reverse_office_inv_summary), 'INFO')
                        print_log('employee_lv00 = {}'.format(ippan.employee_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv01_49_reverse_office_inv_summary is not None: 
                    if float(ippan.employee_lv01_49_reverse_office_inv_summary) - float(ippan.employee_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv01_49_reverse_office_inv_summary = {}'.format(ippan.employee_lv01_49_reverse_office_inv_summary), 'INFO')
                        print_log('employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv50_99_reverse_office_inv_summary is not None:
                    if float(ippan.employee_lv50_99_reverse_office_inv_summary) - float(ippan.employee_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv50_99_reverse_office_inv_summary = {}'.format(ippan.employee_lv50_99_reverse_office_inv_summary), 'INFO')
                        print_log('employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv100_reverse_office_inv_summary is not None:
                    if float(ippan.employee_lv100_reverse_office_inv_summary) - float(ippan.employee_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv100_reverse_office_inv_summary = {}'.format(ippan.employee_lv100_reverse_office_inv_summary), 'INFO')
                        print_log('employee_lv100 = {}'.format(ippan.employee_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.employee_half_reverse_office_inv_summary is not None:
                ###     if float(ippan.employee_half_reverse_office_inv_summary) - float(ippan.employee_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('employee_half_reverse_office_inv_summary = {}'.format(ippan.employee_half_reverse_office_inv_summary), 'INFO')
                ###         print_log('employee_half = {}'.format(ippan.employee_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.employee_full_reverse_office_inv_summary is not None:
                    if float(ippan.employee_full_reverse_office_inv_summary) - float(ippan.employee_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_full_reverse_office_inv_summary = {}'.format(ippan.employee_full_reverse_office_inv_summary), 'INFO')
                        print_log('employee_full = {}'.format(ippan.employee_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0120)
                ### 事業所被害額_営業停止に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果
                ############################################################### 
                if ippan.employee_lv00_reverse_office_sus_summary is not None: 
                    if float(ippan.employee_lv00_reverse_office_sus_summary) - float(ippan.employee_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv00_reverse_office_sus_summary = {}'.format(ippan.employee_lv00_reverse_office_sus_summary), 'INFO')
                        print_log('employee_lv00 = {}'.format(ippan.employee_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv01_49_reverse_office_sus_summary is not None: 
                    if float(ippan.employee_lv01_49_reverse_office_sus_summary) - float(ippan.employee_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv01_49_reverse_office_sus_summary = {}'.format(ippan.employee_lv01_49_reverse_office_sus_summary), 'INFO')
                        print_log('employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv50_99_reverse_office_sus_summary is not None:
                    if float(ippan.employee_lv50_99_reverse_office_sus_summary) - float(ippan.employee_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv50_99_reverse_office_sus_summary = {}'.format(ippan.employee_lv50_99_reverse_office_sus_summary), 'INFO')
                        print_log('employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv100_reverse_office_sus_summary is not None:
                    if float(ippan.employee_lv100_reverse_office_sus_summary) - float(ippan.employee_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv100_reverse_office_sus_summary = {}'.format(ippan.employee_lv100_reverse_office_sus_summary), 'INFO')
                        print_log('employee_lv100 = {}'.format(ippan.employee_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.employee_half_reverse_office_sus_summary is not None:
                ###     if float(ippan.employee_half_reverse_office_sus_summary) - float(ippan.employee_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('employee_half_reverse_office_sus_summary = {}'.format(ippan.employee_half_reverse_office_sus_summary), 'INFO')
                ###         print_log('employee_half = {}'.format(ippan.employee_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.employee_full_reverse_office_sus_summary is not None:
                    if float(ippan.employee_full_reverse_office_sus_summary) - float(ippan.employee_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_full_reverse_office_sus_summary = {}'.format(ippan.employee_full_reverse_office_sus_summary), 'INFO')
                        print_log('employee_full = {}'.format(ippan.employee_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0130)
                ### 事業所被害額_営業停滞に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果
                ############################################################### 
                if ippan.employee_lv00_reverse_office_stg_summary is not None: 
                    if float(ippan.employee_lv00_reverse_office_stg_summary) - float(ippan.employee_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv00_reverse_office_stg_summary = {}'.format(ippan.employee_lv00_reverse_office_stg_summary), 'INFO')
                        print_log('employee_lv00 = {}'.format(ippan.employee_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv01_49_reverse_office_stg_summary is not None: 
                    if float(ippan.employee_lv01_49_reverse_office_stg_summary) - float(ippan.employee_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv01_49_reverse_office_stg_summary = {}'.format(ippan.employee_lv01_49_reverse_office_stg_summary), 'INFO')
                        print_log('employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv50_99_reverse_office_stg_summary is not None:
                    if float(ippan.employee_lv50_99_reverse_office_stg_summary) - float(ippan.employee_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv50_99_reverse_office_stg_summary = {}'.format(ippan.employee_lv50_99_reverse_office_stg_summary), 'INFO')
                        print_log('employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.employee_lv100_reverse_office_stg_summary is not None:
                    if float(ippan.employee_lv100_reverse_office_stg_summary) - float(ippan.employee_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_lv100_reverse_office_stg_summary = {}'.format(ippan.employee_lv100_reverse_office_stg_summary), 'INFO')
                        print_log('employee_lv100 = {}'.format(ippan.employee_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.employee_half_reverse_office_stg_summary is not None:
                ###     if float(ippan.employee_half_reverse_office_stg_summary) - float(ippan.employee_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('employee_half_reverse_office_stg_summary = {}'.format(ippan.employee_half_reverse_office_stg_summary), 'INFO')
                ###         print_log('employee_half = {}'.format(ippan.employee_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.employee_full_reverse_office_stg_summary is not None:
                    if float(ippan.employee_full_reverse_office_stg_summary) - float(ippan.employee_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('employee_full_reverse_office_stg_summary = {}'.format(ippan.employee_full_reverse_office_stg_summary), 'INFO')
                        print_log('employee_full = {}'.format(ippan.employee_full), 'INFO')
                        failure_count = failure_count + 1

                ###############################################################
                ### 計算処理(0140)
                ### 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                ###############################################################
                if ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary is not None: 
                    if float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv00_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary), 'INFO')
                        print_log('farmer_fisher_lv00 = {}'.format(ippan.farmer_fisher_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary is not None: 
                    if float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary), 'INFO')
                        print_log('farmer_fisher_lv01_49 = {}'.format(ippan.farmer_fisher_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary is not None:
                    if float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary), 'INFO')
                        print_log('farmer_fisher_lv50_99 = {}'.format(ippan.farmer_fisher_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary is not None:
                    if float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv100_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary), 'INFO')
                        print_log('farmer_fisher_lv100 = {}'.format(ippan.farmer_fisher_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary is not None:
                ###     if float(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('farmer_fisher_half_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary), 'INFO')
                ###         print_log('farmer_fisher_half = {}'.format(ippan.farmer_fisher_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary is not None:
                    if float(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_full_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary), 'INFO')
                        print_log('farmer_fisher_full = {}'.format(ippan.farmer_fisher_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0150)
                ### 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果
                ############################################################### 
                if ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary is not None: 
                    if float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv00_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary), 'INFO')
                        print_log('farmer_fisher_lv00 = {}'.format(ippan.farmer_fisher_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary is not None: 
                    if float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary), 'INFO')
                        print_log('farmer_fisher_lv01_49 = {}'.format(ippan.farmer_fisher_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary is not None:
                    if float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary), 'INFO')
                        print_log('farmer_fisher_lv50_99 = {}'.format(ippan.farmer_fisher_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary is not None:
                    if float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_lv100_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary), 'INFO')
                        print_log('farmer_fisher_lv100 = {}'.format(ippan.farmer_fisher_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary is not None:
                ###     if float(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('farmer_fisher_half_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary), 'INFO')
                ###         print_log('farmer_fisher_half = {}'.format(ippan.farmer_fisher_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary is not None:
                    if float(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('farmer_fisher_full_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary), 'INFO')
                        print_log('farmer_fisher_full = {}'.format(ippan.farmer_fisher_full), 'INFO')
                        failure_count = failure_count + 1

                ############################################################### 
                ### 計算処理(0160)
                ### 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 
                ############################################################### 
                if ippan.office_lv00_reverse_office_alt_summary is not None: 
                    if float(ippan.office_lv00_reverse_office_alt_summary) - float(ippan.office_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('office_lv00_reverse_office_alt_summary = {}'.format(ippan.office_lv00_reverse_office_alt_summary), 'INFO')
                        print_log('office_lv00 = {}'.format(ippan.office_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.office_lv01_49_reverse_office_alt_summary is not None: 
                    if float(ippan.office_lv01_49_reverse_office_alt_summary) - float(ippan.office_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('office_lv01_49_reverse_office_alt_summary = {}'.format(ippan.office_lv01_49_reverse_office_alt_summary), 'INFO')
                        print_log('office_lv01_49 = {}'.format(ippan.office_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.office_lv50_99_reverse_office_alt_summary is not None:
                    if float(ippan.office_lv50_99_reverse_office_alt_summary) - float(ippan.office_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('office_lv50_99_reverse_office_alt_summary = {}'.format(ippan.office_lv50_99_reverse_office_alt_summary), 'INFO')
                        print_log('office_lv50_99 = {}'.format(ippan.office_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.office_lv100_reverse_office_alt_summary is not None:
                    if float(ippan.office_lv100_reverse_office_alt_summary) - float(ippan.office_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('office_lv100_reverse_office_alt_summary = {}'.format(ippan.office_lv100_reverse_office_alt_summary), 'INFO')
                        print_log('office_lv100 = {}'.format(ippan.office_lv100), 'INFO')
                        failure_count = failure_count + 1
                ### if ippan.office_half_reverse_office_alt_summary is not None:
                ###     if float(ippan.office_half_reverse_office_alt_summary) - float(ippan.office_half) <= 0.0000001:
                ###         success_count = success_count + 1
                ###     else:
                ###         print_log('office_half_reverse_office_alt_summary = {}'.format(ippan.office_half_reverse_office_alt_summary), 'INFO')
                ###         print_log('office_half = {}'.format(ippan.office_half), 'INFO')
                ###         failure_count = failure_count + 1
                if ippan.office_full_reverse_office_alt_summary is not None:
                    if float(ippan.office_full_reverse_office_alt_summary) - float(ippan.office_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('office_full_reverse_office_alt_summary = {}'.format(ippan.office_full_reverse_office_alt_summary), 'INFO')
                        print_log('office_full = {}'.format(ippan.office_full), 'INFO')
                        failure_count = failure_count + 1

            print_log('success_count = {}'.format(success_count), 'INFO')
            print_log('failure_count = {}'.format(failure_count), 'INFO')
                    
            ################################################################### 
            ### DBアクセス処理(0170)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 6/10.', 'INFO')
            print_log('trigger_id_list[0] = {}'.format(trigger_id_list[0]), 'INFO')
            connection_cursor.execute("""
                UPDATE TRIGGER SET 
                CONSUMED_AT=CURRENT_TIMESTAMP, 
                SUCCESS_COUNT=%s, 
                FAILURE_COUNT=%s 
                WHERE TRIGGER_ID=%s""", [
                success_count, 
                failure_count, 
                trigger_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0180)
            ### 当該トリガーの実行が終了したため、当該レポジトリの状態、成功数、失敗数等を更新する。
            ### (1)成功の場合は、ステータスを 3 に更新する。
            ### (2)失敗の場合は、ステータスを 4 に更新する。
            ################################################################### 
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 7/10.', 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            if failure_count == 0: 
                connection_cursor.execute("""
                    UPDATE REPOSITORY SET 
                    ACTION_CODE='7', 
                    STATUS_CODE='3', 
                    UPDATED_AT=CURRENT_TIMESTAMP 
                    WHERE REPOSITORY_ID=%s""", [
                    repository_id_list[0],])
            else:
                connection_cursor.execute("""
                    UPDATE REPOSITORY SET 
                    ACTION_CODE='7', 
                    STATUS_CODE='4', 
                    UPDATED_AT=CURRENT_TIMESTAMP 
                    WHERE REPOSITORY_ID=%s""", [
                    repository_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0190)
            ### 当該トリガーの実行が終了したため、
            ### (1)成功の場合は、次のトリガーを発行する。
            ### (2)失敗の場合は、次のトリガーを発行しない。
            ################################################################### 
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 8/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            if failure_count == 0:
                connection_cursor.execute("""
                    INSERT INTO TRIGGER (TRIGGER_ID, SUIGAI_ID, REPOSITORY_ID, ACTION_CODE, PUBLISHED_AT) VALUES (
                    (SELECT MAX(TRIGGER_ID) + 1 FROM TRIGGER), 
                    %s, 
                    %s, 
                    '8', 
                    CURRENT_TIMESTAMP)""", [
                    suigai_id_list[0], repository_id_list[0], ])
            else:
                pass

            ################################################################### 
            ### DBアクセス処理(0200)
            ################################################################### 
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 9/10.', 'INFO')
            transaction.commit()

            ###################################################################
            ### 戻り値セット処理(0210)
            ###################################################################
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数 STEP 10/10.', 'INFO')
            print_log('[INFO] P0900CI.action_07_reverse.handle()関数が正常終了しました。', 'INFO')
            return 0
        
        except:
            transaction.rollback()
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P0900CI.action_07_reverse.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900CI.action_07_reverse.handle()関数が異常終了しました。', 'ERROR')
            return 8

        finally:
            connection_cursor.close()
            