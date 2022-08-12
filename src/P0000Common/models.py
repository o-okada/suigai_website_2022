# -*- coding: utf-8 -*-
from django.db import models

### データベース設計で絶対役に立つ命名規則
### https://katalog.tokyo/?p=5403
### ID、CODEはテーブル名にあわせる。OK：SUIKEI_CODE、NG：CODE、OK:SUIGAI_ID、NG:ID
### 項目名が同じになるようにするとER図も自動作成できる。

### See django.pdf P442 Using a custom user model when starting a project
### from django.contrib.auth.models import AbstractUser
### class USER(AbstractUser):
###     pass

###############################################################################
###############################################################################
### マスタDB
###############################################################################
###############################################################################

###############################################################################
### 1000: 建物区分（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class BUILDING(models.Model):
    building_code = models.CharField(max_length=10, primary_key=True)          ### 建物区分コード
    building_name = models.CharField(max_length=128)                           ### 建物区分名

    class Meta:
        db_table = 'building'
    
    def __str__(self):
        return '<BUILDING: ' + self.building_code + '>'

###############################################################################
### 1010: 都道府県（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class KEN(models.Model):
    ken_code = models.CharField(max_length=10, primary_key=True)               ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名

    class Meta:
        db_table = 'ken'
    
    def __str__(self):
        return '<KEN: ' + self.ken_code + '>'

###############################################################################
### 1020: 市区町村（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class CITY(models.Model):
    city_code = models.CharField(max_length=10, primary_key=True)              ### 市区町村コード
    city_name = models.CharField(max_length=128)                               ### 市区町村名
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    city_population = models.IntegerField()                                    ### 市区町村人口
    city_area = models.IntegerField()                                          ### 市区町村面積
    ### city_population = models.DecimalField(max_digits=15, decimal_places=2) ### 市区町村人口
    ### city_area = models.DecimalField(max_digits=15, decimal_places=2)       ### 市区町村面積

    class Meta:
        db_table = 'city'
    
    def __str__(self):
        return '<CITY: ' + self.city_code + '>'

###############################################################################
### 1030: 水害発生地点工種（河川海岸区分）（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class KASEN_KAIGAN(models.Model):
    kasen_kaigan_code = models.CharField(max_length=10, primary_key=True)      ### 河川海岸区分コード
    kasen_kaigan_name = models.CharField(max_length=128)                       ### 河川海岸区分名

    class Meta:
        db_table = 'kasen_kaigan'
 
    def __str__(self):
        return '<KASEN_KAIGAN: ' + self.kasen_kaigan_code + '>'

###############################################################################
### 1040: 水系（水系・沿岸）（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class SUIKEI(models.Model):
    suikei_code = models.CharField(max_length=10, primary_key=True)            ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名
    suikei_type_code = models.CharField(max_length=10)                         ### 水系種別コード

    class Meta:
        db_table = 'suikei'

    def __str__(self):
        return '<SUIKEI: ' + self.suikei_code + '>'

###############################################################################
### 1050: 水系種別（水系・沿岸種別）（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class SUIKEI_TYPE(models.Model):
    suikei_type_code = models.CharField(max_length=10, primary_key=True)       ### 水系種別コード
    suikei_type_name = models.CharField(max_length=128)                        ### 水系種別名

    class Meta:
        db_table = 'suikei_type'

    def __str__(self):
        return '<SUIKEI_TYPE: ' + self.suikei_type_code + '>'

###############################################################################
### 1060: 河川（河川・海岸）（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class KASEN(models.Model):
    kasen_code = models.CharField(max_length=10, primary_key=True)             ### 河川コード
    kasen_name = models.CharField(max_length=128)                              ### 河川名
    kasen_type_code = models.CharField(max_length=10)                          ### 河川種別コード
    suikei_code = models.CharField(max_length=10)                              ### 水系コード

    class Meta:
        db_table = 'kasen'

    def __str__(self):
        return '<KASEN: ' + self.kasen_code + '>'

###############################################################################
### 1070: 河川種別（河川・海岸種別）（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class KASEN_TYPE(models.Model):
    kasen_type_code = models.CharField(max_length=10, primary_key=True)        ### 河川種別コード
    kasen_type_name = models.CharField(max_length=128)                         ### 河川種別名

    class Meta:
        db_table = 'kasen_type'

    def __str__(self):
        return '<KASEN_TYPE: ' + self.kasen_type_code + '>'

###############################################################################
### 1080: 水害原因（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class CAUSE(models.Model):    
    cause_code = models.CharField(max_length=10, primary_key=True)             ### 水害原因コード
    cause_name = models.CharField(max_length=128)                              ### 水害原因名

    class Meta:
        db_table = 'cause'
    
    def __str__(self):
        return '<CAUSE: ' + self.cause_code + '>'

###############################################################################
### 1090: 地上地下区分（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class UNDERGROUND(models.Model):
    underground_code = models.CharField(max_length=10, primary_key=True)       ### 地上地下区分コード
    underground_name = models.CharField(max_length=128)                        ### 地上地下区分名

    class Meta:
        db_table = 'underground'

    def __str__(self):
        return '<UNDERGROUND: ' + self.underground_code + '>'

###############################################################################
### 1100: 地下空間の利用形態（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class USAGE(models.Model):
    usage_code = models.CharField(max_length=10, primary_key=True)             ### 地下空間の利用形態コード
    usage_name = models.CharField(max_length=128)                              ### 地下空間の利用形態名

    class Meta:
        db_table = 'usage'

    def __str__(self):
        return '<USAGE: ' + self.usage_code + '>'

###############################################################################
### 1110: 浸水土砂区分（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class FLOOD_SEDIMENT(models.Model):
    flood_sediment_code = models.CharField(max_length=10, primary_key=True)    ### 浸水土砂区分コード
    flood_sediment_name = models.CharField(max_length=128)                     ### 浸水土砂区分名

    class Meta:
        db_table = 'flood_sediment'

    def __str__(self):
        return '<FLOOD_SEDIMENT: ' + self.flood_sediment_code + '>'
    
###############################################################################
### 1120: 地盤勾配区分（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class GRADIENT(models.Model):
    gradient_code = models.CharField(max_length=10, primary_key=True)          ### 地盤勾配区分コード
    gradient_name = models.CharField(max_length=128)                           ### 地盤勾配区分名

    class Meta:
        db_table = 'gradient'

    def __str__(self):
        return '<GRADIENT: ' + self.gradient_code + '>'

###############################################################################
### 1130: 産業分類（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class INDUSTRY(models.Model):
    industry_code = models.CharField(max_length=10, primary_key=True)          ### 産業分類コード
    industry_name = models.CharField(max_length=128)                           ### 産業分類名

    class Meta:
        db_table = 'industry'

    def __str__(self):
        return '<INDUSTRY: ' + self.industry_code + '>'

###############################################################################
### 1140: 公益事業分類（マスタDB）
### 入力用コード、集計用コード
###############################################################################
class KOEKI_INDUSTRY(models.Model):
    koeki_industry_code = models.CharField(max_length=10, primary_key=True)    ### 公益事業分類コード
    koeki_industry_name = models.CharField(max_length=128)                     ### 公益事業分類名

    class Meta:
        db_table = 'koeki_industry'

    def __str__(self):
        return '<KOEKI_INDUSTRY: ' + self.koeki_industry_code + '>'

###############################################################################
### 2000: 家屋評価額（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSE_ASSET(models.Model):
    house_asset_code = models.CharField(max_length=10, primary_key=True)       ### 家屋評価額コード
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    house_asset = models.FloatField(null=True)                                 ### 家屋評価額

    class Meta:
        db_table = 'house_asset'

    def __str__(self):
        return '<HOUSE_ASSET: ' + self.house_asset_code + '>'

###############################################################################
### 2010: 家屋被害率（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSE_RATE(models.Model):
    house_rate_code = models.CharField(max_length=10, primary_key=True)        ### 家屋被害率コード
    flood_sediment_code = models.CharField(max_length=10)                      ### 浸水土砂区分コード
    gradient_code = models.CharField(max_length=10)                            ### 地盤勾配区分コード
    house_rate_lv00 = models.FloatField()                                      ### 家屋被害率_床下
    house_rate_lv00_50 = models.FloatField()                                   ### 家屋被害率_0から50cm未満
    house_rate_lv50_100 = models.FloatField()                                  ### 家屋被害率_50から100cm未満
    house_rate_lv100_200 = models.FloatField()                                 ### 家屋被害率_100から200cm未満
    house_rate_lv200_300 = models.FloatField()                                 ### 家屋被害率_200から300cm未満
    house_rate_lv300 = models.FloatField()                                     ### 家屋被害率_300cm以上

    class Meta:
        db_table = 'house_rate'

    def __str__(self):
        return '<HOUSE_RATE: ' + self.house_rate_code + '>'
    
