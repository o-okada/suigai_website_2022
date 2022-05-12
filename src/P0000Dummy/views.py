#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0000Dummy/views.py
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
        print_log('[INFO] P0000Dummy.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0000Dummy.index_view()関数 request = {}'.format(request.method), 'INFO')
        
        #######################################################################
        ### レスポンスセット処理
        ### （１）テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
        #######################################################################
        template = loader.get_template('P0000Dummy/index.html')
        context = {}
        print_log('[INFO] P0000Dummy.index_view()関数が正常終了しました。', 'INFO')
        return HttpResponse(template.render(context, request))

    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0000Dummy.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0000Dummy.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
        