#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
### ファイル名：P0100Login/views.py
###############################################################################

###############################################################################
### 処理名：インポート処理
###############################################################################
import sys                                                                     ### sysモジュール
from django.contrib.auth import authenticate                                   ### 認証モジュール
from django.contrib.auth import login                                          ### ログインモジュール
from django.contrib.auth import logout                                         ### ログアウトモジュール
from django.http import Http404                                                ### URL404モジュール
from django.http import HttpResponse                                           ### URLレスポンスモジュール
from django.http import HttpResponseRedirect                                   ### URLリダイレクトモジュール
from django.shortcuts import render                                            ### レンダリングモジュール
from django.template import loader                                             ### テンプレート読み込みモジュール
from django.views import generic                                               ### モジュール
from P0000Common.common import print_log                                       ### ログ出力モジュール

###############################################################################
### 関数名：index_view
###############################################################################
### @login_required(None, login_url='/P0100Login/')
def index_view(request):
    try:
        #######################################################################
        ### 引数チェック処理
        ### ブラウザからのリクエストと引数をチェックする。
        #######################################################################
        print_log('[INFO] ########################################', 'INFO')
        print_log('[INFO] P0100Login.index_view()関数が開始しました。', 'INFO')
        print_log('[INFO] P0100Login.index_view()関数 request = {}'.format(request.method), 'INFO')

        ### ログイン中、ログアウト中にかかわらずに、ログアウトする。
        logout(request)
        
        if request.method == 'GET':
            ###################################################################
            ### レスポンスセット処理
            ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            template = loader.get_template('P0100Login/index.html')
            context = {}
            print_log('[INFO] P0100Login.index_view()関数が正常終了しました。', 'INFO')
            return HttpResponse(template.render(context, request))

        if request.method == 'POST':
            ###################################################################
            ### レスポンスセット処理
            ### テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            print_log('[INFO] P0100Login.index_view()関数 request.POST.username = {}'.format(request.POST['username']), 'INFO')
            print_log('[INFO] P0100Login.index_view()関数 request.POST.password = {}'.format(request.POST['password']), 'INFO')
            print_log('[INFO] P0100Login.index_view()関数 user = {}'.format(user), 'INFO')
                
            ###################################################################
            ### レスポンスセット処理
            ### (1)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ### (2)テンプレートとコンテキストを設定して、レスポンスをブラウザに戻す。
            ###################################################################
            if user is not None:
                ### 認証に成功した場合、、、
                if user.is_active:
                    ### ユーザが活性（有効）の場合、、、
                    login(request, user)
                    print_log('[INFO] P0100Login.index_view()関数が正常終了しました。0', 'INFO')
                    return HttpResponseRedirect('/P0100File/R4/')
                else:
                    ### ユーザが非活性（無効）の場合、、、
                    template = loader.get_template('P0100Login/index.html')
                    context = {'message': 'ログインに失敗しました。'}
                    print_log('[WARN] P0100Login.index_view()関数が警告終了しました。1', 'INFO')
                    return HttpResponse(template.render(context, request))
            else:
                ### 認証に失敗した場合、、、
                template = loader.get_template('P0100Login/index.html')
                context = {'message': 'ログインに失敗しました。'}
                print_log('[WARN] P0100Login.index_view()関数が警告終了しました。2', 'INFO')
                return HttpResponse(template.render(context, request))
    except:
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P0100Login.index_view()関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P0100Login.index_view()関数が異常終了しました。', 'ERROR')
        return render(request, 'error.html')
        