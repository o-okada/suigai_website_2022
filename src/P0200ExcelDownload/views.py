from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.views.generic import FormView
from django.views.generic.base import TemplateView

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### from .models import P0200Prefecture
### from .models import P0200City
from .models import BUILDING                ### 01: 建物区分
from .models import KEN                     ### 02: 都道府県
from .models import CITY                    ### 03: 市区町村
from .models import KASEN_KAIGAN            ### 04: 水害発生地点工種（河川海岸区分）
from .models import SUIKEI                  ### 05: 水系（水系・沿岸）
from .models import SUIKEI_TYPE             ### 06: 水系種別（水系・沿岸種別）
from .models import KASEN                   ### 07: 河川（河川・海岸）
from .models import KASEN_TYPE              ### 08: 河川種別（河川・海岸種別）
from .models import CAUSE                   ### 09: 水害原因
from .models import UNDERGROUND             ### 10: 地上地下区分
from .models import USAGE                   ### 11: 地下空間の利用形態
from .models import FLOOD_SEDIMENT          ### 12: 浸水土砂区分
from .models import GRADIENT                ### 13: 地盤勾配区分
from .models import INDUSTRY                ### 14: 産業分類

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################
from .models import HOUSE_ASSET             ### 15: 県別家屋評価額
from .models import HOUSE_DAMAGE            ### 16: 家屋被害率
from .models import HOUSEHOLD_DAMAGE        ### 17: 家庭用品自動車以外被害率
from .models import CAR_DAMAGE              ### 18: 家庭用品自動車被害率
from .models import HOUSE_COST              ### 19: 家庭応急対策費
from .models import OFFICE_ASSET            ### 20: 産業分類別資産額
from .models import OFFICE_DAMAGE           ### 21: 事業所被害率
from .models import OFFICE_COST             ### 22: 事業所営業停止損失
from .models import FARMER_FISHER_DAMAGE    ### 23: 農漁家被害率

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from .models import WEATHER                 ### 24: 異常気象（ほぼ、水害）
from .models import AREA                    ### 25: 区域
from .models import IPPAN                   ### 26: 一般資産調査票

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from .models import RESTORATION             ### 27: 復旧事業工種

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
from .models import KOKYO                   ### 28: 公共土木調査票
from .models import KOEKI                   ### 29: 公益事業調査票

import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

### Imaginary function to handle an uploaded file.
### from somewhere import handle_uploaded_file
### class IndexView(generic.TemplateView):
###     template_name = "index1.html"
### def index(request):
###     try:
###         latest_question_list = P0200Question.objects.order_by('-pub_date')[:5]
###         template = loader.get_template('P0200ExcelDownload/index1.html')
###         context = {
###             'latest_question_list': latest_question_list,
###         }
###     except:
###         raise Http404("P0200Question does not exist.")
###     return HttpResponse(template.render(context, request))

###############################################################################
### index 関数
###############################################################################
def index(request):
    ken_list = KEN.objects.order_by('KEN_CODE')[:]
    city_list01 = CITY.objects.filter(KEN_CODE='01').order_by('CITY_CODE')
    city_list02 = CITY.objects.filter(KEN_CODE='02').order_by('CITY_CODE')
    city_list03 = CITY.objects.filter(KEN_CODE='03').order_by('CITY_CODE')
    city_list04 = CITY.objects.filter(KEN_CODE='04').order_by('CITY_CODE')
    city_list05 = CITY.objects.filter(KEN_CODE='05').order_by('CITY_CODE')
    city_list06 = CITY.objects.filter(KEN_CODE='06').order_by('CITY_CODE')
    city_list07 = CITY.objects.filter(KEN_CODE='07').order_by('CITY_CODE')
    city_list08 = CITY.objects.filter(KEN_CODE='08').order_by('CITY_CODE')
    city_list09 = CITY.objects.filter(KEN_CODE='09').order_by('CITY_CODE')
    city_list10 = CITY.objects.filter(KEN_CODE='10').order_by('CITY_CODE')
    city_list11 = CITY.objects.filter(KEN_CODE='11').order_by('CITY_CODE')
    city_list12 = CITY.objects.filter(KEN_CODE='12').order_by('CITY_CODE')
    city_list13 = CITY.objects.filter(KEN_CODE='13').order_by('CITY_CODE')
    city_list14 = CITY.objects.filter(KEN_CODE='14').order_by('CITY_CODE')
    city_list15 = CITY.objects.filter(KEN_CODE='15').order_by('CITY_CODE')
    city_list16 = CITY.objects.filter(KEN_CODE='16').order_by('CITY_CODE')
    city_list17 = CITY.objects.filter(KEN_CODE='17').order_by('CITY_CODE')
    city_list18 = CITY.objects.filter(KEN_CODE='18').order_by('CITY_CODE')
    city_list19 = CITY.objects.filter(KEN_CODE='19').order_by('CITY_CODE')
    city_list20 = CITY.objects.filter(KEN_CODE='20').order_by('CITY_CODE')
    city_list21 = CITY.objects.filter(KEN_CODE='21').order_by('CITY_CODE')
    city_list22 = CITY.objects.filter(KEN_CODE='22').order_by('CITY_CODE')
    city_list23 = CITY.objects.filter(KEN_CODE='23').order_by('CITY_CODE')
    city_list24 = CITY.objects.filter(KEN_CODE='24').order_by('CITY_CODE')
    city_list25 = CITY.objects.filter(KEN_CODE='25').order_by('CITY_CODE')
    city_list26 = CITY.objects.filter(KEN_CODE='26').order_by('CITY_CODE')
    city_list27 = CITY.objects.filter(KEN_CODE='27').order_by('CITY_CODE')
    city_list28 = CITY.objects.filter(KEN_CODE='28').order_by('CITY_CODE')
    city_list29 = CITY.objects.filter(KEN_CODE='29').order_by('CITY_CODE')
    city_list30 = CITY.objects.filter(KEN_CODE='30').order_by('CITY_CODE')
    city_list31 = CITY.objects.filter(KEN_CODE='31').order_by('CITY_CODE')
    city_list32 = CITY.objects.filter(KEN_CODE='32').order_by('CITY_CODE')
    city_list33 = CITY.objects.filter(KEN_CODE='33').order_by('CITY_CODE')
    city_list34 = CITY.objects.filter(KEN_CODE='34').order_by('CITY_CODE')
    city_list35 = CITY.objects.filter(KEN_CODE='35').order_by('CITY_CODE')
    city_list36 = CITY.objects.filter(KEN_CODE='36').order_by('CITY_CODE')
    city_list37 = CITY.objects.filter(KEN_CODE='37').order_by('CITY_CODE')
    city_list38 = CITY.objects.filter(KEN_CODE='38').order_by('CITY_CODE')
    city_list39 = CITY.objects.filter(KEN_CODE='39').order_by('CITY_CODE')
    city_list40 = CITY.objects.filter(KEN_CODE='40').order_by('CITY_CODE')
    city_list41 = CITY.objects.filter(KEN_CODE='41').order_by('CITY_CODE')
    city_list42 = CITY.objects.filter(KEN_CODE='42').order_by('CITY_CODE')
    city_list43 = CITY.objects.filter(KEN_CODE='43').order_by('CITY_CODE')
    city_list44 = CITY.objects.filter(KEN_CODE='44').order_by('CITY_CODE')
    city_list45 = CITY.objects.filter(KEN_CODE='45').order_by('CITY_CODE')
    city_list46 = CITY.objects.filter(KEN_CODE='46').order_by('CITY_CODE')
    city_list47 = CITY.objects.filter(KEN_CODE='47').order_by('CITY_CODE')
    template = loader.get_template('P0200ExcelDownload/index.html')
    context = {
        'ken_list': ken_list,
        'city_list01': city_list01,
        'city_list02': city_list02,
        'city_list03': city_list03,
        'city_list04': city_list04,
        'city_list05': city_list05,
        'city_list06': city_list06,
        'city_list07': city_list07,
        'city_list08': city_list08,
        'city_list09': city_list09,
        'city_list10': city_list10,
        'city_list11': city_list11,
        'city_list12': city_list12,
        'city_list13': city_list13,
        'city_list14': city_list14,
        'city_list15': city_list15,
        'city_list16': city_list16,
        'city_list17': city_list17,
        'city_list18': city_list18,
        'city_list19': city_list19,
        'city_list20': city_list20,
        'city_list21': city_list21,
        'city_list22': city_list22,
        'city_list23': city_list23,
        'city_list24': city_list24,
        'city_list25': city_list25,
        'city_list26': city_list26,
        'city_list27': city_list27,
        'city_list28': city_list28,
        'city_list29': city_list29,
        'city_list30': city_list30,
        'city_list31': city_list31,
        'city_list32': city_list32,
        'city_list33': city_list33,
        'city_list34': city_list34,
        'city_list35': city_list35,
        'city_list36': city_list36,
        'city_list37': city_list37,
        'city_list38': city_list38,
        'city_list39': city_list39,
        'city_list40': city_list40,
        'city_list41': city_list41,
        'city_list42': city_list42,
        'city_list43': city_list43,
        'city_list44': city_list44,
        'city_list45': city_list45,
        'city_list46': city_list46,
        'city_list47': city_list47,
    }
    return HttpResponse(template.render(context, request))

### def upload_file(request):
###     if request.method == 'POST':
###         form = UploadFileForm(request.POST, request.FILES)
###         if form.is_valid():
###             handle_uploaded_file(request.FILES['file'])
###             return HttpResponseRedirect('/success/url/')
###     else:
###         form = UploadFileForm()
###     return render(request, 'upload.html', {'form': form})
### def handle_uploaded_file(f):
###     with open('some/file/name.txt', 'wb+') as destination:
###         for chunk in f.chunks():
###             destination.write(chunk)
### def download_file(request):
###     try:
###         file_path_to_load = 'static/example.xlsx'
###         file_path_to_save = 'static/example2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         ws['A1'].value = 12345.6789
###         ws['A2'].value = 12345.6789
###         ws['A3'].value = '=sum(A1:A2)'
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="your_book.xlsx"'
###     except:
###         raise Http404("[ERROR] download_file().")
###     return response

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 00: 
### def download_p0200prefecture(request):
###     try:
###         p0200prefecture_list = P0200Prefecture.objects.order_by('CODE')[:]
###         file_path_to_load = 'static/p0200prefecture.xlsx'
###         file_path_to_save = 'static/p0200prefecture2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         if p0200prefecture_list:
###             for i, p0200prefecture in enumerate(p0200prefecture_list):
###                 ws.cell(row=i+1, column=1).value = p0200prefecture.CODE
###                 ws.cell(row=i+1, column=2).value = p0200prefecture.NAME
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="p0200prefecture.xlsx"'
###     except:
###         raise Http404("[ERROR] download_p0200prefecture().")
###     return response
### 00: 
### def download_p0200city(request):
###     try:
###         p0200city_list = P0200City.objects.order_by('CODE')[:]
###         file_path_to_load = 'static/p0200city.xlsx'
###         file_path_to_save = 'static/p0200city2.xlsx'
###         wb = openpyxl.load_workbook(file_path_to_load)
###         ws = wb.active
###         ws.title = 'sheet99'
###         if p0200city_list:
###             for i, p0200city in enumerate(p0200city_list):
###                 ws.cell(row=i+1, column=1).value = p0200city.CODE
###                 ws.cell(row=i+1, column=2).value = p0200city.PREF_CODE
###                 ws.cell(row=i+1, column=3).value = p0200city.NAME
###         wb.save(file_path_to_save)
###         response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
###         response['Content-Disposition'] = 'attachment; filename="p0200city.xlsx"'
###     except:
###         raise Http404("[ERROR] download_p0200city().")
###     return response

###############################################################################
### download_building関数
### 01: 建物区分
###############################################################################
def download_building(request):
    try:
        building_list = BUILDING.objects.order_by('BUILDING_CODE')[:]
        file_path_to_load = 'static/building.xlsx'
        file_path_to_save = 'static/building2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '建物区分コード'
        ws.cell(row=1, column=2).value = '建物区分名'
        
        if building_list:
            for i, building in enumerate(building_list):
                ws.cell(row=i+2, column=1).value = building.BUILDING_CODE
                ws.cell(row=i+2, column=2).value = building.BUILDING_NAME

        # dv = DataValidation(type="list", formula1='"A,B,C"')
        ### dv.add(ws.cell(1, 1))
        ### dv.add(ws.cell(2, 1))
        ### dv.add(ws.cell(3, 1))
        # dv.ranges = 'A1:A100'
        # ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="building.xlsx"'
    except:
        raise Http404("[ERROR] download_building().")
    return response

###############################################################################
### download_ken関数
### 02: 都道府県
###############################################################################
def download_ken(request):
    try:
        ken_list = KEN.objects.order_by('KEN_CODE')[:]
        file_path_to_load = 'static/ken.xlsx'
        file_path_to_save = 'static/ken2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '都道府県コード'
        ws.cell(row=1, column=2).value = '都道府県名'
        
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws.cell(row=i+2, column=1).value = ken.KEN_CODE
                ws.cell(row=i+2, column=2).value = ken.KEN_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ken.xlsx"'
    except:
        raise Http404("[ERROR] download_ken().")
    return response

###############################################################################
### download_city関数
### 03: 市区町村
###############################################################################
def download_city(request):
    try:
        city_list = CITY.objects.order_by('CITY_CODE')[:]
        file_path_to_load = 'static/city.xlsx'
        file_path_to_save = 'static/city2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '市区町村コード'
        ws.cell(row=1, column=2).value = '市区町村名'
        ws.cell(row=1, column=3).value = '都道府県コード'
        ws.cell(row=1, column=4).value = '市区町村人口'
        ws.cell(row=1, column=5).value = '市区町村面積'
        
        if city_list:
            for i, city in enumerate(city_list):
                ws.cell(row=i+2, column=1).value = city.CITY_CODE
                ws.cell(row=i+2, column=2).value = city.CITY_NAME
                ws.cell(row=i+2, column=3).value = city.KEN_CODE
                ws.cell(row=i+2, column=4).value = city.CITY_POPULATION
                ws.cell(row=i+2, column=5).value = city.CITY_AREA
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="city.xlsx"'
    except:
        raise Http404("[ERROR] download_city().")
    return response

