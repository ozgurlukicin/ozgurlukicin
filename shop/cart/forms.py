#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms

class BuyForm(forms.Form):
    price = forms.IntegerField(label="Fiyat", min_value=20)
    count = forms.IntegerField(label="Adet", min_value=20)
    productname = forms.CharField(label="Ürün Adı", max_length=128)
    strorder_tubitak = forms.CharField(label="Ürün Detayları", max_length=256)
    name = forms.CharField(label="İsim", max_length=32)
    lastname = forms.CharField(label="Soyisim", max_length=32)
    email = forms.EmailField(label="E-posta", max_length=64)
    telephone = forms.CharField(label="Telefon", max_length=12, min_length=12)
    telephonegsm = forms.CharField(label="Cep Telefonu", max_length=12, min_length=12)
    adress = forms.CharField(label="Adres", max_length=512)
    postcode = forms.IntegerField(label="Posta Kodu", min_value=10000, max_value=99999)
    ilce = forms.CharField(label="İlçe", max_length=32)
    city = forms.CharField(label="Şehir", max_length=32)
    country = forms.CharField(label="Ülke", max_length=32)

    taxname = forms.CharField(label="Fatura İsim", max_length=32)
    taxlastname = forms.CharField(label="Fatura Soyisim", max_length=32)
    taxadress = forms.CharField(label="Fatura Adresi", max_length=512)
    taxpostcode = forms.IntegerField(label="Fatura Posta Kodu", min_value=10000, max_value=99999)
    taxilce = forms.CharField(label="Fatura İlçesi", max_length=32)
    taxcity = forms.CharField(label="Fatura Şehri", max_length=32)
    taxcountry = forms.CharField(label="Fatura Ülkesi", max_length=32)
    taxvergidairesi = forms.CharField(label="Fatura Vergi Dairesi", max_length=32)
    taxvergino = forms.IntegerField(label="Fatura Vergi No", min_value=100000000, max_value=999999999)
    tckimlikno = forms.IntegerField(label="Fatura TC Kimlik No", min_value=10000000000, max_value=99999999999)
