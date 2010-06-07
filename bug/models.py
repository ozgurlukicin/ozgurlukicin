#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from oi.settings import WEB_URL

STATUS_CODES = (
    (1, "Yeni"),
    (2, "Atandı"),
    (3, "Kapalı"),
    )
PRIORITIES = (
    (1, "Engelleyici"),
    (2, "Büyük"),
    (3, "Normal"),
    (4, "Küçük"),
    (5, "İyileştirme"),
    )

class Bug(models.Model):
    title = models.CharField(verbose_name="Başlık", max_length=100)
    submitted_date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
    submitter = models.ForeignKey(User, verbose_name="Gönderen", related_name="submitter")
    assigned_to = models.ForeignKey(User, verbose_name="Atanan")
    description = models.TextField(verbose_name="Tanım", blank=False)
    status = models.IntegerField(verbose_name="Durum", default=1, choices=STATUS_CODES)
    priority = models.IntegerField(verbose_name="Öncelik", default=3, choices=PRIORITIES)

    def __unicode__(self):
        return self.title

    def get_full_url(self):
        return "%s%s" % (WEB_URL, self.get_absolute_url())

    def get_absolute_url(self):
        return "/hata/%s/" % self.id

    def get_delete_url(self):
        return "/hata/sil/%d/" % self.id

    class Admin:
        list_display = ('status', 'title', 'submitter', 'assigned_to')
        list_filter = ('status', 'submitted_date')
        search_fields = ('assigned_to', 'submitter', 'title', 'description')

class Comment(models.Model):
    bug = models.ForeignKey(Bug, verbose_name="Hata")
    author = models.ForeignKey(User, verbose_name="Yazan")
    text = models.TextField(blank=False, verbose_name="Yorum")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    def __unicode__(self):
        return self.text

    class Admin:
        list_display = ('bug', 'author')
        list_filter = ('bug', 'date')
        search_fields = ('text', 'submitter')