###############################################################################
### 2020: 家庭応急対策費_代替活動費（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSE_ALT(models.Model):
    house_alt_code = models.CharField(max_length=10, primary_key=True)         ### 家庭応急対策費_代替活動費コード
    house_alt_lv00 = models.FloatField()                                       ### 家庭応急対策費_代替活動費_床下
    house_alt_lv00_50 = models.FloatField()                                    ### 家庭応急対策費_代替活動費_0から50cm未満
    house_alt_lv50_100 = models.FloatField()                                   ### 家庭応急対策費_代替活動費_50から100cm未満
    house_alt_lv100_200 = models.FloatField()                                  ### 家庭応急対策費_代替活動費_100から200cm未満
    house_alt_lv200_300 = models.FloatField()                                  ### 家庭応急対策費_代替活動費_200から300cm未満
    house_alt_lv300 = models.FloatField()                                      ### 家庭応急対策費_代替活動費_300cm以上
    
    class Meta:
        db_table = 'house_alt'
    
    def __str__(self):
        return '<HOUSE_ALT: ' + self.house_alt_code + '>'

###############################################################################
### 2030: 家庭応急対策費_清掃日数（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSE_CLEAN(models.Model):
    house_clean_code = models.CharField(max_length=10, primary_key=True)       ### 家庭応急対策費_清掃日数コード
    house_clean_days_lv00 = models.FloatField()                                ### 家庭応急対策費_清掃日数_床下
    house_clean_days_lv00_50 = models.FloatField()                             ### 家庭応急対策費_清掃日数_0から50cm未満
    house_clean_days_lv50_100 = models.FloatField()                            ### 家庭応急対策費_清掃日数_50から100cm未満
    house_clean_days_lv100_200 = models.FloatField()                           ### 家庭応急対策費_清掃日数_100から200cm未満
    house_clean_days_lv200_300 = models.FloatField()                           ### 家庭応急対策費_清掃日数_200から300cm未満
    house_clean_days_lv300 = models.FloatField()                               ### 家庭応急対策費_清掃日数_300cm以上
    house_clean_unit_cost = models.FloatField()                                ### 家庭応急対策費_清掃労働単価
    
    class Meta:
        db_table = 'house_clean'
    
    def __str__(self):
        return '<HOUSE_CLEAN: ' + self.house_clean_code + '>'

###############################################################################
### 3000: 家庭用品自動車以外所有額（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSEHOLD_ASSET(models.Model):
    household_asset_code = models.CharField(max_length=10, primary_key=True)   ### 家庭用品自動車以外所有額コード
    household_asset = models.FloatField()                                      ### 家庭用品自動車以外所有額

    class Meta:
        db_table = 'household_asset'

    def __str__(self):
        return '<HOUSEHOLD_ASSET: ' + self.household_asset_code + '>'

###############################################################################
### 3010: 家庭用品自動車以外被害率（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class HOUSEHOLD_RATE(models.Model):
    household_rate_code = models.CharField(max_length=10, primary_key=True)    ### 家庭用品自動車以外被害率コード
    flood_sediment_code = models.CharField(max_length=10)                      ### 浸水土砂区分コード
    ### gradient_code = models.CharField(max_length=10)                        ### 地盤勾配区分コード
    household_rate_lv00 = models.FloatField()                                  ### 家庭用品自動車以外被害率_床下
    household_rate_lv00_50 = models.FloatField()                               ### 家庭用品自動車以外被害率_0から50cm未満
    household_rate_lv50_100 = models.FloatField()                              ### 家庭用品自動車以外被害率_50から100cm未満
    household_rate_lv100_200 = models.FloatField()                             ### 家庭用品自動車以外被害率_100から200cm未満
    household_rate_lv200_300 = models.FloatField()                             ### 家庭用品自動車以外被害率_200から300cm未満
    household_rate_lv300 = models.FloatField()                                 ### 家庭用品自動車以外被害率_300cm以上

    class Meta:
        db_table = 'household_rate'

    def __str__(self):
        return '<HOUSEHOLD_RATE: ' + self.household_rate_code + '>'

###############################################################################
### 4000: 家庭用品自動車所有額（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class CAR_ASSET(models.Model):
    car_asset_code = models.CharField(max_length=10, primary_key=True)         ### 家庭用品自動車所有額コード
    car_asset = models.FloatField()                                            ### 家庭用品自動車所有額

    class Meta:
        db_table = 'car_asset'

    def __str__(self):
        return '<CAR_ASSET: ' + self.car_asset_code + '>'

###############################################################################
### 4010: 家庭用品自動車被害率（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class CAR_RATE(models.Model):
    car_rate_code = models.CharField(max_length=10, primary_key=True)          ### 家庭用品自動車被害率コード
    ### flood_sediment_code = models.CharField(max_length=10)                  ### 浸水土砂区分コード
    ### gradient_code = models.CharField(max_length=10)                        ### 地盤勾配区分コード
    car_rate_lv00 = models.FloatField()                                        ### 家庭用品自動車被害率_床下
    car_rate_lv00_50 = models.FloatField()                                     ### 家庭用品自動車被害率_0から50cm未満
    car_rate_lv50_100 = models.FloatField()                                    ### 家庭用品自動車被害率_50から100cm未満
    car_rate_lv100_200 = models.FloatField()                                   ### 家庭用品自動車被害率_100から200cm未満
    car_rate_lv200_300 = models.FloatField()                                   ### 家庭用品自動車被害率_200から300cm未満
    car_rate_lv300 = models.FloatField()                                       ### 家庭用品自動車被害率_300cm以上

    class Meta:
        db_table = 'car_rate'

    def __str__(self):
        return '<CAR_RATE: ' + self.car_rate_code + '>'

###############################################################################
### 5000: 事業所資産額（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class OFFICE_ASSET(models.Model):
    office_asset_code = models.CharField(max_length=10, primary_key=True)      ### 事業所資産額コード
    industry_code = models.CharField(max_length=10)                            ### 産業分類コード
    office_dep_asset = models.FloatField(null=True)                            ### 事業所資産額_償却資産額
    office_inv_asset = models.FloatField(null=True)                            ### 事業所資産額_在庫資産額
    office_va_asset = models.FloatField(null=True)                             ### 事業所資産額_付加価値額

    class Meta:
        db_table = 'office_asset'

    def __str__(self):
        return '<OFFICE_ASSET: ' + self.office_asset_code + '>'

###############################################################################
### 5010: 事業所被害率（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class OFFICE_RATE(models.Model):
    office_rate_code = models.CharField(max_length=10, primary_key=True)       ### 事業所被害率コード
    flood_sediment_code = models.CharField(max_length=10)                      ### 浸水土砂区分コード
    ### gradient_code = models.CharField(max_length=10)                        ### 地盤勾配区分コード
    office_dep_rate_lv00 = models.FloatField()                                 ### 事業所被害率_償却資産被害率_床下
    office_dep_rate_lv00_50 = models.FloatField()                              ### 事業所被害率_償却資産被害率_0から50cm未満
    office_dep_rate_lv50_100 = models.FloatField()                             ### 事業所被害率_償却資産被害率_50から100cm未満
    office_dep_rate_lv100_200 = models.FloatField()                            ### 事業所被害率_償却資産被害率_100から200cm未満
    office_dep_rate_lv200_300 = models.FloatField()                            ### 事業所被害率_償却資産被害率_200から300cm未満
    office_dep_rate_lv300 = models.FloatField()                                ### 事業所被害率_償却資産被害率_300cm以上
    office_inv_rate_lv00 = models.FloatField()                                 ### 事業所被害率_在庫資産被害率_床下
    office_inv_rate_lv00_50 = models.FloatField()                              ### 事業所被害率_在庫資産被害率_0から50cm未満
    office_inv_rate_lv50_100 = models.FloatField()                             ### 事業所被害率_在庫資産被害率_50から100cm未満
    office_inv_rate_lv100_200 = models.FloatField()                            ### 事業所被害率_在庫資産被害率_100から200cm未満
    office_inv_rate_lv200_300 = models.FloatField()                            ### 事業所被害率_在庫資産被害率_200から300cm未満
    office_inv_rate_lv300 = models.FloatField()                                ### 事業所被害率_在庫資産被害率_300cm以上

    class Meta:
        db_table = 'office_rate'

    def __str__(self):
        return '<OFFICE_RATE: ' + self.office_rate_code + '>'

###############################################################################
### 5020: 事業所営業停止日数（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class OFFICE_SUSPEND(models.Model):
    office_sus_code = models.CharField(max_length=10, primary_key=True)        ### 事業所営業停止日数コード
    office_sus_days_lv00 = models.FloatField(null=True)                        ### 事業所営業停止日数_床下
    office_sus_days_lv00_50 = models.FloatField(null=True)                     ### 事業所営業停止日数_0から50cm未満
    office_sus_days_lv50_100 = models.FloatField(null=True)                    ### 事業所営業停止日数_50から100cm未満
    office_sus_days_lv100_200 = models.FloatField(null=True)                   ### 事業所営業停止日数_100から200cm未満
    office_sus_days_lv200_300 = models.FloatField(null=True)                   ### 事業所営業停止日数_200から300cm未満
    office_sus_days_lv300 = models.FloatField(null=True)                       ### 事業所営業停止日数_300cm以上
    
    class Meta:
        db_table = 'office_suspend'
        
    def __str__(self):
        return '<OFFICE_SUSPEND: ' + self.office_sus_code + '>'

