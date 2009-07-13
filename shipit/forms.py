#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import forms

from oi.shipit.models import *

class CdClientForm(forms.ModelForm):
    class Meta:
        model = CdClient
        exclude = ("sent", "taken", "hash", "confirmed", "date", "ip")

    def clean(self):
        if self.cleaned_data.has_key("number_of_cds"):
            if self.cleaned_data["number_of_cds"]>1:
                if not self.cleaned_data["reason"]:
                    raise forms.ValidationError("Birden fazla CD istiyorsanız sebebini yazmalısınız.")
        return self.cleaned_data

    def clean_postcode(self):
        postcode = self.cleaned_data["postcode"]
        if postcode:
            match = re.match(re.compile(r"^\d{5}$"), postcode)
            if not match:
                raise forms.ValidationError("Lütfen geçerli bir posta kodu girin veya boş bırakın.")
        return postcode

    def clean_phone_area(self):
        phone_area = self.cleaned_data["phone_area"]
        match = re.match(re.compile(r"^\d{3}$"), phone_area)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir alan kodu girin.")
        return phone_area

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        match = re.match(re.compile(r"^\d{7}$"), phone_number)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin.")
        return phone_number

    def clean_number_of_cds(self):
        number_of_cds = self.cleaned_data["number_of_cds"]
        if number_of_cds < 1:
            raise forms.ValidationError("Lütfen geçerli bir CD sayısı girin.")
        return number_of_cds

class CdClientChangeForm(CdClientForm):
    class Meta:
        model = CdClient
        exclude = ("ip", "hash")

class CodeForm(forms.Form):
    code = forms.IntegerField(label="Sipariş kodu")

    def clean_code(self):
        icode = self.cleaned_data["code"]
        code = str(icode)
        if len(code) < 3 or code[:3] != "700":
            raise forms.ValidationError("Girdiğiniz kod geçerli değil")
        else:
            code = code[3:]
            try:
                CdClient.objects.get(id=int(code))
            except:
                raise forms.ValidationError("Girdiğiniz kod geçerli değil")
        return icode
