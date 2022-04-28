from django.db import models

### データベース設計で絶対役に立つ命名規則
### https://katalog.tokyo/?p=5403
### ID、CODEはテーブル名にあわせる。OK：SUIKEI_CODE、NG：CODE、OK:SUIGAI_ID、NG:ID
### 項目名が同じになるようにするとER図も自動作成できる。

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 00: 
### class P0200Prefecture(models.Model):
###     code = models.CharField(max_length=2, primary_key=True)
###     name = models.CharField(max_length=200)
###     def __str__(self):
###         return '<Prefecture: ' + self.code + ', ' + self.name + '>'

### 00:
### class P0200City(models.Model):
###     code = models.CharField(max_length=6, primary_key=True)
###     pref_code = models.ForeignKey(P0200Prefecture, on_delete=models.CASCADE)
###     name = models.CharField(max_length=200)
###     def __str__(self):
###         return '<City: ' + self.code + ', ' + self.name + '>'

### 01: 建物区分
class BUILDING(models.Model):
    BUILDING_CODE = models.CharField(max_length=10, primary_key=True)          ### 建物区分コード
    BUILDING_NAME = models.CharField(max_length=128)                           ### 建物区分名
    
    def __str__(self):
        return '<BUILDING: ' + self.BUILDING_CODE + ', ' + self.BUILDING_NAME + '>'

### 02: 都道府県
class KEN(models.Model):
    KEN_CODE = models.CharField(max_length=10, primary_key=True)               ### 都道府県コード
    KEN_NAME = models.CharField(max_length=128)                                ### 都道府県名
    
    def __str__(self):
        return '<KEN: ' + self.KEN_CODE + ', ' + self.KEN_NAME + '>'

### 03: 市区町村
class CITY(models.Model):
    CITY_CODE = models.CharField(max_length=10, primary_key=True)              ### 市区町村コード
    CITY_NAME = models.CharField(max_length=128)                               ### 市区町村名
    KEN_CODE = models.CharField(max_length=10)                                 ### 都道府県コード
    CITY_POPULATION = models.IntegerField()                                    ### 市区町村人口
    CITY_AREA = models.IntegerField()                                          ### 市区町村面積
    
    def __str__(self):
        return '<CITY: ' + self.CITY_CODE + ', ' + self.CITY_NAME + '>'

### 04: 水害発生地点工種（河川海岸区分）
class KASEN_KAIGAN(models.Model):
    KASEN_KAIGAN_CODE = models.CharField(max_length=10, primary_key=True)      ### 河川海岸区分コード
    KASEN_KAIGAN_NAME = models.CharField(max_length=128)                       ### 河川海岸区分名
 
    def __str__(self):
        return '<KASEN_KAIGAN: ' + self.KASEN_KAIGAN_CODE + ', ' + self.KASEN_KAIGAN_NAME + '>'

### 05: 水系（水系・沿岸）
class SUIKEI(models.Model):
    SUIKEI_CODE = models.CharField(max_length=10, primary_key=True)            ### 水系コード
    SUIKEI_NAME = models.CharField(max_length=128)                             ### 水系名
    SUIKEI_TYPE_CODE = models.CharField(max_length=10)                         ### 水系種別コード

    def __str__(self):
        return '<SUIKEI: ' + self.SUIKEI_CODE + ', ' + self.SUIKEI_NAME + '>'

### 06: 水系種別（水系・沿岸種別）
class SUIKEI_TYPE(models.Model):
    SUIKEI_TYPE_CODE = models.CharField(max_length=10, primary_key=True)       ### 水系種別コード
    SUIKEI_TYPE_NAME = models.CharField(max_length=128)                        ### 水系種別名

    def __str__(self):
        return '<SUIKEI_TYPE: ' + self.SUIKEI_TYPE_CODE + ', ' + self.SUIKEI_TYPE_NAME + '>'

### 07: 河川（河川・海岸）
class KASEN(models.Model):
    KASEN_CODE = models.CharField(max_length=10, primary_key=True)             ### 河川コード
    KASEN_NAME = models.CharField(max_length=128)                              ### 河川名
    KASEN_TYPE_CODE = models.CharField(max_length=10)                          ### 河川種別コード
    SUIKEI_CODE = models.CharField(max_length=10)                              ### 水系コード

    def __str__(self):
        return '<KASEN: ' + self.KASEN_CODE + ', ' + self.KASEN_NAME + '>'

### 08: 河川種別（河川・海岸種別）
class KASEN_TYPE(models.Model):
    KASEN_TYPE_CODE = models.CharField(max_length=10, primary_key=True)        ### 河川種別コード
    KASEN_TYPE_NAME = models.CharField(max_length=128)                         ### 河川種別名

    def __str__(self):
        return '<KASEN_TYPE: ' + self.KASEN_TYPE_CODE + ', ' + self.KASEN_TYPE_NAME + '>'

