# -*- coding: utf-8 -*-
from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/xlsx'}))