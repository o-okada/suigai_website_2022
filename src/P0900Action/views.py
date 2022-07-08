#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900Action/views.py
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
from django.views.generic.base import TemplateView

import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

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

from P0000Common.models import REPOSITORY              ### 11000: レポジトリ

from P0000Common.common import print_log

###############################################################################
### 関数名：get_trigger_list
###############################################################################
def get_trigger_list(action_code, status_code, suigai_id):
    
    if suigai_id == 0:
        trigger_list = TRIGGER.objects.raw("""
            SELECT 
                TR1.trigger_id AS trigger_id, 
                TR1.suigai_id AS suigai_id, 
                SG1.suigai_name AS suigai_name, 
                SG1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                SG1.city_code AS city_code, 
                CT1.city_name AS city_name, 
                TR1.repository_id AS repository_id, 
                RE1.input_file_path AS input_file_path, 
                RE1.input_file_name AS input_file_name, 
                TR1.action_code AS action_code, 
                AC1.action_name AS action_name, 
                TR1.status_code AS status_code, 
                ST1.status_name AS status_name, 
                TR1.published_at AS published_at, 
                TR1.consumed_at AS consumed_at, 
                TR1.success_count AS success_count, 
                TR1.failure_count AS failure_count, 
                TR1.deleted_at AS deleted_at 
            FROM TRIGGER TR1 
            LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
            LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
            LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
            LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
            LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
            LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
            WHERE TR1.action_code=%s AND TR1.status_code=%s AND TR1.deleted_at IS NULL 
            ORDER BY CAST(TR1.trigger_id AS INTEGER) DESC""", [action_code, status_code, ])
    
    else:
        trigger_list = TRIGGER.objects.raw("""
            SELECT 
                TR1.trigger_id AS trigger_id, 
                TR1.suigai_id AS suigai_id, 
                SG1.suigai_name AS suigai_name, 
                SG1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                SG1.city_code AS city_code, 
                CT1.city_name AS city_name, 
                TR1.repository_id AS repository_id, 
                RE1.input_file_path AS input_file_path, 
                RE1.input_file_name AS input_file_name, 
                TR1.action_code AS action_code, 
                AC1.action_name AS action_name, 
                TR1.status_code AS status_code, 
                ST1.status_name AS status_name, 
                TR1.published_at AS published_at, 
                TR1.consumed_at AS consumed_at, 
                TR1.success_count AS success_count, 
                TR1.failure_count AS failure_count, 
                TR1.deleted_at AS deleted_at 
            FROM TRIGGER TR1 
            LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
            LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
            LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
            LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
            LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
            LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
            WHERE TR1.action_code=%s AND TR1.status_code=%s AND TR1.deleted_at IS NULL AND TR1.suigai_id=%s 
            ORDER BY CAST(TR1.trigger_id AS INTEGER) DESC""", [action_code, status_code, suigai_id, ])
    
    return trigger_list

###############################################################################
### 関数名：get_trigger_count
###############################################################################
def get_trigger_count(action_code, status_code, suigai_id):
    
    if suigai_id == 0:
        trigger_list = TRIGGER.objects.raw("""
            SELECT * FROM TRIGGER 
            WHERE action_code=%s AND status_code=%s AND deleted_at IS NULL""", [action_code, status_code, ])
        
    else:
        trigger_list = TRIGGER.objects.raw("""
            SELECT * FROM TRIGGER 
            WHERE action_code=%s AND status_code=%s AND deleted_at IS NULL AND suigai_id=%s""", [action_code, status_code, suigai_id, ])

    if trigger_list:
        return str(len(trigger_list))
    else:
        return str(0)

