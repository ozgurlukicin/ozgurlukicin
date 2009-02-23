#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms
from oi.st.models import News
from oi.st.forms import XssField

class ContributedNewsForm(forms.ModelForm):
    sum = XssField(label="Özet", required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}), help_text="Açılış görseli haber özetine otomatik eklenecektir. Bu nedenle özetin içine görsel eklemeyin.")
    text = XssField(label="Metin", required=True, widget=forms.Textarea(attrs={'rows': '20', 'cols': '60',}))
    class Meta:
        model = News
        exclude = ("update", "status", "topic")
