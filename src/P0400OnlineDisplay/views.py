#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import Http404
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
def index(request):
    print('index(request): ', flush=True)
    ken_list = KEN.objects.order_by('ken_code')[:]
    template = loader.get_template('P0400OnlineDisplay/index.html')
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
    template = loader.get_template('P0400OnlineDisplay/index.html')
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
    template = loader.get_template('P0400OnlineDisplay/index.html')
    context = {
        'ken_list': ken_list,
        'city_list': city_list,
        'ken_code': ken_code,
        'city_code': city_code,
    }
    return HttpResponse(template.render(context, request))

###############################################################################
### category 関数
###############################################################################
def category(request, ken_code, city_code, category_code):
    print('category(request, ken_code, city_code, category_code): ', ken_code, city_code, category_code, flush=True)
    ken_list = KEN.objects.order_by('ken_code')[:]
    city_list = CITY.objects.filter(ken_code=ken_code).order_by('city_code')[:]
    
    building_list = []
    ### ken_list = []
    ### city_list = []
    kasen_kaigan_list = []
    suikei_list = []
    suikei_type_list = []
    kasen_list = []
    kasen_type_list = []
    cause_list = []
    underground_list = []
    usage_list = []
    flood_sediment_list = []
    gradient_list = []
    industry_list = []
    house_asset_list = []
    house_damage_list = []
    household_damage_list = []
    car_damage_list = []
    house_cost_list = []
    office_asset_list = []
    office_damage_list = []
    farmer_fisher_damage_list = []
    weather_list = []
    area_list = []
    ippan_list = []
    
    if category_code == "1":
        pass
    elif category_code == "2":
        ippan_list = IPPAN.objects.order_by('ippan_id')[:]
    elif category_code == "3":
        pass
    elif category_code == "4":
        pass
    elif category_code == "5":
        pass
    elif category_code == "6":
        pass
    elif category_code == "7":
        pass
    elif category_code == "8":
        pass
    elif category_code == "9":
        pass
    elif category_code == "10":
        building_list = BUILDING.objects.order_by('building_code')[:]
    elif category_code == "11":
        pass
    elif category_code == "12":
        pass
    elif category_code == "13":
        kasen_kaigan_list = KASEN_KAIGAN.objects.order_by('kasen_kaigan_code')[:]
    elif category_code == "14":
        suikei_list = SUIKEI.objects.order_by('suikei_code')[:]
    elif category_code == "15":
        suikei_type_list = SUIKEI_TYPE.objects.order_by('suikei_type_code')[:]
    elif category_code == "16":
        kasen_list = KASEN.objects.order_by('kasen_code')[:]
    elif category_code == "17":
        kasen_type_list = KASEN_TYPE.objects.order_by('kasen_type_code')[:]
    elif category_code == "18":
        cause_list = CAUSE.objects.order_by('cause_code')[:]
    elif category_code == "19":
        underground_list = UNDERGROUND.objects.order_by('underground_code')[:]
    elif category_code == "20":
        usage_list = USAGE.objects.order_by('usage_code')[:]
    elif category_code == "21":
        flood_sediment_list = FLOOD_SEDIMENT.objects.order_by('flood_sediment_code')[:]
    elif category_code == "22":
        gradient_list = GRADIENT.objects.order_by('gradient_code')[:]
    elif category_code == "23":
        industry_list = INDUSTRY.objects.order_by('industry_code')[:]
    elif category_code == "24":
        house_asset_list = HOUSE_ASSET.objects.order_by('house_asset_code')[:]
    elif category_code == "25":
        house_damage_list = HOUSE_DAMAGE.objects.order_by('house_damage_code')[:]
    elif category_code == "26":
        household_damage_list = HOUSEHOLD_DAMAGE.objects.order_by('household_damage_code')[:]
    elif category_code == "27":
        car_damage_list = CAR_DAMAGE.objects.order_by('car_damage_code')[:]
    elif category_code == "28":
        house_cost_list = HOUSE_COST.objects.order_by('house_cost_code')[:]
    elif category_code == "29":
        office_asset_list = OFFICE_ASSET.objects.order_by('office_asset_code')[:]
    elif category_code == "30":
        office_damage_list = OFFICE_DAMAGE.objects.order_by('office_damage_code')[:]
    elif category_code == "31":
        office_cost_list = OFFICE_COST.objects.order_by('office_cost_code')[:]
    elif category_code == "32":
        farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.order_by('farmer_fisher_damage_code')[:]
    elif category_code == "33":
        weather_list = WEATHER.objects.order_by('weather_id')[:]
    elif category_code == "34":
        area_list = AREA.objects.order_by('area_id')[:]
    else:
        pass
    template = loader.get_template('P0400OnlineDisplay/index.html')
    context = {
        'ken_code': ken_code,
        'city_code': city_code,
        'category_code': category_code,
        'building_list': building_list,
        'ken_list': ken_list,
        'city_list': city_list,
        'kasen_kaigan_list': kasen_kaigan_list,
        'suikei_list': suikei_list,
        'suikei_type_list': suikei_type_list,
        'kasen_list': kasen_list,
        'kasen_type_list': kasen_type_list,
        'cause_list': cause_list,
        'underground_list': underground_list,
        'usage_list': usage_list,
        'flood_sediment_list': flood_sediment_list,
        'gradient_list': gradient_list,
        'industry_list': industry_list,
        'house_asset_list': house_asset_list,
        'house_damage_list': house_damage_list,
        'household_damage_list': household_damage_list,
        'car_damage_list': car_damage_list,
        'house_cost_list': house_cost_list,
        'office_asset_list': office_asset_list,
        'office_damage_list': office_damage_list,
        'farmer_fisher_damage_list': farmer_fisher_damage_list,
        'weather_list': weather_list,
        'area_list': area_list,
        'ippan_list': ippan_list,
    }
    return HttpResponse(template.render(context, request))
    
