#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P9100Transact/views.py
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import datetime
import sys
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic.base import TemplateView
from django import forms
from django.forms import formset_factory

from .forms import ChoiceForm
from .forms import ScheduleForm

from P0000Common.models import BUILDING                ### 01: 建物区分
from P0000Common.models import KEN                     ### 02: 都道府県
from P0000Common.models import CITY                    ### 03: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 04: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 05: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 06: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 07: 河川（河川・海岸）
from P0000Common.models import KASEN_TYPE              ### 08: 河川種別（河川・海岸種別）
from P0000Common.models import CAUSE                   ### 09: 水害原因
from P0000Common.models import UNDERGROUND             ### 10: 地上地下区分
from P0000Common.models import USAGE                   ### 11: 地下空間の利用形態
from P0000Common.models import FLOOD_SEDIMENT          ### 12: 浸水土砂区分
from P0000Common.models import GRADIENT                ### 13: 地盤勾配区分
from P0000Common.models import INDUSTRY                ### 14: 産業分類
from P0000Common.models import HOUSE_ASSET             ### 15: 県別家屋評価額
from P0000Common.models import HOUSE_DAMAGE            ### 16: 家屋被害率
from P0000Common.models import HOUSEHOLD_DAMAGE        ### 17: 家庭用品自動車以外被害率
from P0000Common.models import CAR_DAMAGE              ### 18: 家庭用品自動車被害率
from P0000Common.models import HOUSE_COST              ### 19: 家庭応急対策費
from P0000Common.models import OFFICE_ASSET            ### 20: 産業分類別資産額
from P0000Common.models import OFFICE_DAMAGE           ### 21: 事業所被害率
from P0000Common.models import OFFICE_COST             ### 22: 事業所営業停止損失
from P0000Common.models import FARMER_FISHER_DAMAGE    ### 23: 農漁家被害率
from P0000Common.models import WEATHER                 ### 24: 異常気象（ほぼ、水害）
from P0000Common.models import AREA                    ### 25: 区域
from P0000Common.models import IPPAN                   ### 26: 一般資産調査票
from P0000Common.models import RESTORATION             ### 27: 復旧事業工種
from P0000Common.models import KOKYO                   ### 28: 公共土木調査票
from P0000Common.models import KOEKI                   ### 29: 公益事業調査票
from P0000Common.models import TRANSACT                ### 40: 

from P0000Common.common_function import print_log

