#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField('Gerçek Adı', max_length=64, blank=False, unique=True)
    user = models.ForeignKey(User, verbose_name="Öİ Kullanıcı Adı", blank=True, null=True, help_text="Zorunlu değil", related_name="podcast_author")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Konuşmacı"
        verbose_name_plural = "Konuşmacılar"

class License(models.Model):
    name = models.CharField(max_length=16, blank=False, unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Lisans"
        verbose_name_plural = "Lisanslar"

class Episode(models.Model):
    title = models.CharField(max_length=64)
    summary = models.TextField()
    description = models.TextField()
    authors = models.ManyToManyField(Author)
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    file_url_mp3 = models.URLField()
    file_size_mp3 = models.IntegerField()
    file_url_ogg = models.URLField()
    file_size_ogg = models.IntegerField()
    date = models.DateTimeField()
    active = models.BooleanField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
