#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

from oi.settings import CITY_LIST

class CdClient(models.Model):
    firstname = models.CharField("Ad", max_length=30)
    lastname = models.CharField("Soyad", max_length=30)
    address = models.TextField("Adres")
    postcode = models.CharField("Posta Kodu", blank=True, max_length=5)
    town = models.CharField("İlçe", max_length=40)
    city = models.CharField("Şehir", choices=CITY_LIST, max_length=40)
    phone_area = models.CharField("Alan Kodu", max_length=3)
    phone_number = models.CharField("Telefon Numarası", max_length=7)
    sent = models.BooleanField("Gönderildi")
    taken = models.BooleanField("Alındı")

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_full_phone(self):
        return u"%s %s" % (self.phone_area, self.phone_number)

    def __unicode__(self):
        return self.get_full_name()
