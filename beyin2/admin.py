#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin
from oi.beyin2.models import *

admin.site.register(Idea)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(ScreenShot)