###############################################################################
### download_kasen_kaigan関数
### 04: 水害発生地点工種（河川海岸区分）
###############################################################################
def download_kasen_kaigan(request):
    try:
        kasen_kaigan_list = KASEN_KAIGAN.objects.order_by('KASEN_KAIGAN_CODE')[:]
    
        file_path_to_load = 'static/kasen_kaigan.xlsx'
        file_path_to_save = 'static/kasen_kaigan2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '河川海岸区分コード'
        ws.cell(row=1, column=2).value = '河川海岸区分名'
        
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws.cell(row=i+2, column=1).value = kasen_kaigan.KASEN_KAIGAN_CODE
                ws.cell(row=i+2, column=2).value = kasen_kaigan.KASEN_KAIGAN_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_kaigan.xlsx"'
    except:
        raise Http404("[ERROR] download_kasen_kaigan().")
    return response

###############################################################################
### download_suikei関数
### 05: 水系（水系・沿岸）
###############################################################################
def download_suikei(request):
    try:
        suikei_list = SUIKEI.objects.order_by('SUIKEI_CODE')[:]
    
        file_path_to_load = 'static/suikei.xlsx'
        file_path_to_save = 'static/suikei2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '水系コード'
        ws.cell(row=1, column=2).value = '水系名'
        ws.cell(row=1, column=3).value = '水系種別コード'
        
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws.cell(row=i+2, column=1).value = suikei.SUIKEI_CODE
                ws.cell(row=i+2, column=2).value = suikei.SUIKEI_NAME
                ws.cell(row=i+2, column=3).value = suikei.SUIKEI_TYPE_CODE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei.xlsx"'
    except:
        raise Http404("[ERROR] download_suikei().")
    return response

###############################################################################
### download_suikei_type関数
### 06: 水系種別（水系・沿岸種別）
###############################################################################
def download_suikei_type(request):
    try:
        suikei_type_list = SUIKEI_TYPE.objects.order_by('SUIKEI_TYPE_CODE')[:]
    
        file_path_to_load = 'static/suikei_type.xlsx'
        file_path_to_save = 'static/suikei_type2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '水系種別コード'
        ws.cell(row=1, column=2).value = '水系種別名'
        
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws.cell(row=i+2, column=1).value = suikei_type.SUIKEI_TYPE_CODE
                ws.cell(row=i+2, column=2).value = suikei_type.SUIKEI_TYPE_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="suikei_type.xlsx"'
    except:
        raise Http404("[ERROR] download_suikei_type().")
    return response

###############################################################################
### download_kasen関数
### 07: 河川（河川・海岸）
###############################################################################
def download_kasen(request):
    try:
        kasen_list = KASEN.objects.order_by('KASEN_CODE')[:]
    
        file_path_to_load = 'static/kasen.xlsx'
        file_path_to_save = 'static/kasen2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '河川コード'
        ws.cell(row=1, column=2).value = '河川名'
        ws.cell(row=1, column=3).value = '河川種別コード'
        ws.cell(row=1, column=4).value = '水系コード'
        
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws.cell(row=i+2, column=1).value = kasen.KASEN_CODE
                ws.cell(row=i+2, column=2).value = kasen.KASEN_NAME
                ws.cell(row=i+2, column=3).value = kasen.KASEN_TYPE_CODE
                ws.cell(row=i+2, column=4).value = kasen.SUIKEI_CODE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen.xlsx"'
    except:
        raise Http404("[ERROR] download_kasen().")
    return response

###############################################################################
### download_kasen_type関数
### 08: 河川種別（河川・海岸種別）
###############################################################################
def download_kasen_type(request):
    try:
        kasen_type_list = KASEN_TYPE.objects.order_by('KASEN_TYPE_CODE')[:]
    
        file_path_to_load = 'static/kasen_type.xlsx'
        file_path_to_save = 'static/kasen_type2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '河川種別コード'
        ws.cell(row=1, column=2).value = '河川種別名'
        
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws.cell(row=i+2, column=1).value = kasen_type.KASEN_TYPE_CODE
                ws.cell(row=i+2, column=2).value = kasen_type.KASEN_TYPE_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kasen_type.xlsx"'
    except:
        raise Http404("[ERROR] download_kasen_type().")
    return response

###############################################################################
### download_cause関数
### 09: 水害原因
###############################################################################
def download_cause(request):
    try:
        cause_list = CAUSE.objects.order_by('CAUSE_CODE')[:]
    
        file_path_to_load = 'static/cause.xlsx'
        file_path_to_save = 'static/cause2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '水害原因コード'
        ws.cell(row=1, column=2).value = '水害原因名'
        
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws.cell(row=i+2, column=1).value = cause.CAUSE_CODE
                ws.cell(row=i+2, column=2).value = cause.CAUSE_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cause.xlsx"'
    except:
        raise Http404("[ERROR] download_cause().")
    return response

###############################################################################
### download_underground関数
### 10: 地上地下区分
###############################################################################
def download_underground(request):
    try:
        underground_list = UNDERGROUND.objects.order_by('UNDERGROUND_CODE')[:]
    
        file_path_to_load = 'static/underground.xlsx'
        file_path_to_save = 'static/underground2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '地上地下区分コード'
        ws.cell(row=1, column=2).value = '地上地下区分名'
        
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws.cell(row=i+2, column=1).value = underground.UNDERGROUND_CODE
                ws.cell(row=i+2, column=2).value = underground.UNDERGROUND_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="underground.xlsx"'
    except:
        raise Http404("[ERROR] download_underground().")
    return response

###############################################################################
### download_usage関数
### 11: 地下空間の利用形態
###############################################################################
def download_usage(request):
    try:
        usage_list = USAGE.objects.order_by('USAGE_CODE')[:]
    
        file_path_to_load = 'static/usage.xlsx'
        file_path_to_save = 'static/usage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '地下空間の利用形態コード'
        ws.cell(row=1, column=2).value = '地下空間の利用形態名'
        
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws.cell(row=i+2, column=1).value = usage.USAGE_CODE
                ws.cell(row=i+2, column=2).value = usage.USAGE_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="usage.xlsx"'
    except:
        raise Http404("[ERROR] download_usage().")
    return response

###############################################################################
### download_flood_sediment関数
### 12: 浸水土砂区分
###############################################################################
def download_flood_sediment(request):
    try:
        flood_sediment_list = FLOOD_SEDIMENT.objects.order_by('FLOOD_SEDIMENT_CODE')[:]
    
        file_path_to_load = 'static/flood_sediment.xlsx'
        file_path_to_save = 'static/flood_sediment2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '浸水土砂区分コード'
        ws.cell(row=1, column=2).value = '浸水土砂区分名'
        
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws.cell(row=i+2, column=1).value = flood_sediment.FLOOD_SEDIMENT_CODE
                ws.cell(row=i+2, column=2).value = flood_sediment.FLOOD_SEDIMENT_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="flood_sediment.xlsx"'
    except:
        raise Http404("[ERROR] download_flood_sediment().")
    return response

###############################################################################
### download_gradient関数
### 13: 地盤勾配区分
###############################################################################
def download_gradient(request):
    try:
        gradient_list = GRADIENT.objects.order_by('GRADIENT_CODE')[:]
    
        file_path_to_load = 'static/gradient.xlsx'
        file_path_to_save = 'static/gradient2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '地盤勾配区分コード'
        ws.cell(row=1, column=2).value = '地盤勾配区分名'
        
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws.cell(row=i+2, column=1).value = gradient.GRADIENT_CODE
                ws.cell(row=i+2, column=2).value = gradient.GRADIENT_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="gradient.xlsx"'
    except:
        raise Http404("[ERROR] download_gradient().")
    return response

###############################################################################
### download_industry関数
### 14: 産業分類
###############################################################################
def download_industry(request):
    try:
        industry_list = INDUSTRY.objects.order_by('INDUSTRY_CODE')[:]
    
        file_path_to_load = 'static/industry.xlsx'
        file_path_to_save = 'static/industry2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '産業分類コード'
        ws.cell(row=1, column=2).value = '産業分類名'
        
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws.cell(row=i+2, column=1).value = industry.INDUSTRY_CODE
                ws.cell(row=i+2, column=2).value = industry.INDUSTRY_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="industry.xlsx"'
    except:
        raise Http404("[ERROR] download_industry().")
    return response

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################

###############################################################################
### download_house_asset関数
### 15: 県別家屋評価額
###############################################################################
def download_house_asset(request):
    try:
        house_asset_list = HOUSE_ASSET.objects.order_by('HOUSE_ASSET_CODE')[:]
    
        file_path_to_load = 'static/house_asset.xlsx'
        file_path_to_save = 'static/house_asset2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '県別家屋被害コード'
        ws.cell(row=1, column=2).value = '県コード'
        ws.cell(row=1, column=3).value = '県別家屋被害対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        ws.cell(row=1, column=6).value = '県別家屋評価額'
        
        if house_asset_list:
            for i, house_asset in enumerate(house_asset_list):
                ws.cell(row=i+2, column=1).value = house_asset.HOUSE_ASSET_CODE
                ws.cell(row=i+2, column=2).value = house_asset.KEN_CODE
                ws.cell(row=i+2, column=3).value = house_asset.HOUSE_ASSET_YEAR
                ws.cell(row=i+2, column=4).value = house_asset.BEGIN_DATE
                ws.cell(row=i+2, column=5).value = house_asset.END_DATE
                ws.cell(row=i+2, column=6).value = house_asset.HOUSE_ASSET
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_asset.xlsx"'
    except:
        raise Http404("[ERROR] download_house_asset().")
    return response

###############################################################################
### download_house_damage関数
### 16: 家屋被害率
###############################################################################
def download_house_damage(request):
    try:
        house_damage_list = HOUSE_DAMAGE.objects.order_by('HOUSE_DAMAGE_CODE')[:]
    
        file_path_to_load = 'static/house_damage.xlsx'
        file_path_to_save = 'static/house_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '家屋被害率コード'
        ws.cell(row=1, column=2).value = '家屋被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_勾配1_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_勾配1_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_勾配1_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_勾配1_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_勾配1_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_勾配1_300cm以上'

        ws.cell(row=1, column=11).value = '被害率_浸水_勾配2_床下'
        ws.cell(row=1, column=12).value = '被害率_浸水_勾配2_0から50cm未満'
        ws.cell(row=1, column=13).value = '被害率_浸水_勾配2_50から100cm未満'
        ws.cell(row=1, column=14).value = '被害率_浸水_勾配2_100から200cm未満'
        ws.cell(row=1, column=15).value = '被害率_浸水_勾配2_200から300cm未満'
        ws.cell(row=1, column=16).value = '被害率_浸水_勾配2_300cm以上'

        ws.cell(row=1, column=17).value = '被害率_浸水_勾配3_床下'
        ws.cell(row=1, column=18).value = '被害率_浸水_勾配3_0から50cm未満'
        ws.cell(row=1, column=19).value = '被害率_浸水_勾配3_50から100cm未満'
        ws.cell(row=1, column=20).value = '被害率_浸水_勾配3_100から200cm未満'
        ws.cell(row=1, column=21).value = '被害率_浸水_勾配3_200から300cm未満'
        ws.cell(row=1, column=22).value = '被害率_浸水_勾配3_300cm以上'

        ws.cell(row=1, column=23).value = '被害率_土砂_勾配1_床下'
        ws.cell(row=1, column=24).value = '被害率_土砂_勾配1_0から50cm未満'
        ws.cell(row=1, column=25).value = '被害率_土砂_勾配1_50から100cm未満'
        ws.cell(row=1, column=26).value = '被害率_土砂_勾配1_100から200cm未満'
        ws.cell(row=1, column=27).value = '被害率_土砂_勾配1_200から300cm未満'
        ws.cell(row=1, column=28).value = '被害率_土砂_勾配1_300cm以上'

        ws.cell(row=1, column=29).value = '被害率_土砂_勾配2_床下'
        ws.cell(row=1, column=30).value = '被害率_土砂_勾配2_0から50cm未満'
        ws.cell(row=1, column=31).value = '被害率_土砂_勾配2_50から100cm未満'
        ws.cell(row=1, column=32).value = '被害率_土砂_勾配2_100から200cm未満'
        ws.cell(row=1, column=33).value = '被害率_土砂_勾配2_200から300cm未満'
        ws.cell(row=1, column=34).value = '被害率_土砂_勾配2_300cm以上'

        ws.cell(row=1, column=35).value = '被害率_土砂_勾配3_床下'
        ws.cell(row=1, column=36).value = '被害率_土砂_勾配3_0から50cm未満'
        ws.cell(row=1, column=37).value = '被害率_土砂_勾配3_50から100cm未満'
        ws.cell(row=1, column=38).value = '被害率_土砂_勾配3_100から200cm未満'
        ws.cell(row=1, column=39).value = '被害率_土砂_勾配3_200から300cm未満'
        ws.cell(row=1, column=40).value = '被害率_土砂_勾配3_300cm以上'
        
        if house_damage_list:
            for i, house_damage in enumerate(house_damage_list):
                ws.cell(row=i+2, column=1).value = house_damage.HOUSE_DAMAGE_CODE
                ws.cell(row=i+2, column=2).value = house_damage.HOUSE_DAMAGE_YEAR
                ws.cell(row=i+2, column=3).value = house_damage.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = house_damage.END_DATE
                
                ws.cell(row=i+2, column=5).value = house_damage.FL_GR1_LV00
                ws.cell(row=i+2, column=6).value = house_damage.FL_GR1_LV00_50
                ws.cell(row=i+2, column=7).value = house_damage.FL_GR1_LV50_100
                ws.cell(row=i+2, column=8).value = house_damage.FL_GR1_LV100_200
                ws.cell(row=i+2, column=9).value = house_damage.FL_GR1_LV200_300
                ws.cell(row=i+2, column=10).value = house_damage.FL_GR1_LV300
        
                ws.cell(row=i+2, column=11).value = house_damage.FL_GR2_LV00
                ws.cell(row=i+2, column=12).value = house_damage.FL_GR2_LV00_50
                ws.cell(row=i+2, column=13).value = house_damage.FL_GR2_LV50_100
                ws.cell(row=i+2, column=14).value = house_damage.FL_GR2_LV100_200
                ws.cell(row=i+2, column=15).value = house_damage.FL_GR2_LV200_300
                ws.cell(row=i+2, column=16).value = house_damage.FL_GR2_LV300

                ws.cell(row=i+2, column=17).value = house_damage.FL_GR3_LV00
                ws.cell(row=i+2, column=18).value = house_damage.FL_GR3_LV00_50
                ws.cell(row=i+2, column=19).value = house_damage.FL_GR3_LV50_100
                ws.cell(row=i+2, column=20).value = house_damage.FL_GR3_LV100_200
                ws.cell(row=i+2, column=21).value = house_damage.FL_GR3_LV200_300
                ws.cell(row=i+2, column=22).value = house_damage.FL_GR3_LV300
        
                ws.cell(row=i+2, column=23).value = house_damage.SD_GR1_LV00
                ws.cell(row=i+2, column=24).value = house_damage.SD_GR1_LV00_50
                ws.cell(row=i+2, column=25).value = house_damage.SD_GR1_LV50_100
                ws.cell(row=i+2, column=26).value = house_damage.SD_GR1_LV100_200
                ws.cell(row=i+2, column=27).value = house_damage.SD_GR1_LV200_300
                ws.cell(row=i+2, column=28).value = house_damage.SD_GR1_LV300
        
                ws.cell(row=i+2, column=29).value = house_damage.SD_GR2_LV00
                ws.cell(row=i+2, column=30).value = house_damage.SD_GR2_LV00_50
                ws.cell(row=i+2, column=31).value = house_damage.SD_GR2_LV50_100
                ws.cell(row=i+2, column=32).value = house_damage.SD_GR2_LV100_200
                ws.cell(row=i+2, column=33).value = house_damage.SD_GR2_LV200_300
                ws.cell(row=i+2, column=34).value = house_damage.SD_GR2_LV300

                ws.cell(row=i+2, column=35).value = house_damage.SD_GR3_LV00
                ws.cell(row=i+2, column=36).value = house_damage.SD_GR3_LV00_50
                ws.cell(row=i+2, column=37).value = house_damage.SD_GR3_LV50_100
                ws.cell(row=i+2, column=38).value = house_damage.SD_GR3_LV100_200
                ws.cell(row=i+2, column=39).value = house_damage.SD_GR3_LV200_300
                ws.cell(row=i+2, column=40).value = house_damage.SD_GR3_LV300
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_damage.xlsx"'
    except:
        raise Http404("[ERROR] download_house_damage().")
    return response

