#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.st.models import Tag, Wiki, Contribute, OtherFile, ScreenShot, Video, License, FS

class StSimpleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ['-name']
    search_fields = ['name']

class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'desc')
    ordering = ['-id']
    search_fields = ['file', 'desc']

class ArticleAdmin(admin.ModelAdmin):
    field_sets = (
        ('Genel', {'fields': ('author', 'title','sum','text','videos','tags','order','update','status',)}),
        ('Diğer', {'fields': ('slug',), 'classes': ('collapse',)}),
    )
    list_display = ('title', 'author', 'status', 'update')
    list_filter = ('update',)
    ordering = ['order',]
    search_fields = ['title', 'text', 'tags']
    prepopulated_fields = {'slug': ("title",)}

    class Media:
        js = ("js/admin/sef.js", "js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

admin.site.register(Tag, StSimpleAdmin)
admin.site.register(Wiki, StSimpleAdmin)
admin.site.register(Contribute, StSimpleAdmin)
admin.site.register(License, StSimpleAdmin)
admin.site.register(OtherFile, FileAdmin)
admin.site.register(ScreenShot, FileAdmin)
admin.site.register(Video, FileAdmin)
admin.site.register(FS, ArticleAdmin)
