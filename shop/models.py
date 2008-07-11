#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

from django.contrib.auth.models import User

class ShopProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # max_lenght 18 because we want users to write "+90 0212 123 45 67"
    phone = models.CharField('Telefon', max_lenght=18, help_text='Telefon numarası. +90 <alan kodu> <numara> şeklinde belirtin. Örneğin; +90 0212 123 45 67')
    cellphone = models.CharField('Cep Telefonu', max_lenght=18, blank=True, help_text='Cep telefonu. +90 <operator> <numara> şeklinde belirtin. Örneğin; +90 512 345 67 89. (zorunlu değil)')
    adress = models.TextField('Adres', help_text='İkamet ettiğiniz yer')
    second_adress = models.TextField('İkinci Adres', help_text='Size ulaşabileceğimiz 2. bir adres (zorunlu değil')
    postcode = models.IntegerField('Posta Kodu', max_lenght=7)

    bill = models.ManyToManyField(Bill)

# Bill Class

class Bill(models.Model):
    # We don't require filling all fields here, we will control it in the view as user can have 2 bill type.
    # If we require all fields, then user wanting to select only invidual bill type won't be able to select it. Additionally, user can select both bill type.

    # Invidual bill type fields
    adress = models.TextField('Ürünlerin gönderileceği adres', blank=True)

    # Bill type for companies
    company_name = models.CharField('Şirket Adı', max_length=200, blank=True)
    company_adress = models.TextField('Şirket Adresi', blank=True)
    # user's title in company
    employee_title = models.CharField('Ünvan', max_lenght=20, blank=True, help_text='Şirket içerisindeki ünvanınız.')
    tax_number = models.IntegerField('Vergi numarası', max_lenght=15, blank=True)
    tax_department = models.CharField('Vergi dairesi adı', max_lenght=200, blank=True, help_text='İstanbul Bakırköy Vergi Dairesi gibi.')