###############################################################################
### download_household_damage関数
### 17: 家庭用品自動車以外被害率
###############################################################################
def download_household_damage(request):
    try:
        household_damage_list = HOUSEHOLD_DAMAGE.objects.order_by('HOUSEHOLD_DAMAGE_CODE')[:]
    
        file_path_to_load = 'static/household_damage.xlsx'
        file_path_to_save = 'static/household_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '家庭用品自動車以外被害率コード'
        ws.cell(row=1, column=2).value = '家庭用品自動車以外被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '被害率_土砂_床下'
        ws.cell(row=1, column=12).value = '被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '被害率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '家庭用品自動車以外所有額'
        
        if household_damage_list:
            for i, house_damage in enumerate(household_damage_list):
                ws.cell(row=i+2, column=1).value = household_damage.HOUSEHOLD_DAMAGE_CODE
                ws.cell(row=i+2, column=2).value = household_damage.HOUSEHOLD_DAMAGE_YEAR
                ws.cell(row=i+2, column=3).value = household_damage.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = household_damage.END_DATE
                
                ws.cell(row=i+2, column=5).value = household_damage.FL_LV00
                ws.cell(row=i+2, column=6).value = household_damage.FL_LV00_50
                ws.cell(row=i+2, column=7).value = household_damage.FL_LV50_100
                ws.cell(row=i+2, column=8).value = household_damage.FL_LV100_200
                ws.cell(row=i+2, column=9).value = household_damage.FL_LV200_300
                ws.cell(row=i+2, column=10).value = household_damage.FL_LV300
        
                ws.cell(row=i+2, column=11).value = household_damage.SD_LV00
                ws.cell(row=i+2, column=12).value = household_damage.SD_LV00_50
                ws.cell(row=i+2, column=13).value = household_damage.SD_LV50_100
                ws.cell(row=i+2, column=14).value = household_damage.SD_LV100_200
                ws.cell(row=i+2, column=15).value = household_damage.SD_LV200_300
                ws.cell(row=i+2, column=16).value = household_damage.SD_LV300

                ws.cell(row=i+2, column=17).value = household_damage.HOUSEHOLD_ASSET
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="household_damage.xlsx"'
    except:
        raise Http404("[ERROR] download_household_damage().")
    return response

###############################################################################
### download_car_damage関数
### 18: 家庭用品自動車被害率
###############################################################################
def download_car_damage(request):
    try:
        car_damage_list = CAR_DAMAGE.objects.order_by('CAR_DAMAGE_CODE')[:]
    
        file_path_to_load = 'static/car_damage.xlsx'
        file_path_to_save = 'static/car_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '自動車被害率コード'
        ws.cell(row=1, column=2).value = '自動車被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '家庭用品自動車所有額'
        
        if car_damage_list:
            for i, car_damage in enumerate(car_damage_list):
                ws.cell(row=i+2, column=1).value = car_damage.CAR_DAMAGE_CODE
                ws.cell(row=i+2, column=2).value = car_damage.CAR_DAMAGE_YEAR
                ws.cell(row=i+2, column=3).value = car_damage.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = car_damage.END_DATE
                
                ws.cell(row=i+2, column=5).value = car_damage.FL_LV00
                ws.cell(row=i+2, column=6).value = car_damage.FL_LV00_50
                ws.cell(row=i+2, column=7).value = car_damage.FL_LV50_100
                ws.cell(row=i+2, column=8).value = car_damage.FL_LV100_200
                ws.cell(row=i+2, column=9).value = car_damage.FL_LV200_300
                ws.cell(row=i+2, column=10).value = car_damage.FL_LV300

                ws.cell(row=i+2, column=11).value = car_damage.CAR_ASSET
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car_damage.xlsx"'
    except:
        raise Http404("[ERROR] download_car_damage().")
    return response

###############################################################################
### download_house_cost関数
### 19: 家庭応急対策費
###############################################################################
def download_house_cost(request):
    try:
        house_cost_list = HOUSE_COST.objects.order_by('HOUSE_COST_CODE')[:]
    
        file_path_to_load = 'static/house_cost.xlsx'
        file_path_to_save = 'static/house_cost2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '家庭応急対策費コード'
        ws.cell(row=1, column=2).value = '家庭応急対策費対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '代替活動費_床下'
        ws.cell(row=1, column=6).value = '代替活動費_0から50cm未満'
        ws.cell(row=1, column=7).value = '代替活動費_50から100cm未満'
        ws.cell(row=1, column=8).value = '代替活動費_100から200cm未満'
        ws.cell(row=1, column=9).value = '代替活動費_200から300cm未満'
        ws.cell(row=1, column=10).value = '代替活動費_300cm以上'

        ws.cell(row=1, column=11).value = '清掃費_床下'
        ws.cell(row=1, column=12).value = '清掃費_0から50cm未満'
        ws.cell(row=1, column=13).value = '清掃費_50から100cm未満'
        ws.cell(row=1, column=14).value = '清掃費_100から200cm未満'
        ws.cell(row=1, column=15).value = '清掃費_200から300cm未満'
        ws.cell(row=1, column=16).value = '清掃費_300cm以上'

        ws.cell(row=1, column=17).value = '清掃労働単価'
        
        if house_cost_list:
            for i, house_cost in enumerate(house_cost_list):
                ws.cell(row=i+2, column=1).value = house_cost.HOUSE_COST_CODE
                ws.cell(row=i+2, column=2).value = house_cost.HOUSE_COST_YEAR
                ws.cell(row=i+2, column=3).value = house_cost.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = house_cost.END_DATE
                
                ws.cell(row=i+2, column=5).value = house_cost.ALT_LV00
                ws.cell(row=i+2, column=6).value = house_cost.ALT_LV00_50
                ws.cell(row=i+2, column=7).value = house_cost.ALT_LV50_100
                ws.cell(row=i+2, column=8).value = house_cost.ALT_LV100_200
                ws.cell(row=i+2, column=9).value = house_cost.ALT_LV200_300
                ws.cell(row=i+2, column=10).value = house_cost.ALT_LV300

                ws.cell(row=i+2, column=11).value = house_cost.CLEAN_LV00
                ws.cell(row=i+2, column=12).value = house_cost.CLEAN_LV00_50
                ws.cell(row=i+2, column=13).value = house_cost.CLEAN_LV50_100
                ws.cell(row=i+2, column=14).value = house_cost.CLEAN_LV100_200
                ws.cell(row=i+2, column=15).value = house_cost.CLEAN_LV200_300
                ws.cell(row=i+2, column=16).value = house_cost.CLEAN_LV300

                ws.cell(row=i+2, column=17).value = house_cost.HOUSE_COST
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="house_cost.xlsx"'
    except:
        raise Http404("[ERROR] download_house_cost().")
    return response

###############################################################################
### download_office_asset関数
### 20: 産業分類別資産額
###############################################################################
def download_office_asset(request):
    try:
        office_asset_list = OFFICE_ASSET.objects.order_by('OFFICE_ASSET_CODE')[:]
    
        file_path_to_load = 'static/office_asset.xlsx'
        file_path_to_save = 'static/office_asset2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '産業分類別資産額コード'
        ws.cell(row=1, column=2).value = '産業分類コード'
        ws.cell(row=1, column=3).value = '産業分類別資産額対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        
        ws.cell(row=1, column=6).value = '償却資産額'
        ws.cell(row=1, column=7).value = '在庫資産額'
        ws.cell(row=1, column=8).value = '付加価値額'
        
        if office_asset_list:
            for i, office_asset in enumerate(office_asset_list):
                ws.cell(row=i+2, column=1).value = office_asset.OFFICE_ASSET_CODE
                ws.cell(row=i+2, column=2).value = office_asset.INDUSTRY_CODE
                ws.cell(row=i+2, column=3).value = office_asset.OFFICE_ASSET_YEAR
                ws.cell(row=i+2, column=4).value = office_asset.BEGIN_DATE
                ws.cell(row=i+2, column=5).value = office_asset.END_DATE
                
                ws.cell(row=i+2, column=6).value = office_asset.DEPRECIABLE_ASSET
                ws.cell(row=i+2, column=7).value = office_asset.INVENTORY_ASSET
                ws.cell(row=i+2, column=8).value = office_asset.VALUE_ADDED
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_asset.xlsx"'
    except:
        raise Http404("[ERROR] download_office_asset().")
    return response

###############################################################################
### download_office_damage関数
### 21: 事業所被害率
###############################################################################
def download_office_damage(request):
    try:
        office_damage_list = OFFICE_DAMAGE.objects.order_by('OFFICE_DAMAGE_CODE')[:]
    
        file_path_to_load = 'static/office_damage.xlsx'
        file_path_to_save = 'static/office_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '事業所被害率コード'
        ws.cell(row=1, column=2).value = '事業所被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '償却資産率_浸水_床下'
        ws.cell(row=1, column=6).value = '償却資産率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '償却資産率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '償却資産率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '償却資産率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '償却資産率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '償却資産率_土砂_床下'
        ws.cell(row=1, column=12).value = '償却資産率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '償却資産率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '償却資産率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '償却資産率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '償却資産率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '在庫資産率_浸水_床下'
        ws.cell(row=1, column=18).value = '在庫資産率_浸水_0から50cm未満'
        ws.cell(row=1, column=19).value = '在庫資産率_浸水_50から100cm未満'
        ws.cell(row=1, column=20).value = '在庫資産率_浸水_100から200cm未満'
        ws.cell(row=1, column=21).value = '在庫資産率_浸水_200から300cm未満'
        ws.cell(row=1, column=22).value = '在庫資産率_浸水_300cm以上'

        ws.cell(row=1, column=23).value = '在庫資産率_土砂_床下'
        ws.cell(row=1, column=24).value = '在庫資産率_土砂_0から50cm未満'
        ws.cell(row=1, column=25).value = '在庫資産率_土砂_50から100cm未満'
        ws.cell(row=1, column=26).value = '在庫資産率_土砂_100から200cm未満'
        ws.cell(row=1, column=27).value = '在庫資産率_土砂_200から300cm未満'
        ws.cell(row=1, column=28).value = '在庫資産率_土砂_300cm以上'
        
        if office_damage_list:
            for i, office_damage in enumerate(office_damage_list):
                ws.cell(row=i+2, column=1).value = office_damage.OFFICE_DAMAGE_CODE
                ws.cell(row=i+2, column=2).value = office_damage.OFFICE_DAMAGE_YEAR
                ws.cell(row=i+2, column=3).value = office_damage.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = office_damage.END_DATE
                
                ws.cell(row=i+2, column=5).value = office_damage.DEP_FL_LV00
                ws.cell(row=i+2, column=6).value = office_damage.DEP_FL_LV00_50
                ws.cell(row=i+2, column=7).value = office_damage.DEP_FL_LV50_100
                ws.cell(row=i+2, column=8).value = office_damage.DEP_FL_LV100_200
                ws.cell(row=i+2, column=9).value = office_damage.DEP_FL_LV200_300
                ws.cell(row=i+2, column=10).value = office_damage.DEP_FL_LV300

                ws.cell(row=i+2, column=11).value = office_damage.DEP_SD_LV00
                ws.cell(row=i+2, column=12).value = office_damage.DEP_SD_LV00_50
                ws.cell(row=i+2, column=13).value = office_damage.DEP_SD_LV50_100
                ws.cell(row=i+2, column=14).value = office_damage.DEP_SD_LV100_200
                ws.cell(row=i+2, column=15).value = office_damage.DEP_SD_LV200_300
                ws.cell(row=i+2, column=16).value = office_damage.DEP_SD_LV300

                ws.cell(row=i+2, column=17).value = office_damage.INV_FL_LV00
                ws.cell(row=i+2, column=18).value = office_damage.INV_FL_LV00_50
                ws.cell(row=i+2, column=19).value = office_damage.INV_FL_LV50_100
                ws.cell(row=i+2, column=20).value = office_damage.INV_FL_LV100_200
                ws.cell(row=i+2, column=21).value = office_damage.INV_FL_LV200_300
                ws.cell(row=i+2, column=22).value = office_damage.INV_FL_LV300

                ws.cell(row=i+2, column=23).value = office_damage.INV_SD_LV00
                ws.cell(row=i+2, column=24).value = office_damage.INV_SD_LV00_50
                ws.cell(row=i+2, column=25).value = office_damage.INV_SD_LV50_100
                ws.cell(row=i+2, column=26).value = office_damage.INV_SD_LV100_200
                ws.cell(row=i+2, column=27).value = office_damage.INV_SD_LV200_300
                ws.cell(row=i+2, column=28).value = office_damage.INV_SD_LV300
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_damage.xlsx"'
    except:
        raise Http404("[ERROR] download_office_damage().")
    return response

