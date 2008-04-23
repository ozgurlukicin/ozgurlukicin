#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

STATUS_CODES = (
    (1, "Yeni"),
    (2, "Atandı"),
    (3, "Kapalı"),
    )
PRIORITIES = (
    (1, "Büyük"),
    (2, "Engelleyici"),
    (3, "Normal"),
    (4, "İyileştirme"),
    (5, "Küçük"),
    )

class Bug(models.Model):
    title = models.CharField(verbose_name="Başlık", max_length=100)
    submitted_date = models.DateField(verbose_name="Tarih", auto_now_add=True)
    submitter = models.ForeignKey(User, verbose_name="Gönderen", related_name="submitter")
    assigned_to = models.ForeignKey(User, verbose_name="Atanan")
    description = models.TextField(verbose_name="Tanım", blank=False)
    status = models.IntegerField(verbose_name="Durum", default=1, choices=STATUS_CODES)
    priority = models.IntegerField(verbose_name="Öncelik", default=3, choices=PRIORITIES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/bug/%s/" % self.id

    class Admin:
        list_display = ('status', 'title', 'submitter', 'assigned_to')
        list_filter = ('status', 'submitted_date')
        search_fields = ('assigned_to', 'submitter', 'title', 'description')

class Comment(models.Model):
    bug = models.ForeignKey(Bug)
    author = models.ForeignKey(User)
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Admin:
        list_display = ('bug', 'author')
        list_filter = ('bug', 'date')
        search_fields = ('text', 'submitter')
