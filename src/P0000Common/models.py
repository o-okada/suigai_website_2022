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
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 001: 建物区分
class BUILDING(models.Model):
    building_code = models.CharField(max_length=10, primary_key=True)          ### 建物区分コード
    building_name = models.CharField(max_length=128)                           ### 建物区分名

    class Meta:
        ### db_table = 'p0000common_building'
        ### db_table = 'suigai_web_building'
        db_table = 'building'
    
    def __str__(self):
        return '<BUILDING: ' + self.building_code + ', ' + self.building_name + '>'

### 002: 都道府県
class KEN(models.Model):
    ken_code = models.CharField(max_length=10, primary_key=True)               ### 都道府県コード
    ken_name = models.CharField(max_length=128)                                ### 都道府県名

    class Meta:
        ### db_table = 'p0000common_ken'
        ### db_table = 'suigai_web_ken'
        db_table = 'ken'
    
    def __str__(self):
        return '<KEN: ' + self.ken_code + ', ' + self.ken_name + '>'

### 003: 市区町村
class CITY(models.Model):
    city_code = models.CharField(max_length=10, primary_key=True)              ### 市区町村コード
    city_name = models.CharField(max_length=128)                               ### 市区町村名
    ken_code = models.CharField(max_length=10)                                 ### 都道府県コード
    city_population = models.IntegerField()                                    ### 市区町村人口
    city_area = models.IntegerField()                                          ### 市区町村面積

    class Meta:
        ### db_table = 'p0000common_city'
        ### db_table = 'suigai_web_city'
        db_table = 'city'
    
    def __str__(self):
        return '<CITY: ' + self.city_code + ', ' + self.city_name + '>'

### 004: 水害発生地点工種（河川海岸区分）
class KASEN_KAIGAN(models.Model):
    kasen_kaigan_code = models.CharField(max_length=10, primary_key=True)      ### 河川海岸区分コード
    kasen_kaigan_name = models.CharField(max_length=128)                       ### 河川海岸区分名

    class Meta:
        ### db_table = 'p0000common_kasen_kaigan'
        ### db_table = 'suigai_web_kasen_kaigan'
        db_table = 'kasen_kaigan'
 
    def __str__(self):
        return '<KASEN_KAIGAN: ' + self.kasen_kaigan_code + ', ' + self.kasen_kaigan_name + '>'

### 005: 水系（水系・沿岸）
class SUIKEI(models.Model):
    suikei_code = models.CharField(max_length=10, primary_key=True)            ### 水系コード
    suikei_name = models.CharField(max_length=128)                             ### 水系名
    suikei_type_code = models.CharField(max_length=10)                         ### 水系種別コード

    class Meta:
        ### db_table = 'p0000common_suikei'
        ### db_table = 'suigai_web_suikei'
        db_table = 'suikei'

    def __str__(self):
        return '<SUIKEI: ' + self.suikei_code + ', ' + self.suikei_name + '>'

### 006: 水系種別（水系・沿岸種別）
class SUIKEI_TYPE(models.Model):
    suikei_type_code = models.CharField(max_length=10, primary_key=True)       ### 水系種別コード
    suikei_type_name = models.CharField(max_length=128)                        ### 水系種別名

    class Meta:
        ### db_table = 'p0000common_suikei_type'
        ### db_table = 'suigai_web_suikei_type'
        db_table = 'suikei_type'

    def __str__(self):
        return '<SUIKEI_TYPE: ' + self.suikei_type_code + ', ' + self.suikei_type_name + '>'

### 007: 河川（河川・海岸）
class KASEN(models.Model):
    kasen_code = models.CharField(max_length=10, primary_key=True)             ### 河川コード
    kasen_name = models.CharField(max_length=128)                              ### 河川名
    kasen_type_code = models.CharField(max_length=10)                          ### 河川種別コード
    suikei_code = models.CharField(max_length=10)                              ### 水系コード

    class Meta:
        ### db_table = 'p0000common_kasen'
        ### db_table = 'suigai_web_kasen'
        db_table = 'kasen'

    def __str__(self):
        return '<KASEN: ' + self.kasen_code + ', ' + self.kasen_name + '>'