###############################################################################
### download_office_cost関数
### 22: 事業所営業停止損失
###############################################################################
def download_office_cost(request):
    try:
        office_cost_list = OFFICE_COST.objects.order_by('OFFICE_COST_CODE')[:]
    
        file_path_to_load = 'static/office_cost.xlsx'
        file_path_to_save = 'static/office_cost2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '事業所営業損失コード'
        ws.cell(row=1, column=2).value = '事業所営業損失対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '営業停止日数_床下'
        ws.cell(row=1, column=6).value = '営業停止日数_0から50cm未満'
        ws.cell(row=1, column=7).value = '営業停止日数_50から100cm未満'
        ws.cell(row=1, column=8).value = '営業停止日数_100から200cm未満'
        ws.cell(row=1, column=9).value = '営業停止日数_200から300cm未満'
        ws.cell(row=1, column=10).value = '営業停止日数_300cm以上'

        ws.cell(row=1, column=11).value = '営業停滞日数_床下'
        ws.cell(row=1, column=12).value = '営業停滞日数_0から50cm未満'
        ws.cell(row=1, column=13).value = '営業停滞日数_50から100cm未満'
        ws.cell(row=1, column=14).value = '営業停滞日数_100から200cm未満'
        ws.cell(row=1, column=15).value = '営業停滞日数_200から300cm未満'
        ws.cell(row=1, column=16).value = 'cccccc'
        
        if office_cost_list:
            for i, office_cost in enumerate(office_cost_list):
                ws.cell(row=i+2, column=1).value = office_cost.OFFICE_COST_CODE
                ws.cell(row=i+2, column=2).value = office_cost.OFFICE_COST_YEAR
                ws.cell(row=i+2, column=3).value = office_cost.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = office_cost.END_DATE
                
                ws.cell(row=i+2, column=5).value = office_cost.SUSPEND_LV00
                ws.cell(row=i+2, column=6).value = office_cost.SUSPEND_LV00_50
                ws.cell(row=i+2, column=7).value = office_cost.SUSPEND_LV50_100
                ws.cell(row=i+2, column=8).value = office_cost.SUSPEND_LV100_200
                ws.cell(row=i+2, column=9).value = office_cost.SUSPEND_LV200_300
                ws.cell(row=i+2, column=10).value = office_cost.SUSPEND_LV300

                ws.cell(row=i+2, column=11).value = office_cost.STAGNATE_LV00
                ws.cell(row=i+2, column=12).value = office_cost.STAGNATE_LV00_50
                ws.cell(row=i+2, column=13).value = office_cost.STAGNATE_LV50_100
                ws.cell(row=i+2, column=14).value = office_cost.STAGNATE_LV100_200
                ws.cell(row=i+2, column=15).value = office_cost.STAGNATE_LV200_300
                ws.cell(row=i+2, column=16).value = office_cost.STAGNATE_LV300
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="office_cost.xlsx"'
    except:
        raise Http404("[ERROR] download_office_cost().")
    return response

###############################################################################
### download_farmer_fisher_damage関数
### 23: 農漁家被害率
###############################################################################
def download_farmer_fisher_damage(request):
    try:
        farmer_fisher_damage_list = FARMER_FISHER_DAMAGE.objects.order_by('FARMER_FISHER_DAMAGE_CODE')[:]
    
        file_path_to_load = 'static/farmer_fisher_damage.xlsx'
        file_path_to_save = 'static/farmer_fisher_damage2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '農漁家被害率コード'
        ws.cell(row=1, column=2).value = '農漁家被害率対象年'
        ws.cell(row=1, column=3).value = '開始日'
        ws.cell(row=1, column=4).value = '終了日'
        
        ws.cell(row=1, column=5).value = '償却資産被害率_浸水_床下'
        ws.cell(row=1, column=6).value = '償却資産被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=7).value = '償却資産被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=8).value = '償却資産被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=9).value = '償却資産被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=10).value = '償却資産被害率_浸水_300cm以上'

        ws.cell(row=1, column=11).value = '償却資産被害率_土砂_床下'
        ws.cell(row=1, column=12).value = '償却資産被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=13).value = '償却資産被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=14).value = '償却資産被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=15).value = '償却資産被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=16).value = '償却資産被害率_土砂_300cm以上'

        ws.cell(row=1, column=17).value = '在庫資産被害率_浸水_床下'
        ws.cell(row=1, column=18).value = '在庫資産被害率_浸水_0から50cm未満'
        ws.cell(row=1, column=19).value = '在庫資産被害率_浸水_50から100cm未満'
        ws.cell(row=1, column=20).value = '在庫資産被害率_浸水_100から200cm未満'
        ws.cell(row=1, column=21).value = '在庫資産被害率_浸水_200から300cm未満'
        ws.cell(row=1, column=22).value = '在庫資産被害率_浸水_300cm以上'

        ws.cell(row=1, column=23).value = '在庫資産被害率_土砂_床下'
        ws.cell(row=1, column=24).value = '在庫資産被害率_土砂_0から50cm未満'
        ws.cell(row=1, column=25).value = '在庫資産被害率_土砂_50から100cm未満'
        ws.cell(row=1, column=26).value = '在庫資産被害率_土砂_100から200cm未満'
        ws.cell(row=1, column=27).value = '在庫資産被害率_土砂_200から300cm未満'
        ws.cell(row=1, column=28).value = '在庫資産被害率_土砂_300cm以上'

        ws.cell(row=1, column=29).value = '農漁家償却資産額'
        ws.cell(row=1, column=30).value = '農漁家在庫資産額'
        
        if farmer_fisher_damage_list:
            for i, farmer_fisher_damage in enumerate(farmer_fisher_damage_list):
                ws.cell(row=i+2, column=1).value = farmer_fisher_damage.FARMER_FISHER_DAMAGE_CODE
                ws.cell(row=i+2, column=2).value = farmer_fisher_damage.FARMER_FISHER_DAMAGE_YEAR
                ws.cell(row=i+2, column=3).value = farmer_fisher_damage.BEGIN_DATE
                ws.cell(row=i+2, column=4).value = farmer_fisher_damage.END_DATE
                
                ws.cell(row=i+2, column=5).value = farmer_fisher_damage.DEP_FL_LV00
                ws.cell(row=i+2, column=6).value = farmer_fisher_damage.DEP_FL_LV00_50
                ws.cell(row=i+2, column=7).value = farmer_fisher_damage.DEP_FL_LV50_100
                ws.cell(row=i+2, column=8).value = farmer_fisher_damage.DEP_FL_LV100_200
                ws.cell(row=i+2, column=9).value = farmer_fisher_damage.DEP_FL_LV200_300
                ws.cell(row=i+2, column=10).value = farmer_fisher_damage.DEP_FL_LV300

                ws.cell(row=i+2, column=11).value = farmer_fisher_damage.DEP_SD_LV00
                ws.cell(row=i+2, column=12).value = farmer_fisher_damage.DEP_SD_LV00_50
                ws.cell(row=i+2, column=13).value = farmer_fisher_damage.DEP_SD_LV50_100
                ws.cell(row=i+2, column=14).value = farmer_fisher_damage.DEP_SD_LV100_200
                ws.cell(row=i+2, column=15).value = farmer_fisher_damage.DEP_SD_LV200_300
                ws.cell(row=i+2, column=16).value = farmer_fisher_damage.DEP_SD_LV300
        
                ws.cell(row=i+2, column=17).value = farmer_fisher_damage.INV_FL_LV00
                ws.cell(row=i+2, column=18).value = farmer_fisher_damage.INV_FL_LV00_50
                ws.cell(row=i+2, column=19).value = farmer_fisher_damage.INV_FL_LV50_100
                ws.cell(row=i+2, column=20).value = farmer_fisher_damage.INV_FL_LV100_200
                ws.cell(row=i+2, column=21).value = farmer_fisher_damage.INV_FL_LV200_300
                ws.cell(row=i+2, column=22).value = farmer_fisher_damage.INV_FL_LV300

                ws.cell(row=i+2, column=23).value = farmer_fisher_damage.INV_SD_LV00
                ws.cell(row=i+2, column=24).value = farmer_fisher_damage.INV_SD_LV00_50
                ws.cell(row=i+2, column=25).value = farmer_fisher_damage.INV_SD_LV50_100
                ws.cell(row=i+2, column=26).value = farmer_fisher_damage.INV_SD_LV100_200
                ws.cell(row=i+2, column=27).value = farmer_fisher_damage.INV_SD_LV200_300
                ws.cell(row=i+2, column=28).value = farmer_fisher_damage.INV_SD_LV300

                ws.cell(row=i+2, column=29).value = farmer_fisher_damage.DEPRECIABLE_ASSET
                ws.cell(row=i+2, column=30).value = farmer_fisher_damage.INVENTORY_ASSET
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="farmer_fisher_damage.xlsx"'
    except:
        raise Http404("[ERROR] download_farmer_fisher_damage().")
    return response

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_weather関数
### 24: 異常気象
###############################################################################
def download_weather(request):
    try:
        weather_list = WEATHER.objects.order_by('WEATHER_ID')[:]
    
        file_path_to_load = 'static/weather.xlsx'
        file_path_to_save = 'static/weather2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '異常気象ID'
        ws.cell(row=1, column=2).value = '異常気象名'
        ws.cell(row=1, column=3).value = '異常気象対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        
        if weather_list:
            for i, weather in enumerate(weather_list):
                ws.cell(row=i+2, column=1).value = weather.WEATHER_ID
                ws.cell(row=i+2, column=2).value = weather.WEATHER_NAME
                ws.cell(row=i+2, column=3).value = weather.WEATHER_YEAR
                ws.cell(row=i+2, column=4).value = weather.BEGIN_DATE
                ws.cell(row=i+2, column=5).value = weather.END_DATE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="weather.xlsx"'
    except:
        raise Http404("[ERROR] download_weather().")
    return response

###############################################################################
### download_area関数
### 25: 区域
###############################################################################
def download_area(request):
    try:
        area_list = AREA.objects.order_by('AREA_ID')[:]
    
        file_path_to_load = 'static/area.xlsx'
        file_path_to_save = 'static/area2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '区域ID'
        ws.cell(row=1, column=2).value = '区域名'
        ws.cell(row=1, column=3).value = '区域対象年'
        ws.cell(row=1, column=4).value = '開始日'
        ws.cell(row=1, column=5).value = '終了日'
        ws.cell(row=1, column=6).value = '農地面積'
        ws.cell(row=1, column=7).value = '地下面積'
        ws.cell(row=1, column=8).value = '農作物被害額'
        
        if area_list:
            for i, area in enumerate(area_list):
                ws.cell(row=i+2, column=1).value = area.AREA_ID
                ws.cell(row=i+2, column=2).value = area.AREA_NAME
                ws.cell(row=i+2, column=3).value = area.AREA_YEAR
                ws.cell(row=i+2, column=4).value = area.BEGIN_DATE
                ws.cell(row=i+2, column=5).value = area.END_DATE
                ws.cell(row=i+2, column=6).value = area.AGRI_AREA
                ws.cell(row=i+2, column=7).value = area.UNDERGROUND_AREA
                ws.cell(row=i+2, column=8).value = area.CROP_DAMAGE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="area.xlsx"'
    except:
        raise Http404("[ERROR] download_area().")
    return response

