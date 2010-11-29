#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from oi.settings import CITY_LIST

class ShopProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    tcno = models.CharField("TC kimlik no", max_length=11, help_text="TC Kimlik numaranız.")
    phone = models.CharField('Telefon', max_length=10, help_text='Telefon numarası. <alan kodu><numara> şeklinde belirtin. Örneğin; 2121234567')
    cellphone = models.CharField('Cep Telefonu', max_length=10, blank=True, null=True, help_text='Cep telefonu. <alan kodu><numara> şeklinde belirtin. Örneğin; 5123456789. (zorunlu değil)')
    address = models.TextField('Adres', max_length=300)
    postcode = models.IntegerField("Posta Kodu", null=True, blank=True, help_text="5 haneli posta kodunuzu girin. (zorunlu değil)")
    town = models.CharField("İlçe", max_length=20)
    city = models.CharField('Şehir', choices=CITY_LIST, max_length=20)
    billing_firstname = models.CharField("Fatura kesilecek kişi", max_length=200, help_text="Gerçek isim ya da tüzel kişi")
    billing_lastname = models.CharField("Fatura Soyadı", blank=True, max_length=200, help_text="Fatura için soyadınız (tüzel kişiyse boş bırakınız)")
    billing_address = models.TextField('Fatura Adresi', max_length=300, help_text="Fatura için adres")
    billing_postcode = models.IntegerField("Posta Kodu", null=True, blank=True, help_text="5 rakamdan oluşan posta kodunuzu girin. (zorunlu değil)")
    billing_town = models.CharField("İlçe", max_length=50)
    billing_city = models.CharField('Şehir', choices=CITY_LIST, max_length=50)
    billing_office = models.CharField("Vergi Dairesi", max_length=50, null=True, blank=True, help_text="Zorunlu değil")
    billing_no = models.IntegerField("Vergi No", max_length=20, null=True, blank=True, help_text="Zorunlu değil")

    def __unicode__(self):
        return u'%s' % self.user.username

    def get_absolute_url(self):
        return '/dukkan/profil/%s/' % self.user.username

    #FIXME: Add some useful methods for getting user's ordered products

    class Meta:
        verbose_name = 'Alışveriş Profili'
        verbose_name_plural = 'Alışveriş Profilleri'
        ordering = ('user',)