###############################################################################
### 5030: 事業所営業停滞日数（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class OFFICE_STAGNATE(models.Model):
    office_stg_code = models.CharField(max_length=10, primary_key=True)        ### 事業所営業停滞日数コード
    office_stg_days_lv00 = models.FloatField(null=True)                        ### 事業所営業停滞日数_床下
    office_stg_days_lv00_50 = models.FloatField(null=True)                     ### 事業所営業停滞日数_0から50cm未満
    office_stg_days_lv50_100 = models.FloatField(null=True)                    ### 事業所営業停滞日数_50から100cm未満
    office_stg_days_lv100_200 = models.FloatField(null=True)                   ### 事業所営業停滞日数_100から200cm未満
    office_stg_days_lv200_300 = models.FloatField(null=True)                   ### 事業所営業停滞日数_200から300cm未満
    office_stg_days_lv300 = models.FloatField(null=True)                       ### 事業所営業停滞日数_300cm以上

    class Meta:
        db_table = 'office_stagnate'
        
    def __str__(self):
        return '<OFFICE_STAGNATE: ' + self.office_stg_code + '>'

###############################################################################
### 5040: 事業所応急対策費_代替活動費（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class OFFICE_ALT(models.Model):
    office_alt_code = models.CharField(max_length=10, primary_key=True)        ### 事業所応急対策費_代替活動費コード
    office_alt_lv00 = models.FloatField(null=True)                             ### 事業所応急対策費_代替活動費_床下
    office_alt_lv00_50 = models.FloatField(null=True)                          ### 事業所応急対策費_代替活動費_0から50cm未満
    office_alt_lv50_100 = models.FloatField(null=True)                         ### 事業所応急対策費_代替活動費_50から100cm未満
    office_alt_lv100_200 = models.FloatField(null=True)                        ### 事業所応急対策費_代替活動費_100から200cm未満
    office_alt_lv200_300 = models.FloatField(null=True)                        ### 事業所応急対策費_代替活動費_200から300cm未満
    office_alt_lv300 = models.FloatField(null=True)                            ### 事業所応急対策費_代替活動費_300cm以上

    class Meta:
        db_table = 'office_alt'
        
    def __str__(self):
        return '<OFFICE_ALT: ' + self.office_alt_code + '>'

###############################################################################
### 6000: 農漁家資産額（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class FARMER_FISHER_ASSET(models.Model):
    farmer_fisher_asset_code = models.CharField(max_length=10, primary_key=True)    ### 農漁家資産額コード
    farmer_fisher_dep_asset = models.FloatField(null=True)                          ### 農漁家資産額_償却資産額
    farmer_fisher_inv_asset = models.FloatField(null=True)                          ### 農漁家資産額_在庫資産額

    class Meta:
        db_table = 'farmer_fisher_asset'

    def __str__(self):
        return '<FARMER_FISHER_ASSET: ' + self.farmer_fisher_asset_code + '>'

###############################################################################
### 6010: 農漁家被害率（マスタDB）
### 集計用資産額、集計用被害率
###############################################################################
class FARMER_FISHER_RATE(models.Model):
    farmer_fisher_rate_code = models.CharField(max_length=10, primary_key=True)     ### 農漁家被害率コード
    flood_sediment_code = models.CharField(max_length=10)                           ### 浸水土砂区分コード
    ### gradient_code = models.CharField(max_length=10)                             ### 地盤勾配区分コード
    farmer_fisher_dep_rate_lv00 = models.FloatField()                               ### 農漁家被害率_償却資産被害率_床下
    farmer_fisher_dep_rate_lv00_50 = models.FloatField()                            ### 農漁家被害率_償却資産被害率_0から50cm未満
    farmer_fisher_dep_rate_lv50_100 = models.FloatField()                           ### 農漁家被害率_償却資産被害率_50から100cm未満
    farmer_fisher_dep_rate_lv100_200 = models.FloatField()                          ### 農漁家被害率_償却資産被害率_100から200cm未満
    farmer_fisher_dep_rate_lv200_300 = models.FloatField()                          ### 農漁家被害率_償却資産被害率_200から300cm未満
    farmer_fisher_dep_rate_lv300 = models.FloatField()                              ### 農漁家被害率_償却資産被害率_300cm以上
    farmer_fisher_inv_rate_lv00 = models.FloatField()                               ### 農漁家被害率_在庫資産被害率_床下
    farmer_fisher_inv_rate_lv00_50 = models.FloatField()                            ### 農漁家被害率_在庫資産被害率_0から50cm未満
    farmer_fisher_inv_rate_lv50_100 = models.FloatField()                           ### 農漁家被害率_在庫資産被害率_50から100cm未満
    farmer_fisher_inv_rate_lv100_200 = models.FloatField()                          ### 農漁家被害率_在庫資産被害率_100から200cm未満
    farmer_fisher_inv_rate_lv200_300 = models.FloatField()                          ### 農漁家被害率_在庫資産被害率_200から300cm未満
    farmer_fisher_inv_rate_lv300 = models.FloatField()                              ### 農漁家被害率_在庫資産被害率_300cm以上

    class Meta:
        db_table = 'farmer_fisher_rate'

    def __str__(self):
        return '<FARMER_FISHER_RATE: ' + self.farmer_fisher_rate_code + '>'

###############################################################################
###############################################################################
### 入力DB
###############################################################################
###############################################################################

###############################################################################
### 7000: 入力データ_水害区域（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class AREA(models.Model):
    area_id = models.IntegerField(primary_key=True)                            ### 水害区域ID
    area_name = models.CharField(max_length=128)                               ### 水害区域名
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード

    ### file_path = models.CharField(max_length=256, null=True)                ### ファイルパス
    ### file_name = models.CharField(max_length=256, null=True)                ### ファイル名
    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/03 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/03 追加

    action_code = models.CharField(max_length=10, null=True)                   ### 最新のアクションコード ※2022/07/12 追加
    status_code = models.CharField(max_length=10, null=True)                   ### 最新の状態コード ※2022/07/12 追加

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/12 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/12 追加

    class Meta:
        db_table = 'area'

    def __str__(self):
        return '<AREA: ' + self.area_id + '>'

###############################################################################
### 7010: 入力データ_異常気象（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class WEATHER(models.Model):
    weather_id = models.IntegerField(primary_key=True)                         ### 異常気象ID
    weather_name = models.CharField(max_length=128)                            ### 異常気象名
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/27 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/27 追加

    class Meta:
        db_table = 'weather'
    
    def __str__(self):
        return '<WEATHER: ' + self.weather_id + '>'

###############################################################################
### 7020: 入力データ_ヘッダ部分（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class IPPAN_SHEET(models.Model):
    ippan_sheet_id = models.IntegerField(primary_key=True)                     ### シートID
    ippan_sheet_name = models.CharField(max_length=128, null=True)             ### シート名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ### FOR GROUP BY
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ### FOR GROUP BY
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ### FOR GROUP BY
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ### FOR GROUP BY
    cause_1_code = models.CharField(max_length=10, null=True)                  ### 水害原因_1_コード ### FOR GROUP BY
    cause_2_code = models.CharField(max_length=10, null=True)                  ### 水害原因_2_コード ### FOR GROUP BY
    cause_3_code = models.CharField(max_length=10, null=True)                  ### 水害原因_3_コード ### FOR GROUP BY
    area_id = models.IntegerField(null=True)                                   ### 水害区域ID ### FOR GROUP BY

    ### 帳票のヘッダ部分 行10
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ### FOR GROUP BY
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ### FOR GROUP BY
    gradient_code = models.CharField(max_length=10, null=True)                 ### 地盤勾配区分コード FOR PARAM ### FOR GROUP BY

    ### 帳票のヘッダ部分 行14
    residential_area = models.FloatField(null=True)                            ### 宅地面積（単位m2）
    agricultural_area = models.FloatField(null=True)                           ### 農地面積（単位m2）
    underground_area = models.FloatField(null=True)                            ### 地下面積（単位m2）
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ### FOR GROUP BY
    crop_damage = models.FloatField(null=True)                                 ### 農作物被害額（単位千円）
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ### FOR GROUP BY

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/01 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/01 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/01 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/01 追加

    action_code = models.CharField(max_length=10, null=True)                   ### 最新のアクションコード ※2022/07/12 追加
    status_code = models.CharField(max_length=10, null=True)                   ### 最新の状態コード ※2022/07/12 追加

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/11 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/11 追加

    class Meta:
        db_table = 'ippan_sheet'
        ### constraints = [
        ###     models.UniqueConstraint(
        ###         fields=['ken_code', 'city_code', 'begin_date', 'cause_1_code', 'area_id', 'suikei_code', 'kasen_code', 'gradient_code'],
        ###         name='suigai_unique'
        ###     ),
        ### ]

    def __str__(self):
        return '<IPPAN_SHEET: ' + self.ippan_sheet_id + '>'

