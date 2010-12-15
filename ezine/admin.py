#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.ezine.models import Ezine
from oi.st.tags import Tag

class EzineAdmin(admin.ModelAdmin):
    list_display = ('title',)

    class Media:
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js", "js/jquery-1.2.6.min.js", "js/adminimages.js")

admin.site.register(Ezine, EzineAdmin)
