#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.st.models import Tag, Wiki, Contribute, OtherFile, ScreenShot, Video, License, FS, HowTo, Game, News, Package

class StSimpleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ['-name']
    search_fields = ['name']

class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'desc')
    ordering = ['-id']
    search_fields = ['file', 'desc']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'update')
    list_filter = ('update',)
    ordering = ('-id',)
    search_fields = ('title', 'text', 'tags')
    prepopulated_fields = {'slug': ("title",)}

    class Media:
        js = ("js/tinymce/tiny_mce.js", "js/tinymce/textareas.js",)

class FSAdmin(ArticleAdmin):
    fieldsets = (
        ('Genel', {'fields': ('author', 'title', 'image', 'sum', 'text', 'videos', 'tags', 'order', 'update', 'status',)}),
        ('Diğer', {'fields': ('slug',), 'classes': ('collapse',)}),
    )
    ordering = ('order',)

class HowToAdmin(ArticleAdmin):
    fieldsets = (
        ('Genel', {'fields': ('author', 'title', 'image', 'sum', 'text', 'videos', 'tags', 'wiki', 'update', 'status',)}),
        ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
    )

class GameAdmin(ArticleAdmin):
    fieldsets = (
        ('Genel', {'fields': ('author', 'title', 'image', 'sum', 'text', 'videos', 'tags', 'wiki', 'update', 'status')}),
        ('Oyun bilgileri', {'fields': ('url', 'path', 'learning_time', 'license', 'installed_size', 'download_size')}),
        ('Değerlendirme', {'fields': ('gameplay', 'graphics', 'sound', 'scenario', 'atmosphere')}),
        ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
    )

class NewsAdmin(ArticleAdmin):
    fieldsets = (
            ('Genel', {'fields': ('author', 'title', 'image', 'sum', 'text', 'tags', 'update', 'status')}),
            ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
            )
class PackageAdmin(ArticleAdmin):
    fieldsets = (
        ('Genel', {'fields': ('author', 'title', 'image', 'sum','text', 'license','installed_size','download_size','url','point','path','ss','tags','wiki','videos','update','status')}),
        ('Diğer', {'fields': ('slug',), 'classes': 'collapse'}),
    )

admin.site.register(Tag, StSimpleAdmin)
admin.site.register(Wiki, StSimpleAdmin)
admin.site.register(Contribute, StSimpleAdmin)
admin.site.register(License, StSimpleAdmin)
admin.site.register(OtherFile, FileAdmin)
admin.site.register(ScreenShot, FileAdmin)
admin.site.register(Video, FileAdmin)
admin.site.register(FS, FSAdmin)
admin.site.register(HowTo, HowToAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Package, PackageAdmin)
