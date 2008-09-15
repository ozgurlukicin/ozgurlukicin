#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import forms

from oi.shop.shopprofile.models import ShopProfile

def phoneValidator(field_data):
    if field_data == "":
        return field_data
    phone_re = re.compile(r'^\d{10}$')
    if not phone_re.search(field_data):
        raise forms.ValidationError, u"Telefon numarası &lt;alan kodu&gt;&lt;numara&gt; şeklinde olmalıdır. Ör: 2121234567"
    return field_data

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        exclude = ("user",)
    def clean_phone(self):
        return phoneValidator(self.cleaned_data["phone"])

    def clean_cellphone(self):
        return phoneValidator(self.cleaned_data["cellphone"])
