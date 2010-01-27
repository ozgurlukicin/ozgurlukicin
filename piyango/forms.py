#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import forms

from oi.piyango.models import Person
from oi.shipit.forms import TurkishIdentityNumberField

class PersonForm(forms.ModelForm):
    tcidentity = TurkishIdentityNumberField(label="TC kimlik no")
    phone_area = forms.CharField(label="Telefon", max_length=3, widget=forms.TextInput(attrs={"style":"width:30px;margin-right:5px"}))
    phone_number = forms.CharField(label="Telefon Numarası", max_length=7, widget=forms.TextInput(attrs={"style":"width:130px"}))
    class Meta:
        model = Person
        exclude = ("hash", "confirmed", "date", "ip")

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