### 008: 河川種別（河川・海岸種別）
class KASEN_TYPE(models.Model):
    kasen_type_code = models.CharField(max_length=10, primary_key=True)        ### 河川種別コード
    kasen_type_name = models.CharField(max_length=128)                         ### 河川種別名

    class Meta:
        ### db_table = 'p0000common_kasen_type'
        ### db_table = 'suigai_web_kasen_type'
        db_table = 'kasen_type'

    def __str__(self):
        return '<KASEN_TYPE: ' + self.kasen_type_code + ', ' + self.kasen_type_name + '>'

### 009: 水害原因
class CAUSE(models.Model):    
    cause_code = models.CharField(max_length=10, primary_key=True)             ### 水害原因コード
    cause_name = models.CharField(max_length=128)                              ### 水害原因名

    class Meta:
        ### db_table = 'p0000common_cause'
        ### db_table = 'suigai_web_cause'
        db_table = 'cause'
    
    def __str__(self):
        return '<CAUSE: ' + self.cause_code + ', ' + self.cause_name + '>'

### 010: 地上地下区分
class UNDERGROUND(models.Model):
    underground_code = models.CharField(max_length=10, primary_key=True)       ### 地上地下区分コード
    underground_name = models.CharField(max_length=128)                        ### 地上地下区分名

    class Meta:
        ### db_table = 'p0000common_underground'
        ### db_table = 'suigai_web_underground'
        db_table = 'underground'

    def __str__(self):
        return '<UNDERGROUND: ' + self.underground_code + ', ' + self.underground_name + '>'

### 011: 地下空間の利用形態
class USAGE(models.Model):
    usage_code = models.CharField(max_length=10, primary_key=True)             ### 地下空間の利用形態コード
    usage_name = models.CharField(max_length=128)                              ### 地下空間の利用形態名

    class Meta:
        ### db_table = 'p0000common_usage'
        ### db_table = 'suigai_web_usage'
        db_table = 'usage'

    def __str__(self):
        return '<USAGE: ' + self.usage_code + ', ' + self.usage_name + '>'

### 012: 浸水土砂区分
class FLOOD_SEDIMENT(models.Model):
    flood_sediment_code = models.CharField(max_length=10, primary_key=True)    ### 浸水土砂区分コード
    flood_sediment_name = models.CharField(max_length=128)                     ### 浸水土砂区分名

    class Meta:
        ### db_table = 'p0000common_flood_sediment'
        ### db_table = 'suigai_web_flood_sediment'
        db_table = 'flood_sediment'

    def __str__(self):
        return '<FLOOD_SEDIMENT: ' + self.flood_sediment_code + ', ' + self.flood_sediment_name + '>'
    
### 013: 地盤勾配区分
class GRADIENT(models.Model):
    gradient_code = models.CharField(max_length=10, primary_key=True)          ### 地盤勾配区分コード
    gradient_name = models.CharField(max_length=128)                           ### 地盤勾配区分名

    class Meta:
        ### db_table = 'p0000common_gradient'
        ### db_table = 'suigai_web_gradient'
        db_table = 'gradient'

    def __str__(self):
        return '<GRADIENT: ' + self.gradient_code + ', ' + self.gradient_name + '>'

### 014: 産業分類
class INDUSTRY(models.Model):
    industry_code = models.CharField(max_length=10, primary_key=True)          ### 産業分類コード
    industry_name = models.CharField(max_length=128)                           ### 産業分類名

    class Meta:
        ### db_table = 'p0000common_industry'
        ### db_table = 'suigai_web_industry'
        db_table = 'industry'

    def __str__(self):
        return '<INDUSTRY: ' + self.industry_code + ', ' + self.industry_name + '>'

### 015: 復旧事業工種
class RESTORATION(models.Model):
    restoration_code = models.CharField(max_length=10, primary_key=True)
    restoration_name = models.CharField(max_length=128)

    class Meta:
        ### db_table = 'p0000common_restoration'
        ### db_table = 'suigai_web_restoration'
        db_table = 'restoration'

    def __str__(self):
        return '<RESTORATION: ' + self.restoration_code + ', ' + self.restoration_name + '>'