### 09: 水害原因
class CAUSE(models.Model):    
    CAUSE_CODE = models.CharField(max_length=10, primary_key=True)             ### 水害原因コード
    CAUSE_NAME = models.CharField(max_length=128)                              ### 水害原因名
    
    def __str__(self):
        return '<CAUSE: ' + self.CAUSE_CODE + ', ' + self.CAUSE_NAME + '>'

### 10: 地上地下区分
class UNDERGROUND(models.Model):
    UNDERGROUND_CODE = models.CharField(max_length=10, primary_key=True)       ### 地上地下区分コード
    UNDERGROUND_NAME = models.CharField(max_length=128)                        ### 地上地下区分名

    def __str__(self):
        return '<UNDERGROUND: ' + self.UNDERGROUND_CODE + ', ' + self.UNDERGROUND_NAME + '>'

### 11: 地下空間の利用形態
class USAGE(models.Model):
    USAGE_CODE = models.CharField(max_length=10, primary_key=True)             ### 地下空間の利用形態コード
    USAGE_NAME = models.CharField(max_length=128)                              ### 地下空間の利用形態名

    def __str__(self):
        return '<USAGE: ' + self.USAGE_CODE + ', ' + self.USAGE_NAME + '>'

### 12: 浸水土砂区分
class FLOOD_SEDIMENT(models.Model):
    FLOOD_SEDIMENT_CODE = models.CharField(max_length=10, primary_key=True)    ### 浸水土砂区分コード
    FLOOD_SEDIMENT_NAME = models.CharField(max_length=128)                     ### 浸水土砂区分名

    def __str__(self):
        return '<FLOOD_SEDIMENT: ' + self.FLOOD_SEDIMENT_CODE + ', ' + self.FLOOD_SEDIMENT_NAME + '>'
    
### 13: 地盤勾配区分
class GRADIENT(models.Model):
    GRADIENT_CODE = models.CharField(max_length=10, primary_key=True)          ### 地盤勾配区分コード
    GRADIENT_NAME = models.CharField(max_length=128)                           ### 地盤勾配区分名

    def __str__(self):
        return '<GRADIENT: ' + self.GRADIENT_CODE + ', ' + self.GRADIENT_NAME + '>'

### 14: 産業分類
class INDUSTRY(models.Model):
    INDUSTRY_CODE = models.CharField(max_length=10, primary_key=True)          ### 産業分類コード
    INDUSTRY_NAME = models.CharField(max_length=128)                           ### 産業分類名

    def __str__(self):
        return '<INDUSTRY: ' + self.INDUSTRY_CODE + ', ' + self.INDUSTRY_NAME + '>'

###############################################################################
### 一般資産
### マスタ系テーブル（参照テーブル）
### 主に集計用
###############################################################################
### 15: 県別家屋評価額
class HOUSE_ASSET(models.Model):
    HOUSE_ASSET_CODE = models.CharField(max_length=10, primary_key=True)       ### 県別家屋被害コード
    KEN_CODE = models.CharField(max_length=10)                                 ### 県コード
    HOUSE_ASSET_YEAR = models.IntegerField()                                   ### 県別家屋被害対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    HOUSE_ASSET = models.FloatField()                                          ### 県別家屋評価額

    def __str__(self):
        return '<HOUSE_ASSET: ' + self.HOUSE_ASSET_CODE + ', ' + self.HOUSE_ASSET_YEAR + '>'

