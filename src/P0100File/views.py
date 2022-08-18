#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0100File/views.py
### ファイル管理
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
from P0000Common.models import SUIGAI                  ### 7020: 入力データ_一般資産調査票_調査員用_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7030: 入力データ_一般資産調査票_調査員用_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7040: ビューデータ_一般資産調査票_調査員用_一覧表部分
from P0000Common.models import CHITAN_FILE             ### 7050: 入力データ_公共土木施設調査票_地方単独事業_ファイル部分
from P0000Common.models import CHITAN                  ### 7060: 入力データ_公共土木施設調査票_地方単独事業_一覧表部分
from P0000Common.models import HOJO_FILE               ### 7070: 入力データ_公共土木施設調査票_補助事業_ファイル部分
from P0000Common.models import HOJO                    ### 7080: 入力データ_公共土木施設調査票_補助事業_一覧表部分
from P0000Common.models import KOEKI_FILE              ### 7090: 入力データ_公益事業等調査票_ファイル部分
from P0000Common.models import KOEKI                   ### 7100: 入力データ_公益事業等調査票_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8000: 集計データ_一般資産調査票_調査員用_一覧表部分

from P0000Common.models import ACTION                  ### 10000: アクション
from P0000Common.models import STATUS                  ### 10010: 状態
from P0000Common.models import TRIGGER                 ### 10020: トリガーメッセージ

from P0000Common.common import get_all_log
from P0000Common.common import get_debug_log
from P0000Common.common import get_error_log
from P0000Common.common import get_info_log
from P0000Common.common import get_warn_log
from P0000Common.common import print_log
from P0000Common.common import reset_log

###############################################################################
### 関数名：index_view
### urlpattern：path('', views.index_view, name='index_view')
### template：P0100File/type.html
### template：P0100File/error.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0100File.index_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0100File.index_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0100File.index_view()関数 STEP 1/2.', 'DEBUG')

        #######################################################################
        ### レスポンスセット処理(0010)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0100File.index_view()関数 STEP 2/2.', 'DEBUG')
        template = loader.get_template('P0100File/index.html')
        context = {
            'all_log': get_all_log(), 
            'info_log': get_info_log(), 
            'debug_log': get_debug_log(), 
            'warn_log': get_warn_log(), 
            'error_log': get_error_log(), 
        }
        print_log('[INFO] P0100File.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0100File.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0100File.index_view()関数でエラーが発生しました。', 'ERROR')
        template = loader.get_template('P0100File/error.html')
        context = {
            'all_log': get_all_log(), 
            'info_log': get_info_log(), 
            'debug_log': get_debug_log(), 
            'warn_log': get_warn_log(), 
            'error_log': get_error_log(), 
        }
        print_log('[ERROR] P0100File.index_view()関数が異常終了しました。', 'ERROR')
        ### return render(request, 'error.html')
        return HttpResponse(template.render(context, request))