###############################################################################
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################
### 100: 県別家屋評価額
class HOUSE_ASSET(models.Model):
    house_asset_code = models.CharField(max_length=10, primary_key=True)       ### 県別家屋被害コード
    ken_code = models.CharField(max_length=10)                                 ### 県コード
    house_asset_year = models.IntegerField()                                   ### 県別家屋被害対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    house_asset = models.FloatField()                                          ### 県別家屋評価額

    class Meta:
        ### db_table = 'p0000common_house_asset'
        ### db_table = 'suigai_web_house_asset'
        db_table = 'house_asset'

    def __str__(self):
        return '<HOUSE_ASSET: ' + self.house_asset_code + '>'

### 101: 家屋被害率
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
        ### db_table = 'p0000common_house_damage'
        ### db_table = 'suigai_web_house_damage'
        db_table = 'house_damage'

    def __str__(self):
        return '<HOUSE_DAMAGE: ' + self.house_damage_code + '>'

### 102: 家庭用品自動車以外被害率
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
        ### db_table = 'p0000common_household_damage'
        ### db_table = 'suigai_web_household_damage'
        db_table = 'household_damage'

    def __str__(self):
        return '<HOUSEHOLD_DAMAGE: ' + self.household_damage_code + '>'

### 103: 家庭用品自動車被害率
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
        ### db_table = 'p0000common_car_damage'
        ### db_table = 'suigai_web_car_damage'
        db_table = 'car_damage'

    def __str__(self):
        return '<CAR_DAMAGE: ' + self.car_damage_code + '>'

### 104: 家庭応急対策費
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
        ### db_table = 'p0000common_house_cost'
        ### db_table = 'suigai_web_house_cost'
        db_table = 'house_cost'

    def __str__(self):
        return '<HOUSE_COST: ' + self.house_cost_code + '>'

### 105: 産業分類別資産額
class OFFICE_ASSET(models.Model):
    office_asset_code = models.CharField(max_length=10, primary_key=True)      ### 産業分類別資産額コード
    industry_code = models.CharField(max_length=10)                            ### 産業分類コード
    office_asset_year = models.IntegerField()                                  ### 産業分類別資産額対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日
    depreciable_asset = models.IntegerField()                                  ### 償却資産額
    inventory_asset = models.IntegerField()                                    ### 在庫資産額
    value_added = models.IntegerField()                                        ### 付加価値額

    class Meta:
        ### db_table = 'p0000common_office_asset'
        ### db_table = 'suigai_web_office_asset'
        db_table = 'office_asset'

    def __str__(self):
        return '<OFFICE_ASSET: ' + self.office_asset_code + '>'

### 106: 事業所被害率
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
        ### db_table = 'p0000common_office_damage'
        ### db_table = 'suigai_web_office_damage'
        db_table = 'office_damage'

    def __str__(self):
        return '<OFFICE_DAMAGE: ' + self.office_damage_code + '>'

### 107: 事業所営業停止損失
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

    class Meta:
        ### db_table = 'p0000common_office_cost'
        ### db_table = 'suigai_web_office_cost'
        db_table = 'office_cost'

    def __str__(self):
        return '<OFFICE_COST: ' + self.office_cost_code + '>'

### 108: 農漁家被害率
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
        ### db_table = 'p0000common_farmer_fisher_damage'
        ### db_table = 'suigai_web_farmer_fisher_damage'
        db_table = 'farmer_fisher_damage'

    def __str__(self):
        return '<FARMER_FISHER_DAMAGE: ' + self.farmer_fisher_damage_code + '>'