###############################################################################
### 7020: 入力データ_ヘッダ部分（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class SUIGAI(models.Model):
    suigai_id = models.IntegerField(primary_key=True)                          ### シートID
    suigai_name = models.CharField(max_length=128, null=True)                  ### シート名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ### FOR GROUP BY
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ### FOR GROUP BY
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ### FOR GROUP BY
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ### FOR GROUP BY
    cause_1_code = models.CharField(max_length=10, null=True)                  ### 水害原因_1_コード ### FOR GROUP BY
    cause_2_code = models.CharField(max_length=10, null=True)                  ### 水害原因_2_コード ### FOR GROUP BY
    cause_3_code = models.CharField(max_length=10, null=True)                  ### 水害原因_3_コード ### FOR GROUP BY
    area_id = models.IntegerField(null=True)                                   ### 水害区域ID ### FOR GROUP BY

    ### 帳票のヘッダ部分 行10
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ### FOR GROUP BY
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ### FOR GROUP BY
    gradient_code = models.CharField(max_length=10, null=True)                 ### 地盤勾配区分コード FOR PARAM ### FOR GROUP BY

    ### 帳票のヘッダ部分 行14
    residential_area = models.FloatField(null=True)                            ### 宅地面積（単位m2）
    agricultural_area = models.FloatField(null=True)                           ### 農地面積（単位m2）
    underground_area = models.FloatField(null=True)                            ### 地下面積（単位m2）
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ### FOR GROUP BY
    crop_damage = models.FloatField(null=True)                                 ### 農作物被害額（単位千円）
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ### FOR GROUP BY

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/01 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/01 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/01 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/01 追加

    action_code = models.CharField(max_length=10, null=True)                   ### 最新のアクションコード ※2022/07/12 追加
    status_code = models.CharField(max_length=10, null=True)                   ### 最新の状態コード ※2022/07/12 追加

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/11 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/11 追加

    class Meta:
        db_table = 'suigai'
        ### constraints = [
        ###     models.UniqueConstraint(
        ###         fields=['ken_code', 'city_code', 'begin_date', 'cause_1_code', 'area_id', 'suikei_code', 'kasen_code', 'gradient_code'],
        ###         name='suigai_unique'
        ###     ),
        ### ]

    def __str__(self):
        return '<SUIGAI: ' + self.suigai_id + '>'

###############################################################################
### 7030: 入力データ_一覧表部分（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class IPPAN(models.Model):
    ippan_id = models.IntegerField(primary_key=True)                           ### 行ID
    ippan_name = models.CharField(max_length=128, null=True)                   ### 町丁名、大字名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    suigai_id = models.IntegerField(null=True)                                 ### シートID

    ### 帳票の繰り返し部分 行20以降
    building_code = models.CharField(max_length=10, null=True)                 ### 建物区分コード
    underground_code = models.CharField(max_length=10, null=True)              ### 地上地下区分コード
    flood_sediment_code = models.CharField(max_length=10, null=True)           ### 浸水土砂区分コード ### FOR SUM PARAM
    
    ### 入力データ
    building_lv00 = models.FloatField(null=True)                               ### 被害建物棟数_床下
    building_lv01_49 = models.FloatField(null=True)                            ### 被害建物棟数_01から49cm
    building_lv50_99 = models.FloatField(null=True)                            ### 被害建物棟数_50から99cm
    building_lv100 = models.FloatField(null=True)                              ### 被害建物棟数_100cm以上
    building_half = models.FloatField(null=True)                               ### 被害建物棟数_半壊
    building_full = models.FloatField(null=True)                               ### 被害建物棟数_全壊
    
    ### 入力データ
    floor_area = models.FloatField(null=True)                                  ### 延床面積
    family = models.FloatField(null=True)                                      ### 被災世帯数
    office = models.FloatField(null=True)                                      ### 被災事業所数
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    floor_area_lv00 = models.FloatField(null=True)                             ### 延床面積_床下
    floor_area_lv01_49 = models.FloatField(null=True)                          ### 延床面積_01から49cm
    floor_area_lv50_99 = models.FloatField(null=True)                          ### 延床面積_50から99cm
    floor_area_lv100 = models.FloatField(null=True)                            ### 延床面積_100cm以上
    floor_area_half = models.FloatField(null=True)                             ### 延床面積_半壊
    floor_area_full = models.FloatField(null=True)                             ### 延床面積_全壊
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    family_lv00 = models.FloatField(null=True)                                 ### 被災世帯数_床下
    family_lv01_49 = models.FloatField(null=True)                              ### 被災世帯数_01から49cm
    family_lv50_99 = models.FloatField(null=True)                              ### 被災世帯数_50から99cm
    family_lv100 = models.FloatField(null=True)                                ### 被災世帯数_100cm以上
    family_half = models.FloatField(null=True)                                 ### 被災世帯数_半壊
    family_full = models.FloatField(null=True)                                 ### 被災世帯数_全壊
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    office_lv00 = models.FloatField(null=True)                                 ### 被災事業所数_床下
    office_lv01_49 = models.FloatField(null=True)                              ### 被災事業所数_01から49cm
    office_lv50_99 = models.FloatField(null=True)                              ### 被災事業所数_50から99cm
    office_lv100 = models.FloatField(null=True)                                ### 被災事業所数_100cm以上
    office_half = models.FloatField(null=True)                                 ### 被災事業所数_半壊
    office_full = models.FloatField(null=True)                                 ### 被災事業所数_全壊
    
    ### 入力データ
    farmer_fisher_lv00 = models.FloatField(null=True)                          ### 農漁家戸数_床下
    farmer_fisher_lv01_49 = models.FloatField(null=True)                       ### 農漁家戸数_01から49cm
    farmer_fisher_lv50_99 = models.FloatField(null=True)                       ### 農漁家戸数_50から99cm
    farmer_fisher_lv100 = models.FloatField(null=True)                         ### 農漁家戸数_100cm以上
    ### farmer_fisher_half = models.FloatField(null=True)
    farmer_fisher_full = models.FloatField(null=True)                          ### 農漁家戸数_全壊

    ### 入力データ
    employee_lv00 = models.FloatField(null=True)                               ### 被災従業者数_床下
    employee_lv01_49 = models.FloatField(null=True)                            ### 被災従業者数_01から49cm
    employee_lv50_99 = models.FloatField(null=True)                            ### 被災従業者数_50から99cm
    employee_lv100 = models.FloatField(null=True)                              ### 被災従業者数_100cm以上
    ### employee_half = models.FloatField(null=True)
    employee_full = models.FloatField(null=True)                               ### 被災従業者数_全壊

    ### 入力データ
    industry_code = models.CharField(max_length=10, null=True)                 ### 産業分類コード ### FOR SUM PARAM
    usage_code = models.CharField(max_length=10, null=True)                    ### 地下空間の利用形態コード
    comment = models.CharField(max_length=512, null=True)                      ### 備考
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/11 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/11 追加

    class Meta:
        db_table = 'ippan'

    def __str__(self):
        return '<IPPAN: ' + self.ippan_id + '>'