###############################################################################
### 関数名：type_view
### urlpattern：path('type/<slug:type_code>/', views.type_view, name='type_view')
### template：P0100File/type.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def type_view(request, type_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0100File.type_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0100File.type_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0100File.type_view()関数 type_code = {}'.format(type_code), 'DEBUG')
        print_log('[DEBUG] P0100File.type_view()関数 STEP 1/3.', 'DEBUG')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0100File.type_view()関数 STEP 2/3.', 'DEBUG')
        ken_list = KEN.objects.raw("""SELECT * FROM KEN ORDER BY CAST(ken_code AS INTEGER)""", [])
        
        print_log('[DEBUG] P0100File.type_view()関数 STEP 2_1/3.', 'DEBUG')
        suigai_list = []
        for ken in ken_list:
            suigai_list.append(SUIGAI.objects.raw("""
                SELECT 
                    KE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SUB1.suigai_id AS suigai_id, 
                    SUB1.suigai_name AS suigai_name, 
                    SUB1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    AC1.action_name_en AS action_name_en, 
                    SUB1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    SUB1.upload_file_path AS upload_file_path, 
                    SUB1.upload_file_name AS upload_file_name, 
                    SUB1.summary_file_path AS summary_file_path, 
                    SUB1.summary_file_name AS summary_file_name, 
                    TO_CHAR(timezone('JST', SUB1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SUB1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM KEN KE1 
                LEFT JOIN (SELECT * FROM SUIGAI WHERE ken_code=%s AND deleted_at IS NULL ORDER BY suigai_id DESC) SUB1 ON KE1.ken_code=SUB1.ken_code
                LEFT JOIN ACTION AC1 ON SUB1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON SUB1.status_code=ST1.status_code 
                WHERE KE1.ken_code=%s""", [ken.ken_code, ken.ken_code, ]))
            
        print_log('[DEBUG] P0100File.type_view()関数 STEP 2_2/3.', 'DEBUG')
        area_list = []
        for ken in ken_list:
            area_list.append(AREA.objects.raw("""
                SELECT 
                    KE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SUB1.area_id AS area_id, 
                    SUB1.area_name AS area_name, 
                    SUB1.action_code AS action_code, 
                    AC1.action_name AS action_name, 
                    AC1.action_name_en AS action_name_en, 
                    SUB1.status_code AS status_code, 
                    ST1.status_name AS status_name, 
                    SUB1.upload_file_path AS upload_file_path, 
                    SUB1.upload_file_name AS upload_file_name, 
                    TO_CHAR(timezone('JST', SUB1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SUB1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM KEN KE1 
                LEFT JOIN (SELECT * FROM AREA WHERE ken_code=%s AND deleted_at IS NULL ORDER BY area_id DESC) SUB1 ON KE1.ken_code=SUB1.ken_code
                LEFT JOIN ACTION AC1 ON SUB1.action_code=AC1.action_code 
                LEFT JOIN STATUS ST1 ON SUB1.status_code=ST1.status_code 
                WHERE KE1.ken_code=%s""", [ken.ken_code, ken.ken_code, ]))

        print_log('[DEBUG] P0100File.type_view()関数 STEP 2_3/3.', 'DEBUG')
        chitan_file_list = []
        for ken in ken_list:
            chitan_file_list.append(CHITAN_FILE.objects.raw("""
                SELECT 
                    KE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SUB1.chitan_file_id AS chitan_file_id, 
                    SUB1.chitan_file_name AS chitan_file_name, 
                    SUB1.upload_file_path AS upload_file_path, 
                    SUB1.upload_file_name AS upload_file_name, 
                    SUB1.summary_file_path AS summary_file_path, 
                    SUB1.summary_file_name AS summary_file_name, 
                    TO_CHAR(timezone('JST', SUB1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SUB1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM KEN KE1 
                LEFT JOIN (SELECT * FROM CHITAN_FILE WHERE ken_code=%s AND deleted_at IS NULL ORDER BY chitan_file_id DESC) SUB1 ON KE1.ken_code=SUB1.ken_code 
                WHERE KE1.ken_code=%s""", [ken.ken_code, ken.ken_code, ]))

        print_log('[DEBUG] P0100File.type_view()関数 STEP 2_4/3.', 'DEBUG')
        hojo_file_list = []
        for ken in ken_list:
            hojo_file_list.append(HOJO_FILE.objects.raw("""
                SELECT 
                    KE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SUB1.hojo_file_id AS hojo_file_id, 
                    SUB1.hojo_file_name AS hojo_file_name, 
                    SUB1.upload_file_path AS upload_file_path, 
                    SUB1.upload_file_name AS upload_file_name, 
                    SUB1.summary_file_path AS summary_file_path, 
                    SUB1.summary_file_name AS summary_file_name, 
                    TO_CHAR(timezone('JST', SUB1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SUB1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM KEN KE1 
                LEFT JOIN (SELECT * FROM HOJO_FILE WHERE ken_code=%s AND deleted_at IS NULL ORDER BY hojo_file_id DESC) SUB1 ON KE1.ken_code=SUB1.ken_code 
                WHERE KE1.ken_code=%s""", [ken.ken_code, ken.ken_code, ]))

        print_log('[DEBUG] P0100File.type_view()関数 STEP 2_5/3.', 'DEBUG')
        koeki_file_list = []
        for ken in ken_list:
            koeki_file_list.append(KOEKI_FILE.objects.raw("""
                SELECT 
                    KE1.ken_code AS ken_code, 
                    KE1.ken_name AS ken_name, 
                    SUB1.koeki_file_id AS koeki_file_id, 
                    SUB1.koeki_file_name AS koeki_file_name, 
                    SUB1.upload_file_path AS upload_file_path, 
                    SUB1.upload_file_name AS upload_file_name, 
                    SUB1.summary_file_path AS summary_file_path, 
                    SUB1.summary_file_name AS summary_file_name, 
                    TO_CHAR(timezone('JST', SUB1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                    TO_CHAR(timezone('JST', SUB1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
                FROM KEN KE1 
                LEFT JOIN (SELECT * FROM KOEKI_FILE WHERE ken_code=%s AND deleted_at IS NULL ORDER BY koeki_file_id DESC) SUB1 ON KE1.ken_code=SUB1.ken_code 
                WHERE KE1.ken_code=%s""", [ken.ken_code, ken.ken_code, ]))

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0100File.type_view()関数 STEP 3/3.', 'DEBUG')
        template = loader.get_template('P0100File/type.html')
        context = {
            'type_code': type_code, 
            
            'ken_list': ken_list, 
            'suigai_list': suigai_list, 
            'area_list': area_list, 
            'chitan_file_list': chitan_file_list, 
            'hojo_file_list': hojo_file_list, 
            'koeki_file_list': koeki_file_list, 
        }
        print_log('[INFO] P0100File.type_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0100File.type_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0100File.type_view()関数でエラーが発生しました。', 'ERROR')
        template = loader.get_template('P0100File/error.html')
        context = {
            'all_log': get_all_log(), 
            'info_log': get_info_log(), 
            'debug_log': get_debug_log(), 
            'warn_log': get_warn_log(), 
            'error_log': get_error_log(), 
        }
        print_log('[ERROR] P0100File.type_view()関数が異常終了しました。', 'ERROR')
        ### return render(request, 'error.html')
        return HttpResponse(template.render(context, request))

