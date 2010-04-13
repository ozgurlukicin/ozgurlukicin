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
from oi.podcast.utils import getDuration

class Author(models.Model):
    user = models.ForeignKey(User, verbose_name="Öİ Kullanıcı Adı", related_name="podcast_author")

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user']
        verbose_name = "Konuşmacı"
        verbose_name_plural = "Konuşmacılar"

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
    mp3file = models.FileField(upload_to="podcasts/")
    oggfile = models.FileField(upload_to="podcasts/")
    update = models.DateTimeField()
    status = models.BooleanField("Aktif")
    topic = models.ForeignKey(Topic, verbose_name="Forumdaki Konusu")

    def __unicode__(self):
        return self.title

    def save(self):
        self.minutes, self.seconds = getDuration(self.mp3file.path)
        create_forum_topic(self, "Ajans Pardus")
        super(Episode, self).save()

    def get_absolute_url(self):
        return "/podcast/bolum/%s/" % self.slug

    def get_length(self):
        return "%s:%s" % (
            "0%d" % self.minutes if self.minutes<10 else str(self.minutes),
            "0%d" % self.seconds if self.seconds<10 else str(self.seconds)
        )

    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