###############################################################################
### 7040: 入力データ_一覧表部分（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class IPPAN_VIEW(models.Model):
    ippan_id = models.IntegerField(primary_key=True)                           ### 行ID
    ippan_name = models.CharField(max_length=128, null=True)                   ### 町丁名、大字名

    ### 第2正規形の考え方からヘッダ部分を別テーブル（水害テーブル）に分割する。
    suigai_id = models.IntegerField(null=True)                                 ### シートID
    suigai_name = models.CharField(max_length=128, null=True)                  ### シート名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名 LEFT JOIN項目
    city_code = models.CharField(max_length=10)                                ### 市区町村コード
    city_name = models.CharField(max_length=128)                               ### 市区町村名 LEFT JOIN項目
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ### FOR GROUP BY
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ### FOR GROUP BY
    cause_1_code = models.CharField(max_length=10)                             ### 水害原因コード1
    cause_1_name = models.CharField(max_length=128)                            ### 水害原因名1 LEFT JOIN項目
    cause_2_code = models.CharField(max_length=10)                             ### 水害原因コード2
    cause_2_name = models.CharField(max_length=128)                            ### 水害原因名2 LEFT JOIN項目
    cause_3_code = models.CharField(max_length=10)                             ### 水害原因コード3
    cause_3_name = models.CharField(max_length=128)                            ### 水害原因名3 LEFT JOIN項目
    area_id = models.IntegerField()                                            ### 水害区域ID
    area_name = models.CharField(max_length=128)                               ### 水害区域名 LEFT JOIN項目

    ### 帳票のヘッダ部分 行10
    suikei_code = models.CharField(max_length=10)                              ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名 LEFT JOIN項目
    suikei_type_code = models.CharField(max_length=10)                         ### 水系種別コード
    suikei_type_name = models.CharField(max_length=128)                        ### 水系種別名 LEFT JOIN項目
    kasen_code = models.CharField(max_length=10)                               ### 河川コード
    kasen_name = models.CharField(max_length=128)                              ### 河川名 LEFT JOIN項目
    kasen_type_code = models.CharField(max_length=10)                          ### 河川種別コード
    kasen_type_name = models.CharField(max_length=128)                         ### 河川種別名 LEFT JOIN項目
    gradient_code = models.CharField(max_length=10)                            ### 地盤勾配区分コード
    gradient_name = models.CharField(max_length=128)                           ### 地盤勾配区分名 LEFT JOIN項目

    ### 帳票のヘッダ部分 行14
    residential_area = models.FloatField(null=True)                            ### 宅地面積（単位m2）
    agricultural_area = models.FloatField(null=True)                           ### 農地面積（単位m2）
    underground_area = models.FloatField(null=True)                            ### 地下面積（単位m2）
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ### FOR GROUP BY
    kasen_kaigan_name = models.CharField(max_length=128, null=True)            ### 河川海岸（工種）名 ### FOR GROUP BY LEFT JOIN項目
    crop_damage = models.FloatField(null=True)                                 ### 農作物被害額（単位千円）
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ### FOR GROUP BY
    weather_name = models.CharField(max_length=128)                            ### 異常気象名 LEFT JOIN項目

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/02 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/02 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/02 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/02 追加

    action_code = models.CharField(max_length=10, null=True)                   ### 最新のアクションコード ※2022/08/02 追加
    status_code = models.CharField(max_length=10, null=True)                   ### 最新の状態コード ※2022/08/02 追加

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/11 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/07/11 追加

    ### 帳票の繰り返し部分 行20以降
    building_code = models.CharField(max_length=10, null=True)                 ### 建物区分コード
    building_name = models.CharField(max_length=128)                           ### 建物区分名 LEFT JOIN項目
    underground_code = models.CharField(max_length=10, null=True)              ### 地上地下区分コード
    underground_name = models.CharField(max_length=128)                        ### 地上地下区分名 LEFT JOIN項目
    flood_sediment_code = models.CharField(max_length=10, null=True)           ### 浸水土砂区分コード ### FOR SUM PARAM
    flood_sediment_name = models.CharField(max_length=128)                     ### 浸水土砂区分名 LEFT JOIN項目
    
    ### 入力データ
    building_lv00 = models.FloatField(null=True)                               ### 被害建物棟数_床下
    building_lv01_49 = models.FloatField(null=True)                            ### 被害建物棟数_01から49cm
    building_lv50_99 = models.FloatField(null=True)                            ### 被害建物棟数_50から99cm
    building_lv100 = models.FloatField(null=True)                              ### 被害建物棟数_100cm以上
    building_half = models.FloatField(null=True)                               ### 被害建物棟数_半壊
    building_full = models.FloatField(null=True)                               ### 被害建物棟数_全壊
    building_total = models.FloatField(null=True)                              ### 被害建物棟数_合計
    
    ### 入力データ
    floor_area = models.FloatField(null=True)                                  ### 延床面積
    family = models.IntegerField(null=True)                                    ### 被災世帯数
    office = models.IntegerField(null=True)                                    ### 被災事業所数
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    floor_area_lv00 = models.FloatField(null=True)                             ### 延床面積_床下
    floor_area_lv01_49 = models.FloatField(null=True)                          ### 延床面積_01から49cm
    floor_area_lv50_99 = models.FloatField(null=True)                          ### 延床面積_50から99cm
    floor_area_lv100 = models.FloatField(null=True)                            ### 延床面積_100cm以上
    floor_area_half = models.FloatField(null=True)                             ### 延床面積_半壊
    floor_area_full = models.FloatField(null=True)                             ### 延床面積_全壊
    floor_area_total = models.FloatField(null=True)                            ### 延床面積_合計
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    family_lv00 = models.FloatField(null=True)                                 ### 被災世帯数_床下
    family_lv01_49 = models.FloatField(null=True)                              ### 被災世帯数_01から49cm
    family_lv50_99 = models.FloatField(null=True)                              ### 被災世帯数_50から99cm
    family_lv100 = models.FloatField(null=True)                                ### 被災世帯数_100cm以上
    family_half = models.FloatField(null=True)                                 ### 被災世帯数_半壊
    family_full = models.FloatField(null=True)                                 ### 被災世帯数_全壊
    family_total = models.FloatField(null=True)                                ### 被災世帯数_合計
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    office_lv00 = models.FloatField(null=True)                                 ### 被災事業所数_床下
    office_lv01_49 = models.FloatField(null=True)                              ### 被災事業所数_01から49cm
    office_lv50_99 = models.FloatField(null=True)                              ### 被災事業所数_50から99cm
    office_lv100 = models.FloatField(null=True)                                ### 被災事業所数_100cm以上
    office_half = models.FloatField(null=True)                                 ### 被災事業所数_半壊
    office_full = models.FloatField(null=True)                                 ### 被災事業所数_全壊
    office_total = models.FloatField(null=True)                                ### 被災事業所数_合計
    
    ### 入力データ
    farmer_fisher_lv00 = models.FloatField(null=True)                          ### 農漁家戸数_床下
    farmer_fisher_lv01_49 = models.FloatField(null=True)                       ### 農漁家戸数_01から49cm
    farmer_fisher_lv50_99 = models.FloatField(null=True)                       ### 農漁家戸数_50から99cm
    farmer_fisher_lv100 = models.FloatField(null=True)                         ### 農漁家戸数_100cm以上
    ### farmer_fisher_half = models.FloatField(null=True)
    farmer_fisher_full = models.FloatField(null=True)                          ### 農漁家戸数_全壊
    farmer_fisher_total = models.FloatField(null=True)                         ### 農漁家戸数_合計

    ### 入力データ
    employee_lv00 = models.FloatField(null=True)                               ### 被災従業者数_床下
    employee_lv01_49 = models.FloatField(null=True)                            ### 被災従業者数_01から49cm
    employee_lv50_99 = models.FloatField(null=True)                            ### 被災従業者数_50から99cm
    employee_lv100 = models.FloatField(null=True)                              ### 被災従業者数_100cm以上
    ### employee_half = models.FloatField(null=True)
    employee_full = models.FloatField(null=True)                               ### 被災従業者数_全壊
    employee_total = models.FloatField(null=True)                              ### 被災従業者数_合計

    ### 入力データ
    industry_code = models.CharField(max_length=10, null=True)                 ### 産業分類コード ### FOR SUM PARAM
    industry_name = models.CharField(max_length=128)                           ### 産業分類名 LEFT JOIN項目
    usage_code = models.CharField(max_length=10, null=True)                    ### 地下空間の利用形態コード
    usage_name = models.CharField(max_length=128)                              ### 地下空間の利用形態名 LEFT JOIN項目
    comment = models.CharField(max_length=512, null=True)                      ### 備考

    class Meta:
        db_table = 'ippan_view'
        managed = False                                                        ### マイグレーションの対象外とする。

    def __str__(self):
        return '<IPPAN_VIEW: ' + self.ippan_id + '>'

###############################################################################
### 7050: 入力データ_公共土木地単調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class CHITAN_FILE(models.Model):
    chitan_file_id = models.IntegerField(primary_key=True)                     ### ファイルID ※2022/08/05 追加
    chitan_file_name = models.CharField(max_length=128, null=True)             ### ファイル名 ※2022/08/05 追加
    
    ### suikei_code = models.CharField(max_length=10, null=True)               ### 水系コード ※2022/08/05 追加
    ### kasen_code = models.CharField(max_length=10, null=True)                ### 河川コード ※2022/08/05 追加
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    ### city_code = models.CharField(max_length=10, null=True)                 ### 市区町村コード ※2022/08/05 追加
    ### weather_id = models.IntegerField(null=True)                            ### 異常気象ID ※2022/08/05 追加
    ### begin_date = models.DateField(null=True)                               ### 水害発生年月日 ※2022/08/05 追加
    ### end_date = models.DateField(null=True)                                 ### 水害終了年月日 ※2022/08/05 追加
    ### kasen_kaigan_code = models.CharField(max_length=10, null=True)         ### 河川海岸（工種）コード ※2022/08/05 追加
    
    ### point = models.CharField(max_length=128, null=True)                    ### 災害復旧箇所 ※2022/08/05 追加
    ### assessment = models.FloatField(null=True)                              ### 災害復旧査定額（千円） ※2022/08/05 追加
    ### comment = models.CharField(max_length=512, null=True)                  ### 備考 ※2022/08/05 追加

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/01 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/01 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/01 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'chitan_file'

    def __str__(self):
        return '<CHITAN_FILE: ' + self.chitan_file_id + '>'

