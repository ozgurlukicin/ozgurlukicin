#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import forms

from oi.shipit.models import *

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
        if CdClient.objects.filter(tcidentity=value, confirmed=True).count() > 0:
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

class CdClientForm(forms.ModelForm):
    tcidentity = TurkishIdentityNumberField(label="TC kimlik no")
    phone_area = forms.CharField(label="Telefon (sabit hat)", max_length=3, required=False, widget=forms.TextInput(attrs={"style":"width:30px;margin-right:5px"}))
    phone_number = forms.CharField(label="Telefon Numarası", max_length=7, required=False, widget=forms.TextInput(attrs={"style":"width:130px"}))
    gsm_area = forms.CharField(label="Telefon (GSM)", max_length=3, required=False, widget=forms.TextInput(attrs={"style":"width:30px;margin-right:5px"}))
    gsm_number = forms.CharField(label="Cep Telefonu Numarası", max_length=7, required=False, widget=forms.TextInput(attrs={"style":"width:130px"}))
    class Meta:
        model = CdClient
        exclude = ("sent", "taken", "hash", "confirmed", "date", "ip", "reason", "number_of_cds", "company", "postcode")

    def clean(self):
        if self.cleaned_data.has_key("number_of_cds"):
            if self.cleaned_data["number_of_cds"]>1:
                if not self.cleaned_data["reason"]:
                    raise forms.ValidationError("Birden fazla DVD istiyorsanız sebebini yazmalısınız.")

        _phone_area = self.cleaned_data.get('phone_area')
        _phone_number = self.cleaned_data.get('phone_number')
        _gsm_area = self.cleaned_data.get('gsm_area')
        _gsm_number = self.cleaned_data.get('gsm_number')

        if not _phone_area and not _phone_number and not _gsm_area and not _gsm_number:
            raise forms.ValidationError("En azından bir telefon numarası belirtmeniz gerekmektedir.")

        return self.cleaned_data

    def clean_phone_area(self):
        phone_area = self.cleaned_data.get('phone_area')
        if not phone_area:
            return phone_area

        match = re.match(re.compile(r"^\d{3}$"), phone_area)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin.")

        if phone_area.startswith("5"):
            raise forms.ValidationError("5 ile başlayan alan kodları GSM içindir.")

        return phone_area

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            return phone_number

        match = re.match(re.compile(r"^\d{7}$"), phone_number)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin.")

        return phone_number

    def clean_gsm_area(self):
        gsm_area = self.cleaned_data.get('gsm_area')
        if not gsm_area:
            return gsm_area

        match = re.match(re.compile(r"^\d{3}$"), gsm_area)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin.")

        if not gsm_area.startswith("5"):
            raise forms.ValidationError("Türkiye'de GSM alan kodları 5'le başlar.")

        return gsm_area

    def clean_gsm_number(self):
        gsm_number = self.cleaned_data.get('gsm_number')
        if not gsm_number:
            return gsm_number

        match = re.match(re.compile(r"^\d{7}$"), gsm_number)
        if not match:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin.")

        return gsm_number

    def clean_number_of_cds(self):
        number_of_cds = self.cleaned_data["number_of_cds"]
        if number_of_cds < 1:
            raise forms.ValidationError("Lütfen geçerli bir DVD sayısı girin.")
        return number_of_cds

class CdClientChangeForm(CdClientForm):
    class Meta:
        model = CdClient
        exclude = ("ip", "hash")

class SearchForm(forms.Form):
    term = forms.CharField(label="Aranacak metin")

class CargoForm(forms.ModelForm):
    date = forms.DateField(label="Gönderme Tarihi", input_formats=("%d/%m/%Y","%Y-%m-%d"), help_text="15/08/2009 gibi")
    class Meta:
        model = Cargo
        exclude = ("cdclient")