### 16: 家屋被害率
class HOUSE_DAMAGE(models.Model):
    HOUSE_DAMAGE_CODE = models.CharField(max_length=10, primary_key=True)      ### 家屋被害率コード
    HOUSE_DAMAGE_YEAR = models.IntegerField()                                  ### 家屋被害率対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    
    FL_GR1_LV00 = models.FloatField()                                          ### 被害率_浸水_勾配1_床下
    FL_GR1_LV00_50 = models.FloatField()                                       ### 被害率_浸水_勾配1_0から50cm未満
    FL_GR1_LV50_100 = models.FloatField()                                      ### 被害率_浸水_勾配1_50から100cm未満
    FL_GR1_LV100_200 = models.FloatField()                                     ### 被害率_浸水_勾配1_100から200cm未満
    FL_GR1_LV200_300 = models.FloatField()                                     ### 被害率_浸水_勾配1_200から300cm未満
    FL_GR1_LV300 = models.FloatField()                                         ### 被害率_浸水_勾配1_300cm以上
    
    FL_GR2_LV00 = models.FloatField()                                          ### 被害率_浸水_勾配2_床下
    FL_GR2_LV00_50 = models.FloatField()                                       ### 被害率_浸水_勾配2_0から50cm未満
    FL_GR2_LV50_100 = models.FloatField()                                      ### 被害率_浸水_勾配2_50から100cm未満
    FL_GR2_LV100_200 = models.FloatField()                                     ### 被害率_浸水_勾配2_100から200cm未満
    FL_GR2_LV200_300 = models.FloatField()                                     ### 被害率_浸水_勾配2_200から300cm未満
    FL_GR2_LV300 = models.FloatField()                                         ### 被害率_浸水_勾配2_300cm以上
    
    FL_GR3_LV00 = models.FloatField()                                          ### 被害率_浸水_勾配3_床下
    FL_GR3_LV00_50 = models.FloatField()                                       ### 被害率_浸水_勾配3_0から50cm未満
    FL_GR3_LV50_100 = models.FloatField()                                      ### 被害率_浸水_勾配3_50から100cm未満
    FL_GR3_LV100_200 = models.FloatField()                                     ### 被害率_浸水_勾配3_100から200cm未満
    FL_GR3_LV200_300 = models.FloatField()                                     ### 被害率_浸水_勾配3_200から300cm未満
    FL_GR3_LV300 = models.FloatField()                                         ### 被害率_浸水_勾配3_300cm以上
    
    SD_GR1_LV00 = models.FloatField()                                          ### 被害率_土砂_勾配1_床下
    SD_GR1_LV00_50 = models.FloatField()                                       ### 被害率_土砂_勾配1_0から50cm未満
    SD_GR1_LV50_100 = models.FloatField()                                      ### 被害率_土砂_勾配1_50から100cm未満
    SD_GR1_LV100_200 = models.FloatField()                                     ### 被害率_土砂_勾配1_100から200cm未満
    SD_GR1_LV200_300 = models.FloatField()                                     ### 被害率_土砂_勾配1_200から300cm未満
    SD_GR1_LV300 = models.FloatField()                                         ### 被害率_土砂_勾配1_300cm以上
    
    SD_GR2_LV00 = models.FloatField()                                          ### 被害率_土砂_勾配2_床下
    SD_GR2_LV00_50 = models.FloatField()                                       ### 被害率_土砂_勾配2_0から50cm未満
    SD_GR2_LV50_100 = models.FloatField()                                      ### 被害率_土砂_勾配2_50から100cm未満
    SD_GR2_LV100_200 = models.FloatField()                                     ### 被害率_土砂_勾配2_100から200cm未満
    SD_GR2_LV200_300 = models.FloatField()                                     ### 被害率_土砂_勾配2_200から300cm未満
    SD_GR2_LV300 = models.FloatField()                                         ### 被害率_土砂_勾配2_300cm以上
    
    SD_GR3_LV00 = models.FloatField()                                          ### 被害率_土砂_勾配3_床下
    SD_GR3_LV00_50 = models.FloatField()                                       ### 被害率_土砂_勾配3_0から50cm未満
    SD_GR3_LV50_100 = models.FloatField()                                      ### 被害率_土砂_勾配3_50から100cm未満
    SD_GR3_LV100_200 = models.FloatField()                                     ### 被害率_土砂_勾配3_100から200cm未満
    SD_GR3_LV200_300 = models.FloatField()                                     ### 被害率_土砂_勾配3_200から300cm未満
    SD_GR3_LV300 = models.FloatField()                                         ### 被害率_土砂_勾配3_300cm以上

    def __str__(self):
        return '<HOUSE_DAMAGE: ' + self.HOUSE_DAMAGE_CODE + ', ' + self.HOUSE_DAMAGE_YEAR + '>'

### 17: 家庭用品自動車以外被害率
class HOUSEHOLD_DAMAGE(models.Model):
    HOUSEHOLD_DAMAGE_CODE = models.CharField(max_length=10, primary_key=True)  ### 家庭用品自動車以外被害率コード
    HOUSEHOLD_DAMAGE_YEAR = models.IntegerField()                              ### 家庭用品自動車以外被害率対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    FL_LV00 = models.FloatField()                                              ### 被害率_浸水_床下
    FL_LV00_50 = models.FloatField()                                           ### 被害率_浸水_0から50cm未満
    FL_LV50_100 = models.FloatField()                                          ### 被害率_浸水_50から100cm未満
    FL_LV100_200 = models.FloatField()                                         ### 被害率_浸水_100から200cm未満
    FL_LV200_300 = models.FloatField()                                         ### 被害率_浸水_200から300cm未満
    FL_LV300 = models.FloatField()                                             ### 被害率_浸水_300cm以上
    SD_LV00 = models.FloatField()                                              ### 被害率_土砂_床下
    SD_LV00_50 = models.FloatField()                                           ### 被害率_土砂_0から50cm未満
    SD_LV50_100 = models.FloatField()                                          ### 被害率_土砂_50から100cm未満
    SD_LV100_200 = models.FloatField()                                         ### 被害率_土砂_100から200cm未満
    SD_LV200_300 = models.FloatField()                                         ### 被害率_土砂_200から300cm未満
    SD_LV300 = models.FloatField()                                             ### 被害率_土砂_300cm以上
    HOUSEHOLD_ASSET = models.FloatField()                                      ### 家庭用品自動車以外所有額

    def __str__(self):
        return '<HOUSEHOLD_DAMAGE: ' + self.HOUSEHOLD_DAMAGE_CODE + ', ' + self.HOUSEHOLD_DAMAGE_YEAR + '>'