###############################################################################
### 7060: 入力データ_公共土木地単調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class CHITAN(models.Model):
    chitan_id = models.IntegerField(primary_key=True)                          ### 行ID ※2022/08/05 追加
    chitan_name = models.CharField(max_length=128, null=True)                  ### 代表被災地区名 ※2022/08/05 追加

    chitan_file_id = models.IntegerField(null=True)                            ### ファイルID ※2022/08/05 追加
    
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ※2022/08/05 追加
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ※2022/08/05 追加
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ※2022/08/05 追加
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ※2022/08/05 追加
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ※2022/08/05 追加
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ※2022/08/05 追加
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ※2022/08/05 追加
    point = models.CharField(max_length=128, null=True)                        ### 災害復旧箇所 ※2022/08/05 追加
    assessment = models.FloatField(null=True)                                  ### 災害復旧査定額（千円） ※2022/08/05 追加
    comment = models.CharField(max_length=512, null=True)                      ### 備考 ※2022/08/05 追加

    ### upload_file_path = models.CharField(max_length=256, null=True)         ### アップロードファイルパス ※2022/08/01 追加
    ### upload_file_name = models.CharField(max_length=256, null=True)         ### アップロードファイル名 ※2022/08/01 追加
    ### summary_file_path = models.CharField(max_length=256, null=True)        ### 集計結果ファイルパス ※2022/08/01 追加
    ### summary_file_name = models.CharField(max_length=256, null=True)        ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'chitan'

    def __str__(self):
        return '<CHITAN: ' + self.chitan_id + '>'

###############################################################################
### 7070: 入力データ_公共土木補助調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class HOJO_FILE(models.Model):
    hojo_file_id = models.IntegerField(primary_key=True)                       ### ファイルID ※2022/08/05 追加
    hojo_file_name = models.CharField(max_length=128, null=True)               ### ファイル名 ※2022/08/05 追加
    
    ### suikei_code = models.CharField(max_length=10, null=True)               ### 水系コード ※2022/08/05 追加
    ### kasen_code = models.CharField(max_length=10, null=True)                ### 河川コード ※2022/08/05 追加
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    ### city_code = models.CharField(max_length=10, null=True)                 ### 市区町村コード ※2022/08/05 追加
    ### weather_id = models.IntegerField(null=True)                            ### 異常気象ID ※2022/08/05 追加
    ### begin_date = models.DateField(null=True)                               ### 水害発生年月日 ※2022/08/05 追加
    ### kasen_kaigan_code = models.CharField(max_length=10, null=True)         ### 河川海岸（工種）コード ※2022/08/05 追加
    ### koji_code = models.CharField(max_length=10, null=True)                 ### 工事番号 ※2022/08/05 追加
    ### branch_code = models.CharField(max_length=10, null=True)               ### 枝番 ※2022/08/05 追加
    ### determined = models.FloatField(null=True)                              ### 決定額（千円） ※2022/08/05 追加
    ### comment = models.CharField(max_length=512, null=True)                  ### 備考 ※2022/08/05 追加

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/01 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/01 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/01 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'hojo_file'

    def __str__(self):
        return '<HOJO_FILE: ' + self.hojo_file_id + '>'

###############################################################################
### 7080: 入力データ_公共土木補助調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class HOJO(models.Model):
    hojo_id = models.IntegerField(primary_key=True)                            ### 行ID ※2022/08/05 追加
    hojo_name = models.CharField(max_length=128, null=True)                    ###  ※2022/08/05 追加

    hojo_file_id = models.IntegerField(null=True)                              ### ファイルID ※2022/08/05 追加
    
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ※2022/08/05 追加
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ※2022/08/05 追加
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ※2022/08/05 追加
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ※2022/08/05 追加
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ※2022/08/05 追加
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ※2022/08/05 追加
    koji_code = models.CharField(max_length=10, null=True)                     ### 工事番号 ※2022/08/05 追加
    branch_code = models.CharField(max_length=10, null=True)                   ### 枝番 ※2022/08/05 追加
    determined = models.FloatField(null=True)                                  ### 決定額（千円） ※2022/08/05 追加
    comment = models.CharField(max_length=512, null=True)                      ### 備考 ※2022/08/05 追加

    ### upload_file_path = models.CharField(max_length=256, null=True)         ### アップロードファイルパス ※2022/08/01 追加
    ### upload_file_name = models.CharField(max_length=256, null=True)         ### アップロードファイル名 ※2022/08/01 追加
    ### summary_file_path = models.CharField(max_length=256, null=True)        ### 集計結果ファイルパス ※2022/08/01 追加
    ### summary_file_name = models.CharField(max_length=256, null=True)        ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'hojo'

    def __str__(self):
        return '<HOJO: ' + self.hojo_id + ', ' + self.hojo_name + '>'
        
###############################################################################
### 7090: 入力データ_公益事業調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class KOEKI_FILE(models.Model):
    koeki_file_id = models.IntegerField(primary_key=True)                      ### ファイルID ※2022/08/05 追加
    koeki_file_name = models.CharField(max_length=128, null=True)              ### ファイル名 ※2022/08/05 追加
    
    ### suikei_code = models.CharField(max_length=10, null=True)               ### 水系コード ※2022/08/05 追加
    ### kasen_code = models.CharField(max_length=10, null=True)                ### 河川コード ※2022/08/05 追加
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    ### city_code = models.CharField(max_length=10, null=True)                 ### 市区町村コード ※2022/08/05 追加
    ### begin_date = models.DateField(null=True)                               ### 水害発生年月日 ※2022/08/05 追加
    ### end_date = models.DateField(null=True)                                 ### 水害終了年月日 ※2022/08/05 追加
    ### kasen_kaigan_code = models.CharField(max_length=10, null=True)         ### 河川海岸（工種）コード ※2022/08/05 追加
    ### weather_id = models.IntegerField(null=True)                            ### 異常気象ID ※2022/08/05 追加
    ### cause_1_code = models.CharField(max_length=10, null=True)              ### 水害原因_1_コード ※2022/08/05 追加
    ### cause_2_code = models.CharField(max_length=10, null=True)              ### 水害原因_2_コード ※2022/08/05 追加
    ### cause_3_code = models.CharField(max_length=10, null=True)              ### 水害原因_3_コード ※2022/08/05 追加
    ### business_code = models.CharField(max_length=10, null=True)             ### 事業コード ※2022/08/05 追加
    ### koeki_industry_code = models.CharField(max_length=10, null=True)       ### 公益事業分類コード ※2022/08/09 追加
    ### institution_name = models.CharField(max_length=128, null=True)         ### 調査対象機関名称 ※2022/08/05 追加
    
    ### damage_property = models.FloatField(null=True)                         ### 被害金額_物的被害額（千円）
    ### damage_sales = models.FloatField(null=True)                            ### 被害金額_営業停止に伴う売上減少額
    ### damage_alt = models.FloatField(null=True)                              ### 被害金額_代替活動費（外注費）
    ### damage_other = models.FloatField(null=True)                            ### 被害金額_その他
    ### damage_total = models.FloatField(null=True)                            ### 被害金額_営業停止損失額合計（千円）
    
    ### sus_day = models.IntegerField(null=True)                               ### 営業停止期間等_停止期間_日
    ### sus_hour = models.IntegerField(null=True)                              ### 営業停止期間等_停止期間_時間
    ### sus_amount = models.IntegerField(null=True)                            ### 営業停止期間等_停止数量
    
    ### ref_dep_name = models.CharField(max_length=128, null=True)             ### 照会先_調査担当課名
    ### ref_emp_name = models.CharField(max_length=128, null=True)             ### 照会先_調査担当者名
    ### ref_tel = models.CharField(max_length=128, null=True)                  ### 照会先_電話番号
    
    ### comment = models.CharField(max_length=512, null=True)                  ### 備考 ※2022/08/05 追加

    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/08/01 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/08/01 追加
    summary_file_path = models.CharField(max_length=256, null=True)            ### 集計結果ファイルパス ※2022/08/01 追加
    summary_file_name = models.CharField(max_length=256, null=True)            ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'koeki_file'

    def __str__(self):
        return '<KOEKI_FILE: ' + self.koeki_file_id + '>'

