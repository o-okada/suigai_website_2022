# -*- coding: utf-8 -*-
from django import forms

class KoekiUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/xlsx'}))