#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P9200Lock/views.py
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import sys
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic.base import TemplateView

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
from P0000Common.models import TRANSACT

from P0000Common.common import print_log

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
        print_log('[INFO] P9200Lock.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P9200Lock.index_view()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P9200Lock/index.html')
        ### template = loader.get_template('P9200Lock/P9200LockTemplate.html')
        context = {}
        print_log('[INFO] P9200Lock.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))
    
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P9200Lock.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P9200Lock.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
        