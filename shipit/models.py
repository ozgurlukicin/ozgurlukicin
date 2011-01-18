#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import random
from hashlib import sha1 as sha

from django.db import models
from django.contrib.sites.models import Site

from oi.shipit.settings import CITY_LIST
from oi.middleware import threadlocals

class PardusVersion(models.Model):
    version = models.CharField("Sürüm", max_length=64, unique=True)

    def __unicode__(self):
        return self.version

class CdClient(models.Model):
    number_of_cds = models.PositiveIntegerField("DVD adedi", default=1)
    reason = models.TextField("DVD isteme sebebiniz", max_length=512, blank=True)
    first_name = models.CharField("Ad", max_length=30)
    last_name = models.CharField("Soyad", max_length=30)
    tcidentity = models.CharField("TC kimlik no", max_length="11")
    company = models.CharField("Şirket/Kurum", max_length=30, blank=True)
    email = models.EmailField("E-Posta")
    address = models.TextField("Adres")
    postcode = models.CharField("Posta kodu", blank=True, max_length=5)
    town = models.CharField("İlçe", max_length=40)
    city = models.CharField("Şehir", choices=CITY_LIST, max_length=40)
    phone_area = models.CharField("Alan kodu", max_length=3, blank=True)
    phone_number = models.CharField("Telefon numarası", max_length=7, blank=True)
    gsm_area = models.CharField("GSM alan kodu", max_length=3, blank=True)
    gsm_number = models.CharField("Cep telefonu numarası", max_length=7, blank=True)
    ip = models.IPAddressField(blank=True, verbose_name='IP adresi')
    date = models.DateTimeField(auto_now_add=True)
    version = models.ForeignKey("PardusVersion", verbose_name="Sürüm")

    confirmed = models.BooleanField("Onaylandı")
    sent = models.BooleanField("Gönderildi")
    taken = models.BooleanField("Alındı")
    hash = models.CharField("Etkinleştirme Anahtarı", max_length=40)

    def get_full_name(self):
        return unicode("%s %s") % (self.first_name, self.last_name)

    def get_full_phone(self):
        return unicode("(%s) %s") % (self.phone_area, self.phone_number)

    def __unicode__(self):
        return self.get_full_name()

    def save(self):
        if not self.hash:
            random.seed()
            salt = sha(str(random.random())).hexdigest()
            self.hash = sha(salt).hexdigest()
        if not self.ip:
            self.ip = threadlocals.get_current_ip()
        super(CdClient, self).save()

    def get_confirm_url(self):
        return "http://%s/cdgonder/onay/%s/%s/" % (Site.objects.get_current().domain, self.id, self.hash)

    def get_absoulte_url(self):
        return "/cdgonder/detay/%s/" % self.id

    def get_cargo_url(self):
        return "/cdgonder/kargo/%s/" % self.id

    def get_id(self):
        return "700%s" % self.id

class CargoCompany(models.Model):
    name = models.CharField(max_length=64)
    web_site = models.URLField("Web sitesi")

    def __unicode__(self):
        return self.name

class Cargo(models.Model):
    cdclient = models.ForeignKey(CdClient, unique=True)
    serial = models.CharField("Seri No", max_length=8, default="9P")
    follow_code = models.CharField("Takip kodu", max_length=20)
    company = models.ForeignKey(CargoCompany, verbose_name="Kargo şirketi")
    date = models.DateField()