### 18: 家庭用品自動車被害率
class CAR_DAMAGE(models.Model):
    CAR_DAMAGE_CODE = models.CharField(max_length=10, primary_key=True)        ### 自動車被害率コード
    CAR_DAMAGE_YEAR = models.IntegerField()                                    ### 自動車被害率対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    FL_LV00 = models.FloatField()                                              ### 被害率_浸水_床下
    FL_LV00_50 = models.FloatField()                                           ### 被害率_浸水_0から50cm未満
    FL_LV50_100 = models.FloatField()                                          ### 被害率_浸水_50から100cm未満
    FL_LV100_200 = models.FloatField()                                         ### 被害率_浸水_100から200cm未満
    FL_LV200_300 = models.FloatField()                                         ### 被害率_浸水_200から300cm未満
    FL_LV300 = models.FloatField()                                             ### 被害率_浸水_300cm以上
    CAR_ASSET = models.FloatField()                                            ### 家庭用品自動車所有額

    def __str__(self):
        return '<CAR_DAMAGE: ' + self.CAR_DAMAGE_CODE + ', ' + self.CAR_DAMAGE_YEAR + '>'

### 19: 家庭応急対策費
class HOUSE_COST(models.Model):
    HOUSE_COST_CODE = models.CharField(max_length=10, primary_key=True)        ### 家庭応急対策費コード
    HOUSE_COST_YEAR = models.IntegerField()                                    ### 家庭応急対策費対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    ALT_LV00 = models.FloatField()                                             ### 代替活動費_床下
    ALT_LV00_50 = models.FloatField()                                          ### 代替活動費_0から50cm未満
    ALT_LV50_100 = models.FloatField()                                         ### 代替活動費_50から100cm未満
    ALT_LV100_200 = models.FloatField()                                        ### 代替活動費_100から200cm未満
    ALT_LV200_300 = models.FloatField()                                        ### 代替活動費_200から300cm未満
    ALT_LV300 = models.FloatField()                                            ### 代替活動費_300cm以上
    CLEAN_LV00 = models.FloatField()                                           ### 清掃費_床下
    CLEAN_LV00_50 = models.FloatField()                                        ### 清掃費_0から50cm未満
    CLEAN_LV50_100 = models.FloatField()                                       ### 清掃費_50から100cm未満
    CLEAN_LV100_200 = models.FloatField()                                      ### 清掃費_100から200cm未満
    CLEAN_LV200_300 = models.FloatField()                                      ### 清掃費_200から300cm未満
    CLEAN_LV300 = models.FloatField()                                          ### 清掃費_300cm以上
    HOUSE_COST = models.FloatField()                                           ### 清掃労働単価

    def __str__(self):
        return '<HOUSE_COST: ' + self.HOUSE_COST_CODE + ', ' + self.HOUSE_COST_YEAR + '>'

### 20: 産業分類別資産額
class OFFICE_ASSET(models.Model):
    OFFICE_ASSET_CODE = models.CharField(max_length=10, primary_key=True)      ### 産業分類別資産額コード
    INDUSTRY_CODE = models.CharField(max_length=10)                            ### 産業分類コード
    OFFICE_ASSET_YEAR = models.IntegerField()                                  ### 産業分類別資産額対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    DEPRECIABLE_ASSET = models.IntegerField()                                  ### 償却資産額
    INVENTORY_ASSET = models.IntegerField()                                    ### 在庫資産額
    VALUE_ADDED = models.IntegerField()                                        ### 付加価値額

    def __str__(self):
        return '<OFFICE_ASSET: ' + self.OFFICE_ASSET_CODE + ', ' + self.OFFICE_ASSET_YEAR + '>'

