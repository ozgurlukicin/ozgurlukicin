#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django import forms

class BuyForm(forms.Form):
#   price_1 = forms.IntegerField(label="Fiyat", min_value=0)
#   count_1 = forms.IntegerField(label="Adet", min_value=0)
#   productname_1 = forms.CharField(label="Ürün Adı", max_length=50)
#   strorder_tubitak_1 = forms.CharField(label="Ürün Detayları")
#   productid_1 = forms.CharField(label="Ürün Tanım No", max_length=20)
    productcount = forms.IntegerField(label="Sepetteki Ürün Sayısı", min_value=0)
    name = forms.CharField(label="İsim", max_length=50)
    lastname = forms.CharField(label="Soyisim", max_length=50)
    email = forms.EmailField(label="E-posta", max_length=50)
    telephone = forms.CharField(label="Telefon", max_length=12, min_length=12)
    telephonegsm = forms.CharField(label="Cep Telefonu", max_length=12, min_length=12, required=False)
    address = forms.CharField(label="Adres", max_length=200)
    postcode = forms.IntegerField(label="Posta Kodu", min_value=10000, max_value=99999, required=False)
    ilce = forms.CharField(label="İlçe", max_length=50)
    city = forms.CharField(label="Şehir", max_length=50)
    country = forms.CharField(label="Ülke", max_length=50)

    taxname = forms.CharField(label="Fatura İsim", max_length=50)
    taxlastname = forms.CharField(label="Fatura Soyisim", max_length=50)
    taxadress = forms.CharField(label="Fatura Adresi", max_length=200)
    taxpostcode = forms.IntegerField(label="Fatura Posta Kodu", min_value=10000, max_value=99999, required=False)
    taxilce = forms.CharField(label="Fatura İlçesi", max_length=50)
    taxcity = forms.CharField(label="Fatura Şehri", max_length=50)
    taxcountry = forms.CharField(label="Fatura Ülkesi", max_length=50)
    taxvergidairesi = forms.CharField(label="Fatura Vergi Dairesi", max_length=50, required=False)
    taxvergino = forms.IntegerField(label="Fatura Vergi No", min_value=100000000, max_value=999999999, required=False)
    tckimlikno = forms.IntegerField(label="Fatura TC Kimlik No", min_value=10000000000, max_value=99999999999)
