#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900CI/management/commands/action_06_summary.py
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
            print_log('[INFO] P0900CI.action_06_summary.handle()関数が開始しました。', 'INFO')
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 1/10.', 'INFO')
    
            ###################################################################
            ### DBアクセス処理(0010)
            ### TRIGGERテーブルからSUIGAI_IDのリストを取得する。
            ### トリガーメッセージにアクションが発行されているかを検索する。
            ### 処理対象の水害IDを取得する。
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 2/10.', 'INFO')
            trigger_list = None
            trigger_id_list = None
            suigai_id_list = None
            repository_id_list = None
            
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE ACTION_CODE='6' AND CONSUMED_AT IS NULL 
                ORDER BY CAST(TRIGGER_ID AS INTEGER) LIMIT 1""", [])

            print_log('trigger_list = {}'.format(trigger_list), 'INFO')

            if trigger_list is None:
                print_log('[INFO] P0900CI.action_06_summary.handle()関数が正常終了しました。', 'INFO')
                return 0

            ###################################################################
            ### 計算処理(0020)
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 3/10.', 'INFO')
            trigger_id_list = [trigger.trigger_id for trigger in trigger_list]

            print_log('trigger_id_list = {}'.format(trigger_id_list), 'INFO')

            if len(trigger_id_list) <= 0:
                print_log('[INFO] P0900CI.action_06_summary.handle()関数が正常終了しました。', 'INFO')
                return 0

            suigai_id_list = [trigger.suigai_id for trigger in trigger_list]
            repository_id_list = [trigger.repository_id for trigger in trigger_list]

            print_log('suigai_id_list = {}'.format(suigai_id_list), 'INFO')
            print_log('repository_id_list = {}'.format(repository_id_list), 'INFO')
            
            ###################################################################
            ### DBアクセス処理(0030)
            ### 一般資産集計データから一般資産集計データを1件削除する。
            ###################################################################
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 4/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            connection_cursor.execute("""
                DELETE 
                FROM IPPAN_SUMMARY 
                WHERE suigai_id=%s""", [
                suigai_id_list[0],])
            
            ###################################################################
            ### DBアクセス処理(0040)
            ### 一般資産集計データに一般資産集計データを1件登録する。
            ###################################################################
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 5/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            connection_cursor.execute("""
                INSERT INTO IPPAN_SUMMARY (
                    ippan_id, 
                    suigai_id, 
                    house_summary_lv00, 
                    house_summary_lv01_49, 
                    house_summary_lv50_99, 
                    house_summary_lv100, 
                    house_summary_half, 
                    house_summary_full, 
                    household_summary_lv00, 
                    household_summary_lv01_49, 
                    household_summary_lv50_99, 
                    household_summary_lv100, 
                    household_summary_half, 
                    household_summary_full, 
                    car_summary_lv00, 
                    car_summary_lv01_49, 
                    car_summary_lv50_99, 
                    car_summary_lv100, 
                    car_summary_half, 
                    car_summary_full, 
                    house_alt_summary_lv00, 
                    house_alt_summary_lv01_49, 
                    house_alt_summary_lv50_99, 
                    house_alt_summary_lv100, 
                    house_alt_summary_half, 
                    house_alt_summary_full, 
                    house_clean_summary_lv00, 
                    house_clean_summary_lv01_49, 
                    house_clean_summary_lv50_99, 
                    house_clean_summary_lv100, 
                    house_clean_summary_half, 
                    house_clean_summary_full, 
                    office_dep_summary_lv00, 
                    office_dep_summary_lv01_49, 
                    office_dep_summary_lv50_99, 
                    office_dep_summary_lv100, 
                    -- office_dep_summary_half, 
                    office_dep_summary_full, 
                    office_inv_summary_lv00, 
                    office_inv_summary_lv01_49, 
                    office_inv_summary_lv50_99, 
                    office_inv_summary_lv100, 
                    -- office_inv_summary_half, 
                    office_inv_summary_full, 
                    office_sus_summary_lv00, 
                    office_sus_summary_lv01_49, 
                    office_sus_summary_lv50_99, 
                    office_sus_summary_lv100, 
                    -- office_sus_summary_half, 
                    office_sus_summary_full, 
                    office_stg_summary_lv00, 
                    office_stg_summary_lv01_49, 
                    office_stg_summary_lv50_99, 
                    office_stg_summary_lv100, 
                    -- office_stg_summary_half, 
                    office_stg_summary_full, 
                    farmer_fisher_dep_summary_lv00, 
                    farmer_fisher_dep_summary_lv01_49, 
                    farmer_fisher_dep_summary_lv50_99, 
                    farmer_fisher_dep_summary_lv100, 
                    -- farmer_fisher_dep_summary_half, 
                    farmer_fisher_dep_summary_full, 
                    farmer_fisher_inv_summary_lv00, 
                    farmer_fisher_inv_summary_lv01_49, 
                    farmer_fisher_inv_summary_lv50_99, 
                    farmer_fisher_inv_summary_lv100, 
                    -- farmer_fisher_inv_summary_half, 
                    farmer_fisher_inv_summary_full, 
                    office_alt_summary_lv00, 
                    office_alt_summary_lv01_49, 
                    office_alt_summary_lv50_99, 
                    office_alt_summary_lv100, 
                    office_alt_summary_half, 
                    office_alt_summary_full 
                ) 
                SELECT 
                    IV1.ippan_id AS ippan_id, 
                    IV1.suigai_id AS suigai_id, 
                    IV1.floor_area_lv00 * HA1.house_asset * HR1.house_rate_lv00 AS house_summary_lv00, 
                    IV1.floor_area_lv01_49 * HA1.house_asset * HR1.house_rate_lv00_50 AS house_summary_lv01_49, 
                    IV1.floor_area_lv50_99 * HA1.house_asset * HR1.house_rate_lv50_100 AS house_summary_lv50_99, 
                    IV1.floor_area_lv100 * HA1.house_asset * HR1.house_rate_lv100_200 AS house_summary_lv100, 
                    IV1.floor_area_half * HA1.house_asset * HR1.house_rate_lv200_300 AS house_summary_half, 
                    IV1.floor_area_full * HA1.house_asset * HR1.house_rate_lv300 AS house_summary_full, 
                    IV1.family_lv00 * HHA1.household_asset * HHR1.household_rate_lv00 AS household_summary_lv00, 
                    IV1.family_lv01_49 * HHA1.household_asset * HHR1.household_rate_lv00_50 AS household_summary_lv01_49, 
                    IV1.family_lv50_99 * HHA1.household_asset * HHR1.household_rate_lv50_100 AS household_summary_lv50_99, 
                    IV1.family_lv100 * HHA1.household_asset * HHR1.household_rate_lv100_200 AS household_summary_lv100, 
                    IV1.family_half * HHA1.household_asset * HHR1.household_rate_lv200_300 AS household_summary_half, 
                    IV1.family_full * HHA1.household_asset * HHR1.household_rate_lv300 AS household_summary_full, 
                    IV1.family_lv00 * CA1.car_asset * CR1.car_rate_lv00 AS car_summary_lv00, 
                    IV1.family_lv01_49 * CA1.car_asset * CR1.car_rate_lv00_50 AS car_summary_lv01_49, 
                    IV1.family_lv50_99 * CA1.car_asset * CR1.car_rate_lv50_100 AS car_summary_lv50_99, 
                    IV1.family_lv100 * CA1.car_asset * CR1.car_rate_lv100_200 AS car_summary_lv100, 
                    IV1.family_half * CA1.car_asset * CR1.car_rate_lv200_300 AS car_summary_half, 
                    IV1.family_full * CA1.car_asset * CR1.car_rate_lv300 AS car_summary_full, 
                    IV1.family_lv00 * HALT1.house_alt_lv00 AS house_alt_summary_lv00, 
                    IV1.family_lv01_49 * HALT1.house_alt_lv00_50 AS house_alt_summary_lv01_49, 
                    IV1.family_lv50_99 * HALT1.house_alt_lv50_100 AS house_alt_summary_lv50_99, 
                    IV1.family_lv100 * HALT1.house_alt_lv100_200 AS house_alt_summary_lv100, 
                    IV1.family_half * HALT1.house_alt_lv200_300 AS house_alt_summary_half, 
                    IV1.family_full * HALT1.house_alt_lv300 AS house_alt_summary_full, 
                    IV1.family_lv00 * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_lv00, 
                    IV1.family_lv01_49 * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_lv01_49, 
                    IV1.family_lv50_99 * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_lv50_99, 
                    IV1.family_lv100 * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_lv100, 
                    IV1.family_half * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_half, 
                    IV1.family_full * HCL1.house_clean_days_lv00 * HCL1.house_clean_unit_cost AS house_clean_summary_full, 
                    IV1.employee_lv00 * OA1.office_dep_asset * OR1.office_dep_rate_lv00 AS office_dep_summary_lv00, 
                    IV1.employee_lv01_49 * OA1.office_dep_asset * OR1.office_dep_rate_lv00_50 AS office_dep_summary_lv01_49, 
                    IV1.employee_lv50_99 * OA1.office_dep_asset * OR1.office_dep_rate_lv50_100 AS office_dep_summary_lv50_99, 
                    IV1.employee_lv100 * OA1.office_dep_asset * OR1.office_dep_rate_lv100_200 AS office_dep_summary_lv100, 
                    -- IV1.employee_half * OA1.office_dep_asset * OR1.office_dep_rate_lv200_300 AS office_dep_summary_half, 
                    IV1.employee_full * OA1.office_dep_asset * OR1.office_dep_rate_lv300 AS office_dep_summary_full, 
                    IV1.employee_lv00 * OA1.office_inv_asset * OR1.office_inv_rate_lv00 AS office_inv_summary_lv00, 
                    IV1.employee_lv01_49 * OA1.office_inv_asset * OR1.office_inv_rate_lv00_50 AS office_inv_summary_lv01_49, 
                    IV1.employee_lv50_99 * OA1.office_inv_asset * OR1.office_inv_rate_lv50_100 AS office_inv_summary_lv50_99, 
                    IV1.employee_lv100 * OA1.office_inv_asset * OR1.office_inv_rate_lv100_200 AS office_inv_summary_lv100, 
                    -- IV1.employee_half * OA1.office_inv_asset * OR1.office_inv_rate_lv200_300 AS office_inv_summary_half, 
                    IV1.employee_full * OA1.office_inv_asset * OR1.office_inv_rate_lv300 AS office_inv_summary_full, 
                    IV1.employee_lv00 * OA1.office_va_asset * OSUS1.office_sus_days_lv00 AS office_sus_summary_lv00, 
                    IV1.employee_lv01_49 * OA1.office_va_asset * OSUS1.office_sus_days_lv00_50 AS office_sus_summary_lv00_50, 
                    IV1.employee_lv50_99 * OA1.office_va_asset * OSUS1.office_sus_days_lv50_100 AS office_sus_summary_lv50_100, 
                    IV1.employee_lv100 * OA1.office_va_asset * OSUS1.office_sus_days_lv100_200 AS office_sus_summary_lv100_200, 
                    -- IV1.employee_half * OA1.office_va_asset * OSUS1.office_sus_days_lv200_300 AS office_sus_summary_lv200_300, 
                    IV1.employee_full * OA1.office_va_asset * OSUS1.office_sus_days_lv300 AS office_sus_summary_lv300, 
                    IV1.employee_lv00 * OA1.office_va_asset * OSTG1.office_stg_days_lv00 / 2.0 AS office_stg_summary_lv00, 
                    IV1.employee_lv01_49 * OA1.office_va_asset * OSTG1.office_stg_days_lv00_50 / 2.0 AS office_stg_summary_lv01_49, 
                    IV1.employee_lv50_99 * OA1.office_va_asset * OSTG1.office_stg_days_lv50_100 / 2.0 AS office_stg_summary_lv50_99, 
                    IV1.employee_lv100 * OA1.office_va_asset * OSTG1.office_stg_days_lv100_200 / 2.0 AS office_stg_summary_lv100, 
                    -- IV1.employee_half * OA1.office_va_asset * OSTG1.office_stg_days_lv200_300 / 2.0 AS office_stg_summary_half, 
                    IV1.employee_full * OA1.office_va_asset * OSTG1.office_stg_days_lv300 / 2.0 AS office_stg_summary_full, 
                    IV1.farmer_fisher_lv00 * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00 AS farmer_fisher_dep_summary_lv00, 
                    IV1.farmer_fisher_lv01_49 * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv00_50 AS farmer_fisher_dep_summary_lv01_49, 
                    IV1.farmer_fisher_lv50_99 * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv50_100 AS farmer_fisher_dep_summary_lv50_99, 
                    IV1.farmer_fisher_lv100 * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv100_200 AS farmer_fisher_dep_summary_lv100, 
                    --IV1.farmer_fisher_half * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv200_300 AS farmer_fisher_dep_summary_half, 
                    IV1.farmer_fisher_full * FFA1.farmer_fisher_dep_asset * FFR1.farmer_fisher_dep_rate_lv300 AS farmer_fisher_dep_summary_full, 
                    IV1.farmer_fisher_lv00 * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00 AS farmer_fisher_inv_summary_lv00, 
                    IV1.farmer_fisher_lv01_49 * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv00_50 AS farmer_fisher_inv_summary_lv01_49, 
                    IV1.farmer_fisher_lv50_99 * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv50_100 AS farmer_fisher_inv_summary_lv50_99, 
                    IV1.farmer_fisher_lv100 * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv100_200 AS farmer_fisher_inv_summary_lv100, 
                    -- IV1.farmer_fisher_half * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv200_300 AS farmer_fisher_inv_summary_half, 
                    IV1.farmer_fisher_full * FFA1.farmer_fisher_inv_asset * FFR1.farmer_fisher_inv_rate_lv300 AS farmer_fisher_inv_summary_full, 
                    IV1.office_lv00 * OALT1.office_alt_lv00 AS office_alt_summary_lv00, 
                    IV1.office_lv01_49 * OALT1.office_alt_lv00_50 AS office_alt_summary_lv01_49, 
                    IV1.office_lv50_99 * OALT1.office_alt_lv50_100 AS office_alt_summary_lv50_99, 
                    IV1.office_lv100 * OALT1.office_alt_lv100_200 AS office_alt_summary_lv100, 
                    IV1.office_half * OALT1.office_alt_lv200_300 AS office_alt_summary_half, 
                    IV1.office_full * OALT1.office_alt_lv300 AS office_alt_summary_full 
                FROM 
                    IPPAN_VIEW IV1 
                    LEFT JOIN HOUSE_ASSET HA1 ON IV1.ken_code = HA1.ken_code 
                    LEFT JOIN HOUSE_RATE HR1 ON IV1.flood_sediment_code = HR1.flood_sediment_code AND IV1.gradient_code = HR1.gradient_code 
                    LEFT JOIN HOUSEHOLD_RATE HHR1 ON IV1.flood_sediment_code = HHR1.flood_sediment_code 
                    LEFT JOIN OFFICE_ASSET OA1 ON IV1.industry_code = OA1.industry_code 
                    LEFT JOIN OFFICE_RATE OR1 ON IV1.flood_sediment_code = OR1.flood_sediment_code 
                    LEFT JOIN FARMER_FISHER_RATE FFR1 ON IV1.flood_sediment_code = FFR1.flood_sediment_code, 
                    HOUSEHOLD_ASSET HHA1, 
                    CAR_ASSET CA1, 
                    CAR_RATE CR1, 
                    HOUSE_ALT HALT1, 
                    HOUSE_CLEAN HCL1, 
                    OFFICE_SUSPEND OSUS1, 
                    OFFICE_STAGNATE OSTG1, 
                    FARMER_FISHER_ASSET FFA1, 
                    OFFICE_ALT OALT1 
                WHERE IV1.suigai_id=%s""", [
                suigai_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0050)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 6/10.', 'INFO')
            print_log('trigger_id_list[0] = {}'.format(trigger_id_list[0]), 'INFO')
            connection_cursor.execute("""
                UPDATE TRIGGER SET 
                STATUS_CODE='3', 
                CONSUMED_AT=CURRENT_TIMESTAMP, 
                SUCCESS_COUNT=%s, 
                FAILURE_COUNT=%s 
                WHERE TRIGGER_ID=%s""", [
                None, 
                None, 
                trigger_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0060)
            ### 当該トリガーの実行が終了したため、当該レポジトリの状態、成功数、失敗数等を更新する。
            ### (1)成功の場合は、ステータスを 3 に更新する。
            ### (2)失敗の場合は、ステータスを 4 に更新する。
            ################################################################### 
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 7/10.', 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            connection_cursor.execute("""
                UPDATE REPOSITORY SET 
                ACTION_CODE='6', 
                STATUS_CODE='3', 
                UPDATED_AT=CURRENT_TIMESTAMP, 
                WHERE REPOSITORY_ID=%s""", [
                repository_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0070)
            ### 当該トリガーの実行が終了したため、
            ### (1)成功の場合は、次のトリガーを発行する。
            ### (2)失敗の場合は、次のトリガーを発行しない。
            ################################################################### 
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 8/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            connection_cursor.execute("""
                INSERT INTO TRIGGER (TRIGGER_ID, SUIGAI_ID, REPOSITORY_ID, ACTION_CODE, PUBLISHED_AT) VALUES (
                (SELECT MAX(TRIGGER_ID) + 1 FROM TRIGGER), 
                %s, 
                %s, 
                '7', 
                CURRENT_TIMESTAMP)""", [
                suigai_id_list[0], repository_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0080)
            ################################################################### 
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 9/10.', 'INFO')
            transaction.commit()
            
            ###################################################################
            ### 戻り値セット処理(0090)
            ###################################################################
            print_log('[INFO] P0900CI.action_06_summary.handle()関数 STEP 10/10.', 'INFO')
            print_log('[INFO] P0900CI.action_06_summary.handle()関数が正常終了しました。', 'INFO')
            return 0
        
        except:
            transaction.rollback()
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P0900CI.action_06_summary.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900CI.action_06_summary.handle()関数が異常終了しました。', 'ERROR')
            return 8

        finally:
            connection_cursor.close()
            