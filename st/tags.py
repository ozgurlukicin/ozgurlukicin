#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.utils.translation import ugettext as _

class Tag(models.Model):
    name = models.CharField(_("Tag"), max_length=32, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/etiket/%s/" % self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
