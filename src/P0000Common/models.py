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
### マスタDB
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
        return '<BUILDING: ' + self.building_code + ', ' + self.building_name + '>'

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
        return '<KEN: ' + self.ken_code + ', ' + self.ken_name + '>'

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

    class Meta:
        db_table = 'city'
    
    def __str__(self):
        return '<CITY: ' + self.city_code + ', ' + self.city_name + '>'

class CITY_VIEW(models.Model):
    city_code = models.CharField(max_length=10, primary_key=True)              ### 市区町村コード
    city_name = models.CharField(max_length=128)                               ### 市区町村名
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名
    city_population = models.IntegerField()                                    ### 市区町村人口
    city_area = models.IntegerField()                                          ### 市区町村面積

    class Meta:
        db_table = 'city_view'
        managed = False                                                        ### マイグレーションの対象外とする。
    
    def __str__(self):
        return '<CITY_VIEW: ' + self.city_code + ', ' + self.city_name + '>'

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
        return '<KASEN_KAIGAN: ' + self.kasen_kaigan_code + ', ' + self.kasen_kaigan_name + '>'

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
        return '<SUIKEI: ' + self.suikei_code + ', ' + self.suikei_name + '>'

class SUIKEI_VIEW(models.Model):
    suikei_code = models.CharField(max_length=10, primary_key=True)            ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名
    suikei_type_code = models.CharField(max_length=10)                         ### 水系種別コード
    suikei_type_name = models.CharField(max_length=128)                        ### 水系種別名
    
    class Meta:
        db_table = 'suikei_view'
        managed = False                                                        ### マイグレーションの対象外とする。
    
    def __str__(self):
        return '<SUIKEI_VIEW: ' + self.suikei_code + ', ' + self.suikei_name + '>'

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
        return '<SUIKEI_TYPE: ' + self.suikei_type_code + ', ' + self.suikei_type_name + '>'

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
        return '<KASEN: ' + self.kasen_code + ', ' + self.kasen_name + '>'

class KASEN_VIEW(models.Model):
    kasen_code = models.CharField(max_length=10, primary_key=True)             ### 河川コード
    kasen_name = models.CharField(max_length=128)                              ### 河川名
    kasen_type_code = models.CharField(max_length=10)                          ### 河川種別コード
    kasen_type_name = models.CharField(max_length=128)                         ### 河川種別名
    suikei_code = models.CharField(max_length=10)                              ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名

    class Meta:
        db_table = 'kasen_view'
        managed = False                                                        ### マイグレーションの対象外とする。

    def __str__(self):
        return '<KASEN_VIEW: ' + self.kasen_code + ', ' + self.kasen_name + '>'

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
        return '<KASEN_TYPE: ' + self.kasen_type_code + ', ' + self.kasen_type_name + '>'

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
        return '<CAUSE: ' + self.cause_code + ', ' + self.cause_name + '>'

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
        return '<UNDERGROUND: ' + self.underground_code + ', ' + self.underground_name + '>'

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
        return '<USAGE: ' + self.usage_code + ', ' + self.usage_name + '>'

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
        return '<FLOOD_SEDIMENT: ' + self.flood_sediment_code + ', ' + self.flood_sediment_name + '>'
    
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
        return '<GRADIENT: ' + self.gradient_code + ', ' + self.gradient_name + '>'

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
        return '<INDUSTRY: ' + self.industry_code + ', ' + self.industry_name + '>'

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

class HOUSE_ASSET_VIEW(models.Model):
    house_asset_code = models.CharField(max_length=10, primary_key=True)       ### 家屋評価額コード
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名
    house_asset = models.FloatField(null=True)                                 ### 家屋評価額

    class Meta:
        db_table = 'house_asset_view'
        managed = False                                                        ### マイグレーションの対象外とする。

    def __str__(self):
        return '<HOUSE_ASSET_VIEW: ' + self.house_asset_code + '>'

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

class HOUSE_RATE_VIEW(models.Model):
    house_rate_code = models.CharField(max_length=10, primary_key=True)        ### 家屋被害率コード
    flood_sediment_code = models.CharField(max_length=10)                      ### 浸水土砂区分コード
    flood_sediment_name = models.CharField(max_length=128)                     ### 浸水土砂区分名
    gradient_code = models.CharField(max_length=10)                            ### 地盤勾配区分コード
    gradient_name = models.CharField(max_length=128)                           ### 地盤勾配区分名
    house_rate_lv00 = models.FloatField()                                      ### 家屋被害率_床下
    house_rate_lv00_50 = models.FloatField()                                   ### 家屋被害率_0から50cm未満
    house_rate_lv50_100 = models.FloatField()                                  ### 家屋被害率_50から100cm未満
    house_rate_lv100_200 = models.FloatField()                                 ### 家屋被害率_100から200cm未満
    house_rate_lv200_300 = models.FloatField()                                 ### 家屋被害率_200から300cm未満
    house_rate_lv300 = models.FloatField()                                     ### 家屋被害率_300cm以上

    class Meta:
        db_table = 'house_rate_view'
        managed = False                                                        ### マイグレーションの対象外とする。

    def __str__(self):
        return '<HOUSE_RATE_VIEW: ' + self.house_rate_code + '>'
    
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

### ---: 家庭応急対策費（マスタDB） ※削除予定
class HOUSE_COST(models.Model):
    house_cost_code = models.CharField(max_length=10, primary_key=True)        ### 家庭応急対策費コード
    house_cost_year = models.IntegerField()                                    ### 家庭応急対策費対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    alt_lv00 = models.FloatField()                                             ### 代替活動費_床下
    alt_lv00_50 = models.FloatField()                                          ### 代替活動費_0から50cm未満
    alt_lv50_100 = models.FloatField()                                         ### 代替活動費_50から100cm未満
    alt_lv100_200 = models.FloatField()                                        ### 代替活動費_100から200cm未満
    alt_lv200_300 = models.FloatField()                                        ### 代替活動費_200から300cm未満
    alt_lv300 = models.FloatField()                                            ### 代替活動費_300cm以上
    clean_lv00 = models.FloatField()                                           ### 清掃費_床下
    clean_lv00_50 = models.FloatField()                                        ### 清掃費_0から50cm未満
    clean_lv50_100 = models.FloatField()                                       ### 清掃費_50から100cm未満
    clean_lv100_200 = models.FloatField()                                      ### 清掃費_100から200cm未満
    clean_lv200_300 = models.FloatField()                                      ### 清掃費_200から300cm未満
    clean_lv300 = models.FloatField()                                          ### 清掃費_300cm以上
    house_cost = models.FloatField()                                           ### 清掃労働単価

    class Meta:
        db_table = 'house_cost'

    def __str__(self):
        return '<HOUSE_COST: ' + self.house_cost_code + '>'

