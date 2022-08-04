#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/management/commands/action_A05_prorate_idb.py
### A05：按分処理
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

import openpyxl
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.writer.excel import save_virtual_workbook

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
            print_log('[INFO] P0900Action.action_A05_prorate_idb.handle()関数が開始しました。', 'INFO')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 STEP 1/5.', 'DEBUG')

            ###################################################################
            ### DBアクセス処理(0010)
            ### TRIGGERテーブルからSUIGAI_IDのリストを取得する。
            ### トリガーメッセージにアクションが発行されているかを検索する。
            ### 処理対象の水害IDを取得する。
            ### トリガーメッセージにアクションが発行されていなければ、処理を終了する。
            ### ※ネストを浅くするために、処理対象外の場合、処理を終了させる。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 STEP 2/5.', 'DEBUG')
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
                print_log('[INFO] P0900Action.action_A05_prorate_idb.handle()関数が正常終了しました。', 'INFO')
                return 0
            
            if len(trigger_list) == 0:
                print_log('[INFO] P0900Action.action_A05_prorate_idb.handle()関数が正常終了しました。', 'INFO')
                return 0

            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].trigger_id = {}'.format(trigger_list[0].trigger_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].suigai_id = {}'.format(trigger_list[0].suigai_id), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].city_code = {}'.format(trigger_list[0].city_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].ken_code = {}'.format(trigger_list[0].ken_code), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].download_file_path = {}'.format(trigger_list[0].download_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].download_file_name = {}'.format(trigger_list[0].download_file_name), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].upload_file_path = {}'.format(trigger_list[0].upload_file_path), 'DEBUG')
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 trigger_list[0].upload_file_name = {}'.format(trigger_list[0].upload_file_name), 'DEBUG')

            ################################################################### 
            ### DBアクセス処理(0020)
            ### 当該トリガーの実行が終了したため、当該トリガーの状態、成功数、失敗数等を更新する。
            ################################################################### 
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 STEP 3/5.', 'DEBUG')
            connection_cursor = connection.cursor()
            try:
                connection_cursor.execute("""BEGIN""", [])
                
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
                ### DBアクセス処理(0030)
                ### 当該トリガーの実行が終了したため、
                ### 次のトリガーを発行する。
                ###############################################################
                print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 STEP 4/5.', 'DEBUG')
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
                        'A06',  ### action_code 
                        None, ### status_code 
                        None, ### success_count 
                        None, ### failure_count 
                        None, ### consumed_at 
                        None, ### deleted_at 
                        None, ### integrity_ok 
                        None, ### integrity_ng 
                        trigger_list[0].ken_code,  ### ken_code 
                        trigger_list[0].city_code, ### city_code 
                        trigger_list[0].download_file_path, ### download_file_path 
                        trigger_list[0].download_file_name, ### download_file_name 
                        trigger_list[0].upload_file_path, ### upload_file_path 
                        trigger_list[0].upload_file_name, ### upload_file_name
                    ])
                ### transaction.commit()
                connection_cursor.execute("""COMMIT""", [])
            except:
                print_log('[ERROR] P0900Action.action_A05_prorate_idb.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
                ### connection_cursor.rollback()
                connection_cursor.execute("""ROLLBACK""", [])
            finally:
                connection_cursor.close()

            ###################################################################
            ### 戻り値セット処理(0040)
            ### 戻り値を戻す。
            ###################################################################
            print_log('[DEBUG] P0900Action.action_A05_prorate_idb.handle()関数 STEP 5/5.', 'DEBUG')
            print_log('[INFO] P0900Action.action_A05_prorate_idb.handle()関数が正常終了しました。', 'INFO')
            return 0
        except:
            print_log('[ERROR] P0900Action.action_A05_prorate_idb.handle()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            print_log('[ERROR] P0900Action.action_A05_prorate_idb.handle()関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P0900Action.action_A05_prorate_idb.handle()関数が異常終了しました。', 'ERROR')
            return 8
            