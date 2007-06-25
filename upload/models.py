#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

class Image(models.Model):
    file = models.FileField(upload_to='uploads/image/')

    def __str__(self):
        return self.file