### ---: 事業所営業停止損失（マスタDB） ※削除予定
class OFFICE_COST(models.Model):
    office_cost_code = models.CharField(max_length=10, primary_key=True)       ### 事業所営業損失コード
    office_cost_year = models.IntegerField()                                   ### 事業所営業損失対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    suspend_lv00 = models.FloatField()                                         ### 営業停止日数_床下
    suspend_lv00_50 = models.FloatField()                                      ### 営業停止日数_0から50cm未満
    suspend_lv50_100 = models.FloatField()                                     ### 営業停止日数_50から100cm未満
    suspend_lv100_200 = models.FloatField()                                    ### 営業停止日数_100から200cm未満
    suspend_lv200_300 = models.FloatField()                                    ### 営業停止日数_200から300cm未満
    suspend_lv300 = models.FloatField()                                        ### 営業停止日数_300cm以上
    stagnate_lv00 = models.FloatField()                                        ### 営業停滞日数_床下
    stagnate_lv00_50 = models.FloatField()                                     ### 営業停滞日数_0から50cm未満
    stagnate_lv50_100 = models.FloatField()                                    ### 営業停滞日数_50から100cm未満
    stagnate_lv100_200 = models.FloatField()                                   ### 営業停滞日数_100から200cm未満
    stagnate_lv200_300 = models.FloatField()                                   ### 営業停滞日数_200から300cm未満
    stagnate_lv300 = models.FloatField()                                       ### 営業停滞日数_300cm以上
    alt_lv00 = models.FloatField(null=True)                                    ### 代替活動費_床下
    alt_lv00_50 = models.FloatField(null=True)                                 ### 代替活動費_0から50cm未満
    alt_lv50_100 = models.FloatField(null=True)                                ### 代替活動費_50から100cm未満
    alt_lv100_200 = models.FloatField(null=True)                               ### 代替活動費_100から200cm未満
    alt_lv200_300 = models.FloatField(null=True)                               ### 代替活動費_200から300cm未満
    alt_lv300 = models.FloatField(null=True)                                   ### 代替活動費_300cm以上

    class Meta:
        db_table = 'office_cost'

    def __str__(self):
        return '<OFFICE_COST: ' + self.office_cost_code + '>'
    
### ---: 家屋被害率（マスタDB） ※削除予定
class HOUSE_DAMAGE(models.Model):
    house_damage_code = models.CharField(max_length=10, primary_key=True)      ### 家屋被害率コード
    house_damage_year = models.IntegerField()                                  ### 家屋被害率対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    fl_gr1_lv00 = models.FloatField()                                          ### 被害率_浸水_勾配1_床下
    fl_gr1_lv00_50 = models.FloatField()                                       ### 被害率_浸水_勾配1_0から50cm未満
    fl_gr1_lv50_100 = models.FloatField()                                      ### 被害率_浸水_勾配1_50から100cm未満
    fl_gr1_lv100_200 = models.FloatField()                                     ### 被害率_浸水_勾配1_100から200cm未満
    fl_gr1_lv200_300 = models.FloatField()                                     ### 被害率_浸水_勾配1_200から300cm未満
    fl_gr1_lv300 = models.FloatField()                                         ### 被害率_浸水_勾配1_300cm以上
    fl_gr2_lv00 = models.FloatField()                                          ### 被害率_浸水_勾配2_床下
    fl_gr2_lv00_50 = models.FloatField()                                       ### 被害率_浸水_勾配2_0から50cm未満
    fl_gr2_lv50_100 = models.FloatField()                                      ### 被害率_浸水_勾配2_50から100cm未満
    fl_gr2_lv100_200 = models.FloatField()                                     ### 被害率_浸水_勾配2_100から200cm未満
    fl_gr2_lv200_300 = models.FloatField()                                     ### 被害率_浸水_勾配2_200から300cm未満
    fl_gr2_lv300 = models.FloatField()                                         ### 被害率_浸水_勾配2_300cm以上
    fl_gr3_lv00 = models.FloatField()                                          ### 被害率_浸水_勾配3_床下
    fl_gr3_lv00_50 = models.FloatField()                                       ### 被害率_浸水_勾配3_0から50cm未満
    fl_gr3_lv50_100 = models.FloatField()                                      ### 被害率_浸水_勾配3_50から100cm未満
    fl_gr3_lv100_200 = models.FloatField()                                     ### 被害率_浸水_勾配3_100から200cm未満
    fl_gr3_lv200_300 = models.FloatField()                                     ### 被害率_浸水_勾配3_200から300cm未満
    fl_gr3_lv300 = models.FloatField()                                         ### 被害率_浸水_勾配3_300cm以上
    sd_gr1_lv00 = models.FloatField()                                          ### 被害率_土砂_勾配1_床下
    sd_gr1_lv00_50 = models.FloatField()                                       ### 被害率_土砂_勾配1_0から50cm未満
    sd_gr1_lv50_100 = models.FloatField()                                      ### 被害率_土砂_勾配1_50から100cm未満
    sd_gr1_lv100_200 = models.FloatField()                                     ### 被害率_土砂_勾配1_100から200cm未満
    sd_gr1_lv200_300 = models.FloatField()                                     ### 被害率_土砂_勾配1_200から300cm未満
    sd_gr1_lv300 = models.FloatField()                                         ### 被害率_土砂_勾配1_300cm以上
    sd_gr2_lv00 = models.FloatField()                                          ### 被害率_土砂_勾配2_床下
    sd_gr2_lv00_50 = models.FloatField()                                       ### 被害率_土砂_勾配2_0から50cm未満
    sd_gr2_lv50_100 = models.FloatField()                                      ### 被害率_土砂_勾配2_50から100cm未満
    sd_gr2_lv100_200 = models.FloatField()                                     ### 被害率_土砂_勾配2_100から200cm未満
    sd_gr2_lv200_300 = models.FloatField()                                     ### 被害率_土砂_勾配2_200から300cm未満
    sd_gr2_lv300 = models.FloatField()                                         ### 被害率_土砂_勾配2_300cm以上
    sd_gr3_lv00 = models.FloatField()                                          ### 被害率_土砂_勾配3_床下
    sd_gr3_lv00_50 = models.FloatField()                                       ### 被害率_土砂_勾配3_0から50cm未満
    sd_gr3_lv50_100 = models.FloatField()                                      ### 被害率_土砂_勾配3_50から100cm未満
    sd_gr3_lv100_200 = models.FloatField()                                     ### 被害率_土砂_勾配3_100から200cm未満
    sd_gr3_lv200_300 = models.FloatField()                                     ### 被害率_土砂_勾配3_200から300cm未満
    sd_gr3_lv300 = models.FloatField()                                         ### 被害率_土砂_勾配3_300cm以上

    class Meta:
        db_table = 'house_damage'

    def __str__(self):
        return '<HOUSE_DAMAGE: ' + self.house_damage_code + '>'