###############################################################################
### 関数名：index_view
### 自動実行進捗状況一覧表示画面
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.index_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900Action.index_view()関数 STEP 2/3.', 'INFO')
        trigger_WF1_success_list = get_trigger_list(action_code='1', status_code='3', suigai_id=0)
        trigger_WF2_success_list = get_trigger_list(action_code='2', status_code='3', suigai_id=0)
        trigger_WF3_success_list = get_trigger_list(action_code='3', status_code='3', suigai_id=0)
        trigger_WF4_success_list = get_trigger_list(action_code='4', status_code='3', suigai_id=0)
        trigger_WF5_success_list = get_trigger_list(action_code='5', status_code='3', suigai_id=0)
        trigger_WF6_success_list = get_trigger_list(action_code='6', status_code='3', suigai_id=0)
        trigger_WF7_success_list = get_trigger_list(action_code='7', status_code='3', suigai_id=0)
        trigger_WF8_success_list = get_trigger_list(action_code='8', status_code='3', suigai_id=0)
        trigger_WF9_success_list = get_trigger_list(action_code='9', status_code='3', suigai_id=0)
        trigger_WF10_success_list = get_trigger_list(action_code='10', status_code='3', suigai_id=0)
        trigger_WF11_success_list = get_trigger_list(action_code='11', status_code='3', suigai_id=0)
        trigger_WF12_success_list = get_trigger_list(action_code='12', status_code='3', suigai_id=0)
        trigger_WF13_success_list = get_trigger_list(action_code='13', status_code='3', suigai_id=0)
        trigger_WF1_failure_list = get_trigger_list(action_code='1', status_code='4', suigai_id=0)
        trigger_WF2_failure_list = get_trigger_list(action_code='2', status_code='4', suigai_id=0)
        trigger_WF3_failure_list = get_trigger_list(action_code='3', status_code='4', suigai_id=0)
        trigger_WF4_failure_list = get_trigger_list(action_code='4', status_code='4', suigai_id=0)
        trigger_WF5_failure_list = get_trigger_list(action_code='5', status_code='4', suigai_id=0)
        trigger_WF6_failure_list = get_trigger_list(action_code='6', status_code='4', suigai_id=0)
        trigger_WF7_failure_list = get_trigger_list(action_code='7', status_code='4', suigai_id=0)
        trigger_WF8_failure_list = get_trigger_list(action_code='8', status_code='4', suigai_id=0)
        trigger_WF9_failure_list = get_trigger_list(action_code='9', status_code='4', suigai_id=0)
        trigger_WF10_failure_list = get_trigger_list(action_code='10', status_code='4', suigai_id=0)
        trigger_WF11_failure_list = get_trigger_list(action_code='11', status_code='4', suigai_id=0)
        trigger_WF12_failure_list = get_trigger_list(action_code='12', status_code='4', suigai_id=0)
        trigger_WF13_failure_list = get_trigger_list(action_code='13', status_code='4', suigai_id=0)
        
        trigger_WF1_success_count = get_trigger_count(action_code='1', status_code='3', suigai_id=0)
        trigger_WF2_success_count = get_trigger_count(action_code='2', status_code='3', suigai_id=0)
        trigger_WF3_success_count = get_trigger_count(action_code='3', status_code='3', suigai_id=0)
        trigger_WF4_success_count = get_trigger_count(action_code='4', status_code='3', suigai_id=0)
        trigger_WF5_success_count = get_trigger_count(action_code='5', status_code='3', suigai_id=0)
        trigger_WF6_success_count = get_trigger_count(action_code='6', status_code='3', suigai_id=0)
        trigger_WF7_success_count = get_trigger_count(action_code='7', status_code='3', suigai_id=0)
        trigger_WF8_success_count = get_trigger_count(action_code='8', status_code='3', suigai_id=0)
        trigger_WF9_success_count = get_trigger_count(action_code='9', status_code='3', suigai_id=0)
        trigger_WF10_success_count = get_trigger_count(action_code='10', status_code='3', suigai_id=0)
        trigger_WF11_success_count = get_trigger_count(action_code='11', status_code='3', suigai_id=0)
        trigger_WF12_success_count = get_trigger_count(action_code='12', status_code='3', suigai_id=0)
        trigger_WF13_success_count = get_trigger_count(action_code='13', status_code='3', suigai_id=0)

        trigger_WF1_failure_count = get_trigger_count(action_code='1', status_code='4', suigai_id=0)
        trigger_WF2_failure_count = get_trigger_count(action_code='2', status_code='4', suigai_id=0)
        trigger_WF3_failure_count = get_trigger_count(action_code='3', status_code='4', suigai_id=0)
        trigger_WF4_failure_count = get_trigger_count(action_code='4', status_code='4', suigai_id=0)
        trigger_WF5_failure_count = get_trigger_count(action_code='5', status_code='4', suigai_id=0)
        trigger_WF6_failure_count = get_trigger_count(action_code='6', status_code='4', suigai_id=0)
        trigger_WF7_failure_count = get_trigger_count(action_code='7', status_code='4', suigai_id=0)
        trigger_WF8_failure_count = get_trigger_count(action_code='8', status_code='4', suigai_id=0)
        trigger_WF9_failure_count = get_trigger_count(action_code='9', status_code='4', suigai_id=0)
        trigger_WF10_failure_count = get_trigger_count(action_code='10', status_code='4', suigai_id=0)
        trigger_WF11_failure_count = get_trigger_count(action_code='11', status_code='4', suigai_id=0)
        trigger_WF12_failure_count = get_trigger_count(action_code='12', status_code='4', suigai_id=0)
        trigger_WF13_failure_count = get_trigger_count(action_code='13', status_code='4', suigai_id=0)

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.index_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900Action/index.html')
        context = {
            'trigger_WF1_success_list': trigger_WF1_success_list, 
            'trigger_WF2_success_list': trigger_WF2_success_list, 
            'trigger_WF3_success_list': trigger_WF3_success_list, 
            'trigger_WF4_success_list': trigger_WF4_success_list, 
            'trigger_WF5_success_list': trigger_WF5_success_list, 
            'trigger_WF6_success_list': trigger_WF6_success_list, 
            'trigger_WF7_success_list': trigger_WF7_success_list, 
            'trigger_WF8_success_list': trigger_WF8_success_list, 
            'trigger_WF9_success_list': trigger_WF9_success_list, 
            'trigger_WF10_success_list': trigger_WF10_success_list, 
            'trigger_WF11_success_list': trigger_WF11_success_list, 
            'trigger_WF12_success_list': trigger_WF12_success_list, 
            'trigger_WF13_success_list': trigger_WF13_success_list, 
            'trigger_WF1_failure_list': trigger_WF1_failure_list, 
            'trigger_WF2_failure_list': trigger_WF2_failure_list, 
            'trigger_WF3_failure_list': trigger_WF3_failure_list, 
            'trigger_WF4_failure_list': trigger_WF4_failure_list, 
            'trigger_WF5_failure_list': trigger_WF5_failure_list, 
            'trigger_WF6_failure_list': trigger_WF6_failure_list, 
            'trigger_WF7_failure_list': trigger_WF7_failure_list, 
            'trigger_WF8_failure_list': trigger_WF8_failure_list, 
            'trigger_WF9_failure_list': trigger_WF9_failure_list, 
            'trigger_WF10_failure_list': trigger_WF10_failure_list, 
            'trigger_WF11_failure_list': trigger_WF11_failure_list, 
            'trigger_WF12_failure_list': trigger_WF12_failure_list, 
            'trigger_WF13_failure_list': trigger_WF13_failure_list, 
            'trigger_WF1_success_count': trigger_WF1_success_count, 
            'trigger_WF2_success_count': trigger_WF2_success_count, 
            'trigger_WF3_success_count': trigger_WF3_success_count, 
            'trigger_WF4_success_count': trigger_WF4_success_count, 
            'trigger_WF5_success_count': trigger_WF5_success_count, 
            'trigger_WF6_success_count': trigger_WF6_success_count, 
            'trigger_WF7_success_count': trigger_WF7_success_count, 
            'trigger_WF8_success_count': trigger_WF8_success_count, 
            'trigger_WF9_success_count': trigger_WF9_success_count, 
            'trigger_WF10_success_count': trigger_WF10_success_count, 
            'trigger_WF11_success_count': trigger_WF11_success_count, 
            'trigger_WF12_success_count': trigger_WF12_success_count, 
            'trigger_WF13_success_count': trigger_WF13_success_count, 
            'trigger_WF1_failure_count': trigger_WF1_failure_count, 
            'trigger_WF2_failure_count': trigger_WF2_failure_count, 
            'trigger_WF3_failure_count': trigger_WF3_failure_count, 
            'trigger_WF4_failure_count': trigger_WF4_failure_count, 
            'trigger_WF5_failure_count': trigger_WF5_failure_count, 
            'trigger_WF6_failure_count': trigger_WF6_failure_count, 
            'trigger_WF7_failure_count': trigger_WF7_failure_count, 
            'trigger_WF8_failure_count': trigger_WF8_failure_count, 
            'trigger_WF9_failure_count': trigger_WF9_failure_count, 
            'trigger_WF10_failure_count': trigger_WF10_failure_count, 
            'trigger_WF11_failure_count': trigger_WF11_failure_count, 
            'trigger_WF12_failure_count': trigger_WF12_failure_count, 
            'trigger_WF13_failure_count': trigger_WF13_failure_count, 
        }
        print_log('[INFO] P0900Action.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：suigai_view
### 自動実行進捗状況一覧表示画面
###############################################################################
@login_required(None, login_url='/P0100Login/')
def suigai_view(request, suigai_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.suigai_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.suigai_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.suigai_view()関数 suigai_id = {}'.format(suigai_id), 'INFO')
        print_log('[INFO] P0900Action.suigai_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900Action.suigai_view()関数 STEP 2/3.', 'INFO')
        trigger_WF1_success_list = get_trigger_list(action_code='1', status_code='3', suigai_id=suigai_id)
        trigger_WF2_success_list = get_trigger_list(action_code='2', status_code='3', suigai_id=suigai_id)
        trigger_WF3_success_list = get_trigger_list(action_code='3', status_code='3', suigai_id=suigai_id)
        trigger_WF4_success_list = get_trigger_list(action_code='4', status_code='3', suigai_id=suigai_id)
        trigger_WF5_success_list = get_trigger_list(action_code='5', status_code='3', suigai_id=suigai_id)
        trigger_WF6_success_list = get_trigger_list(action_code='6', status_code='3', suigai_id=suigai_id)
        trigger_WF7_success_list = get_trigger_list(action_code='7', status_code='3', suigai_id=suigai_id)
        trigger_WF8_success_list = get_trigger_list(action_code='8', status_code='3', suigai_id=suigai_id)
        trigger_WF9_success_list = get_trigger_list(action_code='9', status_code='3', suigai_id=suigai_id)
        trigger_WF10_success_list = get_trigger_list(action_code='10', status_code='3', suigai_id=suigai_id)
        trigger_WF11_success_list = get_trigger_list(action_code='11', status_code='3', suigai_id=suigai_id)
        trigger_WF12_success_list = get_trigger_list(action_code='12', status_code='3', suigai_id=suigai_id)
        trigger_WF13_success_list = get_trigger_list(action_code='13', status_code='3', suigai_id=suigai_id)
        trigger_WF1_failure_list = get_trigger_list(action_code='1', status_code='4', suigai_id=suigai_id)
        trigger_WF2_failure_list = get_trigger_list(action_code='2', status_code='4', suigai_id=suigai_id)
        trigger_WF3_failure_list = get_trigger_list(action_code='3', status_code='4', suigai_id=suigai_id)
        trigger_WF4_failure_list = get_trigger_list(action_code='4', status_code='4', suigai_id=suigai_id)
        trigger_WF5_failure_list = get_trigger_list(action_code='5', status_code='4', suigai_id=suigai_id)
        trigger_WF6_failure_list = get_trigger_list(action_code='6', status_code='4', suigai_id=suigai_id)
        trigger_WF7_failure_list = get_trigger_list(action_code='7', status_code='4', suigai_id=suigai_id)
        trigger_WF8_failure_list = get_trigger_list(action_code='8', status_code='4', suigai_id=suigai_id)
        trigger_WF9_failure_list = get_trigger_list(action_code='9', status_code='4', suigai_id=suigai_id)
        trigger_WF10_failure_list = get_trigger_list(action_code='10', status_code='4', suigai_id=suigai_id)
        trigger_WF11_failure_list = get_trigger_list(action_code='11', status_code='4', suigai_id=suigai_id)
        trigger_WF12_failure_list = get_trigger_list(action_code='12', status_code='4', suigai_id=suigai_id)
        trigger_WF13_failure_list = get_trigger_list(action_code='13', status_code='4', suigai_id=suigai_id)
        
        trigger_WF1_success_count = get_trigger_count(action_code='1', status_code='3', suigai_id=suigai_id)
        trigger_WF2_success_count = get_trigger_count(action_code='2', status_code='3', suigai_id=suigai_id)
        trigger_WF3_success_count = get_trigger_count(action_code='3', status_code='3', suigai_id=suigai_id)
        trigger_WF4_success_count = get_trigger_count(action_code='4', status_code='3', suigai_id=suigai_id)
        trigger_WF5_success_count = get_trigger_count(action_code='5', status_code='3', suigai_id=suigai_id)
        trigger_WF6_success_count = get_trigger_count(action_code='6', status_code='3', suigai_id=suigai_id)
        trigger_WF7_success_count = get_trigger_count(action_code='7', status_code='3', suigai_id=suigai_id)
        trigger_WF8_success_count = get_trigger_count(action_code='8', status_code='3', suigai_id=suigai_id)
        trigger_WF9_success_count = get_trigger_count(action_code='9', status_code='3', suigai_id=suigai_id)
        trigger_WF10_success_count = get_trigger_count(action_code='10', status_code='3', suigai_id=suigai_id)
        trigger_WF11_success_count = get_trigger_count(action_code='11', status_code='3', suigai_id=suigai_id)
        trigger_WF12_success_count = get_trigger_count(action_code='12', status_code='3', suigai_id=suigai_id)
        trigger_WF13_success_count = get_trigger_count(action_code='13', status_code='3', suigai_id=suigai_id)

        trigger_WF1_failure_count = get_trigger_count(action_code='1', status_code='4', suigai_id=suigai_id)
        trigger_WF2_failure_count = get_trigger_count(action_code='2', status_code='4', suigai_id=suigai_id)
        trigger_WF3_failure_count = get_trigger_count(action_code='3', status_code='4', suigai_id=suigai_id)
        trigger_WF4_failure_count = get_trigger_count(action_code='4', status_code='4', suigai_id=suigai_id)
        trigger_WF5_failure_count = get_trigger_count(action_code='5', status_code='4', suigai_id=suigai_id)
        trigger_WF6_failure_count = get_trigger_count(action_code='6', status_code='4', suigai_id=suigai_id)
        trigger_WF7_failure_count = get_trigger_count(action_code='7', status_code='4', suigai_id=suigai_id)
        trigger_WF8_failure_count = get_trigger_count(action_code='8', status_code='4', suigai_id=suigai_id)
        trigger_WF9_failure_count = get_trigger_count(action_code='9', status_code='4', suigai_id=suigai_id)
        trigger_WF10_failure_count = get_trigger_count(action_code='10', status_code='4', suigai_id=suigai_id)
        trigger_WF11_failure_count = get_trigger_count(action_code='11', status_code='4', suigai_id=suigai_id)
        trigger_WF12_failure_count = get_trigger_count(action_code='12', status_code='4', suigai_id=suigai_id)
        trigger_WF13_failure_count = get_trigger_count(action_code='13', status_code='4', suigai_id=suigai_id)

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.suigai_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900Action/index.html')
        context = {
            'trigger_WF1_success_list': trigger_WF1_success_list, 
            'trigger_WF2_success_list': trigger_WF2_success_list, 
            'trigger_WF3_success_list': trigger_WF3_success_list, 
            'trigger_WF4_success_list': trigger_WF4_success_list, 
            'trigger_WF5_success_list': trigger_WF5_success_list, 
            'trigger_WF6_success_list': trigger_WF6_success_list, 
            'trigger_WF7_success_list': trigger_WF7_success_list, 
            'trigger_WF8_success_list': trigger_WF8_success_list, 
            'trigger_WF9_success_list': trigger_WF9_success_list, 
            'trigger_WF10_success_list': trigger_WF10_success_list, 
            'trigger_WF11_success_list': trigger_WF11_success_list, 
            'trigger_WF12_success_list': trigger_WF12_success_list, 
            'trigger_WF13_success_list': trigger_WF13_success_list, 
            'trigger_WF1_failure_list': trigger_WF1_failure_list, 
            'trigger_WF2_failure_list': trigger_WF2_failure_list, 
            'trigger_WF3_failure_list': trigger_WF3_failure_list, 
            'trigger_WF4_failure_list': trigger_WF4_failure_list, 
            'trigger_WF5_failure_list': trigger_WF5_failure_list, 
            'trigger_WF6_failure_list': trigger_WF6_failure_list, 
            'trigger_WF7_failure_list': trigger_WF7_failure_list, 
            'trigger_WF8_failure_list': trigger_WF8_failure_list, 
            'trigger_WF9_failure_list': trigger_WF9_failure_list, 
            'trigger_WF10_failure_list': trigger_WF10_failure_list, 
            'trigger_WF11_failure_list': trigger_WF11_failure_list, 
            'trigger_WF12_failure_list': trigger_WF12_failure_list, 
            'trigger_WF13_failure_list': trigger_WF13_failure_list, 
            'trigger_WF1_success_count': trigger_WF1_success_count, 
            'trigger_WF2_success_count': trigger_WF2_success_count, 
            'trigger_WF3_success_count': trigger_WF3_success_count, 
            'trigger_WF4_success_count': trigger_WF4_success_count, 
            'trigger_WF5_success_count': trigger_WF5_success_count, 
            'trigger_WF6_success_count': trigger_WF6_success_count, 
            'trigger_WF7_success_count': trigger_WF7_success_count, 
            'trigger_WF8_success_count': trigger_WF8_success_count, 
            'trigger_WF9_success_count': trigger_WF9_success_count, 
            'trigger_WF10_success_count': trigger_WF10_success_count, 
            'trigger_WF11_success_count': trigger_WF11_success_count, 
            'trigger_WF12_success_count': trigger_WF12_success_count, 
            'trigger_WF13_success_count': trigger_WF13_success_count, 
            'trigger_WF1_failure_count': trigger_WF1_failure_count, 
            'trigger_WF2_failure_count': trigger_WF2_failure_count, 
            'trigger_WF3_failure_count': trigger_WF3_failure_count, 
            'trigger_WF4_failure_count': trigger_WF4_failure_count, 
            'trigger_WF5_failure_count': trigger_WF5_failure_count, 
            'trigger_WF6_failure_count': trigger_WF6_failure_count, 
            'trigger_WF7_failure_count': trigger_WF7_failure_count, 
            'trigger_WF8_failure_count': trigger_WF8_failure_count, 
            'trigger_WF9_failure_count': trigger_WF9_failure_count, 
            'trigger_WF10_failure_count': trigger_WF10_failure_count, 
            'trigger_WF11_failure_count': trigger_WF11_failure_count, 
            'trigger_WF12_failure_count': trigger_WF12_failure_count, 
            'trigger_WF13_failure_count': trigger_WF13_failure_count, 
        }
        print_log('[INFO] P0900Action.suigai_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.suigai_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.suigai_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：trigger_view
### 自動実行進捗状況詳細表示画面
###############################################################################
@login_required(None, login_url='/P0100Login/')
def trigger_view(request, trigger_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.trigger_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.trigger_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.trigger_view()関数 trigger_id = {}'.format(trigger_id), 'INFO')
        print_log('[INFO] P0900Action.trigger_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900Action.trigger_view()関数 STEP 2/3.', 'INFO')
        trigger = TRIGGER.objects.raw("""
        SELECT 
            TR1.trigger_id AS trigger_id, 
            TR1.suigai_id AS suigai_id, 
            SG1.suigai_name AS suigai_name, 
            SG1.ken_code AS ken_code, 
            KE1.ken_name AS ken_name, 
            SG1.city_code AS city_code, 
            CT1.city_name AS city_name, 
            TR1.repository_id AS repository_id, 
            TR1.action_code AS action_code, 
            AC1.action_name AS action_name, 
            TR1.status_code AS status_code, 
            ST1.status_name AS status_name, 
            TR1.published_at AS published_at, 
            TR1.consumed_at AS consumed_at, 
            TR1.success_count AS success_count, 
            TR1.failure_count AS failure_count, 
            RE1.input_file_path AS input_file_path, 
            TR1.data_integrity_left AS data_integrity_left, 
            TR1.data_integrity_right AS data_integrity_right 
        FROM TRIGGER TR1 
        LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
        LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
        LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
        LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
        LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
        LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
        WHERE trigger_id=%s""", [trigger_id, ])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.trigger_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900Action/trigger.html')
        context = {
            'trigger': trigger, 
        }
        print_log('[INFO] P0900Action.trigger_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.trigger_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.trigger_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：download_file_view
### エクセルファイルダウンロード
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def download_file_view(request, repository_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.download_file_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.download_file_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.download_file_view()関数 STEP 1/1.', 'INFO')
        
        result_file_path = 'static/ippan_chosa_result2.xlsx'
        wb = openpyxl.load_workbook(result_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0010)
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.download_file_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa_result2.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.download_file_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.download_file_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：graph_view
### 自動実行進捗状況グラフ表示画面
###############################################################################
@login_required(None, login_url='/P0100Login/')
def graph_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.graph_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.graph_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.graph_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900Action.graph_view()関数 STEP 2/3.', 'INFO')
        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        trigger_list = TRIGGER.objects.raw("""
            SELECT 
                TR1.trigger_id AS trigger_id, 
                TR1.suigai_id AS suigai_id, 
                SG1.suigai_name AS suigai_name, 
                SG1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                SG1.city_code AS city_code, 
                CT1.city_name AS city_name, 
                TR1.repository_id AS repository_id, 
                TR1.action_code AS action_code, 
                AC1.action_name AS action_name, 
                TR1.status_code AS status_code, 
                ST1.status_name AS status_name, 
                TR1.published_at AS published_at, 
                TR1.consumed_at AS consumed_at, 
                TR1.success_count AS success_count, 
                TR1.failure_count AS failure_count, 
                TR1.deleted_at AS deleted_at 
            FROM TRIGGER TR1 
            LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
            LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
            LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
            LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
            LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
            ORDER BY CAST(TR1.trigger_id AS INTEGER) DESC""", [])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.graph_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900Action/graph.html')
        context = {
            'ken_list': ken_list, 
            'trigger_list': trigger_list, 
        }
        print_log('[INFO] P0900Action.graph_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.graph_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.graph_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_city_repository_view
### 自動実行進捗状況グラフ表示画面
###############################################################################
@login_required(None, login_url='/P0100Login/')
def ken_city_repository_view(request, ken_code, city_code, repository_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 city_code = {}'.format(city_code), 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 repository_id = {}'.format(repository_id), 'INFO')
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 STEP 2/3.', 'INFO')
        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(ken_code AS INTEGER)""", [])
        if ken_code == "0":
            city_list = []
        else:
            city_list = CITY.objects.raw("""
                SELECT * FROM CITY WHERE ken_code=%s ORDER BY CAST(city_code AS INTEGER)""", [ken_code, ])
            
        if city_code == "0": 
            repository_list = []
        else: 
            repository_list = REPOSITORY.objects.raw("""
                SELECT 
                    RE1.repository_id AS repository_id, 
                    RE1.suigai_id AS suigai_id, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    RE1.status_code AS status_code, 
                    RE1.created_at AS created_at, 
                    RE1.updated_at AS updated_at, 
                    RE1.input_file_path AS input_file_path, 
                    RE1.deleted_at AS deleted_at, 
                    RE1.committed_at AS committed_at 
                FROM REPOSITORY RE1 
                LEFT JOIN SUIGAI SG1 ON RE1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                WHERE SG1.city_code=%s 
                ORDER BY CAST(RE1.repository_id AS INTEGER) DESC""", [city_code, ])
        
        if ken_code == "0" and city_code == "0" and repository_id == "0": 
            print_log('ken_code == "0" and city_code == "0" and repository_id == "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ORDER BY CAST(TR1.trigger_id AS INTEGER) DESC""", [])
            
        elif ken_code == "0" and city_code == "0" and repository_id != "0": 
            print_log('ken_code == "0" and city_code == "0" and repository_id != "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                WHERE TR1.repository_id=%s 
                ORDER BY CAST(TR1.trigger_id AS INTEGER) DESC""", [repository_id, ])
        
        elif ken_code == "0" and city_code != "0" and repository_id == "0": 
            print_log('ken_code == "0" and city_code != "0" and repository_id == "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.city_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [city_code, ])
        
        elif ken_code == "0" and city_code != "0" and repository_id != "0": 
            print_log('ken_code == "0" and city_code != "0" and repository_id != "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.city_code=%s AND SUB1.repository_id=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [city_code, repository_id, ])
        
        elif ken_code != "0" and city_code == "0" and repository_id == "0": 
            print_log('ken_code != "0" and city_code == "0" and repository_id == "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.ken_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [ken_code, ])
        
        elif ken_code != "0" and city_code == "0" and repository_id != "0": 
            print_log('ken_code != "0" and city_code == "0" and repository_id != "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.ken_code=%s AND SUB1.repository_id=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [ken_code, repository_id, ])
        
        elif ken_code != "0" and city_code != "0" and repository_id == "0": 
            print_log('ken_code != "0" and city_code != "0" and repository_id == "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.ken_code=%s AND SUB1.city_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [ken_code, city_code, ])
        
        elif ken_code != "0" and city_code != "0" and repository_id != "0": 
            print_log('ken_code != "0" and city_code != "0" and repository_id != "0"', 'INFO')
            trigger_list = TRIGGER.objects.raw("""
                SELECT 
                    SUB1.trigger_id AS trigger_id, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.ken_code AS ken_code, 
                    SUB1.ken_name AS ken_name, 
                    SUB1.city_code AS city_code, 
                    SUB1.city_name AS city_name, 
                    SUB1.repository_id AS repository_id, 
                    SUB1.action_code AS action_code, 
                    SUB1.action_name AS action_name, 
                    SUB1.status_code AS status_code, 
                    SUB1.status_name AS status_name, 
                    SUB1.published_at AS published_at, 
                    SUB1.consumed_at AS consumed_at, 
                    SUB1.success_count AS success_count, 
                    SUB1.failure_count AS failure_count, 
                    SUB1.input_file_path AS input_file_path 
                FROM 
                (
                SELECT 
                    TR1.trigger_id AS trigger_id, 
                    TR1.suigai_id AS suigai_id, 
                    SG1.suigai_name AS suigai_name, 
                    SG1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SG1.city_code AS city_code, 
                    CT1.city_name AS city_name, 
                    TR1.repository_id AS repository_id, 
                    TR1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    TR1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    TR1.published_at AS published_at, 
                    TR1.consumed_at AS consumed_at, 
                    TR1.success_count AS success_count, 
                    TR1.failure_count AS failure_count, 
                    RE1.input_file_path AS input_file_path 
                FROM TRIGGER TR1 
                LEFT JOIN SUIGAI SG1 ON TR1.suigai_id=SG1.suigai_id 
                LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
                LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
                LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
                LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
                ) SUB1 
                WHERE SUB1.ken_code=%s AND SUB1.city_code=%s AND SUB1.repository_id=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER) DESC""", [ken_code, city_code, repository_id, ])
                    
        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900Action.ken_city_repository_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900Action/index.html')
        context = {
            'ken_code': ken_code, 
            'city_code': city_code, 
            'repository_id': int(repository_id), 
            'ken_list': ken_list, 
            'city_list': city_list, 
            'trigger_list': trigger_list, 
            'repository_list': repository_list, 
        }
        print_log('[INFO] P0900Action.ken_city_repository_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900Action.ken_city_repository_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900Action.ken_city_repository_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
