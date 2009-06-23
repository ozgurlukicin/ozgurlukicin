#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.flatpages.models import FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Genel', {'fields': ('url', 'title', 'text', 'tags', 'update')}),
        ('Diğer', {'classes': 'collapse', 'fields': ('template_name',)}),
    )

    list_display = ('id', 'url', 'title', 'update')
    list_filter = ['update']
    ordering = ['-update']
    search_fields = ['title', 'text', 'tags']

    class Media:
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

admin.site.register(FlatPage, FlatPageAdmin)