###############################################################################
### 7100: 入力データ_公益事業調査票（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
class KOEKI(models.Model):
    koeki_id = models.IntegerField(primary_key=True)                           ### 行ID ※2022/08/05 追加
    koeki_name = models.CharField(max_length=128, null=True)                   ### 町丁名、大字名 ※2022/08/05 追加

    koeki_file_id = models.IntegerField(null=True)                             ### ファイルID ※2022/08/05 追加
    
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ※2022/08/05 追加
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ※2022/08/05 追加
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ※2022/08/05 追加
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ※2022/08/05 追加
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ※2022/08/05 追加
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ※2022/08/05 追加
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ※2022/08/05 追加
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ※2022/08/05 追加
    cause_1_code = models.CharField(max_length=10, null=True)                  ### 水害原因_1_コード ※2022/08/05 追加
    cause_2_code = models.CharField(max_length=10, null=True)                  ### 水害原因_2_コード ※2022/08/05 追加
    cause_3_code = models.CharField(max_length=10, null=True)                  ### 水害原因_3_コード ※2022/08/05 追加
    business_code = models.CharField(max_length=10, null=True)                 ### 事業コード ※2022/08/05 追加
    koeki_industry_code = models.CharField(max_length=10, null=True)           ### 公益事業分類コード ※2022/08/09 追加
    institution_name = models.CharField(max_length=128, null=True)             ### 調査対象機関名称 ※2022/08/05 追加
    
    damage_property = models.FloatField(null=True)                             ### 被害金額_物的被害額（千円）
    damage_sales = models.FloatField(null=True)                                ### 被害金額_営業停止に伴う売上減少額
    damage_alt = models.FloatField(null=True)                                  ### 被害金額_代替活動費（外注費）
    damage_other = models.FloatField(null=True)                                ### 被害金額_その他
    damage_total = models.FloatField(null=True)                                ### 被害金額_営業停止損失額合計（千円）
    
    sus_day = models.IntegerField(null=True)                                   ### 営業停止期間等_停止期間_日
    sus_hour = models.IntegerField(null=True)                                  ### 営業停止期間等_停止期間_時間
    sus_amount = models.IntegerField(null=True)                                ### 営業停止期間等_停止数量
    
    ref_dep_name = models.CharField(max_length=128, null=True)                 ### 照会先_調査担当課名
    ref_emp_name = models.CharField(max_length=128, null=True)                 ### 照会先_調査担当者名
    ref_tel = models.CharField(max_length=128, null=True)                      ### 照会先_電話番号
    
    comment = models.CharField(max_length=512, null=True)                      ### 備考 ※2022/08/05 追加

    ### upload_file_path = models.CharField(max_length=256, null=True)         ### アップロードファイルパス ※2022/08/01 追加
    ### upload_file_name = models.CharField(max_length=256, null=True)         ### アップロードファイル名 ※2022/08/01 追加
    ### summary_file_path = models.CharField(max_length=256, null=True)        ### 集計結果ファイルパス ※2022/08/01 追加
    ### summary_file_name = models.CharField(max_length=256, null=True)        ### 集計結果ファイル名 ※2022/08/01 追加
    
    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/08/05 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時 ※2022/08/05 追加

    class Meta:
        db_table = 'koeki'

    def __str__(self):
        return '<KOEKI: ' + self.koeki_id + ', ' + self.koeki_name + '>'

###############################################################################
###############################################################################
### 集計DB
###############################################################################
###############################################################################
        
###############################################################################
### 8000: 集計データ（集計DB）
###############################################################################
class IPPAN_SUMMARY(models.Model):
    ### ippan_summary_id = models.IntegerField(primary_key=True)               ### postgresの自動インクリメントを使用する。 ※一般資産調査票の複数行の集計計算を１個のSQLで行うため ※MAX(*_ID+1)の場合、FORループが必要となる。
    ippan_id = models.IntegerField(null=True)                                  ### 行ID
    suigai_id = models.IntegerField(null=True)                                 ### シートID
    
    ### 家屋被害額(集計DB)
    house_summary_lv00 = models.FloatField(null=True)                          ### 家屋被害額_床下（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）
    house_summary_lv01_49 = models.FloatField(null=True)                       ### 家屋被害額_01から49cm（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）
    house_summary_lv50_99 = models.FloatField(null=True)                       ### 家屋被害額_50から99cm（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）
    house_summary_lv100 = models.FloatField(null=True)                         ### 家屋被害額_100cm以上（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）
    house_summary_half = models.FloatField(null=True)                          ### 家屋被害額_半壊（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）
    house_summary_full = models.FloatField(null=True)                          ### 家屋被害額_全壊（延床面積×家屋評価額×浸水または土砂ごとの勾配差による被害率）

    ### 家庭用品自動車以外被害額(集計DB)
    household_summary_lv00 = models.FloatField(null=True)                      ### 家庭用品自動車以外被害額_床下（被災世帯数×家庭用品所有額×浸水または土砂による被害率）
    household_summary_lv01_49 = models.FloatField(null=True)                   ### 家庭用品自動車以外被害額_01から49cm（被災世帯数×家庭用品所有額×浸水または土砂による被害率）
    household_summary_lv50_99 = models.FloatField(null=True)                   ### 家庭用品自動車以外被害額_50から99cm（被災世帯数×家庭用品所有額×浸水または土砂による被害率）
    household_summary_lv100 = models.FloatField(null=True)                     ### 家庭用品自動車以外被害額_100cm以上（被災世帯数×家庭用品所有額×浸水または土砂による被害率）
    household_summary_half = models.FloatField(null=True)                      ### 家庭用品自動車以外被害額_半壊（被災世帯数×家庭用品所有額×浸水または土砂による被害率）
    household_summary_full = models.FloatField(null=True)                      ### 家庭用品自動車以外被害額_全壊（被災世帯数×家庭用品所有額×浸水または土砂による被害率）

    ### 家庭用品自動車被害額(集計DB) 
    car_summary_lv00 = models.FloatField(null=True)                            ### 家庭用品自動車被害額_床下（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）
    car_summary_lv01_49 = models.FloatField(null=True)                         ### 家庭用品自動車被害額_01から49cm（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）
    car_summary_lv50_99 = models.FloatField(null=True)                         ### 家庭用品自動車被害額_50から99cm（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）
    car_summary_lv100 = models.FloatField(null=True)                           ### 家庭用品自動車被害額_100cm以上（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）
    car_summary_half = models.FloatField(null=True)                            ### 家庭用品自動車被害額_半壊（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）
    car_summary_full = models.FloatField(null=True)                            ### 家庭用品自動車被害額_全壊（被災世帯数×家庭用品自動車所有額×浸水または土砂による被害率）

    ### 家庭応急対策費_代替活動費(集計DB) 
    house_alt_summary_lv00 = models.FloatField(null=True)                      ### 家庭応急対策費_代替活動費_床下（被災世帯数×代替活動費）
    house_alt_summary_lv01_49 = models.FloatField(null=True)                   ### 家庭応急対策費_代替活動費_01から49cm（被災世帯数×代替活動費）
    house_alt_summary_lv50_99 = models.FloatField(null=True)                   ### 家庭応急対策費_代替活動費_50から99cm（被災世帯数×代替活動費）
    house_alt_summary_lv100 = models.FloatField(null=True)                     ### 家庭応急対策費_代替活動費_100cm以上（被災世帯数×代替活動費）
    house_alt_summary_half = models.FloatField(null=True)                      ### 家庭応急対策費_代替活動費_半壊（被災世帯数×代替活動費）
    house_alt_summary_full = models.FloatField(null=True)                      ### 家庭応急対策費_代替活動費_全壊（被災世帯数×代替活動費）

    ### 家庭応急対策費_清掃費(集計DB) 
    house_clean_summary_lv00 = models.FloatField(null=True)                    ### 家庭応急対策費_清掃費_床下（被災世帯数×清掃日数×清掃労働単価）
    house_clean_summary_lv01_49 = models.FloatField(null=True)                 ### 家庭応急対策費_清掃費_01から49cm（被災世帯数×清掃日数×清掃労働単価）
    house_clean_summary_lv50_99 = models.FloatField(null=True)                 ### 家庭応急対策費_清掃費_50から99cm（被災世帯数×清掃日数×清掃労働単価）
    house_clean_summary_lv100 = models.FloatField(null=True)                   ### 家庭応急対策費_清掃費_100cm以上（被災世帯数×清掃日数×清掃労働単価）
    house_clean_summary_half = models.FloatField(null=True)                    ### 家庭応急対策費_清掃費_半壊（被災世帯数×清掃日数×清掃労働単価）
    house_clean_summary_full = models.FloatField(null=True)                    ### 家庭応急対策費_清掃費_全壊（被災世帯数×清掃日数×清掃労働単価）

    ### 事業所被害額_償却資産被害額(集計DB) 
    office_dep_summary_lv00 = models.FloatField(null=True)                     ### 事業所被害額_償却資産被害額_床下（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    office_dep_summary_lv01_49 = models.FloatField(null=True)                  ### 事業所被害額_償却資産被害額_01から49cm（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    office_dep_summary_lv50_99 = models.FloatField(null=True)                  ### 事業所被害額_償却資産被害額_50から99cm（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    office_dep_summary_lv100 = models.FloatField(null=True)                    ### 事業所被害額_償却資産被害額_100cm以上（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    ### office_dep_summary_half = models.FloatField(null=True)                 ### 事業所被害額_償却資産被害額_半壊（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    office_dep_summary_full = models.FloatField(null=True)                     ### 事業所被害額_償却資産被害額_全壊（従業者数×産業分類ごとの償却資産×浸水または土砂による被害率）
    
    ### 事業所被害額_在庫資産被害額(集計DB) 
    office_inv_summary_lv00 = models.FloatField(null=True)                     ### 事業所被害額_在庫資産被害額_床下（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    office_inv_summary_lv01_49 = models.FloatField(null=True)                  ### 事業所被害額_在庫資産被害額_01から49cm（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    office_inv_summary_lv50_99 = models.FloatField(null=True)                  ### 事業所被害額_在庫資産被害額_50から99cm（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    office_inv_summary_lv100 = models.FloatField(null=True)                    ### 事業所被害額_在庫資産被害額_100cm以上（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    ### office_inv_summary_half = models.FloatField(null=True)                 ### 事業所被害額_在庫資産被害額_半壊（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    office_inv_summary_full = models.FloatField(null=True)                     ### 事業所被害額_在庫資産被害額_全壊（従業者数×産業分類ごとの在庫資産×浸水または土砂による被害率）
    
    ### 事業所被害額_営業停止に伴う被害額(集計DB) 
    office_sus_summary_lv00 = models.FloatField(null=True)                     ### 事業所被害額_営業停止に伴う被害額_床下（従業者数×営業停止日数×付加価値額）
    office_sus_summary_lv01_49 = models.FloatField(null=True)                  ### 事業所被害額_営業停止に伴う被害額_01から49cm（従業者数×営業停止日数×付加価値額）
    office_sus_summary_lv50_99 = models.FloatField(null=True)                  ### 事業所被害額_営業停止に伴う被害額_50から99cm（従業者数×営業停止日数×付加価値額）
    office_sus_summary_lv100 = models.FloatField(null=True)                    ### 事業所被害額_営業停止に伴う被害額_100cm以上（従業者数×営業停止日数×付加価値額）
    ### office_sus_summary_half = models.FloatField(null=True)                 ### 事業所被害額_営業停止に伴う被害額_半壊（従業者数×営業停止日数×付加価値額）
    office_sus_summary_full = models.FloatField(null=True)                     ### 事業所被害額_営業停止に伴う被害額_全壊（従業者数×営業停止日数×付加価値額）

    ### 事業所被害額_営業停滞に伴う被害額(集計DB) 
    office_stg_summary_lv00 = models.FloatField(null=True)                     ### 事業所被害額_営業停滞に伴う被害額_床下（従業者数×（営業停滞日数/2）×付加価値額）
    office_stg_summary_lv01_49 = models.FloatField(null=True)                  ### 事業所被害額_営業停滞に伴う被害額_01から49cm（従業者数×（営業停滞日数/2）×付加価値額）
    office_stg_summary_lv50_99 = models.FloatField(null=True)                  ### 事業所被害額_営業停滞に伴う被害額_50から99cm（従業者数×（営業停滞日数/2）×付加価値額）
    office_stg_summary_lv100 = models.FloatField(null=True)                    ### 事業所被害額_営業停滞に伴う被害額_100cm以上（従業者数×（営業停滞日数/2）×付加価値額）
    ### office_stg_summary_half = models.FloatField(null=True)                 ### 事業所被害額_営業停滞に伴う被害額_半壊（従業者数×（営業停滞日数/2）×付加価値額）
    office_stg_summary_full = models.FloatField(null=True)                     ### 事業所被害額_営業停滞に伴う被害額_全壊（従業者数×（営業停滞日数/2）×付加価値額）

    ### 農漁家被害額_償却資産被害額(集計DB)
    farmer_fisher_dep_summary_lv00 = models.FloatField(null=True)              ### 農漁家被害額_償却資産被害額_床下（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）
    farmer_fisher_dep_summary_lv01_49 = models.FloatField(null=True)           ### 農漁家被害額_償却資産被害額_01から49cm（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）
    farmer_fisher_dep_summary_lv50_99 = models.FloatField(null=True)           ### 農漁家被害額_償却資産被害額_50から99cm（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）
    farmer_fisher_dep_summary_lv100 = models.FloatField(null=True)             ### 農漁家被害額_償却資産被害額_100cm以上（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）
    ### farmer_fisher_dep_summary_half = models.FloatField(null=True)          ### 農漁家被害額_償却資産被害額_半壊（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）
    farmer_fisher_dep_summary_full = models.FloatField(null=True)              ### 農漁家被害額_償却資産被害額_全壊（農漁家戸数×農漁家の償却資産×浸水または土砂による被害率）

    ### 農漁家被害額_在庫資産被害額(集計DB) 
    farmer_fisher_inv_summary_lv00 = models.FloatField(null=True)              ### 農漁家被害額_在庫資産被害額_床下（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）
    farmer_fisher_inv_summary_lv01_49 = models.FloatField(null=True)           ### 農漁家被害額_在庫資産被害額_01から49cm（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）
    farmer_fisher_inv_summary_lv50_99 = models.FloatField(null=True)           ### 農漁家被害額_在庫資産被害額_50から99cm（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）
    farmer_fisher_inv_summary_lv100 = models.FloatField(null=True)             ### 農漁家被害額_在庫資産被害額_100cm以上（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）
    ### farmer_fisher_inv_summary_half = models.FloatField(null=True)          ### 農漁家被害額_在庫資産被害額_半壊（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）
    farmer_fisher_inv_summary_full = models.FloatField(null=True)              ### 農漁家被害額_在庫資産被害額_全壊（農漁家戸数×農漁家の在庫資産×浸水または土砂による被害率）

    ### 事業所応急対策費_代替活動費(集計DB) 
    office_alt_summary_lv00 = models.FloatField(null=True)                     ### 事業所応急対策費_代替活動費_床下（事業所数×代替活動費）
    office_alt_summary_lv01_49 = models.FloatField(null=True)                  ### 事業所応急対策費_代替活動費_01から49cm（事業所数×代替活動費）
    office_alt_summary_lv50_99 = models.FloatField(null=True)                  ### 事業所応急対策費_代替活動費_50から99cm（事業所数×代替活動費）
    office_alt_summary_lv100 = models.FloatField(null=True)                    ### 事業所応急対策費_代替活動費_100cm以上（事業所数×代替活動費）
    office_alt_summary_half = models.FloatField(null=True)                     ### 事業所応急対策費_代替活動費_半壊（事業所数×代替活動費）
    office_alt_summary_full = models.FloatField(null=True)                     ### 事業所応急対策費_代替活動費_全壊（事業所数×代替活動費）

    committed_at = models.DateTimeField(null=True)                             ### コミット日時 ※2022/07/11 追加
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時
    
    class Meta:
        db_table = 'ippan_summary'
        
    def __str__(self):
        return '<IPPAN_SUMMARY: ' + self.ippan_summary_id + '>'

