#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import forms

from oi.piyango.models import Person

class TurkishIdentityNumberField(forms.Field):
    """
    A Republic of Turkey Identity number.

    Checks the following rules to determine whether the number is valid:

        * Last 2 characters of ID should validate the following algorithm.
    """
    default_error_messages = {
        'invalid': 'Lütfen geçerli bir TC kimlik numarası girin.',
        'duplicate': 'Bu TC kimlik numarası daha önce kullanılmış.',
    }

    def clean(self, value):
        super(TurkishIdentityNumberField, self).clean(value)
        if not value:
            return u''

        #check for duplicates
        if Person.objects.filter(tcidentity=value, confirmed=True).count() > 0:
            raise forms.ValidationError(self.error_messages['duplicate'])

        #check number integrity
        match = re.match(re.compile(r"^\d{11}$"), value)
        if not match:
            raise forms.ValidationError(self.error_messages['invalid'])

        odds, evens = 0, 0
        for i in range(9):
            if i % 2:
                evens += int(value[i])
            else:
                odds += int(value[i])

        t1 = odds * 3 + evens
        c1 = (10 - t1 % 10) % 10
        t2 = c1 + evens
        t3 = t2 * 3 + odds
        c2 = (10 - t3 % 10) % 10

        if c1 != int(value[9]) or c2 != int(value[10]):
            raise forms.ValidationError(self.error_messages['invalid'])

        return value


class PersonForm(forms.ModelForm):
    tcidentity = TurkishIdentityNumberField(label="TC Kimlik No")
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
