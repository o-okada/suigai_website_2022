from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic

from django.views.generic.base import TemplateView

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
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

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################
from P0000Common.models import HOUSE_ASSET             ### 15: 県別家屋評価額
from P0000Common.models import HOUSE_DAMAGE            ### 16: 家屋被害率
from P0000Common.models import HOUSEHOLD_DAMAGE        ### 17: 家庭用品自動車以外被害率
from P0000Common.models import CAR_DAMAGE              ### 18: 家庭用品自動車被害率
from P0000Common.models import HOUSE_COST              ### 19: 家庭応急対策費
from P0000Common.models import OFFICE_ASSET            ### 20: 産業分類別資産額
from P0000Common.models import OFFICE_DAMAGE           ### 21: 事業所被害率
from P0000Common.models import OFFICE_COST             ### 22: 事業所営業停止損失
from P0000Common.models import FARMER_FISHER_DAMAGE    ### 23: 農漁家被害率

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import WEATHER                 ### 24: 異常気象（ほぼ、水害）
from P0000Common.models import AREA                    ### 25: 区域
from P0000Common.models import IPPAN                   ### 26: 一般資産調査票

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import RESTORATION             ### 27: 復旧事業工種

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from P0000Common.models import KOKYO                   ### 28: 公共土木調査票
from P0000Common.models import KOEKI                   ### 29: 公益事業調査票

###############################################################################
### index 関数
###############################################################################
### def index(request):
###     template = loader.get_template('P9100AdminCheck/index.html')
###     context = {}
###     ### return HttpResponse("Hello, world. You're at the P9100AdminCheck index")
###     return HttpResponse(template.render(context, request))
def index(request):
    print('index(request): ', flush=True)
    ken_list = KEN.objects.order_by('ken_code')[:]
    template = loader.get_template('P9100AdminCheck/index.html')
    context = {
        'ken_list': ken_list,
    }
    return HttpResponse(template.render(context, request))

###############################################################################
### ken 関数
###############################################################################
def ken(request, ken_code):
    print('ken(request, ken_code): ', ken_code, flush=True)
    ken_list = KEN.objects.order_by('ken_code')[:]
    city_list = CITY.objects.filter(ken_code=ken_code).order_by('city_code')[:]
    template = loader.get_template('P9100AdminCheck/index.html')
    context = {
        'ken_list': ken_list,
        'city_list': city_list,
        'ken_code': ken_code,
    }
    return HttpResponse(template.render(context, request))

###############################################################################
### city 関数
###############################################################################
def city(request, ken_code, city_code):    
    print('city(request, ken_code, city_code): ', ken_code, city_code, flush=True)
    ken_list = KEN.objects.order_by('ken_code')[:]
    city_list = CITY.objects.filter(ken_code=ken_code).order_by('city_code')[:]
    template = loader.get_template('P9100AdminCheck/index.html')
    context = {
        'ken_list': ken_list,
        'city_list': city_list,
        'ken_code': ken_code,
        'city_code': city_code,
    }
    return HttpResponse(template.render(context, request))
