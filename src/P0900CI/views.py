#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0900CI/views.py
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
### from P0000Common.models import EXECUTE             ### 10050: 実行管理

from P0000Common.models import REPOSITORY              ### 11000: EXCELファイルレポジトリ

from P0000Common.common import print_log

###############################################################################
### 関数名：index_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900CI.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900CI.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900CI.index_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900CI.index_view()関数 STEP 2/3.', 'INFO')
        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)""", [])
        trigger_list = TRIGGER.objects.raw("""
            SELECT 
                TR1.TRIGGER_ID AS TRIGGER_ID, 
                TR1.SUIGAI_ID AS SUIGAI_ID, 
                TR1.REPOSITORY_ID AS REPOSITORY_ID, 
                TR1.ACTION_CODE AS ACTION_CODE, 
                AC1.ACTION_NAME AS ACTION_NAME, 
                TR1.STATUS_CODE AS STATUS_CODE, 
                ST1.STATUS_NAME AS STATUS_NAME, 
                TR1.PUBLISHED_AT AS PUBLISHED_AT, 
                TR1.CONSUMED_AT AS CONSUMED_AT, 
                TR1.SUCCESS_COUNT AS SUCCESS_COUNT, 
                TR1.FAILURE_COUNT AS FAILURE_COUNT 
            FROM TRIGGER TR1 
            LEFT JOIN ACTION AC1 ON TR1.ACTION_CODE=AC1.ACTION_CODE 
            LEFT JOIN STATUS ST1 ON TR1.STATUS_CODE=ST1.STATUS_CODE 
            ORDER BY CAST(TR1.TRIGGER_ID AS INTEGER)""", [])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900CI.index_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900CI/index.html')
        context = {
            'ken_list': ken_list, 
            'trigger_list': trigger_list, 
        }
        print_log('[INFO] P0900CI.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900CI.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900CI.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_city_status_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def ken_city_status_view(request, ken_code, city_code, status_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数 city_code = {}'.format(city_code), 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数 status_code = {}'.format(status_code), 'INFO')
        print_log('[INFO] P0900CI.ken_city_status_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900CI.ken_city_status_view()関数 STEP 2/3.', 'INFO')
        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(ken_code AS INTEGER)""", [])
        if ken_code == "0":
            city_list = []
        else:
            city_list = CITY.objects.raw("""
                SELECT * FROM CITY WHERE ken_code=%s ORDER BY CAST(city_code AS INTEGER)""", [ken_code,])
        
        if ken_code == "0" and city_code == "0" and status_code == "0": 
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
                ORDER BY CAST(TR1.trigger_id AS INTEGER)""", [])
            
        elif ken_code == "0" and city_code == "0" and status_code != "0": 
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
                WHERE TR1.status_code=%s 
                ORDER BY CAST(TR1.trigger_id AS INTEGER)""", [status_code, ])
        
        elif ken_code == "0" and city_code != "0" and status_code == "0": 
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
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [city_code, ])
        
        elif ken_code == "0" and city_code != "0" and status_code != "0": 
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
                WHERE SUB1.city_code=%s AND SUB1.status_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [city_code, status_code, ])
        
        elif ken_code != "0" and city_code == "0" and status_code == "0": 
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
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [ken_code, ])
        
        elif ken_code != "0" and city_code == "0" and status_code != "0": 
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
                WHERE SUB1.ken_code=%s AND SUB1.status_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [ken_code, status_code, ])
        
        elif ken_code != "0" and city_code != "0" and status_code == "0": 
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
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [ken_code, city_code, ])
        
        elif ken_code != "0" and city_code != "0" and status_code != "0": 
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
                WHERE SUB1.ken_code=%s AND SUB1.city_code=%s AND SUB1.status_code=%s 
                ORDER BY CAST(SUB1.trigger_id AS INTEGER)""", [ken_code, city_code, status_code, ])
                    
        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900CI.ken_city_status_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900CI/index.html')
        context = {
            'ken_code': ken_code, 
            'city_code': city_code, 
            'status_code': status_code, 
            'ken_list': ken_list, 
            'city_list': city_list, 
            'trigger_list': trigger_list, 
        }
        print_log('[INFO] P0900CI.ken_city_status_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900CI.ken_city_status_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900CI.ken_city_status_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：repository_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def repository_view(request, repository_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900CI.repository_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900CI.repository_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900CI.repository_view()関数 repository_id = {}'.format(repository_id), 'INFO')
        print_log('[INFO] P0900CI.repository_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900CI.repository_view()関数 STEP 2/3.', 'INFO')
        repository = REPOSITORY.objects.raw("""
        SELECT 
            RE1.REPOSITORY_ID AS REPOSITORY_ID, 
            RE1.SUIGAI_ID AS SUIGAI_ID, 
            RE1.ACTION_CODE AS ACTION_CODE, 
            AC1.ACTION_NAME AS ACTION_NAME, 
            RE1.STATUS_CODE AS STATUS_CODE, 
            ST1.STATUS_NAME AS STATUS_NAME, 
            RE1.CREATED_AT AS CREATED_AT, 
            RE1.UPDATED_AT AS UPDATED_AT, 
            RE1.INPUT_FILE_PATH AS INPUT_FILE_PATH 
        FROM REPOSITORY RE1 
        LEFT JOIN ACTION AC1 ON RE1.ACTION_CODE=AC1.ACTION_CODE 
        LEFT JOIN STATUS ST1 ON RE1.STATUS_CODE=ST1.STATUS_CODE 
        WHERE REPOSITORY_ID=%s""", [repository_id,])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900CI.repository_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900CI/repository.html')
        context = {
            'repository': repository, 
        }
        print_log('[INFO] P0900CI.repository_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900CI.repository_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900CI.repository_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：trigger_view
###############################################################################
@login_required(None, login_url='/P0100Login/')
def trigger_view(request, trigger_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900CI.trigger_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900CI.trigger_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900CI.trigger_view()関数 trigger_id = {}'.format(trigger_id), 'INFO')
        print_log('[INFO] P0900CI.trigger_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0900CI.trigger_view()関数 STEP 2/3.', 'INFO')
        trigger = TRIGGER.objects.raw("""
        SELECT 
            TR1.trigger_id AS trigger_id, 
            TR1.suigai_id AS suigai_id, 
            SG1.suigai_name AS suigai_name, 
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
        LEFT JOIN ACTION AC1 ON TR1.action_code=AC1.action_code 
        LEFT JOIN STATUS ST1 ON TR1.status_code=ST1.status_code 
        LEFT JOIN REPOSITORY RE1 ON TR1.repository_id=RE1.repository_id 
        WHERE trigger_id=%s""", [trigger_id,])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900CI.trigger_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0900CI/trigger.html')
        context = {
            'trigger': trigger, 
        }
        print_log('[INFO] P0900CI.trigger_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900CI.trigger_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900CI.trigger_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：download_file_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def download_file_view(request, repository_id):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0900CI.download_file_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0900CI.download_file_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0900CI.download_file_view()関数 STEP 1/1.', 'INFO')
        
        result_file_path = 'static/ippan_chosa_result2.xlsx'
        wb = openpyxl.load_workbook(result_file_path)
        
        #######################################################################
        ### レスポンスセット処理(0010)
        ### コンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0900CI.download_file_view()関数が正常終了しました。', 'INFO')
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa_result2.xlsx"'
        return response
        
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0900CI.download_file_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0900CI.download_file_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
