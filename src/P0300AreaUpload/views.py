#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0300AreaUpload/views.py
### 水害区域図アップロード
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import os
import sys
from datetime import date, datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db import transaction
from django.db.models import Max
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
### import openpyxl
### from openpyxl.comments import Comment
### from openpyxl.formatting.rule import FormulaRule
### from openpyxl.styles import PatternFill
### from openpyxl.worksheet.datavalidation import DataValidation
### from openpyxl.writer.excel import save_virtual_workbook

from .forms import AreaUploadForm

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
### 関数名：index_view
### urlpattern：path('', views.index_view, name='index_view')
### template：P0300AreaUpload/index.html
### (1)GETの場合、水害区域図アップロード画面を表示する。
### (2)POSTの場合、アップロードされた水害区域図をチェックして、正常ケースの場合、DBに登録する。
### (3)POSTの場合、アップロードされた水害区域図をチェックして、警告ケースの場合、DBに登録する。
###############################################################################
@login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理(0000)
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        reset_log()
        print_log('[INFO] P0300AreaUpload.index_view()関数が開始しました。', 'INFO')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 request = {}'.format(request.method), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 1/8.', 'DEBUG')

        ken_list = KEN.objects.raw("""
            SELECT * FROM KEN ORDER BY CAST(KEN_CODE AS INTEGER)
            """, [])
    
        #######################################################################
        ### 条件分岐処理(0010)
        ### (1)GETの場合、水害区域図アップロード画面を表示して関数を抜ける。
        ### (2)POSTの場合、アップロードされた水害区域図をチェックする。
        ### ※関数の内部のネスト数を浅くするため。
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 2/8.', 'DEBUG')
        if request.method == 'GET':
            form = AreaUploadForm()
            context = {
                'form': form, 
                'ken_list': ken_list, 
            }
            ### return render(request, 'P0300AreaUpload/index.html', {'form': form})
            return render(request, 'P0300AreaUpload/index.html', context)
        
        elif request.method == 'POST':
            form = AreaUploadForm(request.POST, request.FILES)
            
        #######################################################################
        ### フォーム検証処理(0020)
        ### (1)フォームが正しい場合、処理を継続する。
        ### (2)フォームが正しくない場合、ERROR画面を表示して関数を抜ける。
        ### ※関数の内部のネスト数を浅くするため。
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 3/8.', 'DEBUG')
        if form.is_valid():
            pass
        else:
            return HttpResponseRedirect('fail')
    
        #######################################################################
        ### 水害区域図入出力処理(0030)
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 4/8.', 'DEBUG')
        JST = timezone(timedelta(hours=9), 'JST')
        datetime_now_Ym = datetime.now(JST).strftime('%Y%m')
        datetime_now_YmdHMS = datetime.now(JST).strftime('%Y%m%d%H%M%S')
        
        upload_file_object = request.FILES['file']
        upload_file_name, upload_file_ext = os.path.splitext(request.FILES['file'].name)
        upload_file_name = upload_file_name + '_' + datetime_now_YmdHMS
        upload_file_path = 'static/repository/' + datetime_now_Ym + '/' + upload_file_name + '.pdf'
        
        with open(upload_file_path, 'wb+') as destination:
            for chunk in upload_file_object.chunks():
                destination.write(chunk)
        
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 upload_file_object = {}'.format(upload_file_object), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 upload_file_name = {}'.format(upload_file_name), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 upload_file_ext = {}'.format(upload_file_ext), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 upload_file_path = {}'.format(upload_file_path), 'DEBUG')

        #######################################################################
        ### 水害区域図入出力処理(0040)
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 5/8.', 'DEBUG')
        area_id = request.POST.get('area_id')
        area_name = request.POST.get('area_name')
        ken_code = request.POST.get('ken_code')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 area_id = {}'.format(area_id), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 area_name = {}'.format(area_name), 'DEBUG')
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 ken_code = {}'.format(ken_code), 'DEBUG')

        #######################################################################
        ### DBアクセス処理(1000)
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 6/8.', 'DEBUG')
        connection_cursor = connection.cursor()
        try:
            connection_cursor.execute("""BEGIN""", []);
            
            ###################################################################
            ### DBアクセス処理(1010)
            ### 水害区域テーブルにデータを登録する。
            ### TO-DO TODO TO_DO
            ###################################################################
            print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 7/8.', 'DEBUG')
            connection_cursor.execute("""
                DELETE FROM AREA 
                WHERE 
                    area_id=%s -- area_id
                """, [
                    int(area_id), ### area_id
                ])
            
            connection_cursor.execute("""
                INSERT INTO AREA (
                    area_id, area_name, ken_code, committed_at, deleted_at, file_path, file_name, action_code, status_code
                ) VALUES (
                    %s, -- area_id
                    %s, -- area_name
                    %s, -- ken_code
                    CURRENT_TIMESTAMP, -- committed_at
                    %s, -- deleted_at
                    %s, -- upload_file_path
                    %s, -- upload_file_name
                    %s, -- action_code
                    %s  -- status_code
                )""", [
                    int(area_id), ### area_id
                    area_name, ### area_name
                    ken_code, ### ken_code
                    None, ### deleted_at
                    upload_file_path, ### upload_file_path
                    upload_file_name, ### upload_file_name
                    None, ### action_code
                    None, ### status_code
                ])
    
            ### トリガーテーブルにB01水害区域図アップロードトリガーを実行済、成功として登録する。
            connection_cursor.execute("""
                INSERT INTO TRIGGER (
                    trigger_id, suigai_id, action_code, status_code, success_count, failure_count, 
                    published_at, consumed_at, deleted_at, integrity_ok, integrity_ng, ken_code, 
                    city_code, download_file_path, download_file_name, upload_file_path, upload_file_name 
                ) VALUES (
                    (SELECT CASE WHEN (MAX(trigger_id+1)) IS NULL THEN CAST(0 AS INTEGER) ELSE CAST(MAX(trigger_id+1) AS INTEGER) END AS trigger_id FROM TRIGGER), -- trigger_id 
                    %s, -- suigai_id 
                    %s, -- action_code 
                    %s, -- status_code 
                    %s, -- success_count 
                    %s, -- failure_count 
                    CURRENT_TIMESTAMP, -- published_at 
                    CURRENT_TIMESTAMP, -- consumed_at 
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
                    None, ### suigai_id 
                    'B01', ### action_code 
                    'SUCCESS', ### status_code 
                    1, ### success_count
                    0, ### failure_count
                    None, ### deleted_at 
                    '\n'.join(get_info_log()), ### integrity_ok 
                    '\n'.join(get_warn_log()), ### integrity_ng 
                    ken_code, ### ken_code 
                    None, ### city_code 
                    None, ### download_file_path 
                    None, ### download_file_name 
                    upload_file_path, ### upload_file_path 
                    upload_file_name, ### upload_file_name 
                ])
                
            ### トリガーテーブルにB02水害区域図貼付けトリガーを未実行＝次回実行対象として登録する。
            connection_cursor.execute("""
                INSERT INTO TRIGGER (
                    trigger_id, suigai_id, action_code, status_code, success_count, failure_count, 
                    published_at, consumed_at, deleted_at, integrity_ok, integrity_ng, ken_code, 
                    city_code, download_file_path, download_file_name, upload_file_path, upload_file_name 
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
                    None, ### suigai_id 
                    'B02', ### action_code 
                    None, ### status_code 
                    None, ### success_count
                    None, ### failure_count
                    None, ### consumed_at
                    None, ### deleted_at 
                    None, ### integrity_ok 
                    None, ### integrity_ng 
                    ken_code, ### ken_code 
                    None, ### city_code 
                    None, ### download_file_path 
                    None, ### download_file_name 
                    upload_file_path, ### upload_file_path 
                    upload_file_name, ### upload_file_name 
                ])
            connection_cursor.execute("""COMMIT""", []);
        except:
            print_log('[ERROR] P0300AreaUpload.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
            connection_cursor.execute("""ROLLBACK""", [])
        finally:
            connection_cursor.close()
            
        #######################################################################
        ### レスポンスセット処理(1020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        ### ※入力チェックでエラーが発見された場合、
        ### ※ネストを浅くするために、処理対象外の場合、終了させる。
        #######################################################################
        print_log('[DEBUG] P0300AreaUpload.index_view()関数 STEP 8/8.', 'DEBUG')
        template = loader.get_template('P0300AreaUpload/success.html')
        context = {}
        print_log('[INFO] P0300AreaUpload.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    except:
        print_log('[ERROR] P0300AreaUpload.index_view()関数 {}'.format(sys.exc_info()[0]), 'ERROR')
        print_log('[ERROR] P0300AreaUpload.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0300AreaUpload.index_viwe()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
    