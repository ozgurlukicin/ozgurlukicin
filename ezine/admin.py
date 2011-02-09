#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.ezine.models import Ezine, EzineFile
from oi.st.tags import Tag

class EzineAdmin(admin.ModelAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'admin/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'js/jquery-1.4.2.min.js', 'js/adminimages.js', 'js/tinymce_setup.js')

admin.site.register(Ezine, EzineAdmin)
admin.site.register(EzineFile)