###############################################################################
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
### 調査員調査票のヘッダ部分（都道府県、市区町村、水害区域番号、水害区域面積、農作物被害額、異常気象コードなど）と
### 調査員調査票の一覧部分（町丁名、被害建物棟数など）の扱いについて、
### 重複しても被害額の算出に影響しない項目（都道府県、市区町村、水害区域番号、異常気象コードなど）は、SUIGAI、IPPAN両方に持たせても良い。
### 重複すると被害額の算出に影響する項目（水害区域面積、農作物被害額）は、SUIGAIのみに持たせる。
### DBの正規化（整合性）の観点からは、IPPANの外部キーにSUIGAI_IDを持たせて、SUIGAIに持たせた都道府県、市区町村、水害区域番号、異常気象コードを優先させることが望ましい。
### 水害（発生年月日）と水害区域番号との関係が１対１であるのか？異なる水害（発生年月日）で水害区域（番号）の使い回しがあるのか？疑問。
###############################################################################
### 200: 水害
class SUIGAI(models.Model):
    suigai_id = models.IntegerField(primary_key=True)                         ### 水害ID
    suigai_name = models.CharField(max_length=128, null=True)                 ### 水害名
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ### 例えば、新たなヘッダ部分の情報が登録できるとしても、実際に被害建物棟数が判明するまでは、その情報を管理することができない。
    ### また、ヘッダ部分の終了日が変更になると、複数のレコードを更新しなければならないため不整合を生じる恐れがある。
    ### https://torazuka.hatenablog.com/entry/20110713/pk
    ### https://oss-db.jp/dojo/dojo_info_04
    ken_code = models.CharField(max_length=10, null=True)                      ### 都道府県コード ### FOR GROUP BY
    city_code = models.CharField(max_length=10, null=True)                     ### 市区町村コード ### FOR GROUP BY
    begin_date = models.DateField(null=True)                                   ### 開始日 ### FOR GROUP BY
    end_date = models.DateField(null=True)                                     ### 終了日 ### FOR GROUP BY
    cause_1_code = models.CharField(max_length=10, null=True)                  ### 水害原因_1_コード ### FOR GROUP BY
    cause_2_code = models.CharField(max_length=10, null=True)                  ### 水害原因_2_コード ### FOR GROUP BY
    cause_3_code = models.CharField(max_length=10, null=True)                  ### 水害原因_3_コード ### FOR GROUP BY
    area_id = models.IntegerField(null=True)                                   ### 区域ID ### FOR GROUP BY

    ### 帳票のヘッダ部分 行10
    suikei_code = models.CharField(max_length=10, null=True)                   ### 水系コード ### FOR GROUP BY
    kasen_code = models.CharField(max_length=10, null=True)                    ### 河川コード ### FOR GROUP BY
    gradient_code = models.CharField(max_length=10, null=True)                 ### 地盤勾配区分コード FOR PARAM ### FOR GROUP BY

    ### 帳票のヘッダ部分 行14
    residential_area = models.FloatField()                                     ### 宅地面積（単位m2）
    agricultural_area = models.FloatField()                                    ### 農地面積（単位m2）
    underground_area = models.FloatField()                                     ### 地下面積（単位m2）
    kasen_kaigan_code = models.CharField(max_length=10, null=True)             ### 河川海岸（工種）コード ### FOR GROUP BY
    crop_damage = models.FloatField()                                          ### 農作物被害額（単位千円）
    weather_id = models.IntegerField(null=True)                                ### 異常気象ID ### FOR GROUP BY

    ### 第2正規形の考え方からヘッダ部分を別テーブル（水害テーブル）に分割する。
    ### 別テーブル（水害テーブル）に分割したことによりリレーションを表すSUIGAI_IDを追加する。
    ### 別テーブル（水害テーブル）の主キーは単純な連番とする。
    ### 都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名などに複合ユニークキーを設定する。
    ### 同じ都道府県、市区町村、水害発生日、水害原因、水害区域番号、水系沿岸名、河川海岸名で複数の水害区域面積、農作物被害額、異常気象などが登録できないようにするためである。
    ### 複数の水害区域面積、農作物被害額、異常気象を登録するためには、水害区域番号を別途追加するか、水害発生日を別途追加するようにさせるためである。

    class Meta:
        ### db_table = 'p0000common_suigai'
        ### db_table = 'suigai_web_suigai'
        db_table = 'suigai'

    def __str__(self):
        return '<SUIGAI: ' + self.suigai_id + ', ' + self.suigai_name + '>'

### 201: 異常気象（ほぼ、水害）
class WEATHER(models.Model):
    ### weather_id = models.CharField(max_length=10, primary_key=True)         ### 異常気象ID
    weather_id = models.IntegerField(primary_key=True)                         ### 異常気象ID
    weather_name = models.CharField(max_length=128)                            ### 異常気象名
    ### weather_year = models.IntegerField()                                   ### 異常気象対象年
    begin_date = models.DateField()                                            ### 開始日
    end_date = models.DateField()                                              ### 終了日

    class Meta:
        ### db_table = 'p0000common_weather'
        ### db_table = 'suigai_web_weather'
        db_table = 'weather'
    
    def __str__(self):
        return '<WEATHER: ' + self.weather_id + ', ' + self.weather_name + '>'