### ---: 家庭用品自動車以外被害率（マスタDB） ※削除予定
class HOUSEHOLD_DAMAGE(models.Model):
    household_damage_code = models.CharField(max_length=10, primary_key=True)  ### 家庭用品自動車以外被害率コード
    household_damage_year = models.IntegerField()                              ### 家庭用品自動車以外被害率対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    fl_lv00 = models.FloatField()                                              ### 被害率_浸水_床下
    fl_lv00_50 = models.FloatField()                                           ### 被害率_浸水_0から50cm未満
    fl_lv50_100 = models.FloatField()                                          ### 被害率_浸水_50から100cm未満
    fl_lv100_200 = models.FloatField()                                         ### 被害率_浸水_100から200cm未満
    fl_lv200_300 = models.FloatField()                                         ### 被害率_浸水_200から300cm未満
    fl_lv300 = models.FloatField()                                             ### 被害率_浸水_300cm以上
    sd_lv00 = models.FloatField()                                              ### 被害率_土砂_床下
    sd_lv00_50 = models.FloatField()                                           ### 被害率_土砂_0から50cm未満
    sd_lv50_100 = models.FloatField()                                          ### 被害率_土砂_50から100cm未満
    sd_lv100_200 = models.FloatField()                                         ### 被害率_土砂_100から200cm未満
    sd_lv200_300 = models.FloatField()                                         ### 被害率_土砂_200から300cm未満
    sd_lv300 = models.FloatField()                                             ### 被害率_土砂_300cm以上
    household_asset = models.FloatField()                                      ### 家庭用品自動車以外所有額

    class Meta:
        db_table = 'household_damage'

    def __str__(self):
        return '<HOUSEHOLD_DAMAGE: ' + self.household_damage_code + '>'

### ---: 家庭用品自動車被害率（マスタDB） ※削除予定
class CAR_DAMAGE(models.Model):
    car_damage_code = models.CharField(max_length=10, primary_key=True)        ### 自動車被害率コード
    car_damage_year = models.IntegerField()                                    ### 自動車被害率対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    fl_lv00 = models.FloatField()                                              ### 被害率_浸水_床下
    fl_lv00_50 = models.FloatField()                                           ### 被害率_浸水_0から50cm未満
    fl_lv50_100 = models.FloatField()                                          ### 被害率_浸水_50から100cm未満
    fl_lv100_200 = models.FloatField()                                         ### 被害率_浸水_100から200cm未満
    fl_lv200_300 = models.FloatField()                                         ### 被害率_浸水_200から300cm未満
    fl_lv300 = models.FloatField()                                             ### 被害率_浸水_300cm以上
    car_asset = models.FloatField()                                            ### 家庭用品自動車所有額

    class Meta:
        db_table = 'car_damage'

    def __str__(self):
        return '<CAR_DAMAGE: ' + self.car_damage_code + '>'

### ---: 事業所被害率（マスタDB） ※削除予定
class OFFICE_DAMAGE(models.Model):
    office_damage_code = models.CharField(max_length=10, primary_key=True)     ### 事業所被害率コード
    office_damage_year = models.IntegerField()                                 ### 事業所被害率対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    dep_fl_lv00 = models.FloatField()                                          ### 償却資産率_浸水_床下
    dep_fl_lv00_50 = models.FloatField()                                       ### 償却資産率_浸水_0から50cm未満
    dep_fl_lv50_100 = models.FloatField()                                      ### 償却資産率_浸水_50から100cm未満
    dep_fl_lv100_200 = models.FloatField()                                     ### 償却資産率_浸水_100から200cm未満
    dep_fl_lv200_300 = models.FloatField()                                     ### 償却資産率_浸水_200から300cm未満
    dep_fl_lv300 = models.FloatField()                                         ### 償却資産率_浸水_300cm以上
    dep_sd_lv00 = models.FloatField()                                          ### 償却資産率_土砂_床下
    dep_sd_lv00_50 = models.FloatField()                                       ### 償却資産率_土砂_0から50cm未満
    dep_sd_lv50_100 = models.FloatField()                                      ### 償却資産率_土砂_50から100cm未満
    dep_sd_lv100_200 = models.FloatField()                                     ### 償却資産率_土砂_100から200cm未満
    dep_sd_lv200_300 = models.FloatField()                                     ### 償却資産率_土砂_200から300cm未満
    dep_sd_lv300 = models.FloatField()                                         ### 償却資産率_土砂_300cm以上
    inv_fl_lv00 = models.FloatField()                                          ### 在庫資産率_浸水_床下
    inv_fl_lv00_50 = models.FloatField()                                       ### 在庫資産率_浸水_0から50cm未満
    inv_fl_lv50_100 = models.FloatField()                                      ### 在庫資産率_浸水_50から100cm未満
    inv_fl_lv100_200 = models.FloatField()                                     ### 在庫資産率_浸水_100から200cm未満
    inv_fl_lv200_300 = models.FloatField()                                     ### 在庫資産率_浸水_200から300cm未満
    inv_fl_lv300 = models.FloatField()                                         ### 在庫資産率_浸水_300cm以上
    inv_sd_lv00 = models.FloatField()                                          ### 在庫資産率_土砂_床下
    inv_sd_lv00_50 = models.FloatField()                                       ### 在庫資産率_土砂_0から50cm未満
    inv_sd_lv50_100 = models.FloatField()                                      ### 在庫資産率_土砂_50から100cm未満
    inv_sd_lv100_200 = models.FloatField()                                     ### 在庫資産率_土砂_100から200cm未満
    inv_sd_lv200_300 = models.FloatField()                                     ### 在庫資産率_土砂_200から300cm未満
    inv_sd_lv300 = models.FloatField()                                         ### 在庫資産率_土砂_300cm以上

    class Meta:
        db_table = 'office_damage'

    def __str__(self):
        return '<OFFICE_DAMAGE: ' + self.office_damage_code + '>'