###############################################################################
### download_ippan_chosa関数
### 2601: 一般資産調査票（調査員用）
###############################################################################
def download_ippan_chosa(request):
    try:
        file_path_to_load = 'static/ippan_chosa1.xlsx'
        file_path_to_save = 'static/ippan_chosa2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load, keep_vba=False)

        ws_building = wb["BUILDING"]
        ws_ken = wb["KEN"]
        ws_city = wb["CITY"]
        ws_kasen_kaigan = wb["KASEN_KAIGAN"]
        ws_suikei = wb["SUIKEI"]
        ws_suikei_type = wb["SUIKEI_TYPE"]
        ws_kasen = wb["KASEN"]
        ws_kasen_type = wb["KASEN_TYPE"]
        ws_cause = wb["CAUSE"]
        ws_underground = wb["UNDERGROUND"]
        ws_usage = wb["USAGE"]
        ws_flood_sediment = wb["FLOOD_SEDIMENT"]
        ws_gradient = wb["GRADIENT"]
        ws_industry = wb["INDUSTRY"]
        ws_area = wb["AREA"]
        ws_ippan = wb["IPPAN"]

        ws_city_vlook = wb["CITY_VLOOK"]
        
        ### 01: 建物区分
        building_list = BUILDING.objects.order_by('BUILDING_CODE')[:]
        if building_list:
            for i, building in enumerate(building_list):
                ws_building.cell(row=i+1, column=1).value = building.BUILDING_CODE
                ws_building.cell(row=i+1, column=2).value = building.BUILDING_NAME

        ### 02: 都道府県
        ken_list = KEN.objects.order_by('KEN_CODE')[:]
        if ken_list:
            for i, ken in enumerate(ken_list):
                ws_ken.cell(row=i+1, column=1).value = ken.KEN_CODE
                ws_ken.cell(row=i+1, column=2).value = ken.KEN_NAME
                
                ws_city_vlook.cell(row=i+1, column=1).value = ken.KEN_NAME
        
        city_list01 = CITY.objects.filter(KEN_CODE='01').order_by('CITY_CODE')
        city_list02 = CITY.objects.filter(KEN_CODE='02').order_by('CITY_CODE')
        city_list03 = CITY.objects.filter(KEN_CODE='03').order_by('CITY_CODE')
        city_list04 = CITY.objects.filter(KEN_CODE='04').order_by('CITY_CODE')
        city_list05 = CITY.objects.filter(KEN_CODE='05').order_by('CITY_CODE')
        city_list06 = CITY.objects.filter(KEN_CODE='06').order_by('CITY_CODE')
        city_list07 = CITY.objects.filter(KEN_CODE='07').order_by('CITY_CODE')
        city_list08 = CITY.objects.filter(KEN_CODE='08').order_by('CITY_CODE')
        city_list09 = CITY.objects.filter(KEN_CODE='09').order_by('CITY_CODE')
        city_list10 = CITY.objects.filter(KEN_CODE='10').order_by('CITY_CODE')
        city_list11 = CITY.objects.filter(KEN_CODE='11').order_by('CITY_CODE')
        city_list12 = CITY.objects.filter(KEN_CODE='12').order_by('CITY_CODE')
        city_list13 = CITY.objects.filter(KEN_CODE='13').order_by('CITY_CODE')
        city_list14 = CITY.objects.filter(KEN_CODE='14').order_by('CITY_CODE')
        city_list15 = CITY.objects.filter(KEN_CODE='15').order_by('CITY_CODE')
        city_list16 = CITY.objects.filter(KEN_CODE='16').order_by('CITY_CODE')
        city_list17 = CITY.objects.filter(KEN_CODE='17').order_by('CITY_CODE')
        city_list18 = CITY.objects.filter(KEN_CODE='18').order_by('CITY_CODE')
        city_list19 = CITY.objects.filter(KEN_CODE='19').order_by('CITY_CODE')
        city_list20 = CITY.objects.filter(KEN_CODE='20').order_by('CITY_CODE')
        city_list21 = CITY.objects.filter(KEN_CODE='21').order_by('CITY_CODE')
        city_list22 = CITY.objects.filter(KEN_CODE='22').order_by('CITY_CODE')
        city_list23 = CITY.objects.filter(KEN_CODE='23').order_by('CITY_CODE')
        city_list24 = CITY.objects.filter(KEN_CODE='24').order_by('CITY_CODE')
        city_list25 = CITY.objects.filter(KEN_CODE='25').order_by('CITY_CODE')
        city_list26 = CITY.objects.filter(KEN_CODE='26').order_by('CITY_CODE')
        city_list27 = CITY.objects.filter(KEN_CODE='27').order_by('CITY_CODE')
        city_list28 = CITY.objects.filter(KEN_CODE='28').order_by('CITY_CODE')
        city_list29 = CITY.objects.filter(KEN_CODE='29').order_by('CITY_CODE')
        city_list30 = CITY.objects.filter(KEN_CODE='30').order_by('CITY_CODE')
        city_list31 = CITY.objects.filter(KEN_CODE='31').order_by('CITY_CODE')
        city_list32 = CITY.objects.filter(KEN_CODE='32').order_by('CITY_CODE')
        city_list33 = CITY.objects.filter(KEN_CODE='33').order_by('CITY_CODE')
        city_list34 = CITY.objects.filter(KEN_CODE='34').order_by('CITY_CODE')
        city_list35 = CITY.objects.filter(KEN_CODE='35').order_by('CITY_CODE')
        city_list36 = CITY.objects.filter(KEN_CODE='36').order_by('CITY_CODE')
        city_list37 = CITY.objects.filter(KEN_CODE='37').order_by('CITY_CODE')
        city_list38 = CITY.objects.filter(KEN_CODE='38').order_by('CITY_CODE')
        city_list39 = CITY.objects.filter(KEN_CODE='39').order_by('CITY_CODE')
        city_list40 = CITY.objects.filter(KEN_CODE='40').order_by('CITY_CODE')
        city_list41 = CITY.objects.filter(KEN_CODE='41').order_by('CITY_CODE')
        city_list42 = CITY.objects.filter(KEN_CODE='42').order_by('CITY_CODE')
        city_list43 = CITY.objects.filter(KEN_CODE='43').order_by('CITY_CODE')
        city_list44 = CITY.objects.filter(KEN_CODE='44').order_by('CITY_CODE')
        city_list45 = CITY.objects.filter(KEN_CODE='45').order_by('CITY_CODE')
        city_list46 = CITY.objects.filter(KEN_CODE='46').order_by('CITY_CODE')
        city_list47 = CITY.objects.filter(KEN_CODE='47').order_by('CITY_CODE')
        
        ws_city_vlook.cell(row=1, column=2).value = 'CITY!$B$1:$B$%d' % len(city_list01)
        ws_city_vlook.cell(row=2, column=2).value = 'CITY!$G$1:$G$%d' % len(city_list02)
        ws_city_vlook.cell(row=3, column=2).value = 'CITY!$L$1:$L$%d' % len(city_list03)
        ws_city_vlook.cell(row=4, column=2).value = 'CITY!$Q$1:$Q$%d' % len(city_list04)
        ws_city_vlook.cell(row=5, column=2).value = 'CITY!$V$1:$V$%d' % len(city_list05)
        ws_city_vlook.cell(row=6, column=2).value = 'CITY!$AA$1:$AA$%d' % len(city_list06)
        ws_city_vlook.cell(row=7, column=2).value = 'CITY!$AF$1:$AF$%d' % len(city_list07)
        ws_city_vlook.cell(row=8, column=2).value = 'CITY!$AK$1:$AK$%d' % len(city_list08)
        ws_city_vlook.cell(row=9, column=2).value = 'CITY!$AP$1:$AP$%d' % len(city_list09)
        ws_city_vlook.cell(row=10, column=2).value = 'CITY!$AU$1:$AU$%d' % len(city_list10)
        ws_city_vlook.cell(row=11, column=2).value = 'CITY!$AZ$1:$AZ$%d' % len(city_list11)
        ws_city_vlook.cell(row=12, column=2).value = 'CITY!$BE$1:$BE$%d' % len(city_list12)
        ws_city_vlook.cell(row=13, column=2).value = 'CITY!$BJ$1:$BJ$%d' % len(city_list13)
        
        ws_city_vlook.cell(row=14, column=2).value = 'CITY!$BO$1:$BO$%d' % len(city_list14)
        ws_city_vlook.cell(row=15, column=2).value = 'CITY!$BT$1:$BT$%d' % len(city_list15)
        ws_city_vlook.cell(row=16, column=2).value = 'CITY!$BY$1:$BY$%d' % len(city_list16)
        ws_city_vlook.cell(row=17, column=2).value = 'CITY!$CD$1:$CD$%d' % len(city_list17)
        ws_city_vlook.cell(row=18, column=2).value = 'CITY!$CI$1:$CI$%d' % len(city_list18)
        ws_city_vlook.cell(row=19, column=2).value = 'CITY!$CN$1:$CN$%d' % len(city_list19)
        ws_city_vlook.cell(row=20, column=2).value = 'CITY!$CS$1:$CS$%d' % len(city_list20)
        ws_city_vlook.cell(row=21, column=2).value = 'CITY!$CX$1:$CX$%d' % len(city_list21)
        ws_city_vlook.cell(row=22, column=2).value = 'CITY!$DC$1:$DC$%d' % len(city_list22)
        ws_city_vlook.cell(row=23, column=2).value = 'CITY!$DH$1:$DH$%d' % len(city_list23)
        ws_city_vlook.cell(row=24, column=2).value = 'CITY!$DM$1:$DM$%d' % len(city_list24)
        ws_city_vlook.cell(row=25, column=2).value = 'CITY!$DR$1:$DR$%d' % len(city_list25)
        ws_city_vlook.cell(row=26, column=2).value = 'CITY!$DW$1:$DW$%d' % len(city_list26)
        
        ws_city_vlook.cell(row=27, column=2).value = 'CITY!$EB$1:$EB$%d' % len(city_list27)
        ws_city_vlook.cell(row=28, column=2).value = 'CITY!$EG$1:$EG$%d' % len(city_list28)
        ws_city_vlook.cell(row=29, column=2).value = 'CITY!$EL$1:$EL$%d' % len(city_list29)
        ws_city_vlook.cell(row=30, column=2).value = 'CITY!$EQ$1:$EQ$%d' % len(city_list30)
        ws_city_vlook.cell(row=31, column=2).value = 'CITY!$EV$1:$EV$%d' % len(city_list31)
        ws_city_vlook.cell(row=32, column=2).value = 'CITY!$FA$1:$FA$%d' % len(city_list32)
        ws_city_vlook.cell(row=33, column=2).value = 'CITY!$FF$1:$FF$%d' % len(city_list33)
        ws_city_vlook.cell(row=34, column=2).value = 'CITY!$FK$1:$FK$%d' % len(city_list34)
        ws_city_vlook.cell(row=35, column=2).value = 'CITY!$FP$1:$FP$%d' % len(city_list35)
        ws_city_vlook.cell(row=36, column=2).value = 'CITY!$FU$1:$FU$%d' % len(city_list36)
        ws_city_vlook.cell(row=37, column=2).value = 'CITY!$FZ$1:$FZ$%d' % len(city_list37)
        ws_city_vlook.cell(row=38, column=2).value = 'CITY!$GE$1:$GE$%d' % len(city_list38)
        ws_city_vlook.cell(row=39, column=2).value = 'CITY!$GJ$1:$GJ$%d' % len(city_list39)
        
        ws_city_vlook.cell(row=40, column=2).value = 'CITY!$GO$1:$GO$%d' % len(city_list40)
        ws_city_vlook.cell(row=41, column=2).value = 'CITY!$GT$1:$GT$%d' % len(city_list41)
        ws_city_vlook.cell(row=42, column=2).value = 'CITY!$GY$1:$GY$%d' % len(city_list42)
        ws_city_vlook.cell(row=43, column=2).value = 'CITY!$HD$1:$HD$%d' % len(city_list43)
        ws_city_vlook.cell(row=44, column=2).value = 'CITY!$HI$1:$HI$%d' % len(city_list44)
        ws_city_vlook.cell(row=45, column=2).value = 'CITY!$HN$1:$HN$%d' % len(city_list45)
        ws_city_vlook.cell(row=46, column=2).value = 'CITY!$HS$1:$HS$%d' % len(city_list46)
        ws_city_vlook.cell(row=47, column=2).value = 'CITY!$HX$1:$HX$%d' % len(city_list47)

        ### 03: 市区町村
        ### city_list = CITY.objects.order_by('CITY_CODE')[:]
        if city_list01:
            for i, city in enumerate(city_list01):
                ws_city.cell(row=i+1, column=1).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=2).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=3).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=4).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=5).value = city.CITY_AREA

        if city_list02:
            for i, city in enumerate(city_list02):
                ws_city.cell(row=i+1, column=6).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=7).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=8).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=9).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=10).value = city.CITY_AREA

        if city_list03:
            for i, city in enumerate(city_list03):
                ws_city.cell(row=i+1, column=11).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=12).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=13).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=14).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=15).value = city.CITY_AREA

        if city_list04:
            for i, city in enumerate(city_list04):
                ws_city.cell(row=i+1, column=16).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=17).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=18).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=19).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=20).value = city.CITY_AREA

        if city_list05:
            for i, city in enumerate(city_list05):
                ws_city.cell(row=i+1, column=21).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=22).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=23).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=24).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=25).value = city.CITY_AREA

        if city_list06:
            for i, city in enumerate(city_list06):
                ws_city.cell(row=i+1, column=26).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=27).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=28).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=29).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=30).value = city.CITY_AREA

        if city_list07:
            for i, city in enumerate(city_list07):
                ws_city.cell(row=i+1, column=31).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=32).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=33).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=34).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=35).value = city.CITY_AREA

        if city_list08:
            for i, city in enumerate(city_list08):
                ws_city.cell(row=i+1, column=36).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=37).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=38).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=39).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=40).value = city.CITY_AREA

        if city_list09:
            for i, city in enumerate(city_list09):
                ws_city.cell(row=i+1, column=41).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=42).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=43).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=44).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=45).value = city.CITY_AREA

        if city_list10:
            for i, city in enumerate(city_list10):
                ws_city.cell(row=i+1, column=46).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=47).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=48).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=49).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=50).value = city.CITY_AREA

        if city_list11:
            for i, city in enumerate(city_list11):
                ws_city.cell(row=i+1, column=51).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=52).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=53).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=54).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=55).value = city.CITY_AREA

        if city_list12:
            for i, city in enumerate(city_list12):
                ws_city.cell(row=i+1, column=56).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=57).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=58).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=59).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=60).value = city.CITY_AREA

        if city_list13:
            for i, city in enumerate(city_list13):
                ws_city.cell(row=i+1, column=61).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=62).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=63).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=64).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=65).value = city.CITY_AREA

        if city_list14:
            for i, city in enumerate(city_list14):
                ws_city.cell(row=i+1, column=66).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=67).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=68).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=69).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=70).value = city.CITY_AREA

        if city_list15:
            for i, city in enumerate(city_list15):
                ws_city.cell(row=i+1, column=71).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=72).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=73).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=74).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=75).value = city.CITY_AREA

        if city_list16:
            for i, city in enumerate(city_list16):
                ws_city.cell(row=i+1, column=76).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=77).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=78).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=79).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=80).value = city.CITY_AREA

        if city_list17:
            for i, city in enumerate(city_list17):
                ws_city.cell(row=i+1, column=81).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=82).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=83).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=84).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=85).value = city.CITY_AREA

        if city_list18:
            for i, city in enumerate(city_list18):
                ws_city.cell(row=i+1, column=86).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=87).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=88).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=89).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=90).value = city.CITY_AREA

        if city_list19:
            for i, city in enumerate(city_list19):
                ws_city.cell(row=i+1, column=91).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=92).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=93).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=94).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=95).value = city.CITY_AREA

        if city_list20:
            for i, city in enumerate(city_list20):
                ws_city.cell(row=i+1, column=96).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=97).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=98).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=99).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=100).value = city.CITY_AREA

        if city_list21:
            for i, city in enumerate(city_list21):
                ws_city.cell(row=i+1, column=101).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=102).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=103).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=104).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=105).value = city.CITY_AREA

        if city_list22:
            for i, city in enumerate(city_list22):
                ws_city.cell(row=i+1, column=106).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=107).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=108).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=109).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=110).value = city.CITY_AREA

        if city_list23:
            for i, city in enumerate(city_list23):
                ws_city.cell(row=i+1, column=111).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=112).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=113).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=114).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=115).value = city.CITY_AREA

        if city_list24:
            for i, city in enumerate(city_list24):
                ws_city.cell(row=i+1, column=116).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=117).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=118).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=119).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=120).value = city.CITY_AREA

        if city_list25:
            for i, city in enumerate(city_list25):
                ws_city.cell(row=i+1, column=121).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=122).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=123).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=124).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=125).value = city.CITY_AREA

        if city_list26:
            for i, city in enumerate(city_list26):
                ws_city.cell(row=i+1, column=126).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=127).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=128).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=129).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=130).value = city.CITY_AREA

        if city_list27:
            for i, city in enumerate(city_list27):
                ws_city.cell(row=i+1, column=131).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=132).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=133).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=134).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=135).value = city.CITY_AREA

        if city_list28:
            for i, city in enumerate(city_list28):
                ws_city.cell(row=i+1, column=136).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=137).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=138).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=139).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=140).value = city.CITY_AREA

        if city_list29:
            for i, city in enumerate(city_list29):
                ws_city.cell(row=i+1, column=141).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=142).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=143).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=144).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=145).value = city.CITY_AREA

        if city_list30:
            for i, city in enumerate(city_list30):
                ws_city.cell(row=i+1, column=146).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=147).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=148).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=149).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=150).value = city.CITY_AREA

        if city_list31:
            for i, city in enumerate(city_list31):
                ws_city.cell(row=i+1, column=151).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=152).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=153).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=154).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=155).value = city.CITY_AREA

        if city_list32:
            for i, city in enumerate(city_list32):
                ws_city.cell(row=i+1, column=156).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=157).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=158).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=159).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=160).value = city.CITY_AREA

        if city_list33:
            for i, city in enumerate(city_list33):
                ws_city.cell(row=i+1, column=161).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=162).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=163).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=164).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=165).value = city.CITY_AREA

        if city_list34:
            for i, city in enumerate(city_list34):
                ws_city.cell(row=i+1, column=166).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=167).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=168).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=160).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=170).value = city.CITY_AREA

        if city_list35:
            for i, city in enumerate(city_list35):
                ws_city.cell(row=i+1, column=171).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=172).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=173).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=174).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=175).value = city.CITY_AREA

        if city_list36:
            for i, city in enumerate(city_list36):
                ws_city.cell(row=i+1, column=176).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=177).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=178).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=179).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=180).value = city.CITY_AREA

        if city_list37:
            for i, city in enumerate(city_list37):
                ws_city.cell(row=i+1, column=181).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=182).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=183).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=184).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=185).value = city.CITY_AREA

        if city_list38:
            for i, city in enumerate(city_list38):
                ws_city.cell(row=i+1, column=186).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=187).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=188).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=189).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=190).value = city.CITY_AREA

        if city_list39:
            for i, city in enumerate(city_list39):
                ws_city.cell(row=i+1, column=191).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=192).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=193).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=194).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=195).value = city.CITY_AREA

        if city_list40:
            for i, city in enumerate(city_list40):
                ws_city.cell(row=i+1, column=196).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=197).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=198).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=199).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=200).value = city.CITY_AREA

        if city_list41:
            for i, city in enumerate(city_list41):
                ws_city.cell(row=i+1, column=201).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=202).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=203).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=204).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=205).value = city.CITY_AREA

        if city_list42:
            for i, city in enumerate(city_list42):
                ws_city.cell(row=i+1, column=206).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=207).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=208).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=209).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=210).value = city.CITY_AREA

        if city_list43:
            for i, city in enumerate(city_list43):
                ws_city.cell(row=i+1, column=211).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=212).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=213).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=214).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=215).value = city.CITY_AREA

        if city_list44:
            for i, city in enumerate(city_list44):
                ws_city.cell(row=i+1, column=216).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=217).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=218).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=219).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=220).value = city.CITY_AREA

        if city_list45:
            for i, city in enumerate(city_list45):
                ws_city.cell(row=i+1, column=221).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=222).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=223).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=224).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=225).value = city.CITY_AREA

        if city_list46:
            for i, city in enumerate(city_list46):
                ws_city.cell(row=i+1, column=226).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=227).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=228).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=229).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=230).value = city.CITY_AREA

        if city_list47:
            for i, city in enumerate(city_list47):
                ws_city.cell(row=i+1, column=231).value = city.CITY_CODE
                ws_city.cell(row=i+1, column=232).value = city.CITY_NAME
                ws_city.cell(row=i+1, column=233).value = city.KEN_CODE
                ws_city.cell(row=i+1, column=234).value = city.CITY_POPULATION
                ws_city.cell(row=i+1, column=235).value = city.CITY_AREA

        ### 04: 水害発生地点工種（河川海岸区分）
        kasen_kaigan_list = KASEN_KAIGAN.objects.order_by('KASEN_KAIGAN_CODE')[:]
        if kasen_kaigan_list:
            for i, kasen_kaigan in enumerate(kasen_kaigan_list):
                ws_kasen_kaigan.cell(row=i+1, column=1).value = kasen_kaigan.KASEN_KAIGAN_CODE
                ws_kasen_kaigan.cell(row=i+1, column=2).value = kasen_kaigan.KASEN_KAIGAN_NAME

        ### 05: 水系（水系・沿岸）
        suikei_list = SUIKEI.objects.order_by('SUIKEI_CODE')[:]
        if suikei_list:
            for i, suikei in enumerate(suikei_list):
                ws_suikei.cell(row=i+1, column=1).value = suikei.SUIKEI_CODE
                ws_suikei.cell(row=i+1, column=2).value = suikei.SUIKEI_NAME
                ws_suikei.cell(row=i+1, column=3).value = suikei.SUIKEI_TYPE_CODE

        ### 06: 水系種別（水系・沿岸種別）
        suikei_type_list = SUIKEI_TYPE.objects.order_by('SUIKEI_TYPE_CODE')[:]
        if suikei_type_list:
            for i, suikei_type in enumerate(suikei_type_list):
                ws_suikei_type.cell(row=i+1, column=1).value = suikei_type.SUIKEI_TYPE_CODE
                ws_suikei_type.cell(row=i+1, column=2).value = suikei_type.SUIKEI_TYPE_NAME

        ### 07: 河川（河川・海岸）
        kasen_list = KASEN.objects.order_by('KASEN_CODE')[:]
        if kasen_list:
            for i, kasen in enumerate(kasen_list):
                ws_kasen.cell(row=i+1, column=1).value = kasen.KASEN_CODE
                ws_kasen.cell(row=i+1, column=2).value = kasen.KASEN_NAME
                ws_kasen.cell(row=i+1, column=3).value = kasen.KASEN_TYPE_CODE
                ws_kasen.cell(row=i+1, column=4).value = kasen.SUIKEI_CODE
                
        ### 08: 河川種別（河川・海岸種別）
        kasen_type_list = KASEN_TYPE.objects.order_by('KASEN_TYPE_CODE')[:]
        if kasen_type_list:
            for i, kasen_type in enumerate(kasen_type_list):
                ws_kasen_type.cell(row=i+1, column=1).value = kasen_type.KASEN_TYPE_CODE
                ws_kasen_type.cell(row=i+1, column=2).value = kasen_type.KASEN_TYPE_NAME
        
        ### 09: 水害原因
        cause_list = CAUSE.objects.order_by('CAUSE_CODE')[:]
        if cause_list:
            for i, cause in enumerate(cause_list):
                ws_cause.cell(row=i+1, column=1).value = cause.CAUSE_CODE
                ws_cause.cell(row=i+1, column=2).value = cause.CAUSE_NAME
                
        ### 10: 地上地下区分
        underground_list = UNDERGROUND.objects.order_by('UNDERGROUND_CODE')[:]
        if underground_list:
            for i, underground in enumerate(underground_list):
                ws_underground.cell(row=i+1, column=1).value = underground.UNDERGROUND_CODE
                ws_underground.cell(row=i+1, column=2).value = underground.UNDERGROUND_NAME
        
        ### 11: 地下空間の利用形態
        usage_list = USAGE.objects.order_by('USAGE_CODE')[:]
        if usage_list:
            for i, usage in enumerate(usage_list):
                ws_usage.cell(row=i+1, column=1).value = usage.USAGE_CODE
                ws_usage.cell(row=i+1, column=2).value = usage.USAGE_NAME
        
        ### 12: 浸水土砂区分
        flood_sediment_list = FLOOD_SEDIMENT.objects.order_by('FLOOD_SEDIMENT_CODE')[:]
        if flood_sediment_list:
            for i, flood_sediment in enumerate(flood_sediment_list):
                ws_flood_sediment.cell(row=i+1, column=1).value = flood_sediment.FLOOD_SEDIMENT_CODE
                ws_flood_sediment.cell(row=i+1, column=2).value = flood_sediment.FLOOD_SEDIMENT_NAME
        
        ### 13: 地盤勾配区分
        gradient_list = GRADIENT.objects.order_by('GRADIENT_CODE')[:]
        if gradient_list:
            for i, gradient in enumerate(gradient_list):
                ws_gradient.cell(row=i+1, column=1).value = gradient.GRADIENT_CODE
                ws_gradient.cell(row=i+1, column=2).value = gradient.GRADIENT_NAME
        
        ### 14: 産業分類
        industry_list = INDUSTRY.objects.order_by('INDUSTRY_CODE')[:]
        if industry_list:
            for i, industry in enumerate(industry_list):
                ws_industry.cell(row=i+1, column=1).value = industry.INDUSTRY_CODE
                ws_industry.cell(row=i+1, column=2).value = industry.INDUSTRY_NAME
        
        ### 25: 区域
        area_list = AREA.objects.order_by('AREA_ID')[:]
        if area_list:
            for i, area in enumerate(area_list):
                ws_area.cell(row=i+1, column=1).value = area.AREA_ID
                ws_area.cell(row=i+1, column=2).value = area.AREA_NAME
                ws_area.cell(row=i+1, column=3).value = area.AREA_YEAR
                ws_area.cell(row=i+1, column=4).value = area.BEGIN_DATE
                ws_area.cell(row=i+1, column=5).value = area.END_DATE
                ws_area.cell(row=i+1, column=6).value = area.AGRI_AREA
                ws_area.cell(row=i+1, column=7).value = area.UNDERGROUND_AREA
                ws_area.cell(row=i+1, column=8).value = area.CROP_DAMAGE
        
        ippan_list = IPPAN.objects.order_by('IPPAN_ID')[:]
        ws_ippan.cell(row=5, column=2).value = '都道府県'
        ws_ippan.cell(row=5, column=3).value = '市区町村'
        ws_ippan.cell(row=5, column=4).value = '水害発生月日'
        ws_ippan.cell(row=5, column=5).value = '水害終了月日'
        ws_ippan.cell(row=5, column=6).value = '水害原因'
        ws_ippan.cell(row=5, column=9).value = '水害区域番号'
        ws_ippan.cell(row=6, column=6).value = '1'
        ws_ippan.cell(row=6, column=7).value = '2'
        ws_ippan.cell(row=6, column=8).value = '3'
        ws_ippan.cell(row=9, column=2).value = '水系・沿岸名'
        ws_ippan.cell(row=9, column=3).value = '水系種別'
        ws_ippan.cell(row=9, column=4).value = '河川・海岸名'
        ws_ippan.cell(row=9, column=5).value = '河川種別'
        ws_ippan.cell(row=9, column=6).value = '地盤勾配区分※1'
        ws_ippan.cell(row=12, column=2).value = '水害区域面積（m2）'
        ws_ippan.cell(row=12, column=6).value = '工種'
        ws_ippan.cell(row=12, column=8).value = '農作物被害額（千円）'
        ws_ippan.cell(row=12, column=10).value = '異常気象コード'
        ws_ippan.cell(row=16, column=2).value = '町丁名・大字名'
        ws_ippan.cell(row=16, column=3).value = '名称'
        ws_ippan.cell(row=16, column=4).value = '地上・地下被害の区分※2'
        ws_ippan.cell(row=16, column=5).value = '浸水土砂被害の区分※3'
        ws_ippan.cell(row=16, column=6).value = '被害建物棟数'
        ws_ippan.cell(row=16, column=12).value = '被害建物の延床面積（m2）'
        ws_ippan.cell(row=16, column=13).value = '被災世帯数'
        ws_ippan.cell(row=16, column=14).value = '被災事業所数'
        ws_ippan.cell(row=16, column=15).value = '被害建物内での農業家又は事業所活動'
        ws_ippan.cell(row=16, column=25).value = '事業所の産業区分※7'
        ws_ippan.cell(row=16, column=26).value = '地下空間の利用形態※8'
        ws_ippan.cell(row=16, column=27).value = '備考'
        ws_ippan.cell(row=17, column=7).value = '床上浸水・土砂堆積・地下浸水'
        ws_ippan.cell(row=17, column=15).value = '農家・漁家戸数※5'
        ws_ippan.cell(row=17, column=20).value = '事業所従業者数※6'
        ws_ippan.cell(row=18, column=16).value = '床上浸水'
        ws_ippan.cell(row=18, column=21).value = '床上浸水'
        ws_ippan.cell(row=20, column=7).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=8).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=9).value = '1m以上'
        ws_ippan.cell(row=20, column=10).value = '半壊※4'
        ws_ippan.cell(row=20, column=11).value = '全壊・流失※4'
        ws_ippan.cell(row=20, column=16).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=17).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=18).value = '1m以上半壊'
        ws_ippan.cell(row=20, column=19).value = '全壊・流失'
        ws_ippan.cell(row=20, column=21).value = '1cm〜49cm'
        ws_ippan.cell(row=20, column=22).value = '50cm〜99cm'
        ws_ippan.cell(row=20, column=23).value = '1m以上半壊'
        ws_ippan.cell(row=20, column=24).value = '全壊・流失'

        ### 01: 建物区分
        dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$%d" % len(building_list))
        dv_building.ranges = 'C20:C1048576'
        ws_ippan.add_data_validation(dv_building)

        ### 02: 都道府県
        dv_ken = DataValidation(type="list", formula1="KEN!$B$1:$B$%d" % len(ken_list))
        dv_ken.ranges = 'B7:B7'
        ws_ippan.add_data_validation(dv_ken)
        
        ### 03: 市区町村
        ### ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK.A:B,2,0)" ### FOR LINUX
        ws_ippan.cell(row=3, column=30).value = "=VLOOKUP(B7,CITY_VLOOK!A:B,2,0)" ### FOR WINDOWS
        dv_city = DataValidation(type="list", formula1="=INDIRECT(AD3)")
        dv_city.ranges = 'C7:C7'
        ws_ippan.add_data_validation(dv_city)
        
        ### 04: 水害発生地点工種（河川海岸区分）
        dv_kasen_kaigan = DataValidation(type="list", formula1="KASEN_KAIGAN!$B$1:$B$%d" % len(kasen_kaigan_list))
        dv_kasen_kaigan.ranges = 'F14:F14'
        ws_ippan.add_data_validation(dv_kasen_kaigan)
        
        ### 05: 水系（水系・沿岸）
        dv_suikei = DataValidation(type="list", formula1="SUIKEI!$B$1:$B$%d" % len(suikei_list))
        dv_suikei.ranges = 'B10:B10'
        ws_ippan.add_data_validation(dv_suikei)
        
        ### 06: 水系種別（水系・沿岸種別）
        dv_suikei_type = DataValidation(type="list", formula1="SUIKEI_TYPE!$B$1:$B$%d" % len(suikei_type_list))
        dv_suikei_type.ranges = 'C10:C10'
        ws_ippan.add_data_validation(dv_suikei_type)
        
        ### 07: 河川（河川・海岸）
        dv_kasen = DataValidation(type="list", formula1="KASEN!$B$1:$B$%d" % len(kasen_list))
        dv_kasen.ranges = 'D10:D10'
        ws_ippan.add_data_validation(dv_kasen)
        
        ### 08: 河川種別（河川・海岸種別）
        dv_kasen_type = DataValidation(type="list", formula1="KASEN_TYPE!$B$1:$B$%d" % len(kasen_type_list))
        dv_kasen_type.ranges = 'E10:E10'
        ws_ippan.add_data_validation(dv_kasen_type)
        
        ### 09: 水害原因
        dv_cause = DataValidation(type="list", formula1="CAUSE!$B$1:$B$%d" % len(cause_list))
        dv_cause.ranges = 'F7:H7'
        ws_ippan.add_data_validation(dv_cause)
        
        ### 10: 地上地下区分
        dv_underground = DataValidation(type="list", formula1="UNDERGROUND!$B$1:$B$%d" % len(underground_list))
        dv_underground.ranges = 'D20:D1048576'
        ws_ippan.add_data_validation(dv_underground)
        
        ### 11: 地下空間の利用形態
        dv_usage = DataValidation(type="list", formula1="USAGE!$B$1:$B$%d" % len(usage_list))
        dv_usage.ranges = 'Z20:Z1048576'
        ws_ippan.add_data_validation(dv_usage)
        
        ### 12: 浸水土砂区分
        dv_flood_sediment = DataValidation(type="list", formula1="FLOOD_SEDIMENT!$B$1:$B$%d" % len(flood_sediment_list))
        dv_flood_sediment.ranges = 'E20:E1048576'
        ws_ippan.add_data_validation(dv_flood_sediment)
        
        ### 13: 地盤勾配区分
        dv_gradient = DataValidation(type="list", formula1="GRADIENT!$B$1:$B$%d" % len(gradient_list))
        dv_gradient.ranges = 'F10:F10'
        ws_ippan.add_data_validation(dv_gradient)
        
        ### 14: 産業分類
        dv_industry = DataValidation(type="list", formula1="INDUSTRY!$B$1:$B$%d" % len(industry_list))
        dv_industry.ranges = 'Y20:Y1048576'
        ws_ippan.add_data_validation(dv_industry)
        
        ### 25: 区域
        dv_area = DataValidation(type="list", formula1="AREA!$B$1:$B$%d" % len(area_list))
        dv_area.ranges = 'I7:I7'
        ws_ippan.add_data_validation(dv_area)
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws_ippan.cell(row=i+20, column=2).value = ippan.IPPAN_NAME
                ws_ippan.cell(row=i+20, column=3).value = '戸建住宅'
                ws_ippan.cell(row=i+20, column=4).value = '地上のみ'
                ws_ippan.cell(row=i+20, column=5).value = '浸水'
                ws_ippan.cell(row=i+20, column=6).value = ippan.BUILDING_LV00
                ws_ippan.cell(row=i+20, column=7).value = ippan.BUILDING_LV01_49
                ws_ippan.cell(row=i+20, column=8).value = ippan.BUILDING_LV50_99
                ws_ippan.cell(row=i+20, column=9).value = ippan.BUILDING_LV100
                ws_ippan.cell(row=i+20, column=10).value = ippan.BUILDING_HALF
                ws_ippan.cell(row=i+20, column=11).value = ippan.BUILDING_FULL
                ws_ippan.cell(row=i+20, column=12).value = ippan.FLOOR_AREA
                ws_ippan.cell(row=i+20, column=13).value = ippan.FAMILY
                ws_ippan.cell(row=i+20, column=14).value = ippan.OFFICE
                ws_ippan.cell(row=i+20, column=15).value = ippan.FARMER_FISHER_LV00
                ws_ippan.cell(row=i+20, column=16).value = ippan.FARMER_FISHER_LV01_49
                ws_ippan.cell(row=i+20, column=17).value = ippan.FARMER_FISHER_LV50_99
                ws_ippan.cell(row=i+20, column=18).value = ippan.FARMER_FISHER_LV100
                ws_ippan.cell(row=i+20, column=19).value = ippan.FARMER_FISHER_FULL
                ws_ippan.cell(row=i+20, column=20).value = ippan.EMPLOYEE_LV00
                ws_ippan.cell(row=i+20, column=21).value = ippan.EMPLOYEE_LV01_49
                ws_ippan.cell(row=i+20, column=22).value = ippan.EMPLOYEE_LV50_99
                ws_ippan.cell(row=i+20, column=23).value = ippan.EMPLOYEE_LV100
                ws_ippan.cell(row=i+20, column=24).value = ippan.EMPLOYEE_FULL
                ws_ippan.cell(row=i+20, column=25).value = '建設業'
                ws_ippan.cell(row=i+20, column=26).value = '住居'
                ws_ippan.cell(row=i+20, column=27).value = ''

        ### dv_building = DataValidation(type="list", formula1="BUILDING!$B$1:$B$6")
        ### dv_building.ranges = 'C20:C1048576'
        ### ws_ippan.add_data_validation(dv_building)
        
        gray_fill = PatternFill(bgColor='C0C0C0', fill_type='solid')
        white_fill = PatternFill(bgColor='FFFFFF', fill_type='solid')
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="戸建住宅"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="共同住宅"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('N20:Y1048576', FormulaRule(formula=['$C20="事業所併用住宅"'], fill=white_fill))
        ws_ippan.conditional_formatting.add('M20:M1048576', FormulaRule(formula=['$C20="事業所"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('M20:N1048576', FormulaRule(formula=['$C20="その他建物"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('T20:Y1048576', FormulaRule(formula=['$C20="その他建物"'], fill=gray_fill))
        ws_ippan.conditional_formatting.add('F20:Z1048576', FormulaRule(formula=['$C20="建物以外"'], fill=gray_fill))
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_chosa.xlsx"'
    except:
        raise Http404("[ERROR] download_ippan_chosa().")
    return response

###############################################################################
### download_ippan_city関数
### 2602: 一般資産調査票（市区町村用）
###############################################################################
def download_ippan_city(request):
    try:
        ippan_list = IPPAN.objects.order_by('IPPAN_ID')[:]
    
        file_path_to_load = 'static/ippan_city1.xlsx'
        file_path_to_save = 'static/ippan_city2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '一般資産調査票ID'
        ws.cell(row=1, column=2).value = '一般資産調査票名'
        
        ws.cell(row=1, column=3).value = '建物区分コード'
        
        ws.cell(row=1, column=4).value = '浸水土砂区分コード'
        ws.cell(row=1, column=5).value = '地盤勾配区分コード'
        ws.cell(row=1, column=6).value = '産業分類コード'
        
        ws.cell(row=1, column=7).value = '都道府県コード'
        ws.cell(row=1, column=8).value = '市区町村コード'
        ws.cell(row=1, column=9).value = '異常気象ID'
        ws.cell(row=1, column=10).value = '区域ID'
        ws.cell(row=1, column=11).value = '水害原因_1_コード'
        ws.cell(row=1, column=12).value = '水害原因_2_コード'
        ws.cell(row=1, column=13).value = '水害原因_3_コード'
        
        ws.cell(row=1, column=14).value = '水系コード'
        ws.cell(row=1, column=15).value = '河川コード'
        ws.cell(row=1, column=16).value = '河川海岸コード'

        ws.cell(row=1, column=17).value = '地上地下区分コード'
        ws.cell(row=1, column=18).value = '地下空間の利用形態コード'
        
        ws.cell(row=1, column=19).value = '被害建物棟数_床下'
        ws.cell(row=1, column=20).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=21).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=22).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=23).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=24).value = '被害建物棟数_全壊'

        ws.cell(row=1, column=25).value = '延床面積'
        ws.cell(row=1, column=26).value = '被災世帯数'
        ws.cell(row=1, column=27).value = '被災事業所数'
        
        ws.cell(row=1, column=28).value = '延床面積_床下'
        ws.cell(row=1, column=29).value = '延床面積_01から49cm'
        ws.cell(row=1, column=30).value = '延床面積_50から99cm'
        ws.cell(row=1, column=31).value = '延床面積_100cm以上'
        ws.cell(row=1, column=32).value = '延床面積_半壊'
        ws.cell(row=1, column=33).value = '延床面積_全壊'
        
        ws.cell(row=1, column=34).value = '被災世帯数_床下'
        ws.cell(row=1, column=35).value = '被災世帯数_01から49cm'
        ws.cell(row=1, column=36).value = '被災世帯数_50から99cm'
        ws.cell(row=1, column=37).value = '被災世帯数_100cm以上'
        ws.cell(row=1, column=38).value = '被災世帯数_半壊'
        ws.cell(row=1, column=39).value = '被災世帯数_全壊'

        ws.cell(row=1, column=40).value = '被災事業所数_床下'
        ws.cell(row=1, column=41).value = '被災事業所数_01から49cm'
        ws.cell(row=1, column=42).value = '被災事業所数_50から99cm'
        ws.cell(row=1, column=43).value = '被災事業所数_100cm以上'
        ws.cell(row=1, column=44).value = '被災事業所数_半壊'
        ws.cell(row=1, column=45).value = '被災事業所数_全壊'


        ws.cell(row=1, column=46).value = '被災従業者数_床下'
        ws.cell(row=1, column=47).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=48).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=49).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=50).value = '被災従業者数_全壊'

        ws.cell(row=1, column=51).value = '農漁家戸数_床下'
        ws.cell(row=1, column=52).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=53).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=54).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=55).value = '農漁家戸数_全壊'
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws.cell(row=i+2, column=1).value = ippan.IPPAN_ID
                ws.cell(row=i+2, column=2).value = ippan.IPPAN_NAME
                
                ws.cell(row=i+2, column=3).value = ippan.BUILDING_CODE
                
                ws.cell(row=i+2, column=4).value = ippan.FLOOD_SEDIMENT_CODE
                ws.cell(row=i+2, column=5).value = ippan.GRADIENT_CODE
                ws.cell(row=i+2, column=6).value = ippan.INDUSTRY_CODE
                
                ws.cell(row=i+2, column=7).value = ippan.KEN_CODE
                ws.cell(row=i+2, column=8).value = ippan.CITY_CODE
                ws.cell(row=i+2, column=9).value = ippan.WEATHER_ID
                ws.cell(row=i+2, column=10).value = ippan.AREA_ID
                ws.cell(row=i+2, column=11).value = ippan.CAUSE_1_CODE
                ws.cell(row=i+2, column=12).value = ippan.CAUSE_2_CODE
                ws.cell(row=i+2, column=13).value = ippan.CAUSE_3_CODE
                
                ws.cell(row=i+2, column=14).value = ippan.SUIKEI_CODE
                ws.cell(row=i+2, column=15).value = ippan.KASEN_CODE
                ws.cell(row=i+2, column=16).value = ippan.KASEN_KAIGAN_CODE

                ws.cell(row=i+2, column=17).value = ippan.UNDERGROUND_CODE
                ws.cell(row=i+2, column=18).value = ippan.USAGE_CODE
                
                ws.cell(row=i+2, column=19).value = ippan.BUILDING_LV00
                ws.cell(row=i+2, column=20).value = ippan.BUILDING_LV01_49
                ws.cell(row=i+2, column=21).value = ippan.BUILDING_LV50_99
                ws.cell(row=i+2, column=22).value = ippan.BUILDING_LV100
                ws.cell(row=i+2, column=23).value = ippan.BUILDING_HALF
                ws.cell(row=i+2, column=24).value = ippan.BUILDING_FULL

                ws.cell(row=i+2, column=25).value = ippan.FLOOR_AREA
                ws.cell(row=i+2, column=26).value = ippan.FAMILY
                ws.cell(row=i+2, column=27).value = ippan.OFFICE
                
                ws.cell(row=i+2, column=28).value = ippan.FLOOR_AREA_LV00
                ws.cell(row=i+2, column=29).value = ippan.FLOOR_AREA_LV01_49
                ws.cell(row=i+2, column=30).value = ippan.FLOOR_AREA_LV50_99
                ws.cell(row=i+2, column=31).value = ippan.FLOOR_AREA_LV100
                ws.cell(row=i+2, column=32).value = ippan.FLOOR_AREA_HALF
                ws.cell(row=i+2, column=33).value = ippan.FLOOR_AREA_FULL
                
                ws.cell(row=i+2, column=34).value = ippan.FAMILY_LV00
                ws.cell(row=i+2, column=35).value = ippan.FAMILY_LV01_49
                ws.cell(row=i+2, column=36).value = ippan.FAMILY_LV50_99
                ws.cell(row=i+2, column=37).value = ippan.FAMILY_LV100
                ws.cell(row=i+2, column=38).value = ippan.FAMILY_HALF
                ws.cell(row=i+2, column=39).value = ippan.FAMILY_FULL

                ws.cell(row=i+2, column=40).value = ippan.OFFICE_LV00
                ws.cell(row=i+2, column=41).value = ippan.OFFICE_LV01_49
                ws.cell(row=i+2, column=42).value = ippan.OFFICE_LV50_99
                ws.cell(row=i+2, column=43).value = ippan.OFFICE_LV100
                ws.cell(row=i+2, column=44).value = ippan.OFFICE_HALF
                ws.cell(row=i+2, column=45).value = ippan.OFFICE_FULL


                ws.cell(row=i+2, column=46).value = ippan.EMPLOYEE_LV00
                ws.cell(row=i+2, column=47).value = ippan.EMPLOYEE_LV01_49
                ws.cell(row=i+2, column=48).value = ippan.EMPLOYEE_LV50_99
                ws.cell(row=i+2, column=49).value = ippan.EMPLOYEE_LV100
                ws.cell(row=i+2, column=50).value = ippan.EMPLOYEE_FULL
        
                ws.cell(row=i+2, column=51).value = ippan.FARMER_FISHER_LV00
                ws.cell(row=i+2, column=52).value = ippan.FARMER_FISHER_LV01_49
                ws.cell(row=i+2, column=53).value = ippan.FARMER_FISHER_LV50_99
                ws.cell(row=i+2, column=54).value = ippan.FARMER_FISHER_LV100
                ws.cell(row=i+2, column=55).value = ippan.FARMER_FISHER_FULL

        ### dv = DataValidation(type="list", formula1="$B$1:$B$10")
        ### dv.ranges = 'F7:I7'
        ### ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_city.xlsx"'
    except:
        raise Http404("[ERROR] download_ippan_city().")
    return response

