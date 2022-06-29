#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/management/commands/action_05_reverse.py
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
### from P0000Common.models import EXECUTE             ### 10050: 実行管理

from P0000Common.models import REPOSITORY              ### 10100: レポジトリ

from P0000Common.common import print_log

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
        connection_cursor = connection.cursor()
        try:
            ###################################################################
            ### 引数チェック処理(0000)
            ### コマンドラインからの引数をチェックする。
            ###################################################################
            print_log('[INFO] ########################################', 'INFO')
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数が開始しました。', 'INFO')
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 1/10.', 'INFO')
    
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
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 2/10.', 'INFO')
            trigger_list = None
            trigger_id_list = None
            suigai_id_list = None
            repository_id_list = None
            ippan_reverse_list = None
            
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    * 
                FROM TRIGGER 
                WHERE 
                    action_code='5' AND 
                    consumed_at IS NULL AND 
                    deleted_at IS NULL
                ORDER BY CAST(trigger_id AS INTEGER) LIMIT 1""", [])
            
            print_log('trigger_list = {}'.format(trigger_list), 'INFO')

            if trigger_list is None:
                print_log('[INFO] P0900Action.action_05_reverse.handle()関数が正常終了しました。', 'INFO')
                return 0

            ###################################################################
            ### 計算処理(0020)
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 3/10.', 'INFO')
            trigger_id_list = [trigger.trigger_id for trigger in trigger_list]
            
            print_log('trigger_id_list = {}'.format(trigger_id_list), 'INFO')

            if len(trigger_id_list) <= 0:
                print_log('[INFO] P0900Action.action_05_reverse.handle()関数が正常終了しました。', 'INFO')
                return 0

            suigai_id_list = [trigger.suigai_id for trigger in trigger_list]
            repository_id_list = [trigger.repository_id for trigger in trigger_list]

            print_log('suigai_id_list = {}'.format(suigai_id_list), 'INFO')
            print_log('repository_id_list = {}'.format(repository_id_list), 'INFO')
            
            ###################################################################
            ### DBアクセス処理(0030)
            ### (1)IPPAN_VIEWテーブルにアクセスして、按分計算結果から被害建物棟数等の逆計算結果を取得する。
            ### (2)被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
            ### (3)被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
            ### (4)被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
            ### トリガメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 4/10.', 'INFO')
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
                    
                    CASE WHEN (IV1.building_lv00) IS NULL THEN 0 ELSE (IV1.building_lv00) END AS building_lv00, 
                    CASE WHEN (IV1.building_lv01_49) IS NULL THEN 0 ELSE (IV1.building_lv01_49) END AS building_lv01_49, 
                    CASE WHEN (IV1.building_lv50_99) IS NULL THEN 0 ELSE (IV1.building_lv50_99) END AS building_lv50_99, 
                    CASE WHEN (IV1.building_lv100) IS NULL THEN 0 ELSE (IV1.building_lv100) END AS building_lv100, 
                    CASE WHEN (IV1.building_half) IS NULL THEN 0 ELSE (IV1.building_half) END AS building_half, 
                    CASE WHEN (IV1.building_full) IS NULL THEN 0 ELSE (IV1.building_full) END AS building_full, 
                    CASE WHEN (IV1.building_total) IS NULL THEN 0 ELSE (IV1.building_total) END AS building_total, 
     
                    CASE WHEN (IV1.floor_area) IS NULL THEN 0 ELSE (IV1.floor_area) END AS floor_area, 
                    CASE WHEN (IV1.family) IS NULL THEN 0 ELSE (IV1.family) END AS family, 
                    CASE WHEN (IV1.office) IS NULL THEN 0 ELSE (IV1.office) END AS office, 
    
                    CASE WHEN (IV1.floor_area_lv00) IS NULL THEN 0 ELSE (IV1.floor_area_lv00) END AS floor_area_lv00, 
                    CASE WHEN (IV1.floor_area_lv01_49) IS NULL THEN 0 ELSE (IV1.floor_area_lv01_49) END AS floor_area_lv01_49, 
                    CASE WHEN (IV1.floor_area_lv50_99) IS NULL THEN 0 ELSE (IV1.floor_area_lv50_99) END AS floor_area_lv50_99, 
                    CASE WHEN (IV1.floor_area_lv100) IS NULL THEN 0 ELSE (IV1.floor_area_lv100) END AS floor_area_lv100, 
                    CASE WHEN (IV1.floor_area_half) IS NULL THEN 0 ELSE (IV1.floor_area_half) END AS floor_area_half, 
                    CASE WHEN (IV1.floor_area_full) IS NULL THEN 0 ELSE (IV1.floor_area_full) END AS floor_area_full, 
                    CASE WHEN (IV1.floor_area_total) IS NULL THEN 0 ELSE (IV1.floor_area_total) END AS floor_area_total, 
                    
                    CASE WHEN (IV1.family_lv00) IS NULL THEN 0 ELSE (IV1.family_lv00) END AS family_lv00, 
                    CASE WHEN (IV1.family_lv01_49) IS NULL THEN 0 ELSE (IV1.family_lv01_49) END AS family_lv01_49, 
                    CASE WHEN (IV1.family_lv50_99) IS NULL THEN 0 ELSE (IV1.family_lv50_99) END AS family_lv50_99, 
                    CASE WHEN (IV1.family_lv100) IS NULL THEN 0 ELSE (IV1.family_lv100) END AS family_lv100, 
                    CASE WHEN (IV1.family_half) IS NULL THEN 0 ELSE (IV1.family_half) END AS family_half, 
                    CASE WHEN (IV1.family_full) IS NULL THEN 0 ELSE (IV1.family_full) END AS family_full, 
                    CASE WHEN (IV1.family_total) IS NULL THEN 0 ELSE (IV1.family_total) END AS family_total, 
                   
                    CASE WHEN (IV1.office_lv00) IS NULL THEN 0 ELSE (IV1.office_lv00) END AS office_lv00, 
                    CASE WHEN (IV1.office_lv01_49) IS NULL THEN 0 ELSE (IV1.office_lv01_49) END AS office_lv01_49, 
                    CASE WHEN (IV1.office_lv50_99) IS NULL THEN 0 ELSE (IV1.office_lv50_99) END AS office_lv50_99, 
                    CASE WHEN (IV1.office_lv100) IS NULL THEN 0 ELSE (IV1.office_lv100) END AS office_lv100, 
                    CASE WHEN (IV1.office_half) IS NULL THEN 0 ELSE (IV1.office_half) END AS office_half, 
                    CASE WHEN (IV1.office_full) IS NULL THEN 0 ELSE (IV1.office_full) END AS office_full, 
                    CASE WHEN (IV1.office_total) IS NULL THEN 0 ELSE (IV1.office_total) END AS office_total, 
    
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
                    IV1.deleted_at AS deleted_at, 

                    -- 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_lv00 / IV1.floor_area_total) END AS building_lv00_reverse_floor_area, 
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_lv01_49 / IV1.floor_area_total) END AS building_lv01_49_reverse_floor_area, 
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_lv50_99 / IV1.floor_area_total) END AS building_lv50_99_reverse_floor_area, 
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_lv100 / IV1.floor_area_total) END AS building_lv100_reverse_floor_area, 
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_half / IV1.floor_area_total) END AS building_half_reverse_floor_area, 
                    CASE WHEN (IV1.floor_area_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.floor_area_full / IV1.floor_area_total) END AS building_full_reverse_floor_area, 
    
                    -- 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_lv00 / IV1.family_total) END AS building_lv00_reverse_family, 
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_lv01_49 / IV1.family_total) END AS building_lv01_49_reverse_family, 
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_lv50_99 / IV1.family_total) END AS building_lv50_99_reverse_family, 
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_lv100 / IV1.family_total) END AS building_lv100_reverse_family, 
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_half / IV1.family_total) END AS building_half_reverse_family, 
                    CASE WHEN (IV1.family_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.family_full / IV1.family_total) END AS building_full_reverse_family, 
    
                    -- 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_lv00 / IV1.office_total) END AS building_lv00_reverse_office, 
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_lv01_49 / IV1.office_total) END AS building_lv01_49_reverse_office, 
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_lv50_99 / IV1.office_total) END AS building_lv50_99_reverse_office, 
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_lv100 / IV1.office_total) END AS building_lv100_reverse_office, 
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_half / IV1.office_total) END AS building_half_reverse_office, 
                    CASE WHEN (IV1.office_total) <= 0 THEN 0 ELSE ((IV1.building_total) * IV1.office_full / IV1.office_total) END AS building_full_reverse_office 
                    
                FROM IPPAN_VIEW IV1 
                WHERE 
                    IV1.suigai_id=%s AND 
                    IV1.deleted_at IS NULL 
                ORDER BY CAST(IV1.ippan_id AS INTEGER)
                """, [suigai_id_list[0],])

            print_log('ippan_reverse_list'.format(ippan_reverse_list), 'INFO')

            if ippan_reverse_list is None:
                print_log('[INFO] P0900Action.action_05_reverse.handle()関数が警告終了しました。', 'INFO')
                return 4
    
            ###################################################################
            ### 計算処理(0040)
            ### 成功、失敗の行数、レコード数をカウントする。
            ### 成功:按分計算結果から逆計算した結果と入力DBに登録されている被害建物棟数が同じ場合、成功とする。
            ### 失敗:按分計算結果から逆計算した結果と入力DBに登録されている被害建物棟数が異なる場合、失敗とする。
            ###################################################################
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 5/10.', 'INFO')
            success_count = 0
            failure_count = 0
            epsilon = 0.0000001
                
            for ippan in ippan_reverse_list:
                print_log('suigai_id = {}'.format(ippan.suigai_id), 'INFO')
                ###############################################################
                ### 計算処理(0050)
                ### 被害建物の延床面積(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                if ippan.building_lv00_reverse_floor_area is not None:
                    if float(ippan.building_lv00_reverse_floor_area) - float(ippan.building_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv00_reverse_floor_area = {}'.format(ippan.building_lv00_reverse_floor_area), 'INFO')
                        print_log('building_lv00 = {}'.format(ippan.building_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv01_49_reverse_floor_area is not None:
                    if float(ippan.building_lv01_49_reverse_floor_area) - float(ippan.building_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv01_49_reverse_floor_area = {}'.format(ippan.building_lv01_49_reverse_floor_area), 'INFO')
                        print_log('building_lv01_49 = {}'.format(ippan.building_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv50_99_reverse_floor_area is not None:
                    if float(ippan.building_lv50_99_reverse_floor_area) - float(ippan.building_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv50_99_reverse_floor_area = {}'.format(ippan.building_lv50_99_reverse_floor_area), 'INFO')
                        print_log('building_lv50_99 = {}'.format(ippan.building_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv100_reverse_floor_area is not None:
                    if float(ippan.building_lv100_reverse_floor_area) - float(ippan.building_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv100_reverse_floor_area = {}'.format(ippan.building_lv100_reverse_floor_area), 'INFO')
                        print_log('building_lv100 = {}'.format(ippan.building_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_half_reverse_floor_area is not None:
                    if float(ippan.building_half_reverse_floor_area) - float(ippan.building_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_half_reverse_floor_area = {}'.format(ippan.building_half_reverse_floor_area), 'INFO')
                        print_log('building_half = {}'.format(ippan.building_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_full_reverse_floor_area is not None:
                    if float(ippan.building_full_reverse_floor_area) - float(ippan.building_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_full_reverse_floor_area = {}'.format(ippan.building_full_reverse_floor_area), 'INFO')
                        print_log('building_full = {}'.format(ippan.building_full), 'INFO')
                        failure_count = failure_count + 1

                ###############################################################
                ### 計算処理(0060)
                ### 被災世帯数(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                if ippan.building_lv00_reverse_family is not None:
                    if float(ippan.building_lv00_reverse_family) - float(ippan.building_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv00_reverse_family = {}'.format(ippan.building_lv00_reverse_family), 'INFO')
                        print_log('building_lv00 = {}'.format(ippan.building_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv01_49_reverse_family is not None:
                    if float(ippan.building_lv01_49_reverse_family) - float(ippan.building_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv01_49_reverse_family = {}'.format(ippan.building_lv01_49_reverse_family), 'INFO')
                        print_log('building_lv01_49 = {}'.format(ippan.building_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv50_99_reverse_family is not None:
                    if float(ippan.building_lv50_99_reverse_family) - float(ippan.building_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv50_99_reverse_family = {}'.format(ippan.building_lv50_99_reverse_family), 'INFO')
                        print_log('building_lv50_99 = {}'.format(ippan.building_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv100_reverse_family is not None:
                    if float(ippan.building_lv100_reverse_family) - float(ippan.building_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv100_reverse_family = {}'.format(ippan.building_lv100_reverse_family), 'INFO')
                        print_log('building_lv100 = {}'.format(ippan.building_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_half_reverse_family is not None:
                    if float(ippan.building_half_reverse_family) - float(ippan.building_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_half_reverse_family = {}'.format(ippan.building_half_reverse_family), 'INFO')
                        print_log('building_half = {}'.format(ippan.building_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_full_reverse_family is not None:
                    if float(ippan.building_full_reverse_family) - float(ippan.building_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_full_reverse_family = {}'.format(ippan.building_full_reverse_family), 'INFO')
                        print_log('building_full = {}'.format(ippan.building_full), 'INFO')
                        failure_count = failure_count + 1

                ###############################################################
                ### 計算処理(0070)
                ### 被災事業所数(入力DB)から逆計算により被害建物棟数を求めた結果
                ###############################################################
                if ippan.building_lv00_reverse_office is not None: 
                    if float(ippan.building_lv00_reverse_office) - float(ippan.building_lv00) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv00_reverse_office = {}'.format(ippan.building_lv00_reverse_office), 'INFO')
                        print_log('building_lv00 = {}'.format(ippan.building_lv00), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv01_49_reverse_office is not None: 
                    if float(ippan.building_lv01_49_reverse_office) - float(ippan.building_lv01_49) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv01_49_reverse_office = {}'.format(ippan.building_lv01_49_reverse_office), 'INFO')
                        print_log('building_lv01_49 = {}'.format(ippan.building_lv01_49), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv50_99_reverse_office is not None:
                    if float(ippan.building_lv50_99_reverse_office) - float(ippan.building_lv50_99) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv50_99_reverse_office = {}'.format(ippan.building_lv50_99_reverse_office), 'INFO')
                        print_log('building_lv50_99 = {}'.format(ippan.building_lv50_99), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_lv100_reverse_office is not None:
                    if float(ippan.building_lv100_reverse_office) - float(ippan.building_lv100) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_lv100_reverse_office = {}'.format(ippan.building_lv100_reverse_office), 'INFO')
                        print_log('building_lv100 = {}'.format(ippan.building_lv100), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_half_reverse_office is not None:
                    if float(ippan.building_half_reverse_office) - float(ippan.building_half) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_half_reverse_office = {}'.format(ippan.building_half_reverse_office), 'INFO')
                        print_log('building_half = {}'.format(ippan.building_half), 'INFO')
                        failure_count = failure_count + 1
                if ippan.building_full_reverse_office is not None:
                    if float(ippan.building_full_reverse_office) - float(ippan.building_full) <= 0.0000001:
                        success_count = success_count + 1
                    else:
                        print_log('building_full_reverse_office = {}'.format(ippan.building_full_reverse_office), 'INFO')
                        print_log('building_full = {}'.format(ippan.building_full), 'INFO')
                        failure_count = failure_count + 1

            print_log('success_count = {}'.format(success_count), 'INFO')
            print_log('failure_count = {}'.format(failure_count), 'INFO')
                
            ################################################################### 
            ### DBアクセス処理(0080)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 6/10.', 'INFO')
            print_log('trigger_id_list[0] = {}'.format(trigger_id_list[0]), 'INFO')
            if failure_count == 0:
                connection_cursor.execute("""
                    UPDATE TRIGGER SET 
                        status_code='3', 
                        consumed_at=CURRENT_TIMESTAMP, 
                        success_count=%s, 
                        failure_count=%s 
                    WHERE 
                        trigger_id=%s""", [
                        success_count, 
                        failure_count, 
                        trigger_id_list[0],])
            else:
                connection_cursor.execute("""
                    UPDATE TRIGGER SET 
                        status_code='4', 
                        consumed_at=CURRENT_TIMESTAMP, 
                        success_count=%s, 
                        failure_count=%s 
                    WHERE 
                        trigger_id=%s""", [
                        success_count, 
                        failure_count, 
                        trigger_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0900)
            ### 当該トリガーの実行が終了したため、
            ### (1)成功の場合は、次のトリガーを発行する。
            ### (2)失敗の場合は、次のトリガーを発行しない。
            ################################################################### 
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 7/10.', 'INFO')
            print_log('suigai_id_list[0] = {}'.format(suigai_id_list[0]), 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            if failure_count == 0:
                connection_cursor.execute("""
                    INSERT INTO TRIGGER (
                        trigger_id, 
                        suigai_id, 
                        repository_id, 
                        action_code, 
                        published_at 
                    ) VALUES (
                        (SELECT MAX(trigger_id) + 1 FROM TRIGGER), -- trigger_id
                        %s,                                        -- suigai_id 
                        %s,                                        -- repository_id
                        '6',                                       -- action_code
                        CURRENT_TIMESTAMP                          -- published_at
                    )""", [
                        suigai_id_list[0], 
                        repository_id_list[0],])
    
            ################################################################### 
            ### DBアクセス処理(0090)
            ### 当該トリガーの実行が終了したため、当該レポジトリの状態、成功数、失敗数等を更新する。
            ### (1)成功の場合は、ステータスを 3 に更新する。
            ### (2)失敗の場合は、ステータスを 4 に更新する。
            ################################################################### 
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 8/10.', 'INFO')
            print_log('repository_id_list[0] = {}'.format(repository_id_list[0]), 'INFO')
            if failure_count == 0: 
                connection_cursor.execute("""
                    UPDATE REPOSITORY SET 
                        action_code='5', 
                        status_code='3', 
                        updated_at=CURRENT_TIMESTAMP 
                    WHERE 
                        repository_id=%s AND 
                        deleted_at IS NULL""", [
                        repository_id_list[0],])
            else:
                connection_cursor.execute("""
                    UPDATE REPOSITORY SET 
                        action_code='5', 
                        status_code='4', 
                        updated_at=CURRENT_TIMESTAMP 
                    WHERE 
                        repository_id=%s""", [
                        repository_id_list[0],])

            ################################################################### 
            ### DBアクセス処理(0110)
            ################################################################### 
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 9/10.', 'INFO')
            transaction.commit()

            ###################################################################
            ### 戻り値セット処理(0120)
            ###################################################################
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数 STEP 10/10.', 'INFO')
            print_log('[INFO] P0900Action.action_05_reverse.handle()関数が正常終了しました。', 'INFO')
            return 0
        
        except:
            transaction.rollback()
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P0900Action.action_05_reverse.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900Action.action_05_reverse.handle()関数が異常終了しました。', 'ERROR')
            return 8

        finally:
            connection_cursor.close()
            