### ---: 農漁家被害率（マスタDB） ※削除予定
class FARMER_FISHER_DAMAGE(models.Model):
    farmer_fisher_damage_code = models.CharField(max_length=10, primary_key=True)   ### 農漁家被害率コード
    farmer_fisher_damage_year = models.IntegerField()                          ### 農漁家被害率対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    dep_fl_lv00 = models.FloatField()                                          ### 償却資産被害率_浸水_床下
    dep_fl_lv00_50 = models.FloatField()                                       ### 償却資産被害率_浸水_0から50cm未満
    dep_fl_lv50_100 = models.FloatField()                                      ### 償却資産被害率_浸水_50から100cm未満
    dep_fl_lv100_200 = models.FloatField()                                     ### 償却資産被害率_浸水_100から200cm未満
    dep_fl_lv200_300 = models.FloatField()                                     ### 償却資産被害率_浸水_200から300cm未満
    dep_fl_lv300 = models.FloatField()                                         ### 償却資産被害率_浸水_300cm以上
    dep_sd_lv00 = models.FloatField()                                          ### 償却資産被害率_土砂_床下
    dep_sd_lv00_50 = models.FloatField()                                       ### 償却資産被害率_土砂_0から50cm未満
    dep_sd_lv50_100 = models.FloatField()                                      ### 償却資産被害率_土砂_50から100cm未満
    dep_sd_lv100_200 = models.FloatField()                                     ### 償却資産被害率_土砂_100から200cm未満
    dep_sd_lv200_300 = models.FloatField()                                     ### 償却資産被害率_土砂_200から300cm未満
    dep_sd_lv300 = models.FloatField()                                         ### 償却資産被害率_土砂_300cm以上
    inv_fl_lv00 = models.FloatField()                                          ### 在庫資産被害率_浸水_床下
    inv_fl_lv00_50 = models.FloatField()                                       ### 在庫資産被害率_浸水_0から50cm未満
    inv_fl_lv50_100 = models.FloatField()                                      ### 在庫資産被害率_浸水_50から100cm未満
    inv_fl_lv100_200 = models.FloatField()                                     ### 在庫資産被害率_浸水_100から200cm未満
    inv_fl_lv200_300 = models.FloatField()                                     ### 在庫資産被害率_浸水_200から300cm未満
    inv_fl_lv300 = models.FloatField()                                         ### 在庫資産被害率_浸水_300cm以上
    inv_sd_lv00 = models.FloatField()                                          ### 在庫資産被害率_土砂_床下
    inv_sd_lv00_50 = models.FloatField()                                       ### 在庫資産被害率_土砂_0から50cm未満
    inv_sd_lv50_100 = models.FloatField()                                      ### 在庫資産被害率_土砂_50から100cm未満
    inv_sd_lv100_200 = models.FloatField()                                     ### 在庫資産被害率_土砂_100から200cm未満
    inv_sd_lv200_300 = models.FloatField()                                     ### 在庫資産被害率_土砂_200から300cm未満
    inv_sd_lv300 = models.FloatField()                                         ### 在庫資産被害率_土砂_300cm以上
    depreciable_asset = models.IntegerField()                                  ### 農漁家償却資産額
    inventory_asset = models.IntegerField()                                    ### 農漁家在庫資産額

    class Meta:
        db_table = 'farmer_fisher_damage'

    def __str__(self):
        return '<FARMER_FISHER_DAMAGE: ' + self.farmer_fisher_damage_code + '>'

###############################################################################
### 入力DB
###############################################################################

###############################################################################
### 7000: 一般資産入力データ_水害区域（入力DB）
###############################################################################
class AREA(models.Model):
    area_id = models.IntegerField(primary_key=True)                            ### 水害区域ID
    area_name = models.CharField(max_length=128)                               ### 水害区域名

    class Meta:
        db_table = 'area'

    def __str__(self):
        return '<AREA: ' + self.area_id + ', ' + self.area_name + '>'

###############################################################################
### 7010: 一般資産入力データ_異常気象（入力DB）
###############################################################################
class WEATHER(models.Model):
    weather_id = models.IntegerField(primary_key=True)                         ### 異常気象ID
    weather_name = models.CharField(max_length=128)                            ### 異常気象名
    ### weather_year = models.IntegerField()                                   ### 異常気象対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日

    class Meta:
        db_table = 'weather'
    
    def __str__(self):
        return '<WEATHER: ' + self.weather_id + ', ' + self.weather_name + '>'

###############################################################################
### 7020: 一般資産入力データ_ヘッダ部分（入力DB）
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
### 調査員調査票のヘッダ部分（都道府県、市区町村、水害区域番号、水害区域面積、農作物被害額、異常気象コードなど）と
### 調査員調査票の一覧部分（町丁名、被害建物棟数など）の扱いについて、
### 重複しても被害額の算出に影響しない項目（都道府県、市区町村、水害区域番号、異常気象コードなど）は、SUIGAI、IPPAN両方に持たせても良い。
### 重複すると被害額の算出に影響する項目（水害区域面積、農作物被害額）は、SUIGAIのみに持たせる。
### DBの正規化（整合性）の観点からは、IPPANの外部キーにSUIGAI_IDを持たせて、SUIGAIに持たせた都道府県、市区町村、水害区域番号、異常気象コードを優先させることが望ましい。
### 水害（発生年月日）と水害区域番号との関係が１対１であるのか？異なる水害（発生年月日）で水害区域（番号）の使い回しがあるのか？疑問。
###############################################################################
class SUIGAI(models.Model):
    suigai_id = models.IntegerField(primary_key=True)                          ### 水害ID
    suigai_name = models.CharField(max_length=128, null=True)                  ### 水害名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ### 例えば、新たなヘッダ部分の情報が登録できるとしても、実際に被害建物棟数が判明するまでは、その情報を管理することができない。
    ### また、ヘッダ部分の終了日が変更になると、複数のレコードを更新しなければならないため不整合を生じる恐れがある。
    ### https://torazuka.hatenablog.com/entry/20110713/pk
    ### https://oss-db.jp/dojo/dojo_info_04
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

    ### 第2正規形の考え方からヘッダ部分を別テーブル（水害テーブル）に分割する。
    ### 別テーブル（水害テーブル）に分割したことによりリレーションを表すSUIGAI_IDを追加する。
    ### 別テーブル（水害テーブル）の主キーは単純な連番とする。
    ### 都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名などに複合ユニークキーを設定する。
    ### 同じ都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名で複数の水害区域面積、農作物被害額、異常気象などが登録できないようにするためである。
    ### 複数の水害区域面積、農作物被害額、異常気象を登録するためには、水害区域番号を別途追加するか、水害発生日を別途追加するようにさせるためである。

    class Meta:
        db_table = 'suigai'
        ### constraints = [
        ###     models.UniqueConstraint(
        ###         fields=['ken_code', 'city_code', 'begin_date', 'cause_1_code', 'area_id', 'suikei_code', 'kasen_code', 'gradient_code'],
        ###         name='suigai_unique'
        ###     ),
        ### ]

    def __str__(self):
        return '<SUIGAI: ' + self.suigai_id + ', ' + self.suigai_name + '>'