### 202: 区域
class AREA(models.Model):
    ### area_id = models.CharField(max_length=10, primary_key=True)            ### 区域ID
    area_id = models.IntegerField(primary_key=True)                            ### 区域ID
    area_name = models.CharField(max_length=128)                               ### 区域名
    ### area_year = models.IntegerField()                                      ### 区域対象年
    ### begin_date = models.DateField()                                        ### 開始日
    ### end_date = models.DateField()                                          ### 終了日
    ### agri_area = models.IntegerField()                                      ### 農地面積
    ### underground_area = models.IntegerField()                               ### 地下面積
    ### crop_damage = models.IntegerField()                                    ### 農作物被害額

    class Meta:
        ### db_table = 'p0000common_area'
        ### db_table = 'suigai_web_area'
        db_table = 'area'

    def __str__(self):
        return '<AREA: ' + self.area_id + ', ' + self.area_name + '>'

### 203: 一般資産調査票
class IPPAN(models.Model):
    ippan_id = models.IntegerField(primary_key=True)                           ### 一般資産調査票ID
    ippan_name = models.CharField(max_length=128, null=True)                   ### 一般資産調査票名（町丁名、大字名）
    
    ### 帳票のヘッダ部分 行7
    ### 第2正規形の考え方からはヘッダ部分は別テーブルに分割する。
    ### 例えば、新たなヘッダ部分の情報が登録できるとしても、実際に被害建物棟数が判明するまでは、その情報を管理することができない。
    ### また、ヘッダ部分の終了日が変更になると、複数のレコードを更新しなければならないため不整合を生じる恐れがある。
    ### https://torazuka.hatenablog.com/entry/20110713/pk
    ### https://oss-db.jp/dojo/dojo_info_04
    ### ken_code = models.CharField(max_length=10, null=True)                  ### 都道府県コード ### FOR GROUP BY
    ### city_code = models.CharField(max_length=10, null=True)                 ### 市区町村コード ### FOR GROUP BY
    ### begin_date = models.DateField(null=True)                               ### 開始日 ### FOR GROUP BY
    ### end_date = models.DateField(null=True)                                 ### 終了日 ### FOR GROUP BY
    ### cause_1_code = models.CharField(max_length=10, null=True)              ### 水害原因_1_コード ### FOR GROUP BY
    ### cause_2_code = models.CharField(max_length=10, null=True)              ### 水害原因_2_コード ### FOR GROUP BY
    ### cause_3_code = models.CharField(max_length=10, null=True)              ### 水害原因_3_コード ### FOR GROUP BY
    ### area_id = models.IntegerField(null=True)                               ### 区域ID ### FOR GROUP BY

    ### 帳票のヘッダ部分 行10
    ### suikei_code = models.CharField(max_length=10, null=True)               ### 水系コード ### FOR GROUP BY
    ### kasen_code = models.CharField(max_length=10, null=True)                ### 河川コード ### FOR GROUP BY
    ### gradient_code = models.CharField(max_length=10, null=True)             ### 地盤勾配区分コードFOR PARAM ### FOR GROUP BY

    ### 帳票のヘッダ部分 行14
    ### residential_area = models.FloatField()                                 ### 農地面積（単位m2）
    ### agricultural_area = models.FloatField()                                ### 農地面積（単位m2）
    ### underground_area = models.FloatField()                                 ### 地下面積（単位m2）
    ### kasen_kaigan_code = models.CharField(max_length=10, null=True)         ### 河川海岸（工種）コード ### FOR GROUP BY
    ### crop_damage = models.FloatField()                                      ### 農作物被害額（単位千円）
    ### weather_id = models.IntegerField(null=True)                            ### 異常気象ID ### FOR GROUP BY

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
        ### db_table = 'p0000common_ippan'
        ### db_table = 'suigai_web_ippan'
        db_table = 'ippan'

    def __str__(self):
        return '<IPPAN: ' + self.ippan_id + ', ' + self.ippan_name + '>'