###############################################################################
### 関数名：index_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def index(request):
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P9100Transact.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P9100Transact.index_view()関数 request = {}'.format(request.method), 'INFO')
        
        if request.method == 'POST':
            ###################################################################
            ### FORMSETセット処理
            ### （１）フォームに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm)
            ScheduleFormSet = formset_factory(ScheduleForm)
            choice_formset = ChoiceFormSet(request.POST, prefix='choice')
            schedule_formset = ScheduleFormSet(request.POST, prefix='schedule')
            if form.is_valid():
                return HttpResponseRedirect('P9100Transact/success.html')
            else:
                pass

        else:
            ###################################################################
            ### DBアクセス処理
            ### （１）DBにアクセスして、データを取得する。
            ###################################################################
            ken_list = KEN.objects.raw("""
                SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
                """, [])
            transact_list = TRANSACT.objects.raw("""
                SELECT 
                    TR1.TRANSACT_ID AS TRANSACT_ID, 
                    TR1.DOWNLOAD_DATE AS DOWNLOAD_DATE, 
                    TR1.UPLOAD_DATE AS UPLOAD_DATE, 
                    TR1.TRANSACT_DATE AS TRANSACT_DATE, 
                    TR1.SCHEDULE_DATE AS SCHEDULE_DATE, 
                    TR1.DOWNLOAD_USER_ID AS DOWNLOAD_USER_ID, 
                    TR1.UPLOAD_USER_ID AS UPLOAD_USER_ID, 
                    TR1.TRANSACT_USER_ID AS TRANSACT_USER_ID, 
                    TR1.KEN_CODE AS KEN_CODE, 
                    KE1.KEN_NAME AS KEN_NAME, 
                    TR1.CITY_CODE AS CITY_CODE, 
                    CI1.CITY_NAME AS CITY_NAME, 
                    TR1.APPROVE_DISAPPROVE_UNDETERMIN_CODE AS APPROVE_DISAPPROVE_UNDETERMIN_CODE, 
                    TR1.IPPAN_KOKYO_KOEKI_CODE AS IPPAN_KOKYO_KOEKI_CODE, 
                    IKK1.IPPAN_KOKYO_KOEKI_NAME AS IPPAN_KOKYO_KOEKI_NAME, 
                    TR1.IPPAN_KOKYO_KOEKI_ID AS IPPAN_KOKYO_KOEKI_ID, 
                    TR1.COMMENT AS COMMENT 
                FROM P0000COMMON_TRANSACT AS TR1 
                    LEFT OUTER JOIN P0000COMMON_KEN AS KE1 ON (TR1.KEN_CODE=KE1.KEN_CODE) 
                    LEFT OUTER JOIN P0000COMMON_CITY AS CI1 ON (TR1.CITY_CODE=CI1.CITY_CODE) 
                    LEFT OUTER JOIN P0000COMMON_IPPAN_KOKYO_KOEKI AS IKK1 ON (TR1.IPPAN_KOKYO_KOEKI_CODE=IKK1.IPPAN_KOKYO_KOEKI_CODE) 
                ORDER BY CAST(TR1.TRANSACT_ID AS INTEGER) 
                """, [])
            
            ###################################################################
            ### FORMSETセット処理
            ### （１）choice_formsetのchoice_data用に辞書形式のリストを計算してローカル変数にセットする。
            ### （２）ChoiceFormSetフォームセットに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm, extra=5)
            
            ### choice_data = {
            ###     'choice-TOTAL_FORMS': '1',
            ###     'choice-INITIAL_FORMS': '0',
            ###     'choice-0-upload_date_hidden': '承認時コメント',
            ###     'choice-0-ken_code_hidden': '承認時コメント',
            ###     'choice-0-city_code_hidden': '承認時コメント',
            ###     'choice-0-ippan_kokyo_koeki_code_hidden': '承認時コメント',
            ###     'choice-0-choice_hidden': '1',
            ### }
            
            choice_list = []
            choice_list.append(['choice-TOTAL_FORMS', str(len(transact_list))])
            choice_list.append(['choice-INITIAL_FORMS', '0'])
            for i, transact in enumerate(transact_list):
                choice_list.append(['choice-{}-upload_date_hidden'.format(i), transact.upload_date])
                choice_list.append(['choice-{}-ken_code_hidden'.format(i), transact.ken_code])
                choice_list.append(['choice-{}-ken_name_hidden'.format(i), transact.ken_name])
                choice_list.append(['choice-{}-city_code_hidden'.format(i), transact.city_code])
                choice_list.append(['choice-{}-city_name_hidden'.format(i), transact.city_name])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_code_hidden'.format(i), transact.ippan_kokyo_koeki_code])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_name_hidden'.format(i), transact.ippan_kokyo_koeki_name])
                choice_list.append(['choice-{}-choice_hidden'.format(i), ''])
                
            choice_data = dict(choice_list)
            choice_formset = ChoiceFormSet(prefix='choice', data=choice_data)
            
            ###################################################################
            ### FORMSETセット処理
            ### （１）schedule_formsetのschedule_data用に現在の年、月、日、時、分を計算してローカル変数にセットする。
            ### （２）datetime.datetime.now()関数のデフォルトがUTCのため、タイムゾーンのJSTを計算してローカル変数にセットする。
            ### （３）ScheduleFormSetフォームセットに値をセットする。
            ###################################################################
            JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')
            current_now = datetime.datetime.now(JST)
            current_year = str(int(current_now.strftime("%Y")))
            current_month = str(int(current_now.strftime("%m")))
            current_day = str(int(current_now.strftime("%d")))
            current_hour = str(int(current_now.strftime("%H")))
            current_minute = str(int(current_now.strftime("%M")))

            ScheduleFormSet = formset_factory(ScheduleForm, extra=1)

            schedule_data = {
                'schedule-TOTAL_FORMS': '1',
                'schedule-INITIAL_FORMS': '0',
                'schedule-0-year_hidden': current_year,
                'schedule-0-month_hidden': current_month,
                'schedule-0-day_hidden': current_day,
                'schedule-0-hour_hidden': current_hour,
                'schedule-0-minute_hidden': current_minute,
                'schedule-0-comment_hidden': '承認時コメント承認時コメント',
                'schedule-0-choice_hidden': '1',
            }
            
            schedule_formset = ScheduleFormSet(prefix='schedule', data=schedule_data)
            
            ###################################################################
            ### レスポンスセット処理
            ### （１）context用に今年と来年の年を計算してローカル変数にセットする。
            ### （２）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            current_now = datetime.datetime.now()
            current_date = current_now.date()
            current_year = current_date.strftime("%Y")
            next_year = str(int(current_year) + 1)
            
            template = loader.get_template('P9100Transact/index.html')
            context = {
                'ken_list': ken_list,
                'choice_formset': choice_formset,
                'schedule_formset': schedule_formset,
                'year_list': [current_year, next_year],
                'month_list': [x for x in range(1, 13)],
                'day_list': [x for x in range(1, 32)],
                'hour_list': [x for x in range(0, 24)],
                'minute_list': [x for x in range(0, 60)],
            }
            print_log('[INFO] P9100Transact.index_view()関数が正常終了しました。', 'INFO')
            return HttpResponse(template.render(context, request))
            
    except:    
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P9100Transact.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P9100Transact.index_viwe()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：ken_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def ken(request, ken_code):
def ken_view(request, ken_code):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P9100Transact.ken_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P9100Transact.ken_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P9100Transact.ken_view()関数 ken_code = {}'.format(ken_code), 'INFO')

        if request.method == 'POST':
            ###################################################################
            ### FORMSETセット処理
            ### （１）フォームに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm)
            ScheduleFormSet = formset_factory(ScheduleForm)
            choice_formset = ChoiceFormSet(request.POST, prefix='choice')
            schedule_formset = ScheduleFormSet(request.POST, prefix='schedule')
            if form.is_valid():
                return HttpResponseRedirect('P9100Transact/success.html')
            else:
                pass

        else:
            ###################################################################
            ### DBアクセス処理
            ### （１）DBにアクセスして、データを取得する。
            ###################################################################
            ken_list = KEN.objects.raw(""" 
                SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
                """, [])
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
            transact_list = TRANSACT.objects.raw("""
                SELECT 
                    TR1.TRANSACT_ID AS TRANSACT_ID, 
                    TR1.DOWNLOAD_DATE AS DOWNLOAD_DATE, 
                    TR1.UPLOAD_DATE AS UPLOAD_DATE, 
                    TR1.TRANSACT_DATE AS TRANSACT_DATE, 
                    TR1.SCHEDULE_DATE AS SCHEDULE_DATE, 
                    TR1.DOWNLOAD_USER_ID AS DOWNLOAD_USER_ID, 
                    TR1.UPLOAD_USER_ID AS UPLOAD_USER_ID, 
                    TR1.TRANSACT_USER_ID AS TRANSACT_USER_ID, 
                    TR1.KEN_CODE AS KEN_CODE, 
                    KE1.KEN_NAME AS KEN_NAME, 
                    TR1.CITY_CODE AS CITY_CODE, 
                    CI1.CITY_NAME AS CITY_NAME, 
                    TR1.APPROVE_DISAPPROVE_UNDETERMIN_CODE AS APPROVE_DISAPPROVE_UNDETERMIN_CODE, 
                    TR1.IPPAN_KOKYO_KOEKI_CODE AS IPPAN_KOKYO_KOEKI_CODE, 
                    IKK1.IPPAN_KOKYO_KOEKI_NAME AS IPPAN_KOKYO_KOEKI_NAME, 
                    TR1.IPPAN_KOKYO_KOEKI_ID AS IPPAN_KOKYO_KOEKI_ID, 
                    TR1.COMMENT AS COMMENT 
                FROM P0000COMMON_TRANSACT AS TR1 
                    LEFT OUTER JOIN P0000COMMON_KEN AS KE1 ON (TR1.KEN_CODE=KE1.KEN_CODE) 
                    LEFT OUTER JOIN P0000COMMON_CITY AS CI1 ON (TR1.CITY_CODE=CI1.CITY_CODE) 
                    LEFT OUTER JOIN P0000COMMON_IPPAN_KOKYO_KOEKI AS IKK1 ON (TR1.IPPAN_KOKYO_KOEKI_CODE=IKK1.IPPAN_KOKYO_KOEKI_CODE) 
                WHERE TR1.KEN_CODE=%s 
                ORDER BY CAST(TR1.TRANSACT_ID AS INTEGER) 
                """, [ken_code,])

            ###################################################################
            ### FORMSETセット処理
            ### （１）choice_formsetのchoice_data用に辞書形式のリストを計算してローカル変数にセットする。
            ### （２）ChoiceFormSetフォームセットに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm, extra=5)

            choice_list = []
            choice_list.append(['choice-TOTAL_FORMS', str(len(transact_list))])
            choice_list.append(['choice-INITIAL_FORMS', '0'])
            for i, transact in enumerate(transact_list):
                choice_list.append(['choice-{}-upload_date_hidden'.format(i), transact.upload_date])
                choice_list.append(['choice-{}-ken_code_hidden'.format(i), transact.ken_code])
                choice_list.append(['choice-{}-ken_name_hidden'.format(i), transact.ken_name])
                choice_list.append(['choice-{}-city_code_hidden'.format(i), transact.city_code])
                choice_list.append(['choice-{}-city_name_hidden'.format(i), transact.city_name])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_code_hidden'.format(i), transact.ippan_kokyo_koeki_code])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_name_hidden'.format(i), transact.ippan_kokyo_koeki_name])
                choice_list.append(['choice-{}-choice_hidden'.format(i), ''])
                
            choice_data = dict(choice_list)
            choice_formset = ChoiceFormSet(prefix='choice', data=choice_data)

            ###################################################################
            ### FORMSETセット処理
            ### （１）schedule_formsetのschedule_data用に現在の年、月、日、時、分を計算してローカル変数にセットする。
            ### （２）datetime.datetime.now()関数のデフォルトがUTCのため、タイムゾーンのJSTを計算してローカル変数にセットする。
            ### （３）ScheduleFormSetフォームセットに値をセットする。
            ###################################################################
            JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')
            current_now = datetime.datetime.now(JST)
            current_year = str(int(current_now.strftime("%Y")))
            current_month = str(int(current_now.strftime("%m")))
            current_day = str(int(current_now.strftime("%d")))
            current_hour = str(int(current_now.strftime("%H")))
            current_minute = str(int(current_now.strftime("%M")))

            ScheduleFormSet = formset_factory(ScheduleForm, extra=1)
            
            schedule_data = {
                'schedule-TOTAL_FORMS': '1',
                'schedule-INITIAL_FORMS': '0',
                'schedule-0-year_hidden': current_year,
                'schedule-0-month_hidden': current_month,
                'schedule-0-day_hidden': current_day,
                'schedule-0-hour_hidden': current_hour,
                'schedule-0-minute_hidden': current_minute,
                'schedule-0-comment_hidden': '承認時コメント承認時コメント',
                'schedule-0-choice_hidden': '1',
            }
            
            schedule_formset = ScheduleFormSet(prefix='schedule', data=schedule_data)

            ###################################################################
            ### レスポンスセット処理
            ### （１）context用に今年と来年の年を計算してローカル変数にセットする。
            ### （２）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            current_now = datetime.datetime.now()
            current_date = current_now.date()
            current_year = current_date.strftime("%Y")
            next_year = str(int(current_year) + 1)
        
            template = loader.get_template('P9100Transact/index.html')
            context = {
                'ken_list': ken_list,
                'city_list': city_list,
                'ken_code': ken_code,
                'choice_formset': choice_formset,
                'schedule_formset': schedule_formset,
                'year_list': [current_year, next_year],
                'month_list': [x for x in range(1, 13)],
                'day_list': [x for x in range(1, 32)],
                'hour_list': [x for x in range(0, 24)],
                'minute_list': [x for x in range(0, 60)],
            }
            print_log('[INFO] P9100Transact.ken_view()関数が正常終了しました。', 'INFO')
            return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P9100Transact.ken_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P9100Transact.ken_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