###############################################################################
### 7030: 一般資産入力データ_一覧表部分（入力DB）
###############################################################################
class IPPAN(models.Model):
    ippan_id = models.IntegerField(primary_key=True)                           ### 一般資産調査票ID
    ippan_name = models.CharField(max_length=128, null=True)                   ### 一般資産調査票名（町丁名、大字名）
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ### 例えば、新たなヘッダ部分の情報が登録できるとしても、実際に被害建物棟数が判明するまでは、その情報を管理することができない。
    ### また、ヘッダ部分の終了日が変更になると、複数のレコードを更新しなければならないため不整合を生じる恐れがある。
    ### https://torazuka.hatenablog.com/entry/20110713/pk
    ### https://oss-db.jp/dojo/dojo_info_04

    ### 帳票のヘッダ部分 行10

    ### 帳票のヘッダ部分 行14

    ### 第2正規形の考え方からヘッダ部分を別テーブル（水害テーブル）に分割する。
    ### 別テーブル（水害テーブル）に分割したことによりリレーションを表すSUIGAI_IDを追加する。
    ### 別テーブル（水害テーブル）の主キーは単純な連番とする。
    ### 都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名などに複合ユニークキーを設定する。
    ### 同じ都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名で複数の水害区域面積、農作物被害額、異常気象などが登録できないようにするためである。
    ### 複数の水害区域面積、農作物被害額、異常気象を登録するためには、水害区域番号を別途追加するか、水害発生日を別途追加するようにさせるためである。
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID

    ### 帳票の繰り返し部分 行20以降
    building_code = models.CharField(max_length=10, null=True)                 ### 建物区分コード
    underground_code = models.CharField(max_length=10, null=True)              ### 地上地下区分コード
    flood_sediment_code = models.CharField(max_length=10, null=True)           ### 浸水土砂区分コード ### FOR SUM PARAM
    
    ### 入力データ
    building_lv00 = models.IntegerField(null=True)                             ### 被害建物棟数_床下
    building_lv01_49 = models.IntegerField(null=True)                          ### 被害建物棟数_01から49cm
    building_lv50_99 = models.IntegerField(null=True)                          ### 被害建物棟数_50から99cm
    building_lv100 = models.IntegerField(null=True)                            ### 被害建物棟数_100cm以上
    building_half = models.IntegerField(null=True)                             ### 被害建物棟数_半壊
    building_full = models.IntegerField(null=True)                             ### 被害建物棟数_全壊
    
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
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    family_lv00 = models.IntegerField(null=True)                               ### 被災世帯数_床下
    family_lv01_49 = models.IntegerField(null=True)                            ### 被災世帯数_01から49cm
    family_lv50_99 = models.IntegerField(null=True)                            ### 被災世帯数_50から99cm
    family_lv100 = models.IntegerField(null=True)                              ### 被災世帯数_100cm以上
    family_half = models.IntegerField(null=True)                               ### 被災世帯数_半壊
    family_full = models.IntegerField(null=True)                               ### 被災世帯数_全壊
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    office_lv00 = models.IntegerField(null=True)                               ### 被災事業所数_床下
    office_lv01_49 = models.IntegerField(null=True)                            ### 被災事業所数_01から49cm
    office_lv50_99 = models.IntegerField(null=True)                            ### 被災事業所数_50から99cm
    office_lv100 = models.IntegerField(null=True)                              ### 被災事業所数_100cm以上
    office_half = models.IntegerField(null=True)                               ### 被災事業所数_半壊
    office_full = models.IntegerField(null=True)                               ### 被災事業所数_全壊
    
    ### 入力データ
    farmer_fisher_lv00 = models.IntegerField(null=True)                        ### 農漁家戸数_床下
    farmer_fisher_lv01_49 = models.IntegerField(null=True)                     ### 農漁家戸数_01から49cm
    farmer_fisher_lv50_99 = models.IntegerField(null=True)                     ### 農漁家戸数_50から99cm
    farmer_fisher_lv100 = models.IntegerField(null=True)                       ### 農漁家戸数_100cm以上
    ### farmer_fisher_half = models.IntegerField(null=True)
    farmer_fisher_full = models.IntegerField(null=True)                        ### 農漁家戸数_全壊

    ### 入力データ
    employee_lv00 = models.IntegerField(null=True)                             ### 被災従業者数_床下
    employee_lv01_49 = models.IntegerField(null=True)                          ### 被災従業者数_01から49cm
    employee_lv50_99 = models.IntegerField(null=True)                          ### 被災従業者数_50から99cm
    employee_lv100 = models.IntegerField(null=True)                            ### 被災従業者数_100cm以上
    ### employee_half = models.IntegerField(null=True)
    employee_full = models.IntegerField(null=True)                             ### 被災従業者数_全壊

    ### 入力データ
    industry_code = models.CharField(max_length=10, null=True)                 ### 産業分類コード ### FOR SUM PARAM
    usage_code = models.CharField(max_length=10, null=True)                    ### 地下空間の利用形態コード
    comment = models.CharField(max_length=512, null=True)                      ### 備考

    class Meta:
        db_table = 'ippan'

    def __str__(self):
        return '<IPPAN: ' + self.ippan_id + ', ' + self.ippan_name + '>'

