#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/management/commands/action_A06_summarize_sdb.py
### A07：集計処理
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
from P0000Common.models import KOEKI_INDUSTRY          ### 1140: 公益事業分類

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
    ### 集計OKの場合、トリガーの状態を成功に更新、消費日時をカレントに更新、新たなトリガーを生成する。
    ### 集計NGの場合、トリガーの状態を失敗に更新、消費日時をカレントに更新する。
    ### 集計NGの場合、当該水害IDについて、以降の処理を止めて、手動？で再実行、または、入力データから再登録するイメージである。
    ### 上記は、このアプリの共通の考え方とする。
    ###########################################################################
    def handle(self, *args, **options):
        try:
            ###################################################################
            ### 引数チェック処理(0000)
            ### コマンドラインからの引数をチェックする。
            ###################################################################
            reset_log()
            print_log('[INFO] P0900Action.action_A06_summarize_sdb.handle()関数が開始しました。', 'INFO')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 1/7.', 'DEBUG')
    
            ###################################################################
            ### DBアクセス処理(0010)
            ### TRIGGERテーブルからSUIGAI_IDのリストを取得する。
            ### トリガーメッセージにアクションが発行されているかを検索する。
            ### 処理対象の水害IDを取得する。
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 2/7.', 'DEBUG')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE 
                    action_code='A06' AND 
                    consumed_at IS NULL AND 
                    deleted_at IS NULL 
                ORDER BY CAST(trigger_id AS INTEGER) LIMIT 1""", [])

            if trigger_list is None:
                print_log('[INFO] P0900Action.action_A06_summarize_sdb.handle()関数が正常終了しました。', 'INFO')
                return 0

            if len(trigger_list) == 0:
                print_log('[INFO] P0900Action.action_A06_summarize_sdb.handle()関数が正常終了しました。', 'INFO')
                return 0

            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].trigger_id = {}'.format(trigger_list[0].trigger_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].suigai_id = {}'.format(trigger_list[0].suigai_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].city_code = {}'.format(trigger_list[0].city_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].ken_code = {}'.format(trigger_list[0].ken_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].download_file_path = {}'.format(trigger_list[0].download_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].download_file_name = {}'.format(trigger_list[0].download_file_name), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].upload_file_path = {}'.format(trigger_list[0].upload_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 trigger_list[0].upload_file_name = {}'.format(trigger_list[0].upload_file_name), 'DEBUG')
            
            ###################################################################
            ### DBアクセス処理(0020)
            ### 集計データから集計データを1件削除する。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 3/7.', 'DEBUG')
            connection_cursor = connection.cursor()
            try:
                connection_cursor.execute("""BEGIN""", [])
                
                connection_cursor.execute("""
                    UPDATE IPPAN_SUMMARY SET 
                        deleted_at=CURRENT_TIMESTAMP 
                    WHERE 
                        suigai_id=%s AND 
                        deleted_at IS NULL""", [
                        trigger_list[0].suigai_id, ### trigger_id
                    ])
            
                ###############################################################
                ### DBアクセス処理(0030)
                ### 集計データに集計データを1件登録する。
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 4/7.', 'DEBUG')
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
                        -- committed_at 
                        -- deleted_at 
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
                        IV1.family_lv01_49 * HCL1.house_clean_days_lv00_50 * HCL1.house_clean_unit_cost AS house_clean_summary_lv01_49, 
                        IV1.family_lv50_99 * HCL1.house_clean_days_lv50_100 * HCL1.house_clean_unit_cost AS house_clean_summary_lv50_99, 
                        IV1.family_lv100 * HCL1.house_clean_days_lv100_200 * HCL1.house_clean_unit_cost AS house_clean_summary_lv100, 
                        IV1.family_half * HCL1.house_clean_days_lv200_300 * HCL1.house_clean_unit_cost AS house_clean_summary_half, 
                        IV1.family_full * HCL1.house_clean_days_lv300 * HCL1.house_clean_unit_cost AS house_clean_summary_full, 
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
                        LEFT JOIN HOUSE_ASSET HA1 ON IV1.ken_code=HA1.ken_code 
                        LEFT JOIN HOUSE_RATE HR1 ON IV1.flood_sediment_code=HR1.flood_sediment_code AND IV1.gradient_code=HR1.gradient_code 
                        LEFT JOIN HOUSEHOLD_RATE HHR1 ON IV1.flood_sediment_code=HHR1.flood_sediment_code 
                        LEFT JOIN OFFICE_ASSET OA1 ON IV1.industry_code=OA1.industry_code 
                        LEFT JOIN OFFICE_RATE OR1 ON IV1.flood_sediment_code=OR1.flood_sediment_code 
                        LEFT JOIN FARMER_FISHER_RATE FFR1 ON IV1.flood_sediment_code=FFR1.flood_sediment_code, 
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
                    """, [
                        trigger_list[0].suigai_id, ### trigger_id
                    ])
    
                ############################################################### 
                ### DBアクセス処理(0040)
                ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 5/7.', 'DEBUG')
                connection_cursor.execute("""
                    UPDATE TRIGGER SET 
                        status_code=%s, -- status_code
                        success_count=%s, -- success_count
                        failure_count=%s, -- failure_count
                        consumed_at=CURRENT_TIMESTAMP, 
                        integrity_ok=%s, -- integrity_ok
                        integrity_ng=%s  -- integrity_ng
                    WHERE 
                        trigger_id=%s -- trigger_id
                    """, [
                        'SUCCESS', ### status_code
                        1, ### success_count 
                        0, ### failure_count 
                        '\n'.join(get_info_log()), ### integrity_ok 
                        '\n'.join(get_warn_log()), ### integrity_ng 
                        trigger_list[0].trigger_id, ### trigger_id 
                    ])
    
                ############################################################### 
                ### DBアクセス処理(0050)
                ### 当該トリガーの実行が終了したため、
                ### (1)成功の場合は、次のトリガーを発行する。
                ### (2)失敗の場合は、次のトリガーを発行しない。
                ############################################################### 
                print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 6/7.', 'DEBUG')
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
                        'A07', ### action_code 
                        None, ### status_code 
                        None, ### success_count 
                        None, ### failure_count 
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
                print_log('[ERROR] P0900Action.action_A06_summarize_sdb.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
                ### connection_cursor.rollback()
                connection_cursor.execute("""ROLLBACK""", [])
            finally:
                connection_cursor.close()
            
            ###################################################################
            ### 戻り値セット処理(0060)
            ### 戻り値を戻す。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A06_summarize_sdb.handle()関数 STEP 7/7.', 'DEBUG')
            print_log('[INFO] P0900Action.action_A06_summarize_sdb.handle()関数が正常終了しました。', 'INFO')
            return 0
        except:
            print_log('[ERROR] P0900Action.action_A06_summarize_sdb.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            print_log('[ERROR] P0900Action.action_A06_summarize_sdb.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900Action.action_A06_summarize_sdb.handle()関数が異常終了しました。', 'ERROR')
            return 8
            