#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

from django.contrib.auth.models import User

class ShopProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    # max_length 18 because we want users to write "+90 0212 123 45 67"
    phone = models.CharField('Telefon', max_length=18, help_text='Telefon numarası. +90 <alan kodu> <numara> şeklinde belirtin. Örneğin; +90 0212 123 45 67')
    cellphone = models.CharField('Cep Telefonu', max_length=18, blank=True, help_text='Cep telefonu. +90 <operator> <numara> şeklinde belirtin. Örneğin; +90 512 345 67 89. (zorunlu değil)')
    adress = models.TextField('Adres', help_text='İkamet ettiğiniz yer')
    second_adress = models.TextField('İkinci Adres', blank=True, help_text='Size ulaşabileceğimiz 2. bir adres (zorunlu değil')
    postcode = models.IntegerField('Posta Kodu', max_length=7)

    bill = models.OneToOneField('Bill')

    def __unicode__(self):
        return u'%s' % self.user.username

    #FIXME: Add some useful methods for getting user's ordered products

    class Meta:
        verbose_name = 'Alışveriş Profili'
        verbose_name_plural = 'Alışveriş Profilleri'
        ordering = ('user',)

    class Admin:
        list_display = ('user', 'phone', 'adress',)

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
    employee_title = models.CharField('Ünvan', max_length=20, blank=True, help_text='Şirket içerisindeki ünvanınız.')
    tax_number = models.IntegerField('Vergi numarası', max_length=15, blank=True, default=0)
    tax_department = models.CharField('Vergi dairesi adı', max_length=200, blank=True, help_text='İstanbul Bakırköy Vergi Dairesi gibi.')

    def __unicode__(self):
        if self.adress:
            return u'%s' % self.adress

    def have_company_information(self):
        """ Checks if the user has company information """
        if self.company_name and self.tax_number:
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Fatura Bilgisi'
        verbose_name_plural = 'Fatura Bilgileri'

    class Admin:
        list_display = ('shop_profile', 'adress', 'company_name', 'tax_number',)
        search_fields = ['adress']

    def shop_profile(self):
        qs = ShopProfile.objects.filter(bill=self)
        if qs.count() >= 1:
            return qs[0]
        else:
            return None
    shop_profile.short_description = 'Profil'
