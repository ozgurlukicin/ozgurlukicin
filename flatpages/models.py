#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User
from oi.st.tags import Tag
from oi.middleware import threadlocals

from django.utils.translation import ugettext as _

class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100)
    title = models.CharField(_('Title'), max_length=200)
    text = models.TextField(_('Text'))
    author = models.ForeignKey(User, blank=True, editable=False)
    tags = models.ManyToManyField(Tag)
    update = models.DateTimeField(_('Date'), blank=False)
    template_name = models.CharField(_('Template name'), max_length=70, blank=True)

    class Meta:
        verbose_name = _('Flatpage')
        verbose_name_plural = _('Flatpages')

    def __unicode__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def get_printable_url(self):
        return "%syazdir/" % self.url

    def save(self):
        self.author = threadlocals.get_current_user()
        super(FlatPage, self).save()