### 21: 事業所被害率
class OFFICE_DAMAGE(models.Model):
    OFFICE_DAMAGE_CODE = models.CharField(max_length=10, primary_key=True)     ### 事業所被害率コード
    OFFICE_DAMAGE_YEAR = models.IntegerField()                                 ### 事業所被害率対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    DEP_FL_LV00 = models.FloatField()                                          ### 償却資産率_浸水_床下
    DEP_FL_LV00_50 = models.FloatField()                                       ### 償却資産率_浸水_0から50cm未満
    DEP_FL_LV50_100 = models.FloatField()                                      ### 償却資産率_浸水_50から100cm未満
    DEP_FL_LV100_200 = models.FloatField()                                     ### 償却資産率_浸水_100から200cm未満
    DEP_FL_LV200_300 = models.FloatField()                                     ### 償却資産率_浸水_200から300cm未満
    DEP_FL_LV300 = models.FloatField()                                         ### 償却資産率_浸水_300cm以上
    DEP_SD_LV00 = models.FloatField()                                          ### 償却資産率_土砂_床下
    DEP_SD_LV00_50 = models.FloatField()                                       ### 償却資産率_土砂_0から50cm未満
    DEP_SD_LV50_100 = models.FloatField()                                      ### 償却資産率_土砂_50から100cm未満
    DEP_SD_LV100_200 = models.FloatField()                                     ### 償却資産率_土砂_100から200cm未満
    DEP_SD_LV200_300 = models.FloatField()                                     ### 償却資産率_土砂_200から300cm未満
    DEP_SD_LV300 = models.FloatField()                                         ### 償却資産率_土砂_300cm以上
    INV_FL_LV00 = models.FloatField()                                          ### 在庫資産率_浸水_床下
    INV_FL_LV00_50 = models.FloatField()                                       ### 在庫資産率_浸水_0から50cm未満
    INV_FL_LV50_100 = models.FloatField()                                      ### 在庫資産率_浸水_50から100cm未満
    INV_FL_LV100_200 = models.FloatField()                                     ### 在庫資産率_浸水_100から200cm未満
    INV_FL_LV200_300 = models.FloatField()                                     ### 在庫資産率_浸水_200から300cm未満
    INV_FL_LV300 = models.FloatField()                                         ### 在庫資産率_浸水_300cm以上
    INV_SD_LV00 = models.FloatField()                                          ### 在庫資産率_土砂_床下
    INV_SD_LV00_50 = models.FloatField()                                       ### 在庫資産率_土砂_0から50cm未満
    INV_SD_LV50_100 = models.FloatField()                                      ### 在庫資産率_土砂_50から100cm未満
    INV_SD_LV100_200 = models.FloatField()                                     ### 在庫資産率_土砂_100から200cm未満
    INV_SD_LV200_300 = models.FloatField()                                     ### 在庫資産率_土砂_200から300cm未満
    INV_SD_LV300 = models.FloatField()                                         ### 在庫資産率_土砂_300cm以上

    def __str__(self):
        return '<OFFICE_DAMAGE: ' + self.OFFICE_DAMAGE_CODE + ', ' + self.OFFICE_DAMAGE_YEAR + '>'

### 22: 事業所営業停止損失
class OFFICE_COST(models.Model):
    OFFICE_COST_CODE = models.CharField(max_length=10, primary_key=True)       ### 事業所営業損失コード
    OFFICE_COST_YEAR = models.IntegerField()                                   ### 事業所営業損失対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    SUSPEND_LV00 = models.FloatField()                                         ### 営業停止日数_床下
    SUSPEND_LV00_50 = models.FloatField()                                      ### 営業停止日数_0から50cm未満
    SUSPEND_LV50_100 = models.FloatField()                                     ### 営業停止日数_50から100cm未満
    SUSPEND_LV100_200 = models.FloatField()                                    ### 営業停止日数_100から200cm未満
    SUSPEND_LV200_300 = models.FloatField()                                    ### 営業停止日数_200から300cm未満
    SUSPEND_LV300 = models.FloatField()                                        ### 営業停止日数_300cm以上
    STAGNATE_LV00 = models.FloatField()                                        ### 営業停滞日数_床下
    STAGNATE_LV00_50 = models.FloatField()                                     ### 営業停滞日数_0から50cm未満
    STAGNATE_LV50_100 = models.FloatField()                                    ### 営業停滞日数_50から100cm未満
    STAGNATE_LV100_200 = models.FloatField()                                   ### 営業停滞日数_100から200cm未満
    STAGNATE_LV200_300 = models.FloatField()                                   ### 営業停滞日数_200から300cm未満
    STAGNATE_LV300 = models.FloatField()                                       ### 営業停滞日数_300cm以上

    def __str__(self):
        return '<OFFICE_COST: ' + self.OFFICE_COST_CODE + ', ' + self.OFFICE_COST_YEAR + '>'

