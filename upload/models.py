#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

class Image(models.Model):
    file = models.FileField(upload_to='upload/image/')

    def __unicode__(self):
        return self.file

    def get_alt_string(self):
        "returns file name without extension"
        return ".".join(self.file.rsplit(".")[:-1])[self.file.rfind("/")+1:]

    class Admin:
        pass