###############################################################################
### 関数名：type_ken_view
### urlpattern：path('type/<slug:type_code>/ken/<slug:ken_code>/', views.type_ken_view, name='type_ken_view')
### template：P0100File/ken.html
### template：P0100File/error.html
###############################################################################
@login_required(None, login_url='/P0100Login/')
def type_ken_view(request, type_code, ken_code):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0100File.type_ken_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0100File.type_ken_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0100File.type_ken_view()関数 type_code = {}'.format(type_code), 'DEBUG')
        print_log('[DEBUG] P0100File.type_ken_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 1/3.', 'DEBUG')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2/3.', 'DEBUG')
        ken_list = KEN.objects.raw("""
            SELECT 
                * 
            FROM KEN 
            WHERE 
                ken_code=%s 
            ORDER BY CAST(ken_code AS INTEGER)""", [ken_code, ])
        
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2_1/3.', 'DEBUG')
        suigai_list = SUIGAI.objects.raw("""
            SELECT 
                SG1.suigai_id AS suigai_id, 
                SG1.suigai_name AS suigai_name, 
                SG1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                SG1.city_code AS city_code, 
                CT1.city_name AS city_name, 
                TO_CHAR(timezone('JST', SG1.begin_date::timestamptz), 'yyyy/mm/dd') AS begin_date, 
                TO_CHAR(timezone('JST', SG1.end_date::timestamptz), 'yyyy/mm/dd') AS end_date, 
                SG1.upload_file_path AS upload_file_path, 
                SG1.upload_file_name AS upload_file_name, 
                SG1.summary_file_path AS summary_file_path, 
                SG1.summary_file_name AS summary_file_name, 
                TO_CHAR(timezone('JST', SG1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                TO_CHAR(timezone('JST', SG1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
            FROM SUIGAI SG1 
            LEFT JOIN KEN KE1 ON SG1.ken_code=KE1.ken_code 
            LEFT JOIN CITY CT1 ON SG1.city_code=CT1.city_code 
            WHERE 
                SG1.ken_code=%s 
            ORDER BY CAST(SG1.city_code AS INTEGER), CAST(SG1.suigai_id AS INTEGER) DESC""", [ken_code, ])
            
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2_2/3.', 'DEBUG')
        area_list = AREA.objects.raw("""
            SELECT 
                AR1.area_id AS area_id, 
                AR1.area_name AS area_name, 
                AR1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                AR1.upload_file_path AS upload_file_path, 
                AR1.upload_file_name AS upload_file_name, 
                TO_CHAR(timezone('JST', AR1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                TO_CHAR(timezone('JST', AR1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
            FROM AREA AR1 
            LEFT JOIN KEN KE1 ON AR1.ken_code=KE1.ken_code 
            WHERE 
                AR1.ken_code=%s 
            ORDER BY CAST(AR1.area_id AS INTEGER) DESC""", [ken_code, ])
        
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2_3/3.', 'DEBUG')
        chitan_file_list = CHITAN_FILE.objects.raw("""
            SELECT 
                CF1.chitan_file_id AS chitan_file_id, 
                CF1.chitan_file_name AS chitan_file_name, 
                CF1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                CF1.upload_file_path AS upload_file_path, 
                CF1.upload_file_name AS upload_file_name, 
                CF1.summary_file_path AS summary_file_path, 
                CF1.summary_file_name AS summary_file_name, 
                TO_CHAR(timezone('JST', CF1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                TO_CHAR(timezone('JST', CF1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
            FROM CHITAN_FILE CF1 
            LEFT JOIN KEN KE1 ON CF1.ken_code=KE1.ken_code 
            WHERE 
                CF1.ken_code=%s 
            ORDER BY CAST(CF1.chitan_file_id AS INTEGER) DESC""", [ken_code, ])

        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2_4/3.', 'DEBUG')
        hojo_file_list = HOJO_FILE.objects.raw("""
            SELECT 
                HF1.hojo_file_id AS hojo_file_id, 
                HF1.hojo_file_name AS hojo_file_name, 
                HF1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                HF1.upload_file_path AS upload_file_path, 
                HF1.upload_file_name AS upload_file_name, 
                HF1.summary_file_path AS summary_file_path, 
                HF1.summary_file_name AS summary_file_name, 
                TO_CHAR(timezone('JST', HF1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                TO_CHAR(timezone('JST', HF1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
            FROM HOJO_FILE HF1 
            LEFT JOIN KEN KE1 ON HF1.ken_code=KE1.ken_code 
            WHERE 
                HF1.ken_code=%s 
            ORDER BY CAST(HF1.hojo_file_id AS INTEGER) DESC""", [ken_code, ])

        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 2_5/3.', 'DEBUG')
        koeki_file_list = KOEKI_FILE.objects.raw("""
            SELECT 
                KF1.koeki_file_id AS koeki_file_id, 
                KF1.koeki_file_name AS koeki_file_name, 
                KF1.ken_code AS ken_code, 
                KE1.ken_name AS ken_name, 
                KF1.upload_file_path AS upload_file_path, 
                KF1.upload_file_name AS upload_file_name, 
                KF1.summary_file_path AS summary_file_path, 
                KF1.summary_file_name AS summary_file_name, 
                TO_CHAR(timezone('JST', KF1.committed_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS committed_at, 
                TO_CHAR(timezone('JST', KF1.deleted_at::timestamptz), 'yyyy/mm/dd HH24:MI') AS deleted_at 
            FROM KOEKI_FILE KF1 
            LEFT JOIN KEN KE1 ON KF1.ken_code=KE1.ken_code 
            WHERE 
                KF1.ken_code=%s 
            ORDER BY CAST(KF1.koeki_file_id AS INTEGER) DESC""", [ken_code, ])

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[DEBUG] P0100File.type_ken_view()関数 STEP 3/3.', 'DEBUG')
        template = loader.get_template('P0100File/ken.html')
        context = {
            'type_code': type_code, 
            'ken_code': ken_code, 
            
            'ken_list': ken_list, 
            'suigai_list': suigai_list, 
            'area_list': area_list, 
            'chitan_file_list': chitan_file_list, 
            'hojo_file_list': hojo_file_list, 
            'koeki_file_list': koeki_file_list, 
        }
        print_log('[INFO] P0100File.type_ken_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log('[ERROR] P0100File.type_ken_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0100File.type_ken_view()関数でエラーが発生しました。', 'ERROR')
        template = loader.get_template('P0100File/error.html')
        context = {
            'all_log': get_all_log(), 
            'info_log': get_info_log(), 
            'debug_log': get_debug_log(), 
            'warn_log': get_warn_log(), 
            'error_log': get_error_log(), 
        }
        print_log('[ERROR] P0100File.type_ken_view()関数が異常終了しました。', 'ERROR')
        ### return render(request, 'error.html')
        return HttpResponse(template.render(context, request))
