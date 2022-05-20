# -*- coding: utf-8 -*-
import datetime

from django import forms

###############################################################################
### 処理名：インポート処理
###############################################################################
class ChoiceForm(forms.Form):
    CHOICES = [('1', '承認'), ('2', '否認'), ('3', '保留')]

    upload_date_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='',
        max_length=100)
    
    ken_code_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)

    ken_name_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)
    
    city_code_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)

    city_name_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)
    
    ippan_kokyo_koeki_code_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)

    ippan_kokyo_koeki_name_hidden = forms.CharField(
        label='', 
        ### widget=forms., 
        initial='', 
        max_length=100)
    
    choice_hidden = forms.ChoiceField(
        label='', 
        widget=forms.RadioSelect, 
        choices=CHOICES)

###############################################################################
### 処理名：インポート処理
###############################################################################
class ScheduleForm(forms.Form):
    CHOICES = [('1', 'スケジュール集計・配布'), ('2', '即時集計・配布')]
    
    ### split_date_time_hidden = forms.SplitDateTimeField(
    ###     label='', 
    ###     widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'}, time_attrs={'type':'time'}),
    ###     initial=datetime.datetime.now)
    
    year_hidden = forms.CharField(
        label='',
        initial='',
        max_length=100)
    
    month_hidden = forms.CharField(
        label='',
        initial='',
        max_length=100)
    
    day_hidden = forms.CharField(
        label='',
        initial='',
        max_length=100)
    
    hour_hidden = forms.CharField(
        label='',
        initial='',
        max_length=100)
    
    minute_hidden = forms.CharField(
        label='',
        initial='',
        max_length=100)
    
    comment_hidden = forms.CharField(
        label='承認時コメント',
        widget=forms.Textarea,
        initial='承認時コメント')

    choice_hidden = forms.ChoiceField(
        label='', 
        widget=forms.RadioSelect, 
        choices=CHOICES)