###############################################################################
###############################################################################
### 自動化DB
###############################################################################
###############################################################################

###############################################################################
### 10000: アクション（自動化DB）
###############################################################################
class ACTION(models.Model):
    action_code = models.CharField(max_length=10, primary_key=True)            ### アクションコード
    action_name = models.CharField(max_length=128, null=True)                  ### アクション名_日本語
    action_name_en = models.CharField(max_length=128, null=True)               ### アクション名_英語
    
    class Meta:
        db_table = 'action'
    
    def __str__(self):
        return '<ACTION: ' + self.action_code + '>'

###############################################################################
### 10010: 状態（自動化DB）
###############################################################################
class STATUS(models.Model):
    status_code = models.CharField(max_length=10, primary_key=True)            ### 状態コード
    status_name = models.CharField(max_length=128, null=True)                  ### 状態名
    
    class Meta:
        db_table = 'status'
    
    def __str__(self):
        return '<STATUS: ' + self.status_code + '>'

###############################################################################
### 10020: トリガーメッセージ（自動化DB）
###############################################################################
class TRIGGER(models.Model):
    trigger_id = models.IntegerField(primary_key=True)                         ### トリガーID
    suigai_id = models.IntegerField(null=True)                                 ### シートID
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード

    action_code = models.CharField(max_length=10, null=True)                   ### アクションコード
    status_code = models.CharField(max_length=10, null=True)                   ### 状態コード
    success_count = models.IntegerField(null=True)                             ### 成功数
    failure_count = models.IntegerField(null=True)                             ### 失敗数

    download_file_path = models.CharField(max_length=256, null=True)           ### ダウンロードファイルパス ※2022/07/14 追加
    download_file_name = models.CharField(max_length=256, null=True)           ### ダウンロードファイル名 ※2022/07/14 追加
    upload_file_path = models.CharField(max_length=256, null=True)             ### アップロードファイルパス ※2022/07/14 追加
    upload_file_name = models.CharField(max_length=256, null=True)             ### アップロードファイル名 ※2022/07/14 追加

    integrity_ok = models.TextField(null=True)                                 ### データ整合性 Row, Col, left, right, verified result, 
    integrity_ng = models.TextField(null=True)                                 ### データ整合性 Row, Col, left, right, verified result, 
    success_log = models.TextField(null=True)                                  ### データ整合性 Row, Col, left, right, verified result, 
    failure_log = models.TextField(null=True)                                  ### データ整合性 Row, Col, left, right, verified result, 

    published_at = models.DateTimeField(null=True)                             ### 発行日時
    consumed_at = models.DateTimeField(null=True)                              ### 消費日時
    deleted_at = models.DateTimeField(null=True)                               ### 削除日時
    
    class Meta:
        db_table = 'trigger'
    
    def __str__(self):
        return '<TRIGGER: ' + self.trigger_id + '>'

### ---: 復旧事業工種
class RESTORATION(models.Model):
    restoration_code = models.CharField(max_length=10, primary_key=True)
    restoration_name = models.CharField(max_length=128)

    class Meta:
        db_table = 'restoration'

    def __str__(self):
        return '<RESTORATION: ' + self.restoration_code + ', ' + self.restoration_name + '>'
