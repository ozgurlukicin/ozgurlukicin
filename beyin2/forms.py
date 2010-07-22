#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from oi.beyin2.models import Idea, ScreenShot
from oi.st.tags import Tag

from oi.st.forms import XssField

class IdeaForm(forms.ModelForm):
    description = XssField(label='Açıklama', required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    title = forms.CharField(label='Açıklama', required=True, widget=forms.TextInput(attrs={'size': '40',}))
    class Meta:
        model = Idea
        fields = ('title', 'description', 'status', 'category', 'tags')
        
    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        return field_data
        
class TagsForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'tags',)
    
    def clean_tags(self):
        field_data = self.cleaned_data['tags']
        return field_data

class IdeaDuplicateForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('duplicate',)

class ScreenShotForm(forms.ModelForm):
    class Meta:
        model = ScreenShot
        fields = ('image',)
