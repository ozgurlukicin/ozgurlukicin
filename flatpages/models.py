#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from oi.st.models import Tag
from oi.middleware import threadlocals

class FlatPage(models.Model):
    url = models.CharField('URL', maxlength=100, validator_list=[validators.isAlphaNumericURL])
    title = models.CharField('Başlık', maxlength=200)
    text = models.TextField('Metin')
    author = models.ForeignKey(User, blank=True, editable=False)
    tags = models.ManyToManyField(Tag)
    update = models.DateTimeField('Tarih', blank=False)
    template_name = models.CharField('Şablon adı', maxlength=70, blank=True)

    class Meta:
        verbose_name = 'Statik sayfa'
        verbose_name_plural = 'Statik sayfalar'

    class Admin:
        fields = (
            ('Genel', {'fields': ('url', 'title', 'text', 'tags', 'update')}),
            ('Diğer', {'classes': 'collapse', 'fields': ('template_name',)}),
        )

        list_display = ('id', 'url', 'title', 'update')
        list_filter = ['update']
        ordering = ['-update']
        search_fields = ['title', 'text', 'tags']
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def get_printable_url(self):
        return "%syazdir/" % self.url

    def save(self):
        self.author = threadlocals.get_current_user()
        super(FlatPage, self).save()