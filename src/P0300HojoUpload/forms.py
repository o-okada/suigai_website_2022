# -*- coding: utf-8 -*-
from django import forms

class HojoUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/xlsx'}))