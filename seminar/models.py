#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007, 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

from oi.settings import CITY_LIST

class Place(models.Model):
    name = models.CharField('Seminer Yeri', max_length=64, blank=False, unique=True)
    city = models.CharField('Şehir', choices=CITY_LIST, max_length=40)
    direction = models.TextField('Adres Tarifi', blank=True)
    phone = PhoneNumberField('Telefon', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Seminer Yeri"
        verbose_name_plural = "Seminer Yerleri"

class Attender(models.Model):
    name = models.CharField('Konuşmacı', max_length=64, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Konuşmacı"
        verbose_name_plural = "Konuşmacılar"

class Seminar(models.Model):
    description = models.CharField('Seminer tanımı', max_length = 64, blank = False, unique = True)
    place = models.ForeignKey(Place)
    attender = models.ManyToManyField(Attender)
    date = models.DateField('Tarih', blank=False)
    status = models.BooleanField('Aktif')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = "Seminer"
        verbose_name_plural = "Seminerler"