###############################################################################
### download_ippan_ken関数
### 2603: 一般資産調査票（都道府県用）
###############################################################################
def download_ippan_ken(request):
    try:
        ippan_list = IPPAN.objects.order_by('IPPAN_ID')[:]
    
        file_path_to_load = 'static/ippan_ken1.xlsx'
        file_path_to_save = 'static/ippan_ken2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '一般資産調査票ID'
        ws.cell(row=1, column=2).value = '一般資産調査票名'
        
        ws.cell(row=1, column=3).value = '建物区分コード'
        
        ws.cell(row=1, column=4).value = '浸水土砂区分コード'
        ws.cell(row=1, column=5).value = '地盤勾配区分コード'
        ws.cell(row=1, column=6).value = '産業分類コード'
        
        ws.cell(row=1, column=7).value = '都道府県コード'
        ws.cell(row=1, column=8).value = '市区町村コード'
        ws.cell(row=1, column=9).value = '異常気象ID'
        ws.cell(row=1, column=10).value = '区域ID'
        ws.cell(row=1, column=11).value = '水害原因_1_コード'
        ws.cell(row=1, column=12).value = '水害原因_2_コード'
        ws.cell(row=1, column=13).value = '水害原因_3_コード'
        
        ws.cell(row=1, column=14).value = '水系コード'
        ws.cell(row=1, column=15).value = '河川コード'
        ws.cell(row=1, column=16).value = '河川海岸コード'

        ws.cell(row=1, column=17).value = '地上地下区分コード'
        ws.cell(row=1, column=18).value = '地下空間の利用形態コード'
        
        ws.cell(row=1, column=19).value = '被害建物棟数_床下'
        ws.cell(row=1, column=20).value = '被害建物棟数_01から49cm'
        ws.cell(row=1, column=21).value = '被害建物棟数_50から99cm'
        ws.cell(row=1, column=22).value = '被害建物棟数_100cm以上'
        ws.cell(row=1, column=23).value = '被害建物棟数_半壊'
        ws.cell(row=1, column=24).value = '被害建物棟数_全壊'

        ws.cell(row=1, column=25).value = '延床面積'
        ws.cell(row=1, column=26).value = '被災世帯数'
        ws.cell(row=1, column=27).value = '被災事業所数'
        
        ws.cell(row=1, column=28).value = '延床面積_床下'
        ws.cell(row=1, column=29).value = '延床面積_01から49cm'
        ws.cell(row=1, column=30).value = '延床面積_50から99cm'
        ws.cell(row=1, column=31).value = '延床面積_100cm以上'
        ws.cell(row=1, column=32).value = '延床面積_半壊'
        ws.cell(row=1, column=33).value = '延床面積_全壊'
        
        ws.cell(row=1, column=34).value = '被災世帯数_床下'
        ws.cell(row=1, column=35).value = '被災世帯数_01から49cm'
        ws.cell(row=1, column=36).value = '被災世帯数_50から99cm'
        ws.cell(row=1, column=37).value = '被災世帯数_100cm以上'
        ws.cell(row=1, column=38).value = '被災世帯数_半壊'
        ws.cell(row=1, column=39).value = '被災世帯数_全壊'

        ws.cell(row=1, column=40).value = '被災事業所数_床下'
        ws.cell(row=1, column=41).value = '被災事業所数_01から49cm'
        ws.cell(row=1, column=42).value = '被災事業所数_50から99cm'
        ws.cell(row=1, column=43).value = '被災事業所数_100cm以上'
        ws.cell(row=1, column=44).value = '被災事業所数_半壊'
        ws.cell(row=1, column=45).value = '被災事業所数_全壊'


        ws.cell(row=1, column=46).value = '被災従業者数_床下'
        ws.cell(row=1, column=47).value = '被災従業者数_01から49cm'
        ws.cell(row=1, column=48).value = '被災従業者数_50から99cm'
        ws.cell(row=1, column=49).value = '被災従業者数_100cm以上'
        ws.cell(row=1, column=50).value = '被災従業者数_全壊'

        ws.cell(row=1, column=51).value = '農漁家戸数_床下'
        ws.cell(row=1, column=52).value = '農漁家戸数_01から49cm'
        ws.cell(row=1, column=53).value = '農漁家戸数_50から99cm'
        ws.cell(row=1, column=54).value = '農漁家戸数_100cm以上'
        ws.cell(row=1, column=55).value = '農漁家戸数_全壊'
        
        if ippan_list:
            for i, ippan in enumerate(ippan_list):
                ws.cell(row=i+2, column=1).value = ippan.IPPAN_ID
                ws.cell(row=i+2, column=2).value = ippan.IPPAN_NAME
                
                ws.cell(row=i+2, column=3).value = ippan.BUILDING_CODE
                
                ws.cell(row=i+2, column=4).value = ippan.FLOOD_SEDIMENT_CODE
                ws.cell(row=i+2, column=5).value = ippan.GRADIENT_CODE
                ws.cell(row=i+2, column=6).value = ippan.INDUSTRY_CODE
                
                ws.cell(row=i+2, column=7).value = ippan.KEN_CODE
                ws.cell(row=i+2, column=8).value = ippan.CITY_CODE
                ws.cell(row=i+2, column=9).value = ippan.WEATHER_ID
                ws.cell(row=i+2, column=10).value = ippan.AREA_ID
                ws.cell(row=i+2, column=11).value = ippan.CAUSE_1_CODE
                ws.cell(row=i+2, column=12).value = ippan.CAUSE_2_CODE
                ws.cell(row=i+2, column=13).value = ippan.CAUSE_3_CODE
                
                ws.cell(row=i+2, column=14).value = ippan.SUIKEI_CODE
                ws.cell(row=i+2, column=15).value = ippan.KASEN_CODE
                ws.cell(row=i+2, column=16).value = ippan.KASEN_KAIGAN_CODE

                ws.cell(row=i+2, column=17).value = ippan.UNDERGROUND_CODE
                ws.cell(row=i+2, column=18).value = ippan.USAGE_CODE
                
                ws.cell(row=i+2, column=19).value = ippan.BUILDING_LV00
                ws.cell(row=i+2, column=20).value = ippan.BUILDING_LV01_49
                ws.cell(row=i+2, column=21).value = ippan.BUILDING_LV50_99
                ws.cell(row=i+2, column=22).value = ippan.BUILDING_LV100
                ws.cell(row=i+2, column=23).value = ippan.BUILDING_HALF
                ws.cell(row=i+2, column=24).value = ippan.BUILDING_FULL

                ws.cell(row=i+2, column=25).value = ippan.FLOOR_AREA
                ws.cell(row=i+2, column=26).value = ippan.FAMILY
                ws.cell(row=i+2, column=27).value = ippan.OFFICE
                
                ws.cell(row=i+2, column=28).value = ippan.FLOOR_AREA_LV00
                ws.cell(row=i+2, column=29).value = ippan.FLOOR_AREA_LV01_49
                ws.cell(row=i+2, column=30).value = ippan.FLOOR_AREA_LV50_99
                ws.cell(row=i+2, column=31).value = ippan.FLOOR_AREA_LV100
                ws.cell(row=i+2, column=32).value = ippan.FLOOR_AREA_HALF
                ws.cell(row=i+2, column=33).value = ippan.FLOOR_AREA_FULL
                
                ws.cell(row=i+2, column=34).value = ippan.FAMILY_LV00
                ws.cell(row=i+2, column=35).value = ippan.FAMILY_LV01_49
                ws.cell(row=i+2, column=36).value = ippan.FAMILY_LV50_99
                ws.cell(row=i+2, column=37).value = ippan.FAMILY_LV100
                ws.cell(row=i+2, column=38).value = ippan.FAMILY_HALF
                ws.cell(row=i+2, column=39).value = ippan.FAMILY_FULL

                ws.cell(row=i+2, column=40).value = ippan.OFFICE_LV00
                ws.cell(row=i+2, column=41).value = ippan.OFFICE_LV01_49
                ws.cell(row=i+2, column=42).value = ippan.OFFICE_LV50_99
                ws.cell(row=i+2, column=43).value = ippan.OFFICE_LV100
                ws.cell(row=i+2, column=44).value = ippan.OFFICE_HALF
                ws.cell(row=i+2, column=45).value = ippan.OFFICE_FULL


                ws.cell(row=i+2, column=46).value = ippan.EMPLOYEE_LV00
                ws.cell(row=i+2, column=47).value = ippan.EMPLOYEE_LV01_49
                ws.cell(row=i+2, column=48).value = ippan.EMPLOYEE_LV50_99
                ws.cell(row=i+2, column=49).value = ippan.EMPLOYEE_LV100
                ws.cell(row=i+2, column=50).value = ippan.EMPLOYEE_FULL
        
                ws.cell(row=i+2, column=51).value = ippan.FARMER_FISHER_LV00
                ws.cell(row=i+2, column=52).value = ippan.FARMER_FISHER_LV01_49
                ws.cell(row=i+2, column=53).value = ippan.FARMER_FISHER_LV50_99
                ws.cell(row=i+2, column=54).value = ippan.FARMER_FISHER_LV100
                ws.cell(row=i+2, column=55).value = ippan.FARMER_FISHER_FULL

        ### dv = DataValidation(type="list", formula1="$B$1:$B$10")
        ### dv.ranges = 'F7:I7'
        ### ws.add_data_validation(dv)
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ippan_ken.xlsx"'
    except:
        raise Http404("[ERROR] download_ippan_ken().")
    return response

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_restoration関数
### 27: 復旧事業工種
###############################################################################
def download_restoration(request):
    try:
        restoration_list = RESTORATION.objects.order_by('RESTORATION_CODE')[:]
    
        file_path_to_load = 'static/restoration.xlsx'
        file_path_to_save = 'static/restoration2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '復旧事業工種コード'
        ws.cell(row=1, column=2).value = '復旧事業工種名'
        
        if restoration_list:
            for i, restoration in enumerate(restoration_list):
                ws.cell(row=i+2, column=1).value = restoration.RESTORATION_CODE
                ws.cell(row=i+2, column=2).value = restoration.RESTORATION_NAME
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="restoration.xlsx"'
    except:
        raise Http404("[ERROR] download_restoration().")
    return response

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################