### 23: 農漁家被害率 2022/04/18 追加
class FARMER_FISHER_DAMAGE(models.Model):
    FARMER_FISHER_DAMAGE_CODE = models.CharField(max_length=10, primary_key=True)   ### 農漁家被害率コード
    FARMER_FISHER_DAMAGE_YEAR = models.IntegerField()                          ### 農漁家被害率対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    DEP_FL_LV00 = models.FloatField()                                          ### 償却資産被害率_浸水_床下
    DEP_FL_LV00_50 = models.FloatField()                                       ### 償却資産被害率_浸水_0から50cm未満
    DEP_FL_LV50_100 = models.FloatField()                                      ### 償却資産被害率_浸水_50から100cm未満
    DEP_FL_LV100_200 = models.FloatField()                                     ### 償却資産被害率_浸水_100から200cm未満
    DEP_FL_LV200_300 = models.FloatField()                                     ### 償却資産被害率_浸水_200から300cm未満
    DEP_FL_LV300 = models.FloatField()                                         ### 償却資産被害率_浸水_300cm以上
    DEP_SD_LV00 = models.FloatField()                                          ### 償却資産被害率_土砂_床下
    DEP_SD_LV00_50 = models.FloatField()                                       ### 償却資産被害率_土砂_0から50cm未満
    DEP_SD_LV50_100 = models.FloatField()                                      ### 償却資産被害率_土砂_50から100cm未満
    DEP_SD_LV100_200 = models.FloatField()                                     ### 償却資産被害率_土砂_100から200cm未満
    DEP_SD_LV200_300 = models.FloatField()                                     ### 償却資産被害率_土砂_200から300cm未満
    DEP_SD_LV300 = models.FloatField()                                         ### 償却資産被害率_土砂_300cm以上
    INV_FL_LV00 = models.FloatField()                                          ### 在庫資産被害率_浸水_床下
    INV_FL_LV00_50 = models.FloatField()                                       ### 在庫資産被害率_浸水_0から50cm未満
    INV_FL_LV50_100 = models.FloatField()                                      ### 在庫資産被害率_浸水_50から100cm未満
    INV_FL_LV100_200 = models.FloatField()                                     ### 在庫資産被害率_浸水_100から200cm未満
    INV_FL_LV200_300 = models.FloatField()                                     ### 在庫資産被害率_浸水_200から300cm未満
    INV_FL_LV300 = models.FloatField()                                         ### 在庫資産被害率_浸水_300cm以上
    INV_SD_LV00 = models.FloatField()                                          ### 在庫資産被害率_土砂_床下
    INV_SD_LV00_50 = models.FloatField()                                       ### 在庫資産被害率_土砂_0から50cm未満
    INV_SD_LV50_100 = models.FloatField()                                      ### 在庫資産被害率_土砂_50から100cm未満
    INV_SD_LV100_200 = models.FloatField()                                     ### 在庫資産被害率_土砂_100から200cm未満
    INV_SD_LV200_300 = models.FloatField()                                     ### 在庫資産被害率_土砂_200から300cm未満
    INV_SD_LV300 = models.FloatField()                                         ### 在庫資産被害率_土砂_300cm以上
    DEPRECIABLE_ASSET = models.IntegerField()                                  ### 農漁家償却資産額
    INVENTORY_ASSET = models.IntegerField()                                    ### 農漁家在庫資産額

    def __str__(self):
        return '<FARMER_FISHER_DAMAGE: ' + self.FARMER_FISHER_CODE + ', ' + self.FARMER_FISHER_YEAR + '>'

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 24: 異常気象（ほぼ、水害）
class WEATHER(models.Model):
    WEATHER_ID = models.CharField(max_length=10, primary_key=True)             ### 異常気象ID
    WEATHER_NAME = models.CharField(max_length=128)                            ### 異常気象名
    WEATHER_YEAR = models.IntegerField()                                       ### 異常気象対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    
    def __str__(self):
        return '<WEATHER: ' + self.WEATHER_ID + ', ' + self.WEATHER_NAME + '>'

### 00: 水害区域
### class SUIGAI_AREA(models.Model):
###     SUIGAI_AREA_ID = models.CharField(max_length=10, primary_key=True)
###     WEATHER_ID = models.CharField(max_length=10)
###     SUIGAI_AREA_YEAR = models.IntegerField()
###     BEGIN_DATE = models.DateField()
###     END_DATE = models.DateField()
###     AGRI_AREA = models.IntegerField()
###     UNDERGROUND_AREA = models.IntegerField()
###     CROP_DAMAGE = models.IntegerField()
###     def __str__(self):
###         return '<SUIGAI_AREA: ' + self.SUIGAI_AREA_ID + ', ' + self.SUIGAI_AREA_YEAR + '>'

