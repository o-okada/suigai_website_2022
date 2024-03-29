#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/management/commands/action_A05_verify_idb_by_reverse_method.py
### A06：データ検証
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
            print_log('[INFO] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が開始しました。', 'INFO')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 1/7.', 'DEBUG')
    
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
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 2/7.', 'DEBUG')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE 
                    action_code='A05' AND 
                    consumed_at IS NULL AND 
                    deleted_at IS NULL
                ORDER BY CAST(trigger_id AS INTEGER) LIMIT 1""", [])

            if trigger_list is None:
                print_log('[INFO] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
                return 0

            if len(trigger_list) == 0:
                print_log('[INFO] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
                return 0

            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].trigger_id = {}'.format(trigger_list[0].trigger_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].suigai_id = {}'.format(trigger_list[0].suigai_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].city_code = {}'.format(trigger_list[0].city_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].ken_code = {}'.format(trigger_list[0].ken_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].download_file_path = {}'.format(trigger_list[0].download_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].download_file_name = {}'.format(trigger_list[0].download_file_name), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].upload_file_path = {}'.format(trigger_list[0].upload_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 trigger_list[0].upload_file_name = {}'.format(trigger_list[0].upload_file_name), 'DEBUG')
            
            ###################################################################
            ### DBアクセス処理(0020)
            ### (1)IPPAN_VIEWテーブルにアクセスして、按分計算結果から被害建物棟数等の逆計算結果を取得する。
            ### (2)被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
            ### (3)被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
            ### (4)被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
            ### トリガメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 3/7.', 'DEBUG')
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
                    TO_CHAR(timezone('JST', IV1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                    TO_CHAR(timezone('JST', IV1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
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
                    IV1.suikei_type_code AS suikei_type_code, 
                    IV1.suikei_type_name AS suikei_type_name, 
                    IV1.kasen_code AS kasen_code, 
                    IV1.kasen_name AS kasen_name, 
                    IV1.kasen_type_code AS kasen_type_code, 
                    IV1.kasen_type_name AS kasen_type_name, 
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
                    IV1.upload_file_path AS upload_file_path, 
                    IV1.upload_file_name AS upload_file_name, 
                    IV1.summary_file_path AS summary_file_path, 
                    IV1.summary_file_name AS summary_file_name, 
                    
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
                    IV1.comment AS comment, 
                    
                    TO_CHAR(timezone('JST', IV1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', IV1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at, 

                    -- 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_lv00 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv00_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_lv01_49 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_lv50_99 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_lv100 / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_lv100_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_half / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_half_reverse_floor_area, 
                    CASE WHEN ABS(IV1.floor_area_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.floor_area_full / IV1.floor_area_total AS NUMERIC(20,10)) END AS building_full_reverse_floor_area, 
    
                    -- 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_lv00 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv00_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_lv01_49 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_lv50_99 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_lv100 / IV1.family_total AS NUMERIC(20,10)) END AS building_lv100_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_half / IV1.family_total AS NUMERIC(20,10)) END AS building_half_reverse_family, 
                    CASE WHEN ABS(IV1.family_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.family_full / IV1.family_total AS NUMERIC(20,10)) END AS building_full_reverse_family, 
    
                    -- 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_lv00 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv00_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_lv01_49 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv01_49_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_lv50_99 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv50_99_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_lv100 / IV1.office_total AS NUMERIC(20,10)) END AS building_lv100_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_half / IV1.office_total AS NUMERIC(20,10)) END AS building_half_reverse_office, 
                    CASE WHEN ABS(IV1.office_total) <= 0.0000001 THEN 0 ELSE CAST(IV1.building_total * IV1.office_full / IV1.office_total AS NUMERIC(20,10)) END AS building_full_reverse_office 
                    
                FROM IPPAN_VIEW IV1 
                WHERE 
                    IV1.suigai_id=%s AND 
                    IV1.deleted_at IS NULL 
                ORDER BY CAST(IV1.ippan_id AS INTEGER)""", [trigger_list[0].suigai_id, ])

            if ippan_reverse_list is None:
                print_log('[WARN] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が警告終了しました。', 'WARN')
                return 4
    
            ###################################################################
            ### 計算処理(0030)
            ### 成功、失敗の行数、レコード数をカウントする。
            ### 成功:按分計算結果から逆計算した結果と入力DBに登録されている被害建物棟数が同じ場合、成功とする。
            ### 失敗:按分計算結果から逆計算した結果と入力DBに登録されている被害建物棟数が異なる場合、失敗とする。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 4/7.', 'DEBUG')
            success_count = 0
            failure_count = 0
            ### epsilon = 0.0000001
                
            for ippan in ippan_reverse_list:
                ###############################################################
                ### 計算処理(0040)
                ### 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 4_1/7.', 'DEBUG')
                if ippan.building_lv00_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00_reverse_floor_area = {}'.format(ippan.building_lv00_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00 = {}'.format(ippan.building_lv00), 'DEBUG')
                    print_log('abs(float(ippan.building_lv00_reverse_floor_area) - float(ippan.building_lv00)) = {}'.format(abs(float(ippan.building_lv00_reverse_floor_area) - float(ippan.building_lv00))), 'DEBUG')
                    if abs(float(ippan.building_lv00_reverse_floor_area) - float(ippan.building_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv00 {0} {1}'.format(ippan.building_lv00_reverse_floor_area, ippan.building_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv01_49_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49_reverse_floor_area = {}'.format(ippan.building_lv01_49_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49 = {}'.format(ippan.building_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.building_lv01_49_reverse_floor_area) - float(ippan.building_lv01_49)) = {}'.format(abs(float(ippan.building_lv01_49_reverse_floor_area) - float(ippan.building_lv01_49))), 'DEBUG')
                    if abs(float(ippan.building_lv01_49_reverse_floor_area) - float(ippan.building_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv01_49 {0} {1}'.format(ippan.building_lv01_49_reverse_floor_area, ippan.building_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv50_99_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99_reverse_floor_area = {}'.format(ippan.building_lv50_99_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99 = {}'.format(ippan.building_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.building_lv50_99_reverse_floor_area) - float(ippan.building_lv50_99)) = {}'.format(abs(float(ippan.building_lv50_99_reverse_floor_area) - float(ippan.building_lv50_99))), 'DEBUG')
                    if abs(float(ippan.building_lv50_99_reverse_floor_area) - float(ippan.building_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv50_99 {0} {1}'.format(ippan.building_lv50_99_reverse_floor_area, ippan.building_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv100_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100_reverse_floor_area = {}'.format(ippan.building_lv100_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100 = {}'.format(ippan.building_lv100), 'DEBUG')
                    print_log('abs(float(ippan.building_lv100_reverse_floor_area) - float(ippan.building_lv100)) = {}'.format(abs(float(ippan.building_lv100_reverse_floor_area) - float(ippan.building_lv100))), 'DEBUG')
                    if abs(float(ippan.building_lv100_reverse_floor_area) - float(ippan.building_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv100 {0} {1}'.format(ippan.building_lv100_reverse_floor_area, ippan.building_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.building_half_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half_reverse_floor_area = {}'.format(ippan.building_half_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half = {}'.format(ippan.building_half), 'DEBUG')
                    print_log('abs(float(ippan.building_half_reverse_floor_area) - float(ippan.building_half)) = {}'.format(abs(float(ippan.building_half_reverse_floor_area) - float(ippan.building_half))), 'DEBUG')
                    if abs(float(ippan.building_half_reverse_floor_area) - float(ippan.building_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_half {0} {1}'.format(ippan.building_half_reverse_floor_area, ippan.building_half), 'WARN')
                        failure_count += 1
                        
                if ippan.building_full_reverse_floor_area is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full_reverse_floor_area = {}'.format(ippan.building_full_reverse_floor_area), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full = {}'.format(ippan.building_full), 'DEBUG')
                    print_log('abs(float(ippan.building_full_reverse_floor_area) - float(ippan.building_full)) = {}'.format(abs(float(ippan.building_full_reverse_floor_area) - float(ippan.building_full))), 'DEBUG')
                    if abs(float(ippan.building_full_reverse_floor_area) - float(ippan.building_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_full {0} {1}'.format(ippan.building_full_reverse_floor_area, ippan.building_full), 'WARN')
                        failure_count += 1

                ###############################################################
                ### 計算処理(0050)
                ### 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 4_2/7.', 'DEBUG')
                if ippan.building_lv00_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00_reverse_family = {}'.format(ippan.building_lv00_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00 = {}'.format(ippan.building_lv00), 'DEBUG')
                    print_log('abs(float(ippan.building_lv00_reverse_family) - float(ippan.building_lv00)) = {}'.format(abs(float(ippan.building_lv00_reverse_family) - float(ippan.building_lv00))), 'DEBUG')
                    if abs(float(ippan.building_lv00_reverse_family) - float(ippan.building_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv00 {0} {1}'.format(ippan.building_lv00_reverse_family, ippan.building_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv01_49_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49_reverse_family = {}'.format(ippan.building_lv01_49_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49 = {}'.format(ippan.building_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.building_lv01_49_reverse_family) - float(ippan.building_lv01_49)) = {}'.format(abs(float(ippan.building_lv01_49_reverse_family) - float(ippan.building_lv01_49))), 'DEBUG')
                    if abs(float(ippan.building_lv01_49_reverse_family) - float(ippan.building_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv01_49 {0} {1}'.format(ippan.building_lv01_49_reverse_family, ippan.building_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv50_99_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99_reverse_family = {}'.format(ippan.building_lv50_99_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99 = {}'.format(ippan.building_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.building_lv50_99_reverse_family) - float(ippan.building_lv50_99)) = {}'.format(abs(float(ippan.building_lv50_99_reverse_family) - float(ippan.building_lv50_99))), 'DEBUG')
                    if abs(float(ippan.building_lv50_99_reverse_family) - float(ippan.building_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv50_99 {0} {1}'.format(ippan.building_lv50_99_reverse_family, ippan.building_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv100_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100_reverse_family = {}'.format(ippan.building_lv100_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100 = {}'.format(ippan.building_lv100), 'DEBUG')
                    print_log('abs(float(ippan.building_lv100_reverse_family) - float(ippan.building_lv100)) = {}'.format(abs(float(ippan.building_lv100_reverse_family) - float(ippan.building_lv100))), 'DEBUG')
                    if abs(float(ippan.building_lv100_reverse_family) - float(ippan.building_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv100 {0} {1}'.format(ippan.building_lv100_reverse_family, ippan.building_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.building_half_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half_reverse_family = {}'.format(ippan.building_half_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half = {}'.format(ippan.building_half), 'DEBUG')
                    print_log('abs(float(ippan.building_half_reverse_family) - float(ippan.building_half)) = {}'.format(abs(float(ippan.building_half_reverse_family) - float(ippan.building_half))), 'DEBUG')
                    if abs(float(ippan.building_half_reverse_family) - float(ippan.building_half)) <= 1e-7:
                        success_count = success_count + 1
                    else:
                        print_log('[WARN] building_half {0} {1}'.format(ippan.building_half_reverse_family, ippan.building_half), 'WARN')
                        failure_count += 1
                        
                if ippan.building_full_reverse_family is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full_reverse_family = {}'.format(ippan.building_full_reverse_family), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full = {}'.format(ippan.building_full), 'DEBUG')
                    print_log('abs(float(ippan.building_full_reverse_family) - float(ippan.building_full)) = {}'.format(abs(float(ippan.building_full_reverse_family) - float(ippan.building_full))), 'DEBUG')
                    if abs(float(ippan.building_full_reverse_family) - float(ippan.building_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_full {0} {1}'.format(ippan.building_full_reverse_family, ippan.building_full), 'WARN')
                        failure_count += 1

                ###############################################################
                ### 計算処理(0060)
                ### 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 4_3/7.', 'DEBUG')
                if ippan.building_lv00_reverse_office is not None: 
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00_reverse_office = {}'.format(ippan.building_lv00_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv00 = {}'.format(ippan.building_lv00), 'DEBUG')
                    print_log('abs(float(ippan.building_lv00_reverse_office) - float(ippan.building_lv00)) = {}'.format(abs(float(ippan.building_lv00_reverse_office) - float(ippan.building_lv00))), 'DEBUG')
                    if abs(float(ippan.building_lv00_reverse_office) - float(ippan.building_lv00)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv00 {0} {1}'.format(ippan.building_lv00_reverse_office, ippan.building_lv00), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv01_49_reverse_office is not None: 
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49_reverse_office = {}'.format(ippan.building_lv01_49_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv01_49 = {}'.format(ippan.building_lv01_49), 'DEBUG')
                    print_log('abs(float(ippan.building_lv01_49_reverse_office) - float(ippan.building_lv01_49)) = {}'.format(abs(float(ippan.building_lv01_49_reverse_office) - float(ippan.building_lv01_49))), 'DEBUG')
                    if abs(float(ippan.building_lv01_49_reverse_office) - float(ippan.building_lv01_49)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv01_49 {0} {1}'.format(ippan.building_lv01_49_reverse_office, ippan.building_lv01_49), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv50_99_reverse_office is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99_reverse_office = {}'.format(ippan.building_lv50_99_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv50_99 = {}'.format(ippan.building_lv50_99), 'DEBUG')
                    print_log('abs(float(ippan.building_lv50_99_reverse_office) - float(ippan.building_lv50_99)) = {}'.format(abs(float(ippan.building_lv50_99_reverse_office) - float(ippan.building_lv50_99))), 'DEBUG')
                    if abs(float(ippan.building_lv50_99_reverse_office) - float(ippan.building_lv50_99)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv50_99 {0} {1}'.format(ippan.building_lv50_99_reverse_office, ippan.building_lv50_99), 'WARN')
                        failure_count += 1
                        
                if ippan.building_lv100_reverse_office is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100_reverse_office = {}'.format(ippan.building_lv100_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_lv100 = {}'.format(ippan.building_lv100), 'DEBUG')
                    print_log('abs(float(ippan.building_lv100_reverse_office) - float(ippan.building_lv100)) = {}'.format(abs(float(ippan.building_lv100_reverse_office) - float(ippan.building_lv100))), 'DEBUG')
                    if abs(float(ippan.building_lv100_reverse_office) - float(ippan.building_lv100)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_lv100 {0} {1}'.format(ippan.building_lv100_reverse_office, ippan.building_lv100), 'WARN')
                        failure_count += 1
                        
                if ippan.building_half_reverse_office is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half_reverse_office = {}'.format(ippan.building_half_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_half = {}'.format(ippan.building_half), 'DEBUG')
                    print_log('abs(float(ippan.building_half_reverse_office) - float(ippan.building_half)) = {}'.format(abs(float(ippan.building_half_reverse_office) - float(ippan.building_half))), 'DEBUG')
                    if abs(float(ippan.building_half_reverse_office) - float(ippan.building_half)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_half {0} {1}'.format(ippan.building_half_reverse_office, ippan.building_half), 'WARN')
                        failure_count += 1
                        
                if ippan.building_full_reverse_office is not None:
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full_reverse_office = {}'.format(ippan.building_full_reverse_office), 'DEBUG')
                    print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 building_full = {}'.format(ippan.building_full), 'DEBUG')
                    print_log('abs(float(ippan.building_full_reverse_office) - float(ippan.building_full)) = {}'.format(abs(float(ippan.building_full_reverse_office) - float(ippan.building_full))), 'DEBUG')
                    if abs(float(ippan.building_full_reverse_office) - float(ippan.building_full)) <= 1e-7:
                        success_count += 1
                    else:
                        print_log('[WARN] building_full {0} {1}'.format(ippan.building_full_reverse_office, ippan.building_full), 'WARN')
                        failure_count += 1

            ################################################################### 
            ### DBアクセス処理(0070)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 5/7.', 'DEBUG')

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
                            'FAILURE', ### status_code
                            success_count, ### success_count
                            failure_count, ### failure_count
                            '\n'.join(get_info_log()), ### integrity_ok
                            '\n'.join(get_warn_log()), ### integrity_ng
                            trigger_list[0].trigger_id, ### trigger_id
                        ])
    
                ###############################################################
                ### DBアクセス処理(0080)
                ### 当該トリガーの実行が終了したため、
                ### (1)成功の場合は、次のトリガーを発行する。
                ### (2)失敗の場合は、次のトリガーを発行しない。
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 6/7.', 'DEBUG')
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
                            'A06', ### action_code 
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
                print_log('[ERROR] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
                ### connection_cursor.rollback()
                connection_cursor.execute("""ROLLBACK""", [])
            finally:
                connection_cursor.close()
                
            ###################################################################
            ### 戻り値セット処理(0090)
            ### 戻り値を戻す。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 STEP 7/7.', 'DEBUG')
            print_log('[INFO] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が正常終了しました。', 'INFO')
            return 0
        except:
            print_log('[ERROR] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            print_log('[ERROR] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900Action.action_A05_verify_idb_by_reverse_method.handle()関数が異常終了しました。', 'ERROR')
            return 8
            