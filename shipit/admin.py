#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin
from oi.shipit.models import *

class PardusVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "status")

admin.site.register(CargoCompany)
admin.site.register(PardusVersion, PardusVersionAdmin)
