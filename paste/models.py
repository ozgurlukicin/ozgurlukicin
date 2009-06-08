#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django.contrib.auth.models import User

class PastedText(models.Model):
    text = models.TextField("Yazı", max_length=250000, help_text="En fazla 250000 karakter")
    author = models.ForeignKey(User, verbose_name="Kullanıcı")
    ip = models.IPAddressField("IP Adresi", blank=True)
    date = models.DateTimeField("Tarih", auto_now_add=True)
    is_hidden = models.BooleanField("Gizli", default=False)
    # No colors for now
    #syntax = models.CharField('Sözdizimi', max_length=10, choices=LANGUAGES, blank=True, null=True)
    #highlighted_text = models.TextField("Renklendirilmiş Metin", blank=True, editable=False)

    def __unicode__(self):
        return text[:20]

    class Meta:
        permissions = (
            ("hide_pastedtext", "Can hide pasted text"),
        )

    def get_absolute_url(self):
        return "/yapistir/%d/" % self.id

    def get_toggle_url(self):
        return "/yapistir/%d/toggle" % self.id