###############################################################################
### 関数名：city_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
### def city(request, ken_code, city_code):
def city_view(request, ken_code, city_code):
    try:
        #######################################################################
        ### 引数チェック処理
        ### （１）ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P9100Transact.city_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P9100Transact.city_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P9100Transact.city_view()関数 ken_code = {}'.format(ken_code), 'INFO')
        print_log('[INFO] P9100Transact.city_view()関数 city_code = {}'.format(city_code), 'INFO')

        if request.method == 'POST':
            ###################################################################
            ### FORMSETセット処理
            ### （１）フォームに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm)
            ScheduleFormSet = formset_factory(ScheduleForm)
            choice_formset = ChoiceFormSet(request.POST, prefix='choice')
            schedule_formset = ScheduleFormSet(request.POST, prefix='schedule')
            if form.is_valid():
                return HttpResponseRedirect('P9100Transact/success.html')
            else:
                pass

        else:
            ###################################################################
            ### DBアクセス処理
            ### （１）DBにアクセスして、データを取得する。
            ###################################################################
            ken_list = KEN.objects.raw(""" 
                SELECT * FROM P0000COMMON_KEN ORDER BY CAST(KEN_CODE AS INTEGER)
                """, [])
            city_list = CITY.objects.raw(""" 
                SELECT * FROM P0000COMMON_CITY WHERE KEN_CODE=%s ORDER BY CAST(CITY_CODE AS INTEGER)
                """, [ken_code,])
            ### transact_list = TRANSACT.objects.raw(""" 
            ###     SELECT * FROM P0000COMMON_TRANSACT WHERE KEN_CODE=%s AND CITY_CODE=%s ORDER BY CAST(TRANSACT_ID AS INTEGER)
            ###     """, [ken_code, city_code, ])
            transact_list = TRANSACT.objects.raw("""
                SELECT 
                    TR1.TRANSACT_ID AS TRANSACT_ID, 
                    TR1.DOWNLOAD_DATE AS DOWNLOAD_DATE, 
                    TR1.UPLOAD_DATE AS UPLOAD_DATE, 
                    TR1.TRANSACT_DATE AS TRANSACT_DATE, 
                    TR1.SCHEDULE_DATE AS SCHEDULE_DATE, 
                    TR1.DOWNLOAD_USER_ID AS DOWNLOAD_USER_ID, 
                    TR1.UPLOAD_USER_ID AS UPLOAD_USER_ID, 
                    TR1.TRANSACT_USER_ID AS TRANSACT_USER_ID, 
                    TR1.KEN_CODE AS KEN_CODE, 
                    KE1.KEN_NAME AS KEN_NAME, 
                    TR1.CITY_CODE AS CITY_CODE, 
                    CI1.CITY_NAME AS CITY_NAME, 
                    TR1.APPROVE_DISAPPROVE_UNDETERMIN_CODE AS APPROVE_DISAPPROVE_UNDETERMIN_CODE, 
                    TR1.IPPAN_KOKYO_KOEKI_CODE AS IPPAN_KOKYO_KOEKI_CODE, 
                    IKK1.IPPAN_KOKYO_KOEKI_NAME AS IPPAN_KOKYO_KOEKI_NAME, 
                    TR1.IPPAN_KOKYO_KOEKI_ID AS IPPAN_KOKYO_KOEKI_ID, 
                    TR1.COMMENT AS COMMENT 
                FROM P0000COMMON_TRANSACT AS TR1 
                    LEFT OUTER JOIN P0000COMMON_KEN AS KE1 ON (TR1.KEN_CODE=KE1.KEN_CODE) 
                    LEFT OUTER JOIN P0000COMMON_CITY AS CI1 ON (TR1.CITY_CODE=CI1.CITY_CODE) 
                    LEFT OUTER JOIN P0000COMMON_IPPAN_KOKYO_KOEKI AS IKK1 ON (TR1.IPPAN_KOKYO_KOEKI_CODE=IKK1.IPPAN_KOKYO_KOEKI_CODE) 
                WHERE TR1.KEN_CODE=%s AND TR1.CITY_CODE=%s 
                ORDER BY CAST(TR1.TRANSACT_ID AS INTEGER) 
                """, [ken_code, city_code, ])

            ###################################################################
            ### FORMSETセット処理
            ### （１）choice_formsetのchoice_data用に辞書形式のリストを計算してローカル変数にセットする。
            ### （２）ChoiceFormSetフォームセットに値をセットする。
            ###################################################################
            ChoiceFormSet = formset_factory(ChoiceForm, extra=5)

            choice_list = []
            choice_list.append(['choice-TOTAL_FORMS', str(len(transact_list))])
            choice_list.append(['choice-INITIAL_FORMS', '0'])
            for i, transact in enumerate(transact_list):
                choice_list.append(['choice-{}-upload_date_hidden'.format(i), transact.upload_date])
                choice_list.append(['choice-{}-ken_code_hidden'.format(i), transact.ken_code])
                choice_list.append(['choice-{}-ken_name_hidden'.format(i), transact.ken_name])
                choice_list.append(['choice-{}-city_code_hidden'.format(i), transact.city_code])
                choice_list.append(['choice-{}-city_name_hidden'.format(i), transact.city_name])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_code_hidden'.format(i), transact.ippan_kokyo_koeki_code])
                choice_list.append(['choice-{}-ippan_kokyo_koeki_name_hidden'.format(i), transact.ippan_kokyo_koeki_name])
                choice_list.append(['choice-{}-choice_hidden'.format(i), ''])
                
            choice_data = dict(choice_list)
            choice_formset = ChoiceFormSet(prefix='choice', data=choice_data)

            ###################################################################
            ### FORMSETセット処理
            ### （１）schedule_formsetのschedule_data用に現在の年、月、日、時、分を計算してローカル変数にセットする。
            ### （２）datetime.datetime.now()関数のデフォルトがUTCのため、タイムゾーンのJSTを計算してローカル変数にセットする。
            ### （３）ScheduleFormSetフォームセットに値をセットする。
            ###################################################################
            JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')
            current_now = datetime.datetime.now(JST)
            current_year = str(int(current_now.strftime("%Y")))
            current_month = str(int(current_now.strftime("%m")))
            current_day = str(int(current_now.strftime("%d")))
            current_hour = str(int(current_now.strftime("%H")))
            current_minute = str(int(current_now.strftime("%M")))

            ScheduleFormSet = formset_factory(ScheduleForm, extra=1)
            
            schedule_data = {
                'schedule-TOTAL_FORMS': '1',
                'schedule-INITIAL_FORMS': '0',
                'schedule-0-year_hidden': current_year,
                'schedule-0-month_hidden': current_month,
                'schedule-0-day_hidden': current_day,
                'schedule-0-hour_hidden': current_hour,
                'schedule-0-minute_hidden': current_minute,
                'schedule-0-comment_hidden': '承認時コメント承認時コメント',
                'schedule-0-choice_hidden': '1',
            }
            
            schedule_formset = ScheduleFormSet(prefix='schedule', data=schedule_data)
        
            ###################################################################
            ### レスポンスセット処理
            ### （１）context用に今年と来年の年を計算してローカル変数にセットする。
            ### （２）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            current_now = datetime.datetime.now()
            current_date = current_now.date()
            current_year = current_date.strftime("%Y")
            next_year = str(int(current_year) + 1)
        
            template = loader.get_template('P9100Transact/index.html')
            context = {
                'ken_list': ken_list,
                'city_list': city_list,
                'ken_code': ken_code,
                'city_code': city_code,
                'choice_formset': choice_formset,
                'schedule_formset': schedule_formset,
                'year_list': [current_year, next_year],
                'month_list': [x for x in range(1, 13)],
                'day_list': [x for x in range(1, 32)],
                'hour_list': [x for x in range(0, 24)],
                'minute_list': [x for x in range(0, 60)],
            }
            print_log('[INFO] P9100Transact.city_view()関数が正常終了しました。', 'INFO')
            return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P9100Transact.city_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P9100Transact.city_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
        