### 25: 区域
class AREA(models.Model):
    AREA_ID = models.CharField(max_length=10, primary_key=True)                ### 区域ID
    AREA_NAME = models.CharField(max_length=128)                               ### 区域名
    AREA_YEAR = models.IntegerField()                                          ### 区域対象年
    BEGIN_DATE = models.DateField()                                            ### 開始日
    END_DATE = models.DateField()                                              ### 終了日
    AGRI_AREA = models.IntegerField()                                          ### 農地面積
    UNDERGROUND_AREA = models.IntegerField()                                   ### 地下面積
    CROP_DAMAGE = models.IntegerField()                                        ### 農作物被害額

    def __str__(self):
        return '<AREA: ' + self.AREA_ID + ', ' + self.AREA_YEAR + '>'

### 26: 一般資産調査票
class IPPAN(models.Model):
    IPPAN_ID = models.CharField(max_length=10, primary_key=True)               ### 一般資産調査票ID
    IPPAN_NAME = models.CharField(max_length=128, null=True)                   ### 一般資産調査票名

    BUILDING_CODE = models.CharField(max_length=10, null=True)                 ### 建物区分コード

    ### FOR PARAM
    FLOOD_SEDIMENT_CODE = models.CharField(max_length=10, null=True)           ### 浸水土砂区分コード
    GRADIENT_CODE = models.CharField(max_length=10, null=True)                 ### 地盤勾配区分コード
    INDUSTRY_CODE = models.CharField(max_length=10, null=True)                 ### 産業分類コード

    ### FOR GROUP BY
    KEN_CODE = models.CharField(max_length=10, null=True)                      ### 都道府県コード
    CITY_CODE = models.CharField(max_length=10, null=True)                     ### 市区町村コード
    WEATHER_ID = models.CharField(max_length=10, null=True)                    ### 異常気象ID
    AREA_ID = models.CharField(max_length=10, null=True)                       ### 区域ID
    CAUSE_1_CODE = models.CharField(max_length=10, null=True)                  ### 水害原因_1_コード
    CAUSE_2_CODE = models.CharField(max_length=10, null=True)                  ### 水害原因_2_コード
    CAUSE_3_CODE = models.CharField(max_length=10, null=True)                  ### 水害原因_3_コード

    SUIKEI_CODE = models.CharField(max_length=10, null=True)                   ### 水系コード
    KASEN_CODE = models.CharField(max_length=10, null=True)                    ### 河川コード
    KASEN_KAIGAN_CODE = models.CharField(max_length=10, null=True)             ### 河川海岸コード

    ### BUILDING STRUCTURE, For Swith Mandatory and Optional Item
    UNDERGROUND_CODE = models.CharField(max_length=10, null=True)              ### 地上地下区分コード
    USAGE_CODE = models.CharField(max_length=10, null=True)                    ### 地下空間の利用形態コード
    
    ### Input Data
    BUILDING_LV00 = models.IntegerField(null=True)                             ### 被害建物棟数_床下
    BUILDING_LV01_49 = models.IntegerField(null=True)                          ### 被害建物棟数_01から49cm
    BUILDING_LV50_99 = models.IntegerField(null=True)                          ### 被害建物棟数_50から99cm
    BUILDING_LV100 = models.IntegerField(null=True)                            ### 被害建物棟数_100cm以上
    BUILDING_HALF = models.IntegerField(null=True)                             ### 被害建物棟数_半壊
    BUILDING_FULL = models.IntegerField(null=True)                             ### 被害建物棟数_全壊

    ### Input Data
    FLOOR_AREA = models.IntegerField(null=True)                                ### 延床面積
    FAMILY = models.IntegerField(null=True)                                    ### 被災世帯数
    OFFICE = models.IntegerField(null=True)                                    ### 被災事業所数
    
    ### Derived From BUILDING_LV and FLOOR_AREA
    FLOOR_AREA_LV00 = models.FloatField(null=True)                             ### 延床面積_床下
    FLOOR_AREA_LV01_49 = models.FloatField(null=True)                          ### 延床面積_01から49cm
    FLOOR_AREA_LV50_99 = models.FloatField(null=True)                          ### 延床面積_50から99cm
    FLOOR_AREA_LV100 = models.FloatField(null=True)                            ### 延床面積_100cm以上
    FLOOR_AREA_HALF = models.FloatField(null=True)                             ### 延床面積_半壊
    FLOOR_AREA_FULL = models.FloatField(null=True)                             ### 延床面積_全壊
    
    ### Derived from BUILDING_LV and FAMILY
    FAMILY_LV00 = models.IntegerField(null=True)                               ### 被災世帯数_床下
    FAMILY_LV01_49 = models.IntegerField(null=True)                            ### 被災世帯数_01から49cm
    FAMILY_LV50_99 = models.IntegerField(null=True)                            ### 被災世帯数_50から99cm
    FAMILY_LV100 = models.IntegerField(null=True)                              ### 被災世帯数_100cm以上
    FAMILY_HALF = models.IntegerField(null=True)                               ### 被災世帯数_半壊
    FAMILY_FULL = models.IntegerField(null=True)                               ### 被災世帯数_全壊

    ### Derived from BUILDING_LV and OFFICE    
    OFFICE_LV00 = models.IntegerField(null=True)                               ### 被災事業所数_床下
    OFFICE_LV01_49 = models.IntegerField(null=True)                            ### 被災事業所数_01から49cm
    OFFICE_LV50_99 = models.IntegerField(null=True)                            ### 被災事業所数_50から99cm
    OFFICE_LV100 = models.IntegerField(null=True)                              ### 被災事業所数_100cm以上
    OFFICE_HALF = models.IntegerField(null=True)                               ### 被災事業所数_半壊
    OFFICE_FULL = models.IntegerField(null=True)                               ### 被災事業所数_全壊
    
    ### Input Data
    EMPLOYEE_LV00 = models.IntegerField(null=True)                             ### 被災従業者数_床下
    EMPLOYEE_LV01_49 = models.IntegerField(null=True)                          ### 被災従業者数_01から49cm
    EMPLOYEE_LV50_99 = models.IntegerField(null=True)                          ### 被災従業者数_50から99cm
    EMPLOYEE_LV100 = models.IntegerField(null=True)                            ### 被災従業者数_100cm以上
    ### EMPLOYEE_HALF = models.IntegerField(null=True)
    EMPLOYEE_FULL = models.IntegerField(null=True)                             ### 被災従業者数_全壊
    
    ### Input Data
    FARMER_FISHER_LV00 = models.IntegerField(null=True)                        ### 農漁家戸数_床下
    FARMER_FISHER_LV01_49 = models.IntegerField(null=True)                     ### 農漁家戸数_01から49cm
    FARMER_FISHER_LV50_99 = models.IntegerField(null=True)                     ### 農漁家戸数_50から99cm
    FARMER_FISHER_LV100 = models.IntegerField(null=True)                       ### 農漁家戸数_100cm以上
    ### FARMER_FISHER_HALF = models.IntegerField(null=True)
    FARMER_FISHER_FULL = models.IntegerField(null=True)                        ### 農漁家戸数_全壊

    def __str__(self):
        return '<IPPAN: ' + self.IPPAN_ID + ', ' + self.IPPAN_NAME + '>'

###############################################################################
### 一般資産
### トランザクション系テーブル（更新テーブル）
### 主に集計用
###############################################################################

###############################################################################
### 公共土木、公益事業
### マスタ系テーブル（参照テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 27: 復旧事業工種
class RESTORATION(models.Model):
    RESTORATION_CODE = models.CharField(max_length=10, primary_key=True)
    RESTORATION_NAME = models.CharField(max_length=128)

    def __str__(self):
        return '<RESTORATION: ' + self.RESTORATION_CODE + ', ' + self.RESTORATION_NAME + '>'

###############################################################################
### 公共土木、公益事業
### トランザクション系テーブル（更新テーブル）
### 主に入力用（アップロードダウンロード）
###############################################################################
### 28: 公共土木調査票
class KOKYO(models.Model):
    KOKYO_ID = models.CharField(max_length=10, primary_key=True)
    KEN_CODE = models.CharField(max_length=10)
    CITY_CODE = models.CharField(max_length=10)
    WEATHER_ID = models.CharField(max_length=10)
    KOKYO_YEAR = models.IntegerField()
    BEGIN_DATE = models.DateField()
    END_DATE = models.DateField()

    def __str__(self):
        return '<KOKYO: ' + self.KOKYO_ID + '>'
        
### 29: 公益事業調査票
class KOEKI(models.Model):
    KOEKI_ID = models.CharField(max_length=10, primary_key=True)
    KEN_CODE = models.CharField(max_length=10)
    CITY_CODE = models.CharField(max_length=10)
    WEATHER_ID = models.CharField(max_length=10)
    KOEKI_YEAR = models.IntegerField()
    BEGIN_DATE = models.DateField()
    END_DATE = models.DateField()

    def __str__(self):
        return '<KOEKI: ' + self.KOEKI_ID + '>'

    