###############################################################################
### 7040: 一般資産調査票（入力DB）
###############################################################################
class IPPAN_VIEW(models.Model):
    ippan_id = models.IntegerField(primary_key=True)                           ### 一般資産調査票ID
    ippan_name = models.CharField(max_length=128, null=True)                   ### 一般資産調査票名（町丁名、大字名）

    ### 第2正規形の考え方からヘッダ部分を別テーブル（水害テーブル）に分割する。
    ### 別テーブル（水害テーブル）に分割したことによりリレーションを表すSUIGAI_IDを追加する。
    ### 別テーブル（水害テーブル）の主キーは単純な連番とする。
    ### 都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名などに複合ユニークキーを設定する。
    ### 同じ都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名で複数の水害区域面積、農作物被害額、異常気象などが登録できないようにするためである。
    ### 複数の水害区域面積、農作物被害額、異常気象を登録するためには、水害区域番号を別途追加するか、水害発生日を別途追加するようにさせるためである。
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    suigai_name = models.CharField(max_length=128, null=True)                  ### 水害名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ### 例えば、新たなヘッダ部分の情報が登録できるとしても、実際に被害建物棟数が判明するまでは、その情報を管理することができない。
    ### また、ヘッダ部分の終了日が変更になると、複数のレコードを更新しなければならないため不整合を生じる恐れがある。
    ### https://torazuka.hatenablog.com/entry/20110713/pk
    ### https://oss-db.jp/dojo/dojo_info_04
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名
    city_code = models.CharField(max_length=10)                                ### 市区町村コード
    city_name = models.CharField(max_length=128)                               ### 市区町村名
    begin_date = models.DateField(null=True)                                   ### 水害発生年月日 ### FOR GROUP BY
    end_date = models.DateField(null=True)                                     ### 水害終了年月日 ### FOR GROUP BY
    cause_1_code = models.CharField(max_length=10)                             ### 水害原因コード1
    cause_1_name = models.CharField(max_length=128)                            ### 水害原因名1
    cause_2_code = models.CharField(max_length=10)                             ### 水害原因コード2
    cause_2_name = models.CharField(max_length=128)                            ### 水害原因名2
    cause_3_code = models.CharField(max_length=10)                             ### 水害原因コード3
    cause_3_name = models.CharField(max_length=128)                            ### 水害原因名3
    area_id = models.IntegerField()                                            ### 水害区域ID
    area_name = models.CharField(max_length=128)                               ### 水害区域名

    ### 帳票のヘッダ部分 行10
    suikei_code = models.CharField(max_length=10)                              ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名
    suikei_type_code = models.CharField(max_length=10)                         ### 水系種別コード
    suikei_type_name = models.CharField(max_length=128)                        ### 水系種別名
    kasen_code = models.CharField(max_length=10)                               ### 河川コード
    kasen_name = models.CharField(max_length=128)                              ### 河川名
    kasen_type_code = models.CharField(max_length=10)                          ### 河川種別コード
    kasen_type_name = models.CharField(max_length=128)                         ### 河川種別名
    gradient_code = models.CharField(max_length=10)                            ### 地盤勾配区分コード
    gradient_name = models.CharField(max_length=128)                           ### 地盤勾配区分名

    ### 帳票のヘッダ部分 行14
    residential_area = models.FloatField(null=True)                            ### 宅地面積（単位m2）
    agricultural_area = models.FloatField(null=True)                           ### 農地面積（単位m2）
    underground_area = models.FloatField(null=True)                            ### 地下面積（単位m2）
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ### FOR GROUP BY
    kasen_kaigan_name = models.CharField(max_length=128, null=True)            ### 河川海岸（工種）名 ### FOR GROUP BY
    crop_damage = models.FloatField(null=True)                                 ### 農作物被害額（単位千円）
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ### FOR GROUP BY
    weather_name = models.CharField(max_length=128)                            ### 異常気象名

    ### 帳票の繰り返し部分 行20以降
    building_code = models.CharField(max_length=10, null=True)                 ### 建物区分コード
    building_name = models.CharField(max_length=128)                           ### 建物区分名
    underground_code = models.CharField(max_length=10, null=True)              ### 地上地下区分コード
    underground_name = models.CharField(max_length=128)                        ### 地上地下区分名
    flood_sediment_code = models.CharField(max_length=10, null=True)           ### 浸水土砂区分コード ### FOR SUM PARAM
    flood_sediment_name = models.CharField(max_length=128)                     ### 浸水土砂区分名
    
    ### 入力データ
    building_lv00 = models.IntegerField(null=True)                             ### 被害建物棟数_床下
    building_lv01_49 = models.IntegerField(null=True)                          ### 被害建物棟数_01から49cm
    building_lv50_99 = models.IntegerField(null=True)                          ### 被害建物棟数_50から99cm
    building_lv100 = models.IntegerField(null=True)                            ### 被害建物棟数_100cm以上
    building_half = models.IntegerField(null=True)                             ### 被害建物棟数_半壊
    building_full = models.IntegerField(null=True)                             ### 被害建物棟数_全壊
    building_total = models.IntegerField(null=True)                            ### 被害建物棟数_合計
    
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
    family_lv00 = models.IntegerField(null=True)                               ### 被災世帯数_床下
    family_lv01_49 = models.IntegerField(null=True)                            ### 被災世帯数_01から49cm
    family_lv50_99 = models.IntegerField(null=True)                            ### 被災世帯数_50から99cm
    family_lv100 = models.IntegerField(null=True)                              ### 被災世帯数_100cm以上
    family_half = models.IntegerField(null=True)                               ### 被災世帯数_半壊
    family_full = models.IntegerField(null=True)                               ### 被災世帯数_全壊
    family_total = models.IntegerField(null=True)                              ### 被災世帯数_合計
    
    ### 導出データ 第1正規形の考え方からは他のカラムから導出可能な項目は削除する
    office_lv00 = models.IntegerField(null=True)                               ### 被災事業所数_床下
    office_lv01_49 = models.IntegerField(null=True)                            ### 被災事業所数_01から49cm
    office_lv50_99 = models.IntegerField(null=True)                            ### 被災事業所数_50から99cm
    office_lv100 = models.IntegerField(null=True)                              ### 被災事業所数_100cm以上
    office_half = models.IntegerField(null=True)                               ### 被災事業所数_半壊
    office_full = models.IntegerField(null=True)                               ### 被災事業所数_全壊
    office_total = models.IntegerField(null=True)                              ### 被災事業所数_合計
    
    ### 入力データ
    farmer_fisher_lv00 = models.IntegerField(null=True)                        ### 農漁家戸数_床下
    farmer_fisher_lv01_49 = models.IntegerField(null=True)                     ### 農漁家戸数_01から49cm
    farmer_fisher_lv50_99 = models.IntegerField(null=True)                     ### 農漁家戸数_50から99cm
    farmer_fisher_lv100 = models.IntegerField(null=True)                       ### 農漁家戸数_100cm以上
    ### farmer_fisher_half = models.IntegerField(null=True)
    farmer_fisher_full = models.IntegerField(null=True)                        ### 農漁家戸数_全壊
    farmer_fisher_total = models.IntegerField(null=True)                       ### 農漁家戸数_合計

    ### 入力データ
    employee_lv00 = models.IntegerField(null=True)                             ### 被災従業者数_床下
    employee_lv01_49 = models.IntegerField(null=True)                          ### 被災従業者数_01から49cm
    employee_lv50_99 = models.IntegerField(null=True)                          ### 被災従業者数_50から99cm
    employee_lv100 = models.IntegerField(null=True)                            ### 被災従業者数_100cm以上
    ### employee_half = models.IntegerField(null=True)
    employee_full = models.IntegerField(null=True)                             ### 被災従業者数_全壊
    employee_total = models.IntegerField(null=True)                            ### 被災従業者数_合計

    ### 入力データ
    industry_code = models.CharField(max_length=10, null=True)                 ### 産業分類コード ### FOR SUM PARAM
    industry_name = models.CharField(max_length=128)                           ### 産業分類名
    usage_code = models.CharField(max_length=10, null=True)                    ### 地下空間の利用形態コード
    usage_name = models.CharField(max_length=128)                              ### 地下空間の利用形態名
    comment = models.CharField(max_length=512, null=True)                  ### 備考

    class Meta:
        db_table = 'ippan_view'
        managed = False                                                        ### マイグレーションの対象外とする。

    def __str__(self):
        return '<IPPAN_VIEW: ' + self.ippan_id + ', ' + self.ippan_name + '>'

