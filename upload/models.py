#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models
from django import forms

from django.utils.translation import ugettext as _

class ImageUploadForm(forms.Form):
    file = forms.ImageField()

class Image(models.Model):
    file = models.ImageField(_("Image"), upload_to='upload/image/')

    def __unicode__(self):
        return unicode(self.file)

    def get_alt_string(self):
        "returns file name without extension"
        return ".".join(self.file.path.rsplit(".")[:-1])[self.file.path.rfind("/")+1:]

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

class Logo(models.Model):
    file = models.ImageField(_("Image"), upload_to='upload/image/')

    def __unicode__(self):
        return unicode(self.file)

    def get_alt_string(self):
        "returns file name without extension"
        return ".".join(self.file.path.rsplit(".")[:-1])[self.file.path.rfind("/")+1:]

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")
