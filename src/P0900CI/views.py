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

from P0000Common.models import BUILDING                ### 1010: 建物区分
from P0000Common.models import KEN                     ### 1020: 都道府県
from P0000Common.models import CITY                    ### 1030: 市区町村
from P0000Common.models import KASEN_KAIGAN            ### 1040: 水害発生地点工種（河川海岸区分）
from P0000Common.models import SUIKEI                  ### 1050: 水系（水系・沿岸）
from P0000Common.models import SUIKEI_TYPE             ### 1060: 水系種別（水系・沿岸種別）
from P0000Common.models import KASEN                   ### 1070: 河川（河川・海岸）
from P0000Common.models import KASEN_TYPE              ### 1080: 河川種別（河川・海岸種別）
from P0000Common.models import CAUSE                   ### 1090: 水害原因
from P0000Common.models import UNDERGROUND             ### 1100: 地上地下区分
from P0000Common.models import USAGE                   ### 1110: 地下空間の利用形態
from P0000Common.models import FLOOD_SEDIMENT          ### 1120: 浸水土砂区分
from P0000Common.models import GRADIENT                ### 1130: 地盤勾配区分
from P0000Common.models import INDUSTRY                ### 1140: 産業分類

from P0000Common.models import HOUSE_ASSET             ### 2010: 家屋評価額
from P0000Common.models import HOUSE_RATE              ### 2020: 家屋被害率
from P0000Common.models import HOUSE_ALT               ### 2030: 家庭応急対策費_代替活動費
from P0000Common.models import HOUSE_CLEAN             ### 2040: 家庭応急対策費_清掃日数

from P0000Common.models import HOUSEHOLD_ASSET         ### 3010: 家庭用品自動車以外所有額
from P0000Common.models import HOUSEHOLD_RATE          ### 3020: 家庭用品自動車以外被害率

from P0000Common.models import CAR_ASSET               ### 4010: 家庭用品自動車所有額
from P0000Common.models import CAR_RATE                ### 4020: 家庭用品自動車被害率

from P0000Common.models import OFFICE_ASSET            ### 5010: 事業所資産額
from P0000Common.models import OFFICE_RATE             ### 5020: 事業所被害率
from P0000Common.models import OFFICE_SUSPEND          ### 5030: 事業所営業停止日数
from P0000Common.models import OFFICE_STAGNATE         ### 5040: 事業所営業停滞日数
from P0000Common.models import OFFICE_ALT              ### 5050: 事業所応急対策費_代替活動費

from P0000Common.models import FARMER_FISHER_ASSET     ### 6010: 農漁家資産額
from P0000Common.models import FARMER_FISHER_RATE      ### 6020: 農漁家被害率

from P0000Common.models import AREA                    ### 7010: 一般資産入力データ_水害区域
from P0000Common.models import WEATHER                 ### 7020: 一般資産入力データ_異常気象
from P0000Common.models import SUIGAI                  ### 7030: 一般資産入力データ_ヘッダ部分
from P0000Common.models import IPPAN                   ### 7040: 一般資産入力データ_一覧表部分
from P0000Common.models import IPPAN_VIEW              ### 7050: 一般資産ビューデータ_一覧表部分

from P0000Common.models import IPPAN_SUMMARY           ### 8010: 一般資産集計データ

from P0000Common.models import IPPAN_REPOSITORY        ### 9000: 一般資産集計データ

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
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 request = {}'.format(request.method), 'INFO')
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 1/3.', 'INFO')
        
        #######################################################################
        ### DBアクセス処理(0010)
        ### DBにアクセスして、データを取得する。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 2/3.', 'INFO')

        #######################################################################
        ### レスポンスセット処理(0020)
        ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        print_log('[INFO] P0400OnlineDisplay.index_view()関数 STEP 3/3.', 'INFO')
        template = loader.get_template('P0400OnlineDisplay/index.html')
        context = {
        }
        print_log('[INFO] P0400OnlineDisplay.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0400OnlineDisplay.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')