###############################################################################
### 集計DB
###############################################################################
        
###############################################################################
### 8000: 一般資産集計データ（集計DB）
###############################################################################
class IPPAN_SUMMARY(models.Model):
    ### ippan_summary_id = models.IntegerField(primary_key=True)               ### postgresの自動インクリメントを使用する。 ※一般資産調査票の複数行の集計計算を１個のSQLで行うため ※MAX(*_ID+1)の場合、FORループが必要となる。
    ippan_id = models.IntegerField(null=True)                                  ### 一般資産調査票ID
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    
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
    
    class Meta:
        db_table = 'ippan_summary'
        
    def __str__(self):
        return '<IPPAN_SUMMARY: ' + self.ippan_summary_id + '>'

###############################################################################
### 自動化 DB
###############################################################################

###############################################################################
### 9000: 一般資産集計データ（自動化 DB）
### CI/CD Automatic Test, Automatic Quality Assurance, Insight
### circleci
### 出力データ_一般資産調査票_チェックアウト: P0200ExcelDownload
### 入力データ_一般資産調査票_チェックイン: P0300ExcelUpload
###   入力データ検証: Automated Acceptance Test
###   按分計算: Proportional Calculation
###   逆計算による按分データ検証: Automated Reverse Verification
###   集計計算: Summary Calculation
###   逆計算による集計データ検証: Automated Reverse Verification
### 入力データ_水害区域図_チェックイン: P0310AreaUpload
###   入力データ検証: Automated Acceptance Test
###   集計計算: Summary Calculation, Group By Area
###   逆計算による集計データ検証: Automated Reverse Verification
### 入力データ_異常気象コード_チェックイン: P0320WeatherUpload
###   入力データ検証: Automated Acceptance Test
###   集計計算: Summary Calculation, Group By Weather
###   逆計算による集計データ検証: Automated Reverse Verification
### マニュアルによるデータ検証: Manual Verification
### リリース: Release
###############################################################################
class REPOSITORY(models.Model):
    repository_id = models.IntegerField(primary_key=True)                      ### レポジトリID
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    action_code = models.CharField(max_length=10, null=True)                   ### アクションコード
    ### 1: 一般資産調査票_チェックアウト ※ここは管理しないため、REPOSITORY、TRIGGERデータも存在しない。
    ### 2: 一般資産調査票_チェックイン ※ここは管理しないため、REPOSITORY、TRIGGERデータも存在しない。
    ### 3: 入力データ検証 ※一般資産調査票アップロード時の処理である。※ここでREPOSITORY、TRIGGERデータが作成される。
    ### 4: 按分計算 ※ビュー表のため自動で計算される。
    ### 5: 逆計算による按分データ検証
    ### 6: 集計計算
    ### 7: 逆計算による集計データ検証 ※とりあえずここまで実装する。
    ### 8: 水害区域図_チェックイン ※未実装
    ### 9: 入力データ検証 ※未実装
    ### 10: 集計計算 ※未実装
    ### 11: 逆計算による集計データ検証 ※未実装
    ### 12: 異常気象コード_チェックイン ※未実装
    ### 13: 入力データ検証 ※未実装
    ### 14: 集計計算 ※未実装
    ### 15: 逆計算による集計データ検証 ※未実装
    ### 16: マニュアルによるデータ検証 ※未実装
    ### 17: リリース ※未実装

    status_code = models.CharField(max_length=10, null=True)                   ### 状態コード
    ### 1: 実行中: running
    ### 2: キャンセル: cancel
    ### 3: 成功: success
    ### 4: 失敗: failure
    
    created_at = models.DateTimeField(null=True)                               ### 初期生成日
    updated_at = models.DateTimeField(null=True)                               ### 更新日
    
    success_count = models.IntegerField(null=True)                             ### 成功数
    failure_count = models.IntegerField(null=True)                             ### 失敗数
    
    input_file_path = models.CharField(max_length=256, null=True)              ### 
    ### output_file_path = models.CharField(max_length=256, null=True)         ### 
    
    class Meta:
        db_table = 'repository'
    
    def __str__(self):
        return '<REPOSITORY: ' + self.repository_id + '>'