###############################################################################
### download_kokyo関数
### 28: 公共土木調査票
###############################################################################
def download_kokyo(request):
    try:
        kokyo_list = KOKYO.objects.order_by('KOKYO_ID')[:]
    
        file_path_to_load = 'static/kokyo.xlsx'
        file_path_to_save = 'static/kokyo2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=1, column=1).value = '公共土木調査票ID'
        ws.cell(row=1, column=2).value = '都道府県コード'
        ws.cell(row=1, column=3).value = '市区町村コード'
        ws.cell(row=1, column=4).value = '異常気象ID'
        ws.cell(row=1, column=5).value = '公共土木調査対象年'
        ws.cell(row=1, column=6).value = '開始日'
        ws.cell(row=1, column=7).value = '終了日'
        
        if kokyo_list:
            for i, kokyo in enumerate(kokyo_list):
                ws.cell(row=i+2, column=1).value = kokyo.KOKYO_ID
                ws.cell(row=i+2, column=2).value = kokyo.KEN_CODE
                ws.cell(row=i+2, column=3).value = kokyo.CITY_CODE
                ws.cell(row=i+2, column=4).value = kokyo.WEATHER_ID
                ws.cell(row=i+2, column=5).value = kokyo.KOKYO_YEAR
                ws.cell(row=i+2, column=6).value = kokyo.BEGIN_DATE
                ws.cell(row=i+2, column=7).value = kokyo.END_DATE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="kokyo.xlsx"'
    except:
        raise Http404("[ERROR] download_kokyo().")
    return response

