#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/management/commands/action_A08_verify_sdb_by_reverse_method.py
### A08：データ検証
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

from P0000Common.models import AREA                    ### 7000: 入力データ_水害区域
from P0000Common.models import WEATHER                 ### 7010: 入力データ_異常気象
from P0000Common.models import SUIGAI                  ### 7020: 入力データ_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7030: 入力データ_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7040: ビューデータ_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 集計データ

from P0000Common.models import ACTION                  ### 10000: アクション
from P0000Common.models import STATUS                  ### 10010: 状態
from P0000Common.models import TRIGGER                 ### 10020: トリガーメッセージ
from P0000Common.models import APPROVAL                ### 10030: 承認メッセージ
from P0000Common.models import FEEDBACK                ### 10040: フィードバックメッセージ

from P0000Common.common import get_debug_log
from P0000Common.common import get_error_log
from P0000Common.common import get_info_log
from P0000Common.common import get_warn_log
from P0000Common.common import print_log
from P0000Common.common import reset_log

###############################################################################
### クラス名： Command
###############################################################################
class Command(BaseCommand):
    
    ###########################################################################
    ### 関数名： handle
    ### チェックOKの場合、トリガーの状態を成功に更新、消費日時をカレントに更新、新たなトリガーを生成する。
    ### チェックNGの場合、トリガーの状態を失敗に更新、消費日時をカレントに更新する。
    ### チェックNGの場合、当該水害IDについて、以降の処理を止めて、手動？で再実行、または、入力データから再登録するイメージである。
    ### 上記は、このアプリの共通の考え方とする。
    ###########################################################################
    def handle(self, *args, **options):
        try:
            ###################################################################
            ### 引数チェック処理(0000)
            ### コマンドラインからの引数をチェックする。
            ###################################################################
            reset_log()
            print_log('[INFO] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が開始しました。', 'INFO')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 1/8.', 'DEBUG')
    
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
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 2/8.', 'DEBUG')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE 
                    action_code='A08' AND 
                    consumed_at IS NULL AND 
                    deleted_at IS NULL 
                ORDER BY CAST(trigger_id AS INTEGER) LIMIT 1""", [])

            if trigger_list is None:
                print_log('[INFO] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
                return 0

            if len(trigger_list) == 0:
                print_log('[INFO] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
                return 0

            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].trigger_id = {}'.format(trigger_list[0].trigger_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].suigai_id = {}'.format(trigger_list[0].suigai_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].city_code = {}'.format(trigger_list[0].city_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].ken_code = {}'.format(trigger_list[0].ken_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].download_file_path = {}'.format(trigger_list[0].download_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].download_file_name = {}'.format(trigger_list[0].download_file_name), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].upload_file_path = {}'.format(trigger_list[0].upload_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 trigger_list[0].upload_file_name = {}'.format(trigger_list[0].upload_file_name), 'DEBUG')
            
            ###################################################################
            ### DBアクセス処理(0020)
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 3/8.', 'DEBUG')
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
    
                    CASE WHEN (IV1.residential_area) IS NULL THEN 0 ELSE CAST(IV1.residential_area AS NUMERIC(20,10)) END AS residential_area, 
                    CASE WHEN (IV1.agricultural_area) IS NULL THEN 0 ELSE CAST(IV1.agricultural_area AS NUMERIC(20,10)) END AS agricultural_area, 
                    CASE WHEN (IV1.underground_area) IS NULL THEN 0 ELSE CAST(IV1.underground_area AS NUMERIC(20,10)) END AS underground_area, 
                    IV1.kasen_kaigan_code AS kasen_kaigan_code, 
                    IV1.kasen_kaigan_name AS kasen_kaigan_name, 
                    CASE WHEN (IV1.crop_damage) IS NULL THEN 0 ELSE CAST(IV1.crop_damage AS NUMERIC(20,10)) END AS crop_damage, 
                    IV1.weather_id AS weather_id, 
                    IV1.weather_name AS weather_name, 
                    IV1.deleted_at AS deleted_at, 
                    
                    IV1.building_code AS building_code, 
                    IV1.building_name AS building_name, 
                    IV1.underground_code AS underground_code, 
                    IV1.underground_name AS underground_name, 
                    IV1.flood_sediment_code AS flood_sediment_code, 
                    IV1.flood_sediment_name AS flood_sediment_name, 

                    CASE WHEN (IV1.building_lv00) IS NULL THEN 0 ELSE CAST(IV1.building_lv00 AS NUMERIC(20,10)) END AS building_lv00, 
                    CASE WHEN (IV1.building_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.building_lv01_49 AS NUMERIC(20,10)) END AS building_lv01_49, 
                    CASE WHEN (IV1.building_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.building_lv50_99 AS NUMERIC(20,10)) END AS building_lv50_99, 
                    CASE WHEN (IV1.building_lv100) IS NULL THEN 0 ELSE CAST(IV1.building_lv100 AS NUMERIC(20,10)) END AS building_lv100, 
                    CASE WHEN (IV1.building_half) IS NULL THEN 0 ELSE CAST(IV1.building_half AS NUMERIC(20,10)) END AS building_half, 
                    CASE WHEN (IV1.building_full) IS NULL THEN 0 ELSE CAST(IV1.building_full AS NUMERIC(20,10)) END AS building_full, 
                    CASE WHEN (IV1.building_total) IS NULL THEN 0 ELSE CAST(IV1.building_total AS NUMERIC(20,10)) END AS building_total, 
     
                    CASE WHEN (IV1.floor_area) IS NULL THEN 0 ELSE CAST(IV1.floor_area AS NUMERIC(20,10)) END AS floor_area, 
                    CASE WHEN (IV1.family) IS NULL THEN 0 ELSE CAST(IV1.family AS NUMERIC(20,10)) END AS family, 
                    CASE WHEN (IV1.office) IS NULL THEN 0 ELSE CAST(IV1.office AS NUMERIC(20,10)) END AS office, 
    
                    CASE WHEN (IV1.floor_area_lv00) IS NULL THEN 0 ELSE CAST(IV1.floor_area_lv00 AS NUMERIC(20,10)) END AS floor_area_lv00, 
                    CASE WHEN (IV1.floor_area_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.floor_area_lv01_49 AS NUMERIC(20,10)) END AS floor_area_lv01_49, 
                    CASE WHEN (IV1.floor_area_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.floor_area_lv50_99 AS NUMERIC(20,10)) END AS floor_area_lv50_99, 
                    CASE WHEN (IV1.floor_area_lv100) IS NULL THEN 0 ELSE CAST(IV1.floor_area_lv100 AS NUMERIC(20,10)) END AS floor_area_lv100, 
                    CASE WHEN (IV1.floor_area_half) IS NULL THEN 0 ELSE CAST(IV1.floor_area_half AS NUMERIC(20,10)) END AS floor_area_half, 
                    CASE WHEN (IV1.floor_area_full) IS NULL THEN 0 ELSE CAST(IV1.floor_area_full AS NUMERIC(20,10)) END AS floor_area_full, 
                    CASE WHEN (IV1.floor_area_total) IS NULL THEN 0 ELSE CAST(IV1.floor_area_total AS NUMERIC(20,10)) END AS floor_area_total, 
                    
                    CASE WHEN (IV1.family_lv00) IS NULL THEN 0 ELSE CAST(IV1.family_lv00 AS NUMERIC(20,10)) END AS family_lv00, 
                    CASE WHEN (IV1.family_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.family_lv01_49 AS NUMERIC(20,10)) END AS family_lv01_49, 
                    CASE WHEN (IV1.family_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.family_lv50_99 AS NUMERIC(20,10)) END AS family_lv50_99, 
                    CASE WHEN (IV1.family_lv100) IS NULL THEN 0 ELSE CAST(IV1.family_lv100 AS NUMERIC(20,10)) END AS family_lv100, 
                    CASE WHEN (IV1.family_half) IS NULL THEN 0 ELSE CAST(IV1.family_half AS NUMERIC(20,10)) END AS family_half, 
                    CASE WHEN (IV1.family_full) IS NULL THEN 0 ELSE CAST(IV1.family_full AS NUMERIC(20,10)) END AS family_full, 
                    CASE WHEN (IV1.family_total) IS NULL THEN 0 ELSE CAST(IV1.family_total AS NUMERIC(20,10)) END AS family_total, 
                   
                    CASE WHEN (IV1.office_lv00) IS NULL THEN 0 ELSE CAST(IV1.office_lv00 AS NUMERIC(20,10)) END AS office_lv00, 
                    CASE WHEN (IV1.office_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.office_lv01_49 AS NUMERIC(20,10)) END AS office_lv01_49, 
                    CASE WHEN (IV1.office_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.office_lv50_99 AS NUMERIC(20,10)) END AS office_lv50_99, 
                    CASE WHEN (IV1.office_lv100) IS NULL THEN 0 ELSE CAST(IV1.office_lv100 AS NUMERIC(20,10)) END AS office_lv100, 
                    CASE WHEN (IV1.office_half) IS NULL THEN 0 ELSE CAST(IV1.office_half AS NUMERIC(20,10)) END AS office_half, 
                    CASE WHEN (IV1.office_full) IS NULL THEN 0 ELSE CAST(IV1.office_full AS NUMERIC(20,10)) END AS office_full, 
                    CASE WHEN (IV1.office_total) IS NULL THEN 0 ELSE CAST(IV1.office_total AS NUMERIC(20,10)) END AS office_total, 
    
                    CASE WHEN (IV1.farmer_fisher_lv00) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_lv00, 
                    CASE WHEN (IV1.farmer_fisher_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49, 
                    CASE WHEN (IV1.farmer_fisher_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99, 
                    CASE WHEN (IV1.farmer_fisher_lv100) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_lv100, 
                    -- CASE WHEN (IV1.farmer_fisher_half) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_half AS NUMERIC(20,10)) END AS farmer_fisher_half, 
                    CASE WHEN (IV1.farmer_fisher_full) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_full AS NUMERIC(20,10)) END AS farmer_fisher_full, 
                    CASE WHEN (IV1.farmer_fisher_total) IS NULL THEN 0 ELSE CAST(IV1.farmer_fisher_total AS NUMERIC(20,10)) END AS farmer_fisher_total, 
    
                    CASE WHEN (IV1.employee_lv00) IS NULL THEN 0 ELSE CAST(IV1.employee_lv00 AS NUMERIC(20,10)) END AS employee_lv00, 
                    CASE WHEN (IV1.employee_lv01_49) IS NULL THEN 0 ELSE CAST(IV1.employee_lv01_49 AS NUMERIC(20,10)) END AS employee_lv01_49, 
                    CASE WHEN (IV1.employee_lv50_99) IS NULL THEN 0 ELSE CAST(IV1.employee_lv50_99 AS NUMERIC(20,10)) END AS employee_lv50_99, 
                    CASE WHEN (IV1.employee_lv100) IS NULL THEN 0 ELSE CAST(IV1.employee_lv100 AS NUMERIC(20,10)) END AS employee_lv100, 
                    -- CASE WHEN (IV1.employee_half) IS NULL THEN 0 ELSE CAST(IV1.employee_half AS NUMERIC(20,10)) END AS employee_half, 
                    CASE WHEN (IV1.employee_full) IS NULL THEN 0 ELSE CAST(IV1.employee_full AS NUMERIC(20,10)) END AS employee_full,
                    CASE WHEN (IV1.employee_total) IS NULL THEN 0 ELSE CAST(IV1.employee_total AS NUMERIC(20,10)) END AS employee_total, 
    
                    IV1.industry_code AS industry_code, 
                    IV1.industry_name AS industry_name, 
                    IV1.usage_code AS usage_code,
                    IV1.usage_name AS usage_name, 

                    -- 県別家屋評価額(マスタDB) 
                    CASE WHEN (HA1.house_asset) IS NULL THEN 0 ELSE CAST(HA1.house_asset AS NUMERIC(20,10)) END AS house_asset, 
                    
                    -- 家屋被害率(マスタDB) 
                    CASE WHEN (HR1.house_rate_lv00) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv00 AS NUMERIC(20,10)) END AS house_rate_lv00, 
                    CASE WHEN (HR1.house_rate_lv00_50) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv00_50 AS NUMERIC(20,10)) END AS house_rate_lv00_50, 
                    CASE WHEN (HR1.house_rate_lv50_100) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv50_100 AS NUMERIC(20,10)) END AS house_rate_lv50_100, 
                    CASE WHEN (HR1.house_rate_lv100_200) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv100_200 AS NUMERIC(20,10)) END AS house_rate_lv100_200, 
                    CASE WHEN (HR1.house_rate_lv200_300) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv200_300 AS NUMERIC(20,10)) END AS house_rate_lv200_300, 
                    CASE WHEN (HR1.house_rate_lv300) IS NULL THEN 0 ELSE CAST(HR1.house_rate_lv300 AS NUMERIC(20,10)) END AS house_rate_lv300, 
                    
                    -- 家庭用品自動車以外所有額(マスタDB) 
                    CASE WHEN (HHA1.household_asset) IS NULL THEN 0 ELSE CAST(HHA1.household_asset AS NUMERIC(20,10)) END AS household_asset, 
                    
                    -- 家庭用品自動車以外被害率(マスタDB) 
                    CASE WHEN (HHR1.household_rate_lv00) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv00 AS NUMERIC(20,10)) END AS household_rate_lv00, 
                    CASE WHEN (HHR1.household_rate_lv00_50) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv00_50 AS NUMERIC(20,10)) END AS household_rate_lv00_50, 
                    CASE WHEN (HHR1.household_rate_lv50_100) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv50_100 AS NUMERIC(20,10)) END AS household_rate_lv50_100, 
                    CASE WHEN (HHR1.household_rate_lv100_200) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv100_200 AS NUMERIC(20,10)) END AS household_rate_lv100_200, 
                    CASE WHEN (HHR1.household_rate_lv200_300) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv200_300 AS NUMERIC(20,10)) END AS household_rate_lv200_300, 
                    CASE WHEN (HHR1.household_rate_lv300) IS NULL THEN 0 ELSE CAST(HHR1.household_rate_lv300 AS NUMERIC(20,10)) END AS household_rate_lv300, 
                    
                    -- 家庭用品自動車所有額(マスタDB) 
                    CASE WHEN (CA1.car_asset) IS NULL THEN 0 ELSE CAST(CA1.car_asset AS NUMERIC(20,10)) END AS car_asset, 
    
                    -- 家庭用品自動車被害率(マスタDB) 
                    CASE WHEN (CR1.car_rate_lv00) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv00 AS NUMERIC(20,10)) END AS car_rate_lv00, 
                    CASE WHEN (CR1.car_rate_lv00_50) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv00_50 AS NUMERIC(20,10)) END AS car_rate_lv00_50, 
                    CASE WHEN (CR1.car_rate_lv50_100) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv50_100 AS NUMERIC(20,10)) END AS car_rate_lv50_100, 
                    CASE WHEN (CR1.car_rate_lv100_200) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv100_200 AS NUMERIC(20,10)) END AS car_rate_lv100_200, 
                    CASE WHEN (CR1.car_rate_lv200_300) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv200_300 AS NUMERIC(20,10)) END AS car_rate_lv200_300, 
                    CASE WHEN (CR1.car_rate_lv300) IS NULL THEN 0 ELSE CAST(CR1.car_rate_lv300 AS NUMERIC(20,10)) END AS car_rate_lv300, 
                    
                    -- 家庭応急対策費_代替活動費(マスタDB)
                    CASE WHEN (HALT1.house_alt_lv00) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv00 AS NUMERIC(20,10)) END AS house_alt_lv00, 
                    CASE WHEN (HALT1.house_alt_lv00_50) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv00_50 AS NUMERIC(20,10)) END AS house_alt_lv00_50, 
                    CASE WHEN (HALT1.house_alt_lv50_100) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv50_100 AS NUMERIC(20,10)) END AS house_alt_lv50_100, 
                    CASE WHEN (HALT1.house_alt_lv100_200) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv100_200 AS NUMERIC(20,10)) END AS house_alt_lv100_200, 
                    CASE WHEN (HALT1.house_alt_lv200_300) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv200_300 AS NUMERIC(20,10)) END AS house_alt_lv200_300, 
                    CASE WHEN (HALT1.house_alt_lv300) IS NULL THEN 0 ELSE CAST(HALT1.house_alt_lv300 AS NUMERIC(20,10)) END AS house_alt_lv300, 
    
                    -- 家庭応急対策費_清掃労働単価(マスタDB) 
                    CASE WHEN (HCL1.house_clean_unit_cost) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_unit_cost AS NUMERIC(20,10)) END AS house_clean_unit_cost, 
    
                    -- 家庭応急対策費_清掃日数(マスタDB) 
                    CASE WHEN (HCL1.house_clean_days_lv00) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv00 AS NUMERIC(20,10)) END AS house_clean_days_lv00, 
                    CASE WHEN (HCL1.house_clean_days_lv00_50) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv00_50 AS NUMERIC(20,10)) END AS house_clean_days_lv00_50, 
                    CASE WHEN (HCL1.house_clean_days_lv50_100) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv50_100 AS NUMERIC(20,10)) END AS house_clean_days_lv50_100, 
                    CASE WHEN (HCL1.house_clean_days_lv100_200) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv100_200 AS NUMERIC(20,10)) END AS house_clean_days_lv100_200, 
                    CASE WHEN (HCL1.house_clean_days_lv200_300) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv200_300 AS NUMERIC(20,10)) END AS house_clean_days_lv200_300, 
                    CASE WHEN (HCL1.house_clean_days_lv300) IS NULL THEN 0 ELSE CAST(HCL1.house_clean_days_lv300 AS NUMERIC(20,10)) END AS house_clean_days_lv300, 
                    
                    -- 事業所資産額_償却資産額(マスタDB) 
                    CASE WHEN (OA1.office_dep_asset) IS NULL THEN 0 ELSE CAST(OA1.office_dep_asset AS NUMERIC(20,10)) END AS office_dep_asset, 
                    
                    -- 事業所被害率_償却資産被害率(マスタDB) 
                    CASE WHEN (OR1.office_dep_rate_lv00) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv00 AS NUMERIC(20,10)) END AS office_dep_rate_lv00, 
                    CASE WHEN (OR1.office_dep_rate_lv00_50) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv00_50 AS NUMERIC(20,10)) END AS office_dep_rate_lv00_50, 
                    CASE WHEN (OR1.office_dep_rate_lv50_100) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv50_100 AS NUMERIC(20,10)) END AS office_dep_rate_lv50_100, 
                    CASE WHEN (OR1.office_dep_rate_lv100_200) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv100_200 AS NUMERIC(20,10)) END AS office_dep_rate_lv100_200, 
                    -- CASE WHEN (OR1.office_dep_rate_lv200_300) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv200_300 AS NUMERIC(20,10)) END AS office_dep_rate_lv200_300, 
                    CASE WHEN (OR1.office_dep_rate_lv300) IS NULL THEN 0 ELSE CAST(OR1.office_dep_rate_lv300 AS NUMERIC(20,10)) END AS office_dep_rate_lv300, 
    
                    -- 事業所資産額_在庫資産額(マスタDB) 
                    CASE WHEN (OA1.office_inv_asset) IS NULL THEN 0 ELSE CAST(OA1.office_inv_asset AS NUMERIC(20,10)) END AS office_inv_asset, 
    
                    -- 事業所被害率_在庫資産被害率(マスタDB) 
                    CASE WHEN (OR1.office_inv_rate_lv00) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv00 AS NUMERIC(20,10)) END AS office_inv_rate_lv00, 
                    CASE WHEN (OR1.office_inv_rate_lv00_50) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv00_50 AS NUMERIC(20,10)) END AS office_inv_rate_lv00_50, 
                    CASE WHEN (OR1.office_inv_rate_lv50_100) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv50_100 AS NUMERIC(20,10)) END AS office_inv_rate_lv50_100, 
                    CASE WHEN (OR1.office_inv_rate_lv100_200) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv100_200 AS NUMERIC(20,10)) END AS office_inv_rate_lv100_200, 
                    -- CASE WHEN (OR1.office_inv_rate_lv200_300) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv200_300 AS NUMERIC(20,10)) END AS office_inv_rate_lv200_300, 
                    CASE WHEN (OR1.office_inv_rate_lv300) IS NULL THEN 0 ELSE CAST(OR1.office_inv_rate_lv300 AS NUMERIC(20,10)) END AS office_inv_rate_lv300, 
    
                    -- 事業所資産額_付加価値額(マスタDB) 
                    CASE WHEN (OA1.office_va_asset) IS NULL THEN 0 ELSE CAST(OA1.office_va_asset AS NUMERIC(20,10)) END AS office_va_asset, 
    
                    -- 事業所被害額_営業停止に伴う被害額(マスタDB) 
                    CASE WHEN (OSUS1.office_sus_days_lv00) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv00 AS NUMERIC(20,10)) END AS office_sus_days_lv00, 
                    CASE WHEN (OSUS1.office_sus_days_lv00_50) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv00_50 AS NUMERIC(20,10)) END AS office_sus_days_lv00_50, 
                    CASE WHEN (OSUS1.office_sus_days_lv50_100) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv50_100 AS NUMERIC(20,10)) END AS office_sus_days_lv50_100, 
                    CASE WHEN (OSUS1.office_sus_days_lv100_200) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv100_200 AS NUMERIC(20,10)) END AS office_sus_days_lv100_200, 
                    -- CASE WHEN (OSUS1.office_sus_days_lv200_300) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv200_300 AS NUMERIC(20,10)) END AS office_sus_days_lv200_300, 
                    CASE WHEN (OSUS1.office_sus_days_lv300) IS NULL THEN 0 ELSE CAST(OSUS1.office_sus_days_lv300 AS NUMERIC(20,10)) END AS office_sus_days_lv300, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(マスタDB) 
                    CASE WHEN (OSTG1.office_stg_days_lv00) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv00 AS NUMERIC(20,10)) END AS office_stg_days_lv00, 
                    CASE WHEN (OSTG1.office_stg_days_lv00_50) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv00_50 AS NUMERIC(20,10)) END AS office_stg_days_lv00_50, 
                    CASE WHEN (OSTG1.office_stg_days_lv50_100) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv50_100 AS NUMERIC(20,10)) END AS office_stg_days_lv50_100, 
                    CASE WHEN (OSTG1.office_stg_days_lv100_200) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv100_200 AS NUMERIC(20,10)) END AS office_stg_days_lv100_200, 
                    -- CASE WHEN (OSTG1.office_stg_days_lv200_300) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv200_300 AS NUMERIC(20,10)) END AS office_stg_days_lv200_300, 
                    CASE WHEN (OSTG1.office_stg_days_lv300) IS NULL THEN 0 ELSE CAST(OSTG1.office_stg_days_lv300 AS NUMERIC(20,10)) END AS office_stg_days_lv300, 
                    
                    -- 農漁家資産額_償却資産額(マスタDB) 
                    CASE WHEN (FFA1.farmer_fisher_dep_asset) IS NULL THEN 0 ELSE CAST(FFA1.farmer_fisher_dep_asset AS NUMERIC(20,10)) END AS farmer_fisher_dep_asset, 
                    
                    -- 農漁家被害率_償却資産被害率(マスタDB) 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv00) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv00, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv00_50) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv00_50 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv00_50, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv50_100) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv50_100 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv50_100, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv100_200) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv100_200 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv100_200, 
                    -- CASE WHEN (FFR1.farmer_fisher_dep_rate_lv200_300) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv200_300 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv200_300, 
                    CASE WHEN (FFR1.farmer_fisher_dep_rate_lv300) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_dep_rate_lv300 AS NUMERIC(20,10)) END AS farmer_fisher_dep_rate_lv300, 
    
                    -- 農漁家資産額_在庫資産額(マスタDB) 
                    CASE WHEN (FFA1.farmer_fisher_inv_asset) IS NULL THEN 0 ELSE CAST(FFA1.farmer_fisher_inv_asset AS NUMERIC(20,10)) END AS farmer_fisher_inv_asset, 
                    
                    -- 農漁家被害率_在庫資産被害率(マスタDB) 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv00) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv00, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv00_50) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv00_50 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv00_50, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv50_100) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv50_100 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv50_100, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv100_200) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv100_200 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv100_200, 
                    -- CASE WHEN (FFR1.farmer_fisher_inv_rate_lv200_300) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv200_300 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv200_300, 
                    CASE WHEN (FFR1.farmer_fisher_inv_rate_lv300) IS NULL THEN 0 ELSE CAST(FFR1.farmer_fisher_inv_rate_lv300 AS NUMERIC(20,10)) END AS farmer_fisher_inv_rate_lv300, 
                    
                    -- 事業所応急対策費_代替活動費(マスタDB) 
                    CASE WHEN (OALT1.office_alt_lv00) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv00 AS NUMERIC(20,10)) END AS office_alt_lv00, 
                    CASE WHEN (OALT1.office_alt_lv00_50) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv00_50 AS NUMERIC(20,10)) END AS office_alt_lv00_50, 
                    CASE WHEN (OALT1.office_alt_lv50_100) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv50_100 AS NUMERIC(20,10)) END AS office_alt_lv50_100, 
                    CASE WHEN (OALT1.office_alt_lv100_200) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv100_200 AS NUMERIC(20,10)) END AS office_alt_lv100_200, 
                    CASE WHEN (OALT1.office_alt_lv200_300) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv200_300 AS NUMERIC(20,10)) END AS office_alt_lv200_300, 
                    CASE WHEN (OALT1.office_alt_lv300) IS NULL THEN 0 ELSE CAST(OALT1.office_alt_lv300 AS NUMERIC(20,10)) END AS office_alt_lv300, 
                    
                    -- 家屋被害額(集計DB) 
                    CASE WHEN (IS1.house_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.house_summary_lv00 AS NUMERIC(20,10)) END AS house_summary_lv00, 
                    CASE WHEN (IS1.house_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.house_summary_lv01_49 AS NUMERIC(20,10)) END AS house_summary_lv01_49, 
                    CASE WHEN (IS1.house_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.house_summary_lv50_99 AS NUMERIC(20,10)) END AS house_summary_lv50_99, 
                    CASE WHEN (IS1.house_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.house_summary_lv100 AS NUMERIC(20,10)) END AS house_summary_lv100, 
                    CASE WHEN (IS1.house_summary_half) IS NULL THEN 0 ELSE CAST(IS1.house_summary_half AS NUMERIC(20,10)) END AS house_summary_half, 
                    CASE WHEN (IS1.house_summary_full) IS NULL THEN 0 ELSE CAST(IS1.house_summary_full AS NUMERIC(20,10)) END AS house_summary_full, 
                    
                    -- 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv00 / (HA1.house_asset * HR1.house_rate_lv00) AS NUMERIC(20,10)) END AS floor_area_lv00_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv01_49 / (HA1.house_asset * HR1.house_rate_lv00_50) AS NUMERIC(20,10)) END AS floor_area_lv01_49_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv50_99 / (HA1.house_asset * HR1.house_rate_lv50_100) AS NUMERIC(20,10)) END AS floor_area_lv50_99_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_lv100 / (HA1.house_asset * HR1.house_rate_lv100_200) AS NUMERIC(20,10)) END AS floor_area_lv100_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_half / (HA1.house_asset * HR1.house_rate_lv200_300) AS NUMERIC(20,10)) END AS floor_area_half_reverse_house_summary, 
                    CASE WHEN ABS(HA1.house_asset * HR1.house_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_summary_full / (HA1.house_asset * HR1.house_rate_lv300) AS NUMERIC(20,10)) END AS floor_area_full_reverse_house_summary, 
                    
                    -- 家庭用品自動車以外被害額(集計DB) 
                    CASE WHEN (IS1.household_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.household_summary_lv00 AS NUMERIC(20,10)) END AS household_summary_lv00,
                    CASE WHEN (IS1.household_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.household_summary_lv01_49 AS NUMERIC(20,10)) END AS household_summary_lv01_49, 
                    CASE WHEN (IS1.household_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.household_summary_lv50_99 AS NUMERIC(20,10)) END AS household_summary_lv50_99, 
                    CASE WHEN (IS1.household_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.household_summary_lv100 AS NUMERIC(20,10)) END AS household_summary_lv100, 
                    CASE WHEN (IS1.household_summary_half) IS NULL THEN 0 ELSE CAST(IS1.household_summary_half AS NUMERIC(20,10)) END AS household_summary_half, 
                    CASE WHEN (IS1.household_summary_full) IS NULL THEN 0 ELSE CAST(IS1.household_summary_full AS NUMERIC(20,10)) END AS household_summary_full, 
    
                    -- 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv00 / (HHA1.household_asset * HHR1.household_rate_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv01_49 / (HHA1.household_asset * HHR1.household_rate_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv50_99 / (HHA1.household_asset * HHR1.household_rate_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_lv100 / (HHA1.household_asset * HHR1.household_rate_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_half / (HHA1.household_asset * HHR1.household_rate_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_household_summary, 
                    CASE WHEN ABS(HHA1.household_asset * HHR1.household_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.household_summary_full / (HHA1.household_asset * HHR1.household_rate_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_household_summary, 
                    
                    -- 家庭用品自動車被害額(集計DB) 
                    CASE WHEN (IS1.car_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.car_summary_lv00 AS NUMERIC(20,10)) END AS car_summary_lv00, 
                    CASE WHEN (IS1.car_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.car_summary_lv01_49 AS NUMERIC(20,10)) END AS car_summary_lv01_49, 
                    CASE WHEN (IS1.car_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.car_summary_lv50_99 AS NUMERIC(20,10)) END AS car_summary_lv50_99, 
                    CASE WHEN (IS1.car_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.car_summary_lv100 AS NUMERIC(20,10)) END AS car_summary_lv100, 
                    CASE WHEN (IS1.car_summary_half) IS NULL THEN 0 ELSE CAST(IS1.car_summary_half AS NUMERIC(20,10)) END AS car_summary_half, 
                    CASE WHEN (IS1.car_summary_full) IS NULL THEN 0 ELSE CAST(IS1.car_summary_full AS NUMERIC(20,10)) END AS car_summary_full, 
    
                    -- 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv00 / (CA1.car_asset * CR1.car_rate_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv01_49 / (CA1.car_asset * CR1.car_rate_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv50_99 / (CA1.car_asset * CR1.car_rate_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_lv100 / (CA1.car_asset * CR1.car_rate_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_half / (CA1.car_asset * CR1.car_rate_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_car_summary, 
                    CASE WHEN ABS(CA1.car_asset * CR1.car_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.car_summary_full / (CA1.car_asset * CR1.car_rate_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_car_summary, 
    
                    -- 家庭応急対策費_代替活動費(集計DB) 
                    CASE WHEN (IS1.house_alt_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_lv00 AS NUMERIC(20,10)) END AS house_alt_summary_lv00, 
                    CASE WHEN (IS1.house_alt_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_lv01_49 AS NUMERIC(20,10)) END AS house_alt_summary_lv01_49, 
                    CASE WHEN (IS1.house_alt_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_lv50_99 AS NUMERIC(20,10)) END AS house_alt_summary_lv50_99, 
                    CASE WHEN (IS1.house_alt_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_lv100 AS NUMERIC(20,10)) END AS house_alt_summary_lv100, 
                    CASE WHEN (IS1.house_alt_summary_half) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_half AS NUMERIC(20,10)) END AS house_alt_summary_half, 
                    CASE WHEN (IS1.house_alt_summary_full) IS NULL THEN 0 ELSE CAST(IS1.house_alt_summary_full AS NUMERIC(20,10)) END AS house_alt_summary_full, 
    
                    -- 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HALT1.house_alt_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv00 / HALT1.house_alt_lv00 AS NUMERIC(20,10)) END AS family_lv00_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv01_49 / HALT1.house_alt_lv00_50 AS NUMERIC(20,10)) END AS family_lv01_49_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv50_99 / HALT1.house_alt_lv50_100 AS NUMERIC(20,10)) END AS family_lv50_99_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_lv100 / HALT1.house_alt_lv100_200 AS NUMERIC(20,10)) END AS family_lv100_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_half / HALT1.house_alt_lv200_300 AS NUMERIC(20,10)) END AS family_half_reverse_house_alt_summary, 
                    CASE WHEN ABS(HALT1.house_alt_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_alt_summary_full / HALT1.house_alt_lv300 AS NUMERIC(20,10)) END AS family_full_reverse_house_alt_summary, 
    
                    -- 家庭応急対策費_清掃費(集計DB) 
                    CASE WHEN (IS1.house_clean_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_lv00 AS NUMERIC(20,10)) END AS house_clean_summary_lv00, 
                    CASE WHEN (IS1.house_clean_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_lv01_49 AS NUMERIC(20,10)) END AS house_clean_summary_lv01_49, 
                    CASE WHEN (IS1.house_clean_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_lv50_99 AS NUMERIC(20,10)) END AS house_clean_summary_lv50_99, 
                    CASE WHEN (IS1.house_clean_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_lv100 AS NUMERIC(20,10)) END AS house_clean_summary_lv100, 
                    CASE WHEN (IS1.house_clean_summary_half) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_half AS NUMERIC(20,10)) END AS house_clean_summary_half, 
                    CASE WHEN (IS1.house_clean_summary_full) IS NULL THEN 0 ELSE CAST(IS1.house_clean_summary_full AS NUMERIC(20,10)) END AS house_clean_summary_full, 
    
                    -- 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv00 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00) AS NUMERIC(20,10)) END AS family_lv00_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv01_49 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv00_50) AS NUMERIC(20,10)) END AS family_lv01_49_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv50_99 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv50_100) AS NUMERIC(20,10)) END AS family_lv50_99_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_lv100 / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv100_200) AS NUMERIC(20,10)) END AS family_lv100_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_half / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv200_300) AS NUMERIC(20,10)) END AS family_half_reverse_house_clean_summary, 
                    CASE WHEN ABS(HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.house_clean_summary_full / (HCL1.house_clean_unit_cost * HCL1.house_clean_days_lv300) AS NUMERIC(20,10)) END AS family_full_reverse_house_clean_summary, 
    
                    -- 事業所被害額_償却資産被害額(集計DB) 
                    CASE WHEN (IS1.office_dep_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_lv00 AS NUMERIC(20,10)) END AS office_dep_summary_lv00, 
                    CASE WHEN (IS1.office_dep_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_lv01_49 AS NUMERIC(20,10)) END AS office_dep_summary_lv01_49, 
                    CASE WHEN (IS1.office_dep_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_lv50_99 AS NUMERIC(20,10)) END AS office_dep_summary_lv50_99, 
                    CASE WHEN (IS1.office_dep_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_lv100 AS NUMERIC(20,10)) END AS office_dep_summary_lv100, 
                    -- CASE WHEN (IS1.office_dep_summary_half) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_half AS NUMERIC(20,10)) END AS office_dep_summary_half, 
                    CASE WHEN (IS1.office_dep_summary_full) IS NULL THEN 0 ELSE CAST(IS1.office_dep_summary_full AS NUMERIC(20,10)) END AS office_dep_summary_full, 
                    
                    -- 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv00 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv01_49 / (OA1.office_dep_asset * OR1.office_dep_rate_lv00_50) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv50_99 / (OA1.office_dep_asset * OR1.office_dep_rate_lv50_100) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_lv100 / (OA1.office_dep_asset * OR1.office_dep_rate_lv100_200) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_dep_summary, 
                    -- CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_half / (OA1.office_dep_asset * OR1.office_dep_rate_lv200_300) AS NUMERIC(20,10)) END AS employee_half_reverse_office_dep_summary, 
                    CASE WHEN ABS(OA1.office_dep_asset * OR1.office_dep_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_dep_summary_full / (OA1.office_dep_asset * OR1.office_dep_rate_lv300) AS NUMERIC(20,10)) END AS employee_full_reverse_office_dep_summary, 
    
                    -- 事業所被害額_在庫資産被害額(集計DB) 
                    CASE WHEN (IS1.office_inv_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_lv00 AS NUMERIC(20,10)) END AS office_inv_summary_lv00, 
                    CASE WHEN (IS1.office_inv_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_lv01_49 AS NUMERIC(20,10)) END AS office_inv_summary_lv01_49, 
                    CASE WHEN (IS1.office_inv_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_lv50_99 AS NUMERIC(20,10)) END AS office_inv_summary_lv50_99, 
                    CASE WHEN (IS1.office_inv_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_lv100 AS NUMERIC(20,10)) END AS office_inv_summary_lv100, 
                    -- CASE WHEN (IS1.office_inv_summary_half) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_half AS NUMERIC(20,10)) END AS office_inv_summary_half, 
                    CASE WHEN (IS1.office_inv_summary_full) IS NULL THEN 0 ELSE CAST(IS1.office_inv_summary_full AS NUMERIC(20,10)) END AS office_inv_summary_full, 
                    
                    -- 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv00 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv01_49 / (OA1.office_inv_asset * OR1.office_inv_rate_lv00_50) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv50_99 / (OA1.office_inv_asset * OR1.office_inv_rate_lv50_100) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_lv100 / (OA1.office_inv_asset * OR1.office_inv_rate_lv100_200) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_inv_summary, 
                    -- CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_half / (OA1.office_inv_asset * OR1.office_inv_rate_lv200_300) AS NUMERIC(20,10)) END AS employee_half_reverse_office_inv_summary, 
                    CASE WHEN ABS(OA1.office_inv_asset * OR1.office_inv_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_inv_summary_full / (OA1.office_inv_asset * OR1.office_inv_rate_lv300) AS NUMERIC(20,10)) END AS employee_full_reverse_office_inv_summary, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB) 
                    CASE WHEN (IS1.office_sus_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_lv00 AS NUMERIC(20,10)) END AS office_sus_summary_lv00, 
                    CASE WHEN (IS1.office_sus_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_lv01_49 AS NUMERIC(20,10)) END AS office_sus_summary_lv01_49, 
                    CASE WHEN (IS1.office_sus_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_lv50_99 AS NUMERIC(20,10)) END AS office_sus_summary_lv50_99, 
                    CASE WHEN (IS1.office_sus_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_lv100 AS NUMERIC(20,10)) END AS office_sus_summary_lv100, 
                    -- CASE WHEN (IS1.office_sus_summary_half) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_half AS NUMERIC(20,10)) END AS office_sus_summary_half, 
                    CASE WHEN (IS1.office_sus_summary_full) IS NULL THEN 0 ELSE CAST(IS1.office_sus_summary_full AS NUMERIC(20,10)) END AS office_sus_summary_full, 
    
                    -- 事業所被害額_営業停止に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv00 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv00 / (OSUS1.office_sus_days_lv00 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv01_49 / (OSUS1.office_sus_days_lv00_50 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv50_99 / (OSUS1.office_sus_days_lv50_100 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_lv100 / (OSUS1.office_sus_days_lv100_200 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_sus_summary, 
                    -- CASE WHEN ABS(OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_half / (OSUS1.office_sus_days_lv200_300 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_half_reverse_office_sus_summary, 
                    CASE WHEN ABS(OSUS1.office_sus_days_lv300 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_sus_summary_full / (OSUS1.office_sus_days_lv300 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_full_reverse_office_sus_summary, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB) 
                    CASE WHEN (IS1.office_stg_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_lv00 AS NUMERIC(20,10)) END AS office_stg_summary_lv00, 
                    CASE WHEN (IS1.office_stg_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_lv01_49 AS NUMERIC(20,10)) END AS office_stg_summary_lv01_49, 
                    CASE WHEN (IS1.office_stg_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_lv50_99 AS NUMERIC(20,10)) END AS office_stg_summary_lv50_99, 
                    CASE WHEN (IS1.office_stg_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_lv100 AS NUMERIC(20,10)) END AS office_stg_summary_lv100, 
                    -- CASE WHEN (IS1.office_stg_summary_half) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_half AS NUMERIC(20,10)) END AS office_stg_summary_half, 
                    CASE WHEN (IS1.office_stg_summary_full) IS NULL THEN 0 ELSE CAST(IS1.office_stg_summary_full AS NUMERIC(20,10)) END AS office_stg_summary_full, 
    
                    -- 事業所被害額_営業停滞に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv00 / (OSTG1.office_stg_days_lv00 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv00_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv01_49 / (OSTG1.office_stg_days_lv00_50 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv01_49_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv50_99 / (OSTG1.office_stg_days_lv50_100 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv50_99_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_lv100 / (OSTG1.office_stg_days_lv100_200 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_lv100_reverse_office_stg_summary, 
                    -- CASE WHEN ABS(OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_half / (OSTG1.office_stg_days_lv200_300 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_half_reverse_office_stg_summary, 
                    CASE WHEN ABS(OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_stg_summary_full / (OSTG1.office_stg_days_lv300 * 0.5 * OA1.office_va_asset) AS NUMERIC(20,10)) END AS employee_full_reverse_office_stg_summary, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB) 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv00, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv01_49, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv50_99, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_lv100, 
                    -- CASE WHEN (IS1.farmer_fisher_dep_summary_half) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_half AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_half, 
                    CASE WHEN (IS1.farmer_fisher_dep_summary_full) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_dep_summary_full AS NUMERIC(20,10)) END AS farmer_fisher_dep_summary_full, 
    
                    -- 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv00 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00) AS NUMERIC(20,10)) END AS farmer_fisher_lv00_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv01_49 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50) AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv50_99 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100) AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_lv100 / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200) AS NUMERIC(20,10)) END AS farmer_fisher_lv100_reverse_farmer_fisher_dep_summary, 
                    -- CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_half / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300) AS NUMERIC(20,10)) END AS farmer_fisher_half_reverse_farmer_fisher_dep_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_dep_summary_full / (FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300) AS NUMERIC(20,10)) END AS farmer_fisher_full_reverse_farmer_fisher_dep_summary, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB) 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv00 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv00, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv01_49 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv01_49, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv50_99 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv50_99, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_lv100 AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_lv100, 
                    -- CASE WHEN (IS1.farmer_fisher_inv_summary_half) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_half AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_half, 
                    CASE WHEN (IS1.farmer_fisher_inv_summary_full) IS NULL THEN 0 ELSE CAST(IS1.farmer_fisher_inv_summary_full AS NUMERIC(20,10)) END AS farmer_fisher_inv_summary_full, 
    
                    -- 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv00 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00) AS NUMERIC(20,10)) END AS farmer_fisher_lv00_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv01_49 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50) AS NUMERIC(20,10)) END AS farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv50_99 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100) AS NUMERIC(20,10)) END AS farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_lv100 / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200) AS NUMERIC(20,10)) END AS farmer_fisher_lv100_reverse_farmer_fisher_inv_summary, 
                    -- CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_half / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300) AS NUMERIC(20,10)) END AS farmer_fisher_half_reverse_farmer_fisher_inv_summary, 
                    CASE WHEN ABS(FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.farmer_fisher_inv_summary_full / (FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300) AS NUMERIC(20,10)) END AS farmer_fisher_full_reverse_farmer_fisher_inv_summary, 
    
                    -- 事業所応急対策費_代替活動費(集計DB) 
                    CASE WHEN (IS1.office_alt_summary_lv00) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_lv00 AS NUMERIC(20,10)) END AS office_alt_summary_lv00, 
                    CASE WHEN (IS1.office_alt_summary_lv01_49) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_lv01_49 AS NUMERIC(20,10)) END AS office_alt_summary_lv01_49, 
                    CASE WHEN (IS1.office_alt_summary_lv50_99) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_lv50_99 AS NUMERIC(20,10)) END AS office_alt_summary_lv50_99, 
                    CASE WHEN (IS1.office_alt_summary_lv100) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_lv100 AS NUMERIC(20,10)) END AS office_alt_summary_lv100, 
                    CASE WHEN (IS1.office_alt_summary_half) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_half AS NUMERIC(20,10)) END AS office_alt_summary_half, 
                    CASE WHEN (IS1.office_alt_summary_full) IS NULL THEN 0 ELSE CAST(IS1.office_alt_summary_full AS NUMERIC(20,10)) END AS office_alt_summary_full, 
    
                    -- 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 
                    CASE WHEN ABS(OALT1.office_alt_lv00) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv00 / OALT1.office_alt_lv00 AS NUMERIC(20,10)) END AS office_lv00_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv00_50) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv01_49 / OALT1.office_alt_lv00_50 AS NUMERIC(20,10)) END AS office_lv01_49_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv50_100) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv50_99 / OALT1.office_alt_lv50_100 AS NUMERIC(20,10)) END AS office_lv50_99_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv100_200) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_lv100 / OALT1.office_alt_lv100_200 AS NUMERIC(20,10)) END AS office_lv100_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv200_300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_half / OALT1.office_alt_lv200_300 AS NUMERIC(20,10)) END AS office_half_reverse_office_alt_summary, 
                    CASE WHEN ABS(OALT1.office_alt_lv300) <= 0.0000001 THEN NULL ELSE CAST(IS1.office_alt_summary_full / OALT1.office_alt_lv300 AS NUMERIC(20,10)) END AS office_full_reverse_office_alt_summary 
                    
                FROM IPPAN_VIEW IV1 
                LEFT JOIN IPPAN_SUMMARY IS1 ON IV1.ippan_id = IS1.ippan_id 
                LEFT JOIN HOUSE_ASSET HA1 ON IV1.ken_code = HA1.ken_code 
                LEFT JOIN HOUSE_RATE HR1 ON IV1.flood_sediment_code = HR1.flood_sediment_code AND IV1.gradient_code = HR1.gradient_code 
                LEFT JOIN HOUSEHOLD_RATE HHR1 ON IV1.flood_sediment_code = HHR1.flood_sediment_code 
                LEFT JOIN OFFICE_ASSET OA1 ON IV1.industry_code = OA1.industry_code 
                LEFT JOIN OFFICE_RATE OR1 ON IV1.flood_sediment_code = OR1.flood_sediment_code 
                LEFT JOIN FARMER_FISHER_RATE FFR1 ON IV1.flood_sediment_code = FFR1.flood_sediment_code, -- why left join ? see below comment
                HOUSEHOLD_ASSET HHA1, 
                CAR_ASSET CA1, 
                CAR_RATE CR1, 
                HOUSE_ALT HALT1, 
                HOUSE_CLEAN HCL1, 
                OFFICE_SUSPEND OSUS1, 
                OFFICE_STAGNATE OSTG1, 
                FARMER_FISHER_ASSET FFA1, 
                OFFICE_ALT OALT1 
                WHERE 
                    IV1.suigai_id=%s AND 
                    IV1.deleted_at IS NULL 
                ORDER BY CAST(IV1.ippan_id AS INTEGER)""", [trigger_list[0].suigai_id, ])
            
            ### 複数レコードあるテーブルは単純に結合しないこと。
            ### 複数レコードあるテーブルはLEFT JOINにすること。
            ### 理由は、検索結果の件数がメインのテーブルの件数ではなく、結合したテーブルの複数レコード分となるため。

            if ippan_reverse_list is None:
                print_log('[WARN] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が警告終了しました。', 'WARN')
                return 4
    
            ###################################################################
            ### 計算処理(0030)
            ### 成功、失敗の数、レコード数をカウントする。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4/8.', 'DEBUG')
            success_count = 0
            failure_count = 0
            ### epsilon = 0.0000001
                
            for ippan in ippan_reverse_list:
                ###############################################################
                ### 計算処理(0040)
                ### 家屋被害額(集計DB)から逆計算により延床面積を求めた結果 
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_1/8.', 'DEBUG')
                if ippan.floor_area_lv00_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv00_reverse_house_summary = {}'.format(ippan.floor_area_lv00_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv00 = {}'.format(ippan.floor_area_lv00), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_lv00_reverse_house_summary) - float(ippan.floor_area_lv00)) = {}'.format(abs(float(ippan.floor_area_lv00_reverse_house_summary) - float(ippan.floor_area_lv00))), 'DEBUG')
                    if abs(float(ippan.floor_area_lv00_reverse_house_summary) - float(ippan.floor_area_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_lv00_reverse_house_summary {0} {1}'.format(ippan.floor_area_lv00_reverse_house_summary, ippan.floor_area_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.floor_area_lv01_49_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv01_49_reverse_house_summary = {}'.format(ippan.floor_area_lv01_49_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv01_49 = {}'.format(ippan.floor_area_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_lv01_49_reverse_house_summary) - float(ippan.floor_area_lv01_49)) = {}'.format(abs(float(ippan.floor_area_lv01_49_reverse_house_summary) - float(ippan.floor_area_lv01_49))), 'DEBUG')
                    if abs(float(ippan.floor_area_lv01_49_reverse_house_summary) - float(ippan.floor_area_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_lv01_49_reverse_house_summary {0} {1}'.format(ippan.floor_area_lv01_49_reverse_house_summary, ippan.floor_area_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.floor_area_lv50_99_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv50_99_reverse_house_summary = {}'.format(ippan.floor_area_lv50_99_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv50_99 = {}'.format(ippan.floor_area_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_lv50_99_reverse_house_summary) - float(ippan.floor_area_lv50_99)) = {}'.format(abs(float(ippan.floor_area_lv50_99_reverse_house_summary) - float(ippan.floor_area_lv50_99))), 'DEBUG')
                    if abs(float(ippan.floor_area_lv50_99_reverse_house_summary) - float(ippan.floor_area_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_lv50_99_reverse_house_summary {0} {1}'.format(ippan.floor_area_lv50_99_reverse_house_summary, ippan.floor_area_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.floor_area_lv100_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv100_reverse_house_summary = {}'.format(ippan.floor_area_lv100_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_lv100 = {}'.format(ippan.floor_area_lv100), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_lv100_reverse_house_summary) - float(ippan.floor_area_lv100)) = {}'.format(abs(float(ippan.floor_area_lv100_reverse_house_summary) - float(ippan.floor_area_lv100))), 'DEBUG')
                    if abs(float(ippan.floor_area_lv100_reverse_house_summary) - float(ippan.floor_area_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_lv100_reverse_house_summary {0} {1}'.format(ippan.floor_area_lv100_reverse_house_summary, ippan.floor_area_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.floor_area_half_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_half_reverse_house_summary = {}'.format(ippan.floor_area_half_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_half = {}'.format(ippan.floor_area_half), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_half_reverse_house_summary) - float(ippan.floor_area_half)) = {}'.format(abs(float(ippan.floor_area_half_reverse_house_summary) - float(ippan.floor_area_half))), 'DEBUG')
                    if abs(float(ippan.floor_area_half_reverse_house_summary) - float(ippan.floor_area_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_half_reverse_house_summary {0} {1}'.format(ippan.floor_area_half_reverse_house_summary, ippan.floor_area_half), 'WARN')
                        failure_count += 1
                        
                if ippan.floor_area_full_reverse_house_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_full_reverse_house_summary = {}'.format(ippan.floor_area_full_reverse_house_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 floor_area_full = {}'.format(ippan.floor_area_full), 'DEBUG')
                    print_log('abs(float(ippan.floor_area_full_reverse_house_summary) - float(ippan.floor_area_full)) = {}'.format(abs(float(ippan.floor_area_full_reverse_house_summary) - float(ippan.floor_area_full))), 'DEBUG')
                    if abs(float(ippan.floor_area_full_reverse_house_summary) - float(ippan.floor_area_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] floor_area_full_reverse_house_summary {0} {1}'.format(ippan.floor_area_full_reverse_house_summary, ippan.floor_area_full), 'WARN')
                        failure_count += 1

                ###############################################################
                ### 計算処理(0050)
                ### 家庭用品自動車以外被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_2/8.', 'DEBUG')
                if ippan.family_lv00_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00_reverse_household_summary = {}'.format(ippan.family_lv00_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00 = {}'.format(ippan.family_lv00), 'DEBUG')
                    print_log('abs(float(ippan.family_lv00_reverse_household_summary) - float(ippan.family_lv00)) = {}'.format(abs(float(ippan.family_lv00_reverse_household_summary) - float(ippan.family_lv00))), 'DEBUG')
                    if abs(float(ippan.family_lv00_reverse_household_summary) - float(ippan.family_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv00_reverse_household_summary {0} {1}'.format(ippan.family_lv00_reverse_household_summary, ippan.family_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv01_49_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49_reverse_household_summary = {}'.format(ippan.family_lv01_49_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49 = {}'.format(ippan.family_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.family_lv01_49_reverse_household_summary) - float(ippan.family_lv01_49)) = {}'.format(abs(float(ippan.family_lv01_49_reverse_household_summary) - float(ippan.family_lv01_49))), 'DEBUG')
                    if abs(float(ippan.family_lv01_49_reverse_household_summary) - float(ippan.family_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv01_49_reverse_household_summary {0} {1}'.format(ippan.family_lv01_49_reverse_household_summary, ippan.family_lv01_49), 'WARN')
                        failure_count = failure_count + 1
                        
                if ippan.family_lv50_99_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99_reverse_household_summary = {}'.format(ippan.family_lv50_99_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99 = {}'.format(ippan.family_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.family_lv50_99_reverse_household_summary) - float(ippan.family_lv50_99)) = {}'.format(abs(float(ippan.family_lv50_99_reverse_household_summary) - float(ippan.family_lv50_99))), 'DEBUG')
                    if abs(float(ippan.family_lv50_99_reverse_household_summary) - float(ippan.family_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv50_99_reverse_household_summary {0} {1}'.format(ippan.family_lv50_99_reverse_household_summary, ippan.family_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv100_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100_reverse_household_summary = {}'.format(ippan.family_lv100_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 famly_lv100 = {}'.format(ippan.family_lv100), 'DEBUG')
                    print_log('abs(float(ippan.family_lv100_reverse_household_summary) - float(ippan.family_lv100)) = {}'.format(abs(float(ippan.family_lv100_reverse_household_summary) - float(ippan.family_lv100))), 'DEBUG')
                    if abs(float(ippan.family_lv100_reverse_household_summary) - float(ippan.family_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv100_reverse_household_summary {0} {1}'.format(ippan.family_lv100_reverse_household_summary, ippan.family_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.family_half_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half_reverse_household_summary = {}'.format(ippan.family_half_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half = {}'.format(ippan.family_half), 'DEBUG')
                    print_log('abs(float(ippan.family_half_reverse_household_summary) - float(ippan.family_half)) = {}'.format(abs(float(ippan.family_half_reverse_household_summary) - float(ippan.family_half))), 'DEBUG')
                    if abs(float(ippan.family_half_reverse_household_summary) - float(ippan.family_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_half_reverse_household_summary {0} {1}'.format(ippan.family_half_reverse_household_summary, ippan.family_half), 'WARN')
                        failure_count += 1
                        
                if ippan.family_full_reverse_household_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full_reverse_household_summary = {}'.format(ippan.family_full_reverse_household_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full = {}'.format(ippan.family_full), 'DEBUG')
                    print_log('abs(float(ippan.family_full_reverse_household_summary) - float(ippan.family_full)) = {}'.format(abs(float(ippan.family_full_reverse_household_summary) - float(ippan.family_full))), 'DEBUG')
                    if abs(float(ippan.family_full_reverse_household_summary) - float(ippan.family_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_full_reverse_household_summary {0} {1}'.format(ippan.family_full_reverse_household_summary, ippan.family_full), 'WARN')
                        failure_count += 1

                ###############################################################
                ### 計算処理(0060)
                ### 家庭用品自動車被害額(集計DB)から逆計算により被災世帯数を求めた結果 
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_3/8.', 'DEBUG')
                if ippan.family_lv00_reverse_car_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00_reverse_car_summary = {}'.format(ippan.family_lv00_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00 = {}'.format(ippan.family_lv00), 'DEBUG')
                    print_log('abs(float(ippan.family_lv00_reverse_car_summary) - float(ippan.family_lv00)) = {}'.format(abs(float(ippan.family_lv00_reverse_car_summary) - float(ippan.family_lv00))), 'DEBUG')
                    if abs(float(ippan.family_lv00_reverse_car_summary) - float(ippan.family_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv00_reverse_car_summary {0} {1}'.format(ippan.family_lv00_reverse_car_summary, ippan.family_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv01_49_reverse_car_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49_reverse_car_summary = {}'.format(ippan.family_lv01_49_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49 = {}'.format(ippan.family_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.family_lv01_49_reverse_car_summary) - float(ippan.family_lv01_49)) = {}'.format(abs(float(ippan.family_lv01_49_reverse_car_summary) - float(ippan.family_lv01_49))), 'DEBUG')
                    if abs(float(ippan.family_lv01_49_reverse_car_summary) - float(ippan.family_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv01_49_reverse_car_summary {0} {1}'.format(ippan.family_lv01_49_reverse_car_summary, ippan.family_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv50_99_reverse_car_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99_reverse_car_summary = {}'.format(ippan.family_lv50_99_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99 = {}'.format(ippan.family_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.family_lv50_99_reverse_car_summary) - float(ippan.family_lv50_99)) = {}'.format(abs(float(ippan.family_lv50_99_reverse_car_summary) - float(ippan.family_lv50_99))), 'DEBUG')
                    if abs(float(ippan.family_lv50_99_reverse_car_summary) - float(ippan.family_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv50_99_reverse_car_summary {0} {1}'.format(ippan.family_lv50_99_reverse_car_summary, ippan.family_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv100_reverse_car_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100_reverse_car_summary = {}'.format(ippan.family_lv100_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100 = {}'.format(ippan.family_lv100), 'DEBUG')
                    print_log('abs(float(ippan.family_lv100_reverse_car_summary) - float(ippan.family_lv100)) = {}'.format(abs(float(ippan.family_lv100_reverse_car_summary) - float(ippan.family_lv100))), 'DEBUG')
                    if abs(float(ippan.family_lv100_reverse_car_summary) - float(ippan.family_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv100_reverse_car_summary {0} {1}'.format(ippan.family_lv100_reverse_car_summary, ippan.family_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.family_half_reverse_car_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half_reverse_car_summary = {}'.format(ippan.family_half_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half = {}'.format(ippan.family_half), 'DEBUG')
                    print_log('abs(float(ippan.family_half_reverse_car_summary) - float(ippan.family_half)) = {}'.format(abs(float(ippan.family_half_reverse_car_summary) - float(ippan.family_half))), 'DEBUG')
                    if abs(float(ippan.family_half_reverse_car_summary) - float(ippan.family_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_half_reverse_car_summary {0} {1}'.format(ippan.family_half_reverse_car_summary, ippan.family_half), 'WARN')
                        failure_count += 1
                        
                if ippan.family_full_reverse_car_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full_reverse_car_summary = {}'.format(ippan.family_full_reverse_car_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full = {}'.format(ippan.family_full), 'DEBUG')
                    print_log('abs(float(ippan.family_full_reverse_car_summary) - float(ippan.family_full)) = {}'.format(abs(float(ippan.family_full_reverse_car_summary) - float(ippan.family_full))), 'DEBUG')
                    if abs(float(ippan.family_full_reverse_car_summary) - float(ippan.family_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_full_reverse_car_summary {0} {1}'.format(ippan.family_full_reverse_car_summary, ippan.family_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0070)
                ### 家庭応急対策費_代替活動費(集計DB)から逆計算により被災世帯数を求めた結果 
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_4/8.', 'DEBUG')
                if ippan.family_lv00_reverse_house_alt_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00_reverse_house_alt_summary = {}'.format(ippan.family_lv00_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00 = {}'.format(ippan.family_lv00), 'DEBUG')
                    print_log('abs(float(ippan.family_lv00_reverse_house_alt_summary) - float(ippan.family_lv00)) = {}'.format(abs(float(ippan.family_lv00_reverse_house_alt_summary) - float(ippan.family_lv00))), 'DEBUG')
                    if abs(float(ippan.family_lv00_reverse_house_alt_summary) - float(ippan.family_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv00_reverse_house_alt_summary {0} {1}'.format(ippan.family_lv00_reverse_house_alt_summary, ippan.family_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv01_49_reverse_house_alt_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49_reverse_house_alt_summary = {}'.format(ippan.family_lv01_49_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49 = {}'.format(ippan.family_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.family_lv01_49_reverse_house_alt_summary) - float(ippan.family_lv01_49)) = {}'.format(abs(float(ippan.family_lv01_49_reverse_house_alt_summary) - float(ippan.family_lv01_49))), 'DEBUG')
                    if abs(float(ippan.family_lv01_49_reverse_house_alt_summary) - float(ippan.family_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv01_49 {0} {1}'.format(ippan.family_lv01_49_reverse_house_alt_summary, ippan.family_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv50_99_reverse_house_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99_reverse_house_alt_summary = {}'.format(ippan.family_lv50_99_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99 = {}'.format(ippan.family_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.family_lv50_99_reverse_house_alt_summary) - float(ippan.family_lv50_99)) = {}'.format(abs(float(ippan.family_lv50_99_reverse_house_alt_summary) - float(ippan.family_lv50_99))), 'DEBUG')
                    if abs(float(ippan.family_lv50_99_reverse_house_alt_summary) - float(ippan.family_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv50_99_reverse_house_alt_summary {0} {1}'.format(ippan.family_lv50_99_reverse_house_alt_summary, ippan.family_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv100_reverse_house_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100_reverse_house_alt_summary = {}'.format(ippan.family_lv100_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100 = {}'.format(ippan.family_lv100), 'DEBUG')
                    print_log('abs(float(ippan.family_lv100_reverse_house_alt_summary) - float(ippan.family_lv100)) = {}'.format(abs(float(ippan.family_lv100_reverse_house_alt_summary) - float(ippan.family_lv100))), 'DEBUG')
                    if abs(float(ippan.family_lv100_reverse_house_alt_summary) - float(ippan.family_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv100_reverse_house_alt_summary {0} {1}'.format(ippan.family_lv100_reverse_house_alt_summary, ippan.family_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.family_half_reverse_house_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half_reverse_house_alt_summary = {}'.format(ippan.family_half_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half = {}'.format(ippan.family_half), 'DEBUG')
                    print_log('abs(float(ippan.family_half_reverse_house_alt_summary) - float(ippan.family_half)) = {}'.format(abs(float(ippan.family_half_reverse_house_alt_summary) - float(ippan.family_half))), 'DEBUG')
                    if abs(float(ippan.family_half_reverse_house_alt_summary) - float(ippan.family_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_half_reverse_house_alt_summary {0} {1}'.format(ippan.family_half_reverse_house_alt_summary, ippan.family_half), 'WARN')
                        failure_count += 1
                        
                if ippan.family_full_reverse_house_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full_reverse_house_alt_summary = {}'.format(ippan.family_full_reverse_house_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full = {}'.format(ippan.family_full), 'DEBUG')
                    print_log('abs(float(ippan.family_full_reverse_house_alt_summary) - float(ippan.family_full)) = {}'.format(abs(float(ippan.family_full_reverse_house_alt_summary) - float(ippan.family_full))), 'DEBUG')
                    if abs(float(ippan.family_full_reverse_house_alt_summary) - float(ippan.family_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_full_reverse_house_alt_summary {0} {1}'.format(ippan.family_full_reverse_house_alt_summary, ippan.family_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0080)
                ### 家庭応急対策費_清掃費(集計DB)から逆計算により被災世帯数を求めた結果 
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_5/8.', 'DEBUG')
                if ippan.family_lv00_reverse_house_clean_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00_reverse_house_clean_summary = {}'.format(ippan.family_lv00_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv00 = {}'.format(ippan.family_lv00), 'DEBUG')
                    print_log('abs(float(ippan.family_lv00_reverse_house_clean_summary) - float(ippan.family_lv00)) = {}'.format(abs(float(ippan.family_lv00_reverse_house_clean_summary) - float(ippan.family_lv00))), 'DEBUG')
                    if abs(float(ippan.family_lv00_reverse_house_clean_summary) - float(ippan.family_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv00_reverse_house_clean_summary {0} {1}'.format(ippan.family_lv00_reverse_house_clean_summary, ippan.family_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv01_49_reverse_house_clean_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49_reverse_house_clean_summary = {}'.format(ippan.family_lv01_49_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv01_49 = {}'.format(ippan.family_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.family_lv01_49_reverse_house_clean_summary) - float(ippan.family_lv01_49)) = {}'.format(abs(float(ippan.family_lv01_49_reverse_house_clean_summary) - float(ippan.family_lv01_49))), 'DEBUG')
                    if abs(float(ippan.family_lv01_49_reverse_house_clean_summary) - float(ippan.family_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv01_49_reverse_house_clean_summary {0} {1}'.format(ippan.family_lv01_49_reverse_house_clean_summary, ippan.family_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv50_99_reverse_house_clean_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99_reverse_house_clean_summary = {}'.format(ippan.family_lv50_99_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv50_99 = {}'.format(ippan.family_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.family_lv50_99_reverse_house_clean_summary) - float(ippan.family_lv50_99)) = {}'.format(abs(float(ippan.family_lv50_99_reverse_house_clean_summary) - float(ippan.family_lv50_99))), 'DEBUG')
                    if abs(float(ippan.family_lv50_99_reverse_house_clean_summary) - float(ippan.family_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv50_99_reverse_house_clean_summary {0} {1}'.format(ippan.family_lv50_99_reverse_house_clean_summary, ippan.family_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.family_lv100_reverse_house_clean_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100_reverse_house_clean_summary = {}'.format(ippan.family_lv100_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_lv100 = {}'.format(ippan.family_lv100), 'DEBUG')
                    print_log('abs(float(ippan.family_lv100_reverse_house_clean_summary) - float(ippan.family_lv100)) = {}'.format(abs(float(ippan.family_lv100_reverse_house_clean_summary) - float(ippan.family_lv100))), 'DEBUG')
                    if abs(float(ippan.family_lv100_reverse_house_clean_summary) - float(ippan.family_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_lv100_reverse_house_clean_summary {0} {1}'.format(ippan.family_lv100_reverse_house_clean_summary, ippan.family_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.family_half_reverse_house_clean_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half_reverse_house_clean_summary = {}'.format(ippan.family_half_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_half = {}'.format(ippan.family_half), 'DEBUG')
                    print_log('abs(float(ippan.family_half_reverse_house_clean_summary) - float(ippan.family_half)) = {}'.format(abs(float(ippan.family_half_reverse_house_clean_summary) - float(ippan.family_half))), 'DEBUG')
                    if abs(float(ippan.family_half_reverse_house_clean_summary) - float(ippan.family_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_half_reverse_house_clean_summary {0} {1}'.format(ippan.family_half_reverse_house_clean_summary, ippan.family_half), 'WARN')
                        failure_count += 1
                        
                if ippan.family_full_reverse_house_clean_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full_reverse_house_clean_summary = {}'.format(ippan.family_full_reverse_house_clean_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 family_full = {}'.format(ippan.family_full), 'DEBUG')
                    print_log('abs(float(ippan.family_full_reverse_house_clean_summary) - float(ippan.family_full)) = {}'.format(abs(float(ippan.family_full_reverse_house_clean_summary) - float(ippan.family_full))), 'DEBUG')
                    if abs(float(ippan.family_full_reverse_house_clean_summary) - float(ippan.family_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] family_full_reverse_house_clean_summary {0} {1}'.format(ippan.family_full_reverse_house_clean_summary, ippan.family_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0090)
                ### 事業所被害額_償却資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_6/8.', 'DEBUG')
                if ippan.employee_lv00_reverse_office_dep_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00_reverse_office_dep_summary = {}'.format(ippan.employee_lv00_reverse_office_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00 = {}'.format(ippan.employee_lv00), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv00_reverse_office_dep_summary) - float(ippan.employee_lv00)) = {}'.format(abs(float(ippan.employee_lv00_reverse_office_dep_summary) - float(ippan.employee_lv00))), 'DEBUG')
                    if abs(float(ippan.employee_lv00_reverse_office_dep_summary) - float(ippan.employee_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv00_reverse_office_dep_summary {0} {1}'.format(ippan.employee_lv00_reverse_office_dep_summary, ippan.employee_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv01_49_reverse_office_dep_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49_reverse_office_dep_summary = {}'.format(ippan.employee_lv01_49_reverse_office_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv01_49_reverse_office_dep_summary) - float(ippan.employee_lv01_49)) = {}'.format(abs(float(ippan.employee_lv01_49_reverse_office_dep_summary) - float(ippan.employee_lv01_49))), 'DEBUG')
                    if abs(float(ippan.employee_lv01_49_reverse_office_dep_summary) - float(ippan.employee_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv01_49_reverse_office_dep_summary {0} {1}'.format(ippan.employee_lv01_49_reverse_office_dep_summary, ippan.employee_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv50_99_reverse_office_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99_reverse_office_dep_summary = {}'.format(ippan.employee_lv50_99_reverse_office_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv50_99_reverse_office_dep_summary) - float(ippan.employee_lv50_99)) = {}'.format(abs(float(ippan.employee_lv50_99_reverse_office_dep_summary) - float(ippan.employee_lv50_99))), 'DEBUG')
                    if abs(float(ippan.employee_lv50_99_reverse_office_dep_summary) - float(ippan.employee_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv50_99_reverse_office_dep_summary {0} {1}'.format(ippan.employee_lv50_99_reverse_office_dep_summary, ippan.employee_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv100_reverse_office_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100_reverse_office_dep_summary = {}'.format(ippan.employee_lv100_reverse_office_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100 = {}'.format(ippan.employee_lv100), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv100_reverse_office_dep_summary) - float(ippan.employee_lv100)) = {}'.format(abs(float(ippan.employee_lv100_reverse_office_dep_summary) - float(ippan.employee_lv100))), 'DEBUG')
                    if abs(float(ippan.employee_lv100_reverse_office_dep_summary) - float(ippan.employee_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv100_reverse_office_dep_summary {0} {1}'.format(ippan.employee_lv100_reverse_office_dep_summary, ippan.employee_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.employee_half_reverse_office_dep_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half_reverse_office_dep_summary = {}'.format(ippan.employee_half_reverse_office_dep_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half = {}'.format(ippan.employee_half), 'DEBUG')
                ###     print_log('abs(float(ippan.employee_half_reverse_office_dep_summary) - float(ippan.employee_half)) = {}'.format(abs(float(ippan.employee_half_reverse_office_dep_summary) - float(ippan.employee_half))), 'DEBUG')
                ###     if abs(float(ippan.employee_half_reverse_office_dep_summary) - float(ippan.employee_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.employee_full_reverse_office_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full_reverse_office_dep_summary = {}'.format(ippan.employee_full_reverse_office_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full = {}'.format(ippan.employee_full), 'DEBUG')
                    print_log('abs(float(ippan.employee_full_reverse_office_dep_summary) - float(ippan.employee_full)) = {}'.format(abs(float(ippan.employee_full_reverse_office_dep_summary) - float(ippan.employee_full))), 'DEBUG')
                    if abs(float(ippan.employee_full_reverse_office_dep_summary) - float(ippan.employee_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_full_reverse_office_dep_summary {0} {1}'.format(ippan.employee_full_reverse_office_dep_summary, ippan.employee_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0100)
                ### 事業所被害額_在庫資産被害額(集計DB)から逆計算により被災従業者数を求めた結果 
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_7/8.', 'DEBUG')
                if ippan.employee_lv00_reverse_office_inv_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00_reverse_office_inv_summary = {}'.format(ippan.employee_lv00_reverse_office_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00 = {}'.format(ippan.employee_lv00), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv00_reverse_office_inv_summary) - float(ippan.employee_lv00)) = {}'.format(abs(float(ippan.employee_lv00_reverse_office_inv_summary) - float(ippan.employee_lv00))), 'DEBUG')
                    if abs(float(ippan.employee_lv00_reverse_office_inv_summary) - float(ippan.employee_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv00_reverse_office_inv_summary {0} {1}'.format(ippan.employee_lv00_reverse_office_inv_summary, ippan.employee_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv01_49_reverse_office_inv_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49_reverse_office_inv_summary = {}'.format(ippan.employee_lv01_49_reverse_office_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv01_49_reverse_office_inv_summary) - float(ippan.employee_lv01_49)) = {}'.format(abs(float(ippan.employee_lv01_49_reverse_office_inv_summary) - float(ippan.employee_lv01_49))), 'DEBUG')
                    if abs(float(ippan.employee_lv01_49_reverse_office_inv_summary) - float(ippan.employee_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv01_49_reverse_office_inv_summary {0} [1]'.format(ippan.employee_lv01_49_reverse_office_inv_summary, ippan.employee_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv50_99_reverse_office_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99_reverse_office_inv_summary = {}'.format(ippan.employee_lv50_99_reverse_office_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv50_99_reverse_office_inv_summary) - float(ippan.employee_lv50_99)) = {}'.format(abs(float(ippan.employee_lv50_99_reverse_office_inv_summary) - float(ippan.employee_lv50_99))), 'DEBUG')
                    if abs(float(ippan.employee_lv50_99_reverse_office_inv_summary) - float(ippan.employee_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv50_99_reverse_office_inv_summary {0} {1}'.format(ippan.employee_lv50_99_reverse_office_inv_summary, ippan.employee_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv100_reverse_office_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100_reverse_office_inv_summary = {}'.format(ippan.employee_lv100_reverse_office_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100 = {}'.format(ippan.employee_lv100), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv100_reverse_office_inv_summary) - float(ippan.employee_lv100)) = {}'.format(abs(float(ippan.employee_lv100_reverse_office_inv_summary) - float(ippan.employee_lv100))), 'DEBUG')
                    if abs(float(ippan.employee_lv100_reverse_office_inv_summary) - float(ippan.employee_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv100_reverse_office_inv_summary {0} {1}'.format(ippan.employee_lv100_reverse_office_inv_summary, ippan.employee_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.employee_half_reverse_office_inv_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half_reverse_office_inv_summary = {}'.format(ippan.employee_half_reverse_office_inv_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half = {}'.format(ippan.employee_half), 'DEBUG')
                ###     print_log('abs(float(ippan.employee_half_reverse_office_inv_summary) - float(ippan.employee_half)) = {}'.format(abs(float(ippan.employee_half_reverse_office_inv_summary) - float(ippan.employee_half))), 'DEBUG')
                ###     if abs(float(ippan.employee_half_reverse_office_inv_summary) - float(ippan.employee_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.employee_full_reverse_office_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full_reverse_office_inv_summary = {}'.format(ippan.employee_full_reverse_office_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full = {}'.format(ippan.employee_full), 'DEBUG')
                    print_log('abs(float(ippan.employee_full_reverse_office_inv_summary) - float(ippan.employee_full)) = {}'.format(abs(float(ippan.employee_full_reverse_office_inv_summary) - float(ippan.employee_full))), 'DEBUG')
                    if abs(float(ippan.employee_full_reverse_office_inv_summary) - float(ippan.employee_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_full_reverse_office_inv_summary {0} {1}'.format(ippan.employee_full_reverse_office_inv_summary, ippan.employee_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0110)
                ### 事業所被害額_営業停止に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_8/8.', 'DEBUG')
                if ippan.employee_lv00_reverse_office_sus_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00_reverse_office_sus_summary = {}'.format(ippan.employee_lv00_reverse_office_sus_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00 = {}'.format(ippan.employee_lv00), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv00_reverse_office_sus_summary) - float(ippan.employee_lv00)) = {}'.format(abs(float(ippan.employee_lv00_reverse_office_sus_summary) - float(ippan.employee_lv00))), 'DEBUG')
                    if abs(float(ippan.employee_lv00_reverse_office_sus_summary) - float(ippan.employee_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv00_reverse_office_sus_summary {0} {1}'.format(ippan.employee_lv00_reverse_office_sus_summary, ippan.employee_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv01_49_reverse_office_sus_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49_reverse_office_sus_summary = {}'.format(ippan.employee_lv01_49_reverse_office_sus_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv01_49_reverse_office_sus_summary) - float(ippan.employee_lv01_49)) = {}'.format(abs(float(ippan.employee_lv01_49_reverse_office_sus_summary) - float(ippan.employee_lv01_49))), 'DEBUG')
                    if abs(float(ippan.employee_lv01_49_reverse_office_sus_summary) - float(ippan.employee_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv01_49_reverse_office_sus_summary {0} {1}'.format(ippan.employee_lv01_49_reverse_office_sus_summary, ippan.employee_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv50_99_reverse_office_sus_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99_reverse_office_sus_summary = {}'.format(ippan.employee_lv50_99_reverse_office_sus_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv50_99_reverse_office_sus_summary) - float(ippan.employee_lv50_99)) = {}'.format(abs(float(ippan.employee_lv50_99_reverse_office_sus_summary) - float(ippan.employee_lv50_99))), 'DEBUG')
                    if abs(float(ippan.employee_lv50_99_reverse_office_sus_summary) - float(ippan.employee_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv50_99_reverse_office_sus_summary {0} {1}'.format(ippan.employee_lv50_99_reverse_office_sus_summary, ippan.employee_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv100_reverse_office_sus_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100_reverse_office_sus_summary = {}'.format(ippan.employee_lv100_reverse_office_sus_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100 = {}'.format(ippan.employee_lv100), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv100_reverse_office_sus_summary) - float(ippan.employee_lv100)) = {}'.format(abs(float(ippan.employee_lv100_reverse_office_sus_summary) - float(ippan.employee_lv100))), 'DEBUG')
                    if abs(float(ippan.employee_lv100_reverse_office_sus_summary) - float(ippan.employee_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv100_reverse_office_sus_summary {0} {1}'.format(ippan.employee_lv100_reverse_office_sus_summary, ippan.employee_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.employee_half_reverse_office_sus_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half_reverse_office_sus_summary = {}'.format(ippan.employee_half_reverse_office_sus_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half = {}'.format(ippan.employee_half), 'DEBUG')
                ###     print_log('abs(float(ippan.employee_half_reverse_office_sus_summary) - float(ippan.employee_half)) = {}'.format(abs(float(ippan.employee_half_reverse_office_sus_summary) - float(ippan.employee_half))), 'DEBUG')
                ###     if abs(float(ippan.employee_half_reverse_office_sus_summary) - float(ippan.employee_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.employee_full_reverse_office_sus_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full_reverse_office_sus_summary = {}'.format(ippan.employee_full_reverse_office_sus_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full = {}'.format(ippan.employee_full), 'DEBUG')
                    print_log('abs(float(ippan.employee_full_reverse_office_sus_summary) - float(ippan.employee_full)) = {}'.format(abs(float(ippan.employee_full_reverse_office_sus_summary) - float(ippan.employee_full))), 'DEBUG')
                    if abs(float(ippan.employee_full_reverse_office_sus_summary) - float(ippan.employee_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_full_reverse_office_sus_summary {0} {1}'.format(ippan.employee_full_reverse_office_sus_summary, ippan.employee_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0120)
                ### 事業所被害額_営業停滞に伴う被害額(集計DB)から逆計算により被災従業者数を求めた結果
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_9/8.', 'DEBUG')
                if ippan.employee_lv00_reverse_office_stg_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00_reverse_office_stg_summary = {}'.format(ippan.employee_lv00_reverse_office_stg_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv00 = {}'.format(ippan.employee_lv00), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv00_reverse_office_stg_summary) - float(ippan.employee_lv00)) = {}'.format(abs(float(ippan.employee_lv00_reverse_office_stg_summary) - float(ippan.employee_lv00))), 'DEBUG')
                    if abs(float(ippan.employee_lv00_reverse_office_stg_summary) - float(ippan.employee_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv00_reverse_office_stg_summary {0} {1}'.format(ippan.employee_lv00_reverse_office_stg_summary, ippan.employee_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv01_49_reverse_office_stg_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49_reverse_office_stg_summary = {}'.format(ippan.employee_lv01_49_reverse_office_stg_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv01_49 = {}'.format(ippan.employee_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv01_49_reverse_office_stg_summary) - float(ippan.employee_lv01_49)) = {}'.format(abs(float(ippan.employee_lv01_49_reverse_office_stg_summary) - float(ippan.employee_lv01_49))), 'DEBUG')
                    if abs(float(ippan.employee_lv01_49_reverse_office_stg_summary) - float(ippan.employee_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv01_49_reverse_office_stg_summary {0} {1}'.format(ippan.employee_lv01_49_reverse_office_stg_summary, ippan.employee_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv50_99_reverse_office_stg_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99_reverse_office_stg_summary = {}'.format(ippan.employee_lv50_99_reverse_office_stg_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv50_99 = {}'.format(ippan.employee_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv50_99_reverse_office_stg_summary) - float(ippan.employee_lv50_99)) = {}'.format(abs(float(ippan.employee_lv50_99_reverse_office_stg_summary) - float(ippan.employee_lv50_99))), 'DEBUG')
                    if abs(float(ippan.employee_lv50_99_reverse_office_stg_summary) - float(ippan.employee_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv50_99_reverse_office_stg_summary {0} {1}'.format(ippan.employee_lv50_99_reverse_office_stg_summary, ippan.employee_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.employee_lv100_reverse_office_stg_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100_reverse_office_stg_summary = {}'.format(ippan.employee_lv100_reverse_office_stg_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_lv100 = {}'.format(ippan.employee_lv100), 'DEBUG')
                    print_log('abs(float(ippan.employee_lv100_reverse_office_stg_summary) - float(ippan.employee_lv100)) = {}'.format(abs(float(ippan.employee_lv100_reverse_office_stg_summary) - float(ippan.employee_lv100))), 'DEBUG')
                    if abs(float(ippan.employee_lv100_reverse_office_stg_summary) - float(ippan.employee_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_lv100_reverse_office_stg_summary {0} {1}'.format(ippan.employee_lv100_reverse_office_stg_summary, ippan.employee_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.employee_half_reverse_office_stg_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half_reverse_office_stg_summary = {}'.format(ippan.employee_half_reverse_office_stg_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_half = {}'.format(ippan.employee_half), 'DEBUG')
                ###     print_log('abs(float(ippan.employee_half_reverse_office_stg_summary) - float(ippan.employee_half)) = {}'.format(abs(float(ippan.employee_half_reverse_office_stg_summary) - float(ippan.employee_half))), 'DEBUG')
                ###     if abs(float(ippan.employee_half_reverse_office_stg_summary) - float(ippan.employee_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.employee_full_reverse_office_stg_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full_reverse_office_stg_summary = {}'.format(ippan.employee_full_reverse_office_stg_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 employee_full = {}'.format(ippan.employee_full), 'DEBUG')
                    print_log('abs(float(ippan.employee_full_reverse_office_stg_summary) - float(ippan.employee_full)) = {}'.format(abs(float(ippan.employee_full_reverse_office_stg_summary) - float(ippan.employee_full))), 'DEBUG')
                    if abs(float(ippan.employee_full_reverse_office_stg_summary) - float(ippan.employee_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] employee_full_reverse_office_stg_summary {0} {1}'.format(ippan.employee_full_reverse_office_stg_summary, ippan.employee_full), 'WARN')
                        failure_count += 1

                ###############################################################
                ### 計算処理(0130)
                ### 農漁家被害額_償却資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果 
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_10/8.', 'DEBUG')
                if ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv00_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv00 = {}'.format(ippan.farmer_fisher_lv00), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv00)) = {}'.format(abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv00))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv00_reverse_farmer_fisher_dep_summary {0} {1}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_dep_summary, ippan.farmer_fisher_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv01_49 = {}'.format(ippan.farmer_fisher_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv01_49)) = {}'.format(abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv01_49))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary {0} {1}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_dep_summary, ippan.farmer_fisher_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv50_99 = {}'.format(ippan.farmer_fisher_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv50_99)) = {}'.format(abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv50_99))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary {0} {1}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_dep_summary, ippan.farmer_fisher_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv100_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv100 = {}'.format(ippan.farmer_fisher_lv100), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv100)) = {}'.format(abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv100))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv100_reverse_farmer_fisher_dep_summary {0} {1}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_dep_summary, ippan.farmer_fisher_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_half_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_half = {}'.format(ippan.farmer_fisher_half), 'DEBUG')
                ###     print_log('abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_half)) = {}'.format(abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_half))), 'DEBUG')
                ###     if abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_full_reverse_farmer_fisher_dep_summary = {}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_full = {}'.format(ippan.farmer_fisher_full), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_full)) = {}'.format(abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_full))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary) - float(ippan.farmer_fisher_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_full_reverse_farmer_fisher_dep_summary {0} {1}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_dep_summary, ippan.farmer_fisher_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0140)
                ### 農漁家被害額_在庫資産被害額(集計DB)から逆計算により農漁家戸数を求めた結果
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_11/8.', 'DEBUG')
                if ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv00_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv00 = {}'.format(ippan.farmer_fisher_lv00), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv00)) = {}'.format(abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv00))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv00_reverse_farmer_fisher_inv_summary {0} {1}'.format(ippan.farmer_fisher_lv00_reverse_farmer_fisher_inv_summary, ippan.farmer_fisher_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv01_49 = {}'.format(ippan.farmer_fisher_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv01_49)) = {}'.format(abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv01_49))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary {0} {1}'.format(ippan.farmer_fisher_lv01_49_reverse_farmer_fisher_inv_summary, ippan.farmer_fisher_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv50_99 = {}'.format(ippan.farmer_fisher_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv50_99)) = {}'.format(abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv50_99))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary {0} {1}'.format(ippan.farmer_fisher_lv50_99_reverse_farmer_fisher_inv_summary, ippan.farmer_fisher_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv100_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_lv100 = {}'.format(ippan.farmer_fisher_lv100), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv100)) = {}'.format(abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv100))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_lv100_reverse_farmer_fisher_inv_summary {0} {1}'.format(ippan.farmer_fisher_lv100_reverse_farmer_fisher_inv_summary, ippan.farmer_fisher_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_half_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_half = {}'.format(ippan.farmer_fisher_half), 'DEBUG')
                ###     print_log('abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_half)) = {}'.format(abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_half))), 'DEBUG')
                ###     if abs(float(ippan.farmer_fisher_half_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_full_reverse_farmer_fisher_inv_summary = {}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 farmer_fisher_full = {}'.format(ippan.farmer_fisher_full), 'DEBUG')
                    print_log('abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_full)) = {}'.format(abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_full))), 'DEBUG')
                    if abs(float(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary) - float(ippan.farmer_fisher_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] farmer_fisher_full_reverse_farmer_fisher_inv_summary {0} {1}'.format(ippan.farmer_fisher_full_reverse_farmer_fisher_inv_summary, ippan.farmer_fisher_full), 'WARN')
                        failure_count += 1

                ############################################################### 
                ### 計算処理(0150)
                ### 事業所応急対策費_代替活動費(集計DB)から逆計算により被災事業所数を求めた結果 
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 4_12/8.', 'DEBUG')
                if ippan.office_lv00_reverse_office_alt_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv00_reverse_office_alt_summary = {}'.format(ippan.office_lv00_reverse_office_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv00 = {}'.format(ippan.office_lv00), 'DEBUG')
                    print_log('abs(float(ippan.office_lv00_reverse_office_alt_summary) - float(ippan.office_lv00)) = {}'.format(abs(float(ippan.office_lv00_reverse_office_alt_summary) - float(ippan.office_lv00))), 'DEBUG')
                    if abs(float(ippan.office_lv00_reverse_office_alt_summary) - float(ippan.office_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] office_lv00_reverse_office_alt_summary {0} {1}'.format(ippan.office_lv00_reverse_office_alt_summary, ippan.office_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.office_lv01_49_reverse_office_alt_summary is not None: 
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv01_49_reverse_office_alt_summary = {}'.format(ippan.office_lv01_49_reverse_office_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv01_49 = {}'.format(ippan.office_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.office_lv01_49_reverse_office_alt_summary) - float(ippan.office_lv01_49)) = {}'.format(abs(float(ippan.office_lv01_49_reverse_office_alt_summary) - float(ippan.office_lv01_49))), 'DEBUG')
                    if abs(float(ippan.office_lv01_49_reverse_office_alt_summary) - float(ippan.office_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] office_lv01_49_reverse_office_alt_summary {0} {1}'.format(ippan.office_lv01_49_reverse_office_alt_summary, ippan.office_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.office_lv50_99_reverse_office_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv50_99_reverse_office_alt_summary = {}'.format(ippan.office_lv50_99_reverse_office_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv50_99 = {}'.format(ippan.office_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.office_lv50_99_reverse_office_alt_summary) - float(ippan.office_lv50_99)) = {}'.format(abs(float(ippan.office_lv50_99_reverse_office_alt_summary) - float(ippan.office_lv50_99))), 'DEBUG')
                    if abs(float(ippan.office_lv50_99_reverse_office_alt_summary) - float(ippan.office_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] office_lv50_99_reverse_office_alt_summary {0} {1}'.format(ippan.office_lv50_99_reverse_office_alt_summary, ippan.office_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.office_lv100_reverse_office_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv100_reverse_office_alt_summary = {}'.format(ippan.office_lv100_reverse_office_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_lv100 = {}'.format(ippan.office_lv100), 'DEBUG')
                    print_log('abs(float(ippan.office_lv100_reverse_office_alt_summary) - float(ippan.office_lv100)) = {}'.format(abs(float(ippan.office_lv100_reverse_office_alt_summary) - float(ippan.office_lv100))), 'DEBUG')
                    if abs(float(ippan.office_lv100_reverse_office_alt_summary) - float(ippan.office_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] office_lv100_reverse_office_alt_summary {0} {1}'.format(ippan.office_lv100_reverse_office_alt_summary, ippan.office_lv100), 'WARN')
                        failure_count += 1
                        
                ### if ippan.office_half_reverse_office_alt_summary is not None:
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_half_reverse_office_alt_summary = {}'.format(ippan.office_half_reverse_office_alt_summary), 'DEBUG')
                ###     print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_half = {}'.format(ippan.office_half), 'DEBUG')
                ###     print_log('abs(float(ippan.office_half_reverse_office_alt_summary) - float(ippan.office_half)) = {}'.format(abs(float(ippan.office_half_reverse_office_alt_summary) - float(ippan.office_half))), 'DEBUG')
                ###     if abs(float(ippan.office_half_reverse_office_alt_summary) - float(ippan.office_half)) <= 1e-7:
                ###         success_count += 1
                ###     else:
                ###         failure_count += 1
                
                if ippan.office_full_reverse_office_alt_summary is not None:
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_full_reverse_office_alt_summary = {}'.format(ippan.office_full_reverse_office_alt_summary), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 office_full = {}'.format(ippan.office_full), 'DEBUG')
                    print_log('abs(float(ippan.office_full_reverse_office_alt_summary) - float(ippan.office_full)) = {}'.format(abs(float(ippan.office_full_reverse_office_alt_summary) - float(ippan.office_full))), 'DEBUG')
                    if abs(float(ippan.office_full_reverse_office_alt_summary) - float(ippan.office_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] office_full_reverse_office_alt_summary {0} {1}'.format(ippan.office_full_reverse_office_alt_summary, ippan.office_full), 'WARN')
                        failure_count += 1

            ################################################################### 
            ### DBアクセス処理(0160)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 5/8.', 'DEBUG')
            ### 成功
            if failure_count == 0:
                print_log('[INFO] success_count = {}'.format(success_count), 'INFO')
                print_log('[INFO] failure_count = {}'.format(failure_count), 'INFO')
            ### 失敗
            else:
                print_log('[WARN] success_count = {}'.format(success_count), 'WARN')
                print_log('[WARN] failure_count = {}'.format(failure_count), 'WARN')
            
            connection_cursor = connection.cursor()
            try:
                connection_cursor.execute("""BEGIN""", [])
                
                ### 成功
                if failure_count == 0:
                    connection_cursor.execute("""
                        UPDATE TRIGGER SET 
                            status_code=%s, -- status_code
                            consumed_at=CURRENT_TIMESTAMP, 
                            success_count=%s, -- success_count
                            failure_count=%s, -- failure_count
                            integrity_ok=%s, -- integrity_ok
                            integrity_ng=%s  -- integrity_ng
                        WHERE 
                            trigger_id=%s -- trigger_id
                        """, [
                            'SUCCESS', ### status_code
                            success_count, ### success_count
                            failure_count, ### failure_count
                            '\n'.join(get_info_log()), ### integrity_ok
                            '\n'.join(get_warn_log()), ### integrity_ng
                            trigger_list[0].trigger_id, ### trigger_id
                        ])
                ### 失敗
                else:
                    connection_cursor.execute("""
                        UPDATE TRIGGER SET 
                            status_code=%s, -- status_code
                            consumed_at=CURRENT_TIMESTAMP, 
                            success_count=%s, -- success_count
                            failure_count=%s, -- failure_count
                            integrity_ok=%s, -- integrity_ok
                            integrity_ng=%s  -- integrity_ng
                        WHERE 
                            trigger_id=%s -- trigger_id
                        """, [
                            'FAILURE', ## status_code
                            success_count, ### success_count
                            failure_count, ### failure_count
                            '\n'.join(get_info_log()), ### integrity_ok
                            '\n'.join(get_warn_log()), ### integrity_ng
                            trigger_list[0].trigger_id, ### trigger_id
                        ])

                ###############################################################
                ### DBアクセス処理(0170)
                ### 当該トリガーの実行が終了したため、
                ### (1)成功の場合は、次のトリガーを発行する。
                ### (2)失敗の場合は、次のトリガーを発行しない。
                ###############################################################
                ### print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 6/8.', 'DEBUG')
                ### ### 成功
                ### if failure_count == 0:
                ###     connection_cursor.execute("""
                ###         UPDATE SUIGAI SET 
                ###             summary_file_name=%s, -- summary_file_name 
                ###             summary_file_path=%s  -- summary_file_path 
                ###         WHERE 
                ###             suigai_id=%s -- suigai_id 
                ###         """, [
                ###             trigger_list[0].upload_file_name, 
                ###             trigger_list[0].upload_file_path, 
                ###             trigger_list[0].suigai_id 
                ###         ])
    
                ###############################################################
                ### DBアクセス処理(0180)
                ### 当該トリガーの実行が終了したため、
                ### (1)成功の場合は、次のトリガーを発行する。
                ### (2)失敗の場合は、次のトリガーを発行しない。
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 7/8.', 'DEBUG')
                ### 成功
                if failure_count == 0:
                    connection_cursor.execute("""
                        INSERT INTO TRIGGER (
                            trigger_id, suigai_id, action_code, status_code, success_count, failure_count, 
                            published_at, consumed_at, deleted_at, integrity_ok, integrity_ng, ken_code, city_code, 
                            download_file_path, download_file_name, upload_file_path, upload_file_name 
                        ) VALUES (
                            (SELECT CASE WHEN (MAX(trigger_id+1)) IS NULL THEN CAST(0 AS INTEGER) ELSE CAST(MAX(trigger_id+1) AS INTEGER) END AS trigger_id FROM TRIGGER), -- trigger_id 
                            %s, -- suigai_id 
                            %s, -- action_code 
                            %s, -- status_code 
                            %s, -- success_count 
                            %s, -- failure_count 
                            CURRENT_TIMESTAMP, -- published_at 
                            %s, -- consumed_at 
                            %s, -- deleted_at 
                            %s, -- integrity_ok 
                            %s, -- integrity_ng 
                            %s, -- ken_code 
                            %s, -- city_code 
                            %s, -- download_file_path 
                            %s, -- download_file_name 
                            %s, -- upload_file_path 
                            %s  -- upload_file_name 
                        )""", [
                            trigger_list[0].suigai_id, ### suigai_id 
                            'A99', ### action_code 
                            'WAITING', ### status_code 
                            1, ### success_count 
                            0, ### failure_count 
                            None, ### consumed_at 
                            None, ### deleted_at 
                            None, ### integrity_ok 
                            None, ### integrity_ng 
                            trigger_list[0].ken_code, ### ken_code 
                            trigger_list[0].city_code, ### city_code 
                            trigger_list[0].download_file_path, ### download_file_path 
                            trigger_list[0].download_file_name, ### download_file_name 
                            trigger_list[0].upload_file_path, ### upload_file_path 
                            trigger_list[0].upload_file_name, ### upload_file_name 
                        ])
                ### transaction.commit()
                connection_cursor.execute("""COMMIT""", [])
            except:
                print_log('[ERROR] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
                ### connection_cursor.rollback()
                connection_cursor.execute("""ROLLBACK""", [])
            finally:
                connection_cursor.close()

            ###################################################################
            ### 戻り値セット処理(0190)
            ### 戻り値を戻す。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 STEP 8/8.', 'DEBUG')
            print_log('[INFO] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
            return 0
        except:
            print_log('[ERROR] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            print_log('[ERROR] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900Action.action_A08_verify_sdb_by_reverse_method.handle()関数が異常終了しました。', 'ERROR')
            return 8
            