class TRIGGER(models.Model):
    trigger_id = models.IntegerField(primary_key=True)                         ### トリガID
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    repository_id = models.IntegerField(null=True)                             ### レポジトリID
    status_code = models.CharField(max_length=10, null=True)                   ### 状態コード
    action_code = models.CharField(max_length=10, null=True)                   ### アクションコード
    published_at = models.DateTimeField(null=True)                             ### 発行日時
    consumed_at = models.DateTimeField(null=True)                              ### 消費日時
    success_count = models.IntegerField(null=True)                             ### 成功数
    failure_count = models.IntegerField(null=True)                             ### 失敗数
    ### success_rate = models.FloatField(null=True)                            ### 成功率
    
    class Meta:
        db_table = 'trigger'
    
    def __str__(self):
        return '<TRIGGER: ' + self.trigger_id + '>'

class APPROVAL(models.Model):
    approval_id = models.IntegerField(primary_key=True)                        ### 承認ID
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    action_code = models.CharField(max_length=10, null=True)                   ### アクションコード
    published_at = models.DateTimeField(null=True)                             ### 発行日時
    consumed_at = models.DateTimeField(null=True)                              ### 消費日時
    
    class Meta:
        db_table = 'approval'
        
    def __str__(self):
        return '<APPROVAL: ' + self.approval_id + '>'
    
class FEEDBACK(models.Model):
    feedback_id = models.IntegerField(primary_key=True)                        ### フィードバックID
    suigai_id = models.IntegerField(null=True)                                 ### 水害ID
    action_code = models.CharField(max_length=10, null=True)                   ### アクションコード
    published_at = models.DateTimeField(null=True)                             ### 発行日時
    consumed_at = models.DateTimeField(null=True)                              ### 消費日時
    
    class Meta:
        db_table = 'feedback'
        
    def __str__(self):
        return '<FEEDBACK: ' + self.approval_id + '>'

class ACTION(models.Model):
    action_code = models.CharField(max_length=10, primary_key=True)            ### アクションコード
    action_name = models.CharField(max_length=128, null=True)                  ### アクション名
    
    class Meta:
        db_table = 'action'
    
    def __str__(self):
        return '<ACTION: ' + self.action_code + '>'

###############################################################################
### 9010: 一般資産調査票（管理DB）
###############################################################################
class IPPAN_REPORT(models.Model):
    ippan_report_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        db_table = 'ippan_report'
        
    def __str__(self):
        return '<IPPAN_REPORT: ' + self.ippan_report_id + '>'

###############################################################################
### その他DB、未使用DB
###############################################################################
        
### ---: 公共土木レポート
class KOKYO_REPORT(models.Model):
    kokyo_report_id = models.CharField(max_length=10, primary_key=True)        
    
    class Meta:
        db_table = 'kokyo_report'
        
    def __str__(self):
        return '<KOKYO_REPORT: ' + self.kokyo_report_id + '>'
    
### ---: 公益事業レポート
class KOEKI_REPORT(models.Model):
    koeki_report_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        db_table = 'koeki_report'
        
    def __str__(self):
        return '<KOEKI_REPORT: ' + self.koeki_report_id + '>'

### ---: 承認履歴
class APPROVE_HISTORY(models.Model):
    approve_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        db_table = 'approve_history'
        
    def __str__(self):
        return '<APPROVE_HISTORY: ' + self.approve_history_id + '>'

### ---: 集計履歴
class REPORT_HISTORY(models.Model):
    report_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        db_table = 'report_history'
        
    def __str__(self):
        return '<REPORT_HISTORY: ' + self.report_history_id + '>'

### ---: 配布履歴
class DISTRIBUTE_HISTORY(models.Model):
    distribute_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        db_table = 'distribute_history'
        
    def __str__(self):
        return '<DISTRIBUTE_HISTORY: ' + self.distribute_history_id + '>'

### ---: 
class TRANSACT(models.Model):
    transact_id = models.IntegerField(primary_key=True)
    download_date = models.DateTimeField()
    upload_date = models.DateTimeField()
    transact_date = models.DateTimeField()
    schedule_date = models.DateTimeField()
    download_user_id = models.CharField(max_length=10)
    upload_user_id = models.CharField(max_length=10)
    transact_user_id = models.CharField(max_length=10)
    ken_code = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    approve_disapprove_undetermin_code = models.CharField(max_length=10)
    ippan_kokyo_koeki_code = models.CharField(max_length=10)
    ippan_kokyo_koeki_id = models.CharField(max_length=10)
    comment = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'transact'
        
    def __str__(self):
        return '<TRANSACT: ' + self.transact_id + '>'

### ---: 
class IPPAN_KOKYO_KOEKI(models.Model):
    ippan_kokyo_koeki_code = models.CharField(max_length=10)
    ippan_kokyo_koeki_name = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'ippan_kokyo_koeki'
        
    def __str__(self):
        return '<IPPAN_KOKYO_KOEKI: ' + self.ippan_kokyo_koeki_code + '>'

### ---: 復旧事業工種
class RESTORATION(models.Model):
    restoration_code = models.CharField(max_length=10, primary_key=True)
    restoration_name = models.CharField(max_length=128)

    class Meta:
        db_table = 'restoration'

    def __str__(self):
        return '<RESTORATION: ' + self.restoration_code + ', ' + self.restoration_name + '>'

### ---: 公共土木調査票
class KOKYO(models.Model):
    kokyo_id = models.IntegerField(primary_key=True)
    kokyo_name = models.CharField(max_length=128, null=True)
    ken_code = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    weather_id = models.IntegerField()
    kokyo_year = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'kokyo'

    def __str__(self):
        return '<KOKYO: ' + self.kokyo_id + ', ' + self.kokyo_name + '>'
        
### ---: 公益事業調査票
class KOEKI(models.Model):
    koeki_id = models.IntegerField(primary_key=True)
    koeki_name = models.CharField(max_length=128, null=True)
    ken_code = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    weather_id = models.IntegerField()
    koeki_year = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'koeki'

    def __str__(self):
        return '<KOEKI: ' + self.koeki_id + ', ' + self.koeki_name + '>'

### ---: 
class TEST_20220614(models.Model):    
    test_name = models.FloatField(null=True)
    
    class Meta:
        db_table = 'test_20220614'
        
    def __str__(self):
        return '<TEST_20220614: ' + self.test_name + '>'