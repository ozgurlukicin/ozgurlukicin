#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField('Seminer Yeri', max_length=64, blank=False, unique=True)
    description = models.TextField("Yer Tanımı", max_length=512, blank=True)
    phone = models.CharField("Telefon", max_length=16, blank=True)
    latitude = models.DecimalField('Enlem', max_digits=10, decimal_places=6, default=0, help_text="40.903823 gibi")
    longitude = models.DecimalField('Boylam', max_digits=10, decimal_places=6, default=0, help_text="29.226723 gibi")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Seminer Yeri"
        verbose_name_plural = "Seminer Yerleri"

class Attender(models.Model):
    name = models.CharField('Gerçek Adı', max_length=64, blank=False, unique=True)
    user = models.ForeignKey(User, verbose_name="Öİ Kullanıcı Adı", blank=True, null=True, help_text="Zorunlu değil")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Konuşmacı"
        verbose_name_plural = "Konuşmacılar"

class Seminar(models.Model):
    description = models.CharField('Seminer tanımı', max_length = 64, blank = False, unique = True)
    place = models.ForeignKey(Place, verbose_name="Yer")
    attender = models.ManyToManyField(Attender, verbose_name="Katılımcılar")
    start_date = models.DateTimeField('Başlangıç', blank=False)
    end_date = models.DateTimeField('Bitiş', blank=True, null=True, help_text="zorunlu değil")
    status = models.BooleanField('Aktif')

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return "/seminer/%d/" % self.id

    class Meta:
        verbose_name = "Seminer"
        verbose_name_plural = "Seminerler"
