#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.upload.models import Image, Logo

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['file']

admin.site.register(Image, ImageAdmin)
admin.site.register(Logo, ImageAdmin)