### 204: 公共土木調査票
class KOKYO(models.Model):
    ### kokyo_id = models.CharField(max_length=10, primary_key=True)
    kokyo_id = models.IntegerField(primary_key=True)
    kokyo_name = models.CharField(max_length=128, null=True)
    ken_code = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    ### weather_id = models.CharField(max_length=10)
    weather_id = models.IntegerField()
    kokyo_year = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ### db_table = 'p0000common_kokyo'
        ### db_table = 'suigai_web_kokyo'
        db_table = 'kokyo'

    def __str__(self):
        return '<KOKYO: ' + self.kokyo_id + ', ' + self.kokyo_name + '>'
        
### 205: 公益事業調査票
class KOEKI(models.Model):
    ### koeki_id = models.CharField(max_length=10, primary_key=True)
    koeki_id = models.IntegerField(primary_key=True)
    koeki_name = models.CharField(max_length=128, null=True)
    ken_code = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    ### weather_id = models.CharField(max_length=10)
    weather_id = models.IntegerField()
    koeki_year = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ### db_table = 'p0000common_koeki'
        ### db_table = 'suigai_web_koeki'
        db_table = 'koeki'

    def __str__(self):
        return '<KOEKI: ' + self.koeki_id + ', ' + self.koeki_name + '>'

###############################################################################
### トランザクション系テーブル（更新テーブル）
### 主に集計用
###############################################################################
### 300: 一般資産レポート
class IPPAN_REPORT(models.Model):
    ippan_report_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        ### db_table = 'p0000common_ippan_report'
        ### db_table = 'suigai_web_ippan_report'
        db_table = 'ippan_report'
        
    def __str__(self):
        return '<IPPAN_REPORT: ' + self.ippan_report_id + '>'
        
### 301: 公共土木レポート
class KOKYO_REPORT(models.Model):
    kokyo_report_id = models.CharField(max_length=10, primary_key=True)        
    
    class Meta:
        ### db_table = 'p0000common_kokyo_report'
        ### db_table = 'suigai_web_kokyo_report'
        db_table = 'kokyo_report'
        
    def __str__(self):
        return '<KOKYO_REPORT: ' + self.kokyo_report_id + '>'
    
### 302: 公益事業レポート
class KOEKI_REPORT(models.Model):
    koeki_report_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        ### db_table = 'p0000common_koeki_report'
        ### db_table = 'suigai_web_koeki_report'
        db_table = 'koeki_report'
        
    def __str__(self):
        return '<KOEKI_REPORT: ' + self.koeki_report_id + '>'

### 303: 承認履歴
class APPROVE_HISTORY(models.Model):
    approve_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        ### db_table = 'p0000common_approve_history'
        ### db_table = 'suigai_web_approve_history'
        db_table = 'approve_history'
        
    def __str__(self):
        return '<APPROVE_HISTORY: ' + self.approve_history_id + '>'

### 304: 集計履歴
class REPORT_HISTORY(models.Model):
    report_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        ### db_table = 'p0000common_report_history'
        ### db_table = 'suigai_web_report_history'
        db_table = 'report_history'
        
    def __str__(self):
        return '<REPORT_HISTORY: ' + self.report_history_id + '>'

### 305: 配布履歴
class DISTRIBUTE_HISTORY(models.Model):
    distribute_history_id = models.CharField(max_length=10, primary_key=True)
    
    class Meta:
        ### db_table = 'p0000common_distribute_history'
        ### db_table = 'suigai_web_distribute_history'
        db_table = 'distribute_history'
        
    def __str__(self):
        return '<DISTRIBUTE_HISTORY: ' + self.distribute_history_id + '>'

### 306: 
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
        ### db_table = 'p0000common_transact'
        ### db_table = 'suigai_web_transact'
        db_table = 'transact'
        
    def __str__(self):
        return '<TRANSACT: ' + self.transact_id + '>'

### 307: 
class IPPAN_KOKYO_KOEKI(models.Model):
    ippan_kokyo_koeki_code = models.CharField(max_length=10)
    ippan_kokyo_koeki_name = models.CharField(max_length=128)
    
    class Meta:
        ### db_table = 'p0000common_ippan_kokyo_koeki'
        ### db_table = 'suigai_web_ippan_kokyo_koeki'
        db_table = 'ippan_kokyo_koeki'
        
    def __str__(self):
        return '<IPPAN_KOKYO_KOEKI: ' + self.ippan_kokyo_koeki_code + '>'
    