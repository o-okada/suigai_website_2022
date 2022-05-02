# Generated by Django 4.0.3 on 2022-04-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='area',
            fields=[
                ('area_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('area_name', models.CharField(max_length=128)),
                ('area_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('agri_area', models.IntegerField()),
                ('underground_area', models.IntegerField()),
                ('crop_damage', models.IntegerField()),
            ],
            options={
                'db_table': 'p0000common_area',
            },
        ),
        migrations.CreateModel(
            name='building',
            fields=[
                ('building_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('building_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_building',
            },
        ),
        migrations.CreateModel(
            name='car_damage',
            fields=[
                ('car_damage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('car_damage_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('fl_lv00', models.FloatField()),
                ('fl_lv00_50', models.FloatField()),
                ('fl_lv50_100', models.FloatField()),
                ('fl_lv100_200', models.FloatField()),
                ('fl_lv200_300', models.FloatField()),
                ('fl_lv300', models.FloatField()),
                ('car_asset', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_car_damage',
            },
        ),
        migrations.CreateModel(
            name='cause',
            fields=[
                ('cause_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cause_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_cause',
            },
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('city_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=128)),
                ('ken_code', models.CharField(max_length=10)),
                ('city_population', models.IntegerField()),
                ('city_area', models.IntegerField()),
            ],
            options={
                'db_table': 'p0000common_city',
            },
        ),
        migrations.CreateModel(
            name='farmer_fisher_damage',
            fields=[
                ('farmer_fisher_damage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('farmer_fisher_damage_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('dep_fl_lv00', models.FloatField()),
                ('dep_fl_lv00_50', models.FloatField()),
                ('dep_fl_lv50_100', models.FloatField()),
                ('dep_fl_lv100_200', models.FloatField()),
                ('dep_fl_lv200_300', models.FloatField()),
                ('dep_fl_lv300', models.FloatField()),
                ('dep_sd_lv00', models.FloatField()),
                ('dep_sd_lv00_50', models.FloatField()),
                ('dep_sd_lv50_100', models.FloatField()),
                ('dep_sd_lv100_200', models.FloatField()),
                ('dep_sd_lv200_300', models.FloatField()),
                ('dep_sd_lv300', models.FloatField()),
                ('inv_fl_lv00', models.FloatField()),
                ('inv_fl_lv00_50', models.FloatField()),
                ('inv_fl_lv50_100', models.FloatField()),
                ('inv_fl_lv100_200', models.FloatField()),
                ('inv_fl_lv200_300', models.FloatField()),
                ('inv_fl_lv300', models.FloatField()),
                ('inv_sd_lv00', models.FloatField()),
                ('inv_sd_lv00_50', models.FloatField()),
                ('inv_sd_lv50_100', models.FloatField()),
                ('inv_sd_lv100_200', models.FloatField()),
                ('inv_sd_lv200_300', models.FloatField()),
                ('inv_sd_lv300', models.FloatField()),
                ('depreciable_asset', models.IntegerField()),
                ('inventory_asset', models.IntegerField()),
            ],
            options={
                'db_table': 'p0000common_farmer_fisher_damage',
            },
        ),
        migrations.CreateModel(
            name='flood_sediment',
            fields=[
                ('flood_sediment_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('flood_sediment_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_flood_sediment',
            },
        ),
        migrations.CreateModel(
            name='gradient',
            fields=[
                ('gradient_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('gradient_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_gradient',
            },
        ),
        migrations.CreateModel(
            name='house_asset',
            fields=[
                ('house_asset_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ken_code', models.CharField(max_length=10)),
                ('house_asset_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('house_asset', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_house_asset',
            },
        ),
        migrations.CreateModel(
            name='house_cost',
            fields=[
                ('house_cost_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('house_cost_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('alt_lv00', models.FloatField()),
                ('alt_lv00_50', models.FloatField()),
                ('alt_lv50_100', models.FloatField()),
                ('alt_lv100_200', models.FloatField()),
                ('alt_lv200_300', models.FloatField()),
                ('alt_lv300', models.FloatField()),
                ('clean_lv00', models.FloatField()),
                ('clean_lv00_50', models.FloatField()),
                ('clean_lv50_100', models.FloatField()),
                ('clean_lv100_200', models.FloatField()),
                ('clean_lv200_300', models.FloatField()),
                ('clean_lv300', models.FloatField()),
                ('house_cost', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_house_cost',
            },
        ),
        migrations.CreateModel(
            name='house_damage',
            fields=[
                ('house_damage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('house_damage_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('fl_gr1_lv00', models.FloatField()),
                ('fl_gr1_lv00_50', models.FloatField()),
                ('fl_gr1_lv50_100', models.FloatField()),
                ('fl_gr1_lv100_200', models.FloatField()),
                ('fl_gr1_lv200_300', models.FloatField()),
                ('fl_gr1_lv300', models.FloatField()),
                ('fl_gr2_lv00', models.FloatField()),
                ('fl_gr2_lv00_50', models.FloatField()),
                ('fl_gr2_lv50_100', models.FloatField()),
                ('fl_gr2_lv100_200', models.FloatField()),
                ('fl_gr2_lv200_300', models.FloatField()),
                ('fl_gr2_lv300', models.FloatField()),
                ('fl_gr3_lv00', models.FloatField()),
                ('fl_gr3_lv00_50', models.FloatField()),
                ('fl_gr3_lv50_100', models.FloatField()),
                ('fl_gr3_lv100_200', models.FloatField()),
                ('fl_gr3_lv200_300', models.FloatField()),
                ('fl_gr3_lv300', models.FloatField()),
                ('sd_gr1_lv00', models.FloatField()),
                ('sd_gr1_lv00_50', models.FloatField()),
                ('sd_gr1_lv50_100', models.FloatField()),
                ('sd_gr1_lv100_200', models.FloatField()),
                ('sd_gr1_lv200_300', models.FloatField()),
                ('sd_gr1_lv300', models.FloatField()),
                ('sd_gr2_lv00', models.FloatField()),
                ('sd_gr2_lv00_50', models.FloatField()),
                ('sd_gr2_lv50_100', models.FloatField()),
                ('sd_gr2_lv100_200', models.FloatField()),
                ('sd_gr2_lv200_300', models.FloatField()),
                ('sd_gr2_lv300', models.FloatField()),
                ('sd_gr3_lv00', models.FloatField()),
                ('sd_gr3_lv00_50', models.FloatField()),
                ('sd_gr3_lv50_100', models.FloatField()),
                ('sd_gr3_lv100_200', models.FloatField()),
                ('sd_gr3_lv200_300', models.FloatField()),
                ('sd_gr3_lv300', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_house_damage',
            },
        ),
        migrations.CreateModel(
            name='household_damage',
            fields=[
                ('household_damage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('household_damage_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('fl_lv00', models.FloatField()),
                ('fl_lv00_50', models.FloatField()),
                ('fl_lv50_100', models.FloatField()),
                ('fl_lv100_200', models.FloatField()),
                ('fl_lv200_300', models.FloatField()),
                ('fl_lv300', models.FloatField()),
                ('sd_lv00', models.FloatField()),
                ('sd_lv00_50', models.FloatField()),
                ('sd_lv50_100', models.FloatField()),
                ('sd_lv100_200', models.FloatField()),
                ('sd_lv200_300', models.FloatField()),
                ('sd_lv300', models.FloatField()),
                ('household_asset', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_household_damage',
            },
        ),
        migrations.CreateModel(
            name='industry',
            fields=[
                ('industry_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('industry_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_industry',
            },
        ),
        migrations.CreateModel(
            name='ippan',
            fields=[
                ('ippan_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ippan_name', models.CharField(max_length=128, null=True)),
                ('building_code', models.CharField(max_length=10, null=True)),
                ('flood_sediment_code', models.CharField(max_length=10, null=True)),
                ('gradient_code', models.CharField(max_length=10, null=True)),
                ('industry_code', models.CharField(max_length=10, null=True)),
                ('ken_code', models.CharField(max_length=10, null=True)),
                ('city_code', models.CharField(max_length=10, null=True)),
                ('weather_id', models.CharField(max_length=10, null=True)),
                ('area_id', models.CharField(max_length=10, null=True)),
                ('cause_1_code', models.CharField(max_length=10, null=True)),
                ('cause_2_code', models.CharField(max_length=10, null=True)),
                ('cause_3_code', models.CharField(max_length=10, null=True)),
                ('suikei_code', models.CharField(max_length=10, null=True)),
                ('kasen_code', models.CharField(max_length=10, null=True)),
                ('kasen_kaigan_code', models.CharField(max_length=10, null=True)),
                ('underground_code', models.CharField(max_length=10, null=True)),
                ('usage_code', models.CharField(max_length=10, null=True)),
                ('building_lv00', models.IntegerField(null=True)),
                ('building_lv01_49', models.IntegerField(null=True)),
                ('building_lv50_99', models.IntegerField(null=True)),
                ('building_lv100', models.IntegerField(null=True)),
                ('building_half', models.IntegerField(null=True)),
                ('building_full', models.IntegerField(null=True)),
                ('floor_area', models.IntegerField(null=True)),
                ('family', models.IntegerField(null=True)),
                ('office', models.IntegerField(null=True)),
                ('floor_area_lv00', models.FloatField(null=True)),
                ('floor_area_lv01_49', models.FloatField(null=True)),
                ('floor_area_lv50_99', models.FloatField(null=True)),
                ('floor_area_lv100', models.FloatField(null=True)),
                ('floor_area_half', models.FloatField(null=True)),
                ('floor_area_full', models.FloatField(null=True)),
                ('family_lv00', models.IntegerField(null=True)),
                ('family_lv01_49', models.IntegerField(null=True)),
                ('family_lv50_99', models.IntegerField(null=True)),
                ('family_lv100', models.IntegerField(null=True)),
                ('family_half', models.IntegerField(null=True)),
                ('family_full', models.IntegerField(null=True)),
                ('office_lv00', models.IntegerField(null=True)),
                ('office_lv01_49', models.IntegerField(null=True)),
                ('office_lv50_99', models.IntegerField(null=True)),
                ('office_lv100', models.IntegerField(null=True)),
                ('office_half', models.IntegerField(null=True)),
                ('office_full', models.IntegerField(null=True)),
                ('employee_lv00', models.IntegerField(null=True)),
                ('employee_lv01_49', models.IntegerField(null=True)),
                ('employee_lv50_99', models.IntegerField(null=True)),
                ('employee_lv100', models.IntegerField(null=True)),
                ('employee_full', models.IntegerField(null=True)),
                ('farmer_fisher_lv00', models.IntegerField(null=True)),
                ('farmer_fisher_lv01_49', models.IntegerField(null=True)),
                ('farmer_fisher_lv50_99', models.IntegerField(null=True)),
                ('farmer_fisher_lv100', models.IntegerField(null=True)),
                ('farmer_fisher_full', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'p0000common_ippan',
            },
        ),
        migrations.CreateModel(
            name='kasen',
            fields=[
                ('kasen_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('kasen_name', models.CharField(max_length=128)),
                ('kasen_type_code', models.CharField(max_length=10)),
                ('suikei_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'p0000common_kasen',
            },
        ),
        migrations.CreateModel(
            name='kasen_kaigan',
            fields=[
                ('kasen_kaigan_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('kasen_kaigan_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_kasen_kaigan',
            },
        ),
        migrations.CreateModel(
            name='kasen_type',
            fields=[
                ('kasen_type_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('kasen_type_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_kasen_type',
            },
        ),
        migrations.CreateModel(
            name='ken',
            fields=[
                ('ken_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ken_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_ken',
            },
        ),
        migrations.CreateModel(
            name='koeki',
            fields=[
                ('koeki_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ken_code', models.CharField(max_length=10)),
                ('city_code', models.CharField(max_length=10)),
                ('weather_id', models.CharField(max_length=10)),
                ('koeki_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'p0000common_koeki',
            },
        ),
        migrations.CreateModel(
            name='kokyo',
            fields=[
                ('kokyo_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ken_code', models.CharField(max_length=10)),
                ('city_code', models.CharField(max_length=10)),
                ('weather_id', models.CharField(max_length=10)),
                ('kokyo_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'p0000common_kokyo',
            },
        ),
        migrations.CreateModel(
            name='office_asset',
            fields=[
                ('office_asset_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('industry_code', models.CharField(max_length=10)),
                ('office_asset_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('depreciable_asset', models.IntegerField()),
                ('inventory_asset', models.IntegerField()),
                ('value_added', models.IntegerField()),
            ],
            options={
                'db_table': 'p0000common_office_asset',
            },
        ),
        migrations.CreateModel(
            name='office_cost',
            fields=[
                ('office_cost_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('office_cost_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('suspend_lv00', models.FloatField()),
                ('suspend_lv00_50', models.FloatField()),
                ('suspend_lv50_100', models.FloatField()),
                ('suspend_lv100_200', models.FloatField()),
                ('suspend_lv200_300', models.FloatField()),
                ('suspend_lv300', models.FloatField()),
                ('stagnate_lv00', models.FloatField()),
                ('stagnate_lv00_50', models.FloatField()),
                ('stagnate_lv50_100', models.FloatField()),
                ('stagnate_lv100_200', models.FloatField()),
                ('stagnate_lv200_300', models.FloatField()),
                ('stagnate_lv300', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_office_cost',
            },
        ),
        migrations.CreateModel(
            name='office_damage',
            fields=[
                ('office_damage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('office_damage_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('dep_fl_lv00', models.FloatField()),
                ('dep_fl_lv00_50', models.FloatField()),
                ('dep_fl_lv50_100', models.FloatField()),
                ('dep_fl_lv100_200', models.FloatField()),
                ('dep_fl_lv200_300', models.FloatField()),
                ('dep_fl_lv300', models.FloatField()),
                ('dep_sd_lv00', models.FloatField()),
                ('dep_sd_lv00_50', models.FloatField()),
                ('dep_sd_lv50_100', models.FloatField()),
                ('dep_sd_lv100_200', models.FloatField()),
                ('dep_sd_lv200_300', models.FloatField()),
                ('dep_sd_lv300', models.FloatField()),
                ('inv_fl_lv00', models.FloatField()),
                ('inv_fl_lv00_50', models.FloatField()),
                ('inv_fl_lv50_100', models.FloatField()),
                ('inv_fl_lv100_200', models.FloatField()),
                ('inv_fl_lv200_300', models.FloatField()),
                ('inv_fl_lv300', models.FloatField()),
                ('inv_sd_lv00', models.FloatField()),
                ('inv_sd_lv00_50', models.FloatField()),
                ('inv_sd_lv50_100', models.FloatField()),
                ('inv_sd_lv100_200', models.FloatField()),
                ('inv_sd_lv200_300', models.FloatField()),
                ('inv_sd_lv300', models.FloatField()),
            ],
            options={
                'db_table': 'p0000common_office_damage',
            },
        ),
        migrations.CreateModel(
            name='restoration',
            fields=[
                ('restoration_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('restoration_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_restoration',
            },
        ),
        migrations.CreateModel(
            name='suikei',
            fields=[
                ('suikei_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('suikei_name', models.CharField(max_length=128)),
                ('suikei_type_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'p0000common_suikei',
            },
        ),
        migrations.CreateModel(
            name='suikei_type',
            fields=[
                ('suikei_type_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('suikei_type_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_suikei_type',
            },
        ),
        migrations.CreateModel(
            name='underground',
            fields=[
                ('underground_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('underground_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_underground',
            },
        ),
        migrations.CreateModel(
            name='usage',
            fields=[
                ('usage_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('usage_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'p0000common_usage',
            },
        ),
        migrations.CreateModel(
            name='weather',
            fields=[
                ('weather_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('weather_name', models.CharField(max_length=128)),
                ('weather_year', models.IntegerField()),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'p0000common_weather',
            },
        ),
    ]