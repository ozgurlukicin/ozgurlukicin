#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

from oi.upload.models import Image
from oi.forum.models import Topic
from oi.forum.tools import create_forum_topic
from oi.st.tags import Tag

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
    title = models.CharField("Başlık", max_length=32)
    slug = models.SlugField("SEF Başlık")
    image = models.ForeignKey(Image, verbose_name="Görsel", blank=True, null=True)
    sum = models.TextField("Özet")
    text = models.TextField("Metin")
    tags = models.ManyToManyField(Tag)
    authors = models.ManyToManyField(Author)
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    file_url_mp3 = models.URLField()
    file_size_mp3 = models.IntegerField()
    file_url_ogg = models.URLField()
    file_size_ogg = models.IntegerField()
    update = models.DateTimeField()
    status = models.BooleanField("Aktif")
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def save(self):
        create_forum_topic(self, "Podcast")
        super(Episode, self).save()

    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