###############################################################################
### download_koeki関数
### 29: 公益事業調査票
###############################################################################
def download_koeki(request):
    try:
        koeki_list = KOEKI.objects.order_by('KOEKI_ID')[:]
    
        file_path_to_load = 'static/koeki.xlsx'
        file_path_to_save = 'static/koeki2.xlsx'
        wb = openpyxl.load_workbook(file_path_to_load)
        ws = wb.active
        ws.title = 'sheet99'

        ws.cell(row=i+1, column=1).value = '公益事業調査票ID'
        ws.cell(row=i+1, column=2).value = '都道府県コード'
        ws.cell(row=i+1, column=3).value = '市区町村コード'
        ws.cell(row=i+1, column=4).value = '異常気象ID'
        ws.cell(row=i+1, column=5).value = '公益事業調査対象年'
        ws.cell(row=i+1, column=6).value = '開始日'
        ws.cell(row=i+1, column=7).value = '終了日'
        
        if koeki_list:
            for i, koeki in enumerate(koeki_list):
                ws.cell(row=i+1, column=1).value = koeki.KOKYO_ID
                ws.cell(row=i+1, column=2).value = koeki.KEN_CODE
                ws.cell(row=i+1, column=3).value = koeki.CITY_CODE
                ws.cell(row=i+1, column=4).value = koeki.WEATHER_ID
                ws.cell(row=i+1, column=5).value = koeki.KOEKI_YEAR
                ws.cell(row=i+1, column=6).value = koeki.BEGIN_DATE
                ws.cell(row=i+1, column=7).value = koeki.END_DATE
        
        wb.save(file_path_to_save)
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="koeki.xlsx"'
    except:
        raise Http404("[ERROR] download_koeki().")
    return response




