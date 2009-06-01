#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django import forms

class ImageUploadForm(forms.Form):
    file = forms.ImageField()

class Image(models.Model):
    file = models.ImageField("Görsel", upload_to='upload/image/')

    def __unicode__(self):
        return unicode(self.file)

    def get_alt_string(self):
        "returns file name without extension"
        return ".".join(self.file.path.rsplit(".")[:-1])[self.file.path.rfind("/")+1:]

    class Meta:
        verbose_name = "Görsel"
        verbose_name_plural = "Görseller"

class Logo(models.Model):
    file = models.ImageField("Görsel", upload_to='upload/image/')

    def __unicode__(self):
        return unicode(self.file)

    def get_alt_string(self):
        "returns file name without extension"
        return ".".join(self.file.path.rsplit(".")[:-1])[self.file.path.rfind("/")+1:]

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